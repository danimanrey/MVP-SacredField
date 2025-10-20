"""
Middleware de seguridad para Campo Sagrado
Implementa headers de seguridad y protecciones
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import os

from services.rate_limiter import rate_limiter, get_rate_limit_for_endpoint


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Añade headers de seguridad a todas las respuestas."""
    
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # CSP (Content Security Policy)
        if os.getenv("ENV") == "production":
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:;"
            )
        
        # HSTS (solo en producción con HTTPS)
        if os.getenv("ENV") == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Implementa rate limiting por IP."""
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Obtener IP del cliente
        client_ip = request.client.host
        
        # Determinar tipo de endpoint
        path = request.url.path
        
        if "/api/estado-cero" in path:
            endpoint_type = "estado_cero"
        elif "/api/orquestador/planificar" in path:
            endpoint_type = "planificar"
        elif "/health" in path or "/api/health" in path:
            endpoint_type = "health"
        else:
            endpoint_type = "general"
        
        # Verificar rate limit
        config = get_rate_limit_for_endpoint(endpoint_type)
        allowed, remaining, reset_in = rate_limiter.check_rate_limit(
            identifier=client_ip,
            max_requests=config["max_requests"],
            window_minutes=config["window_minutes"]
        )
        
        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": f"Demasiadas peticiones. Intenta de nuevo en {reset_in} segundos.",
                    "retry_after": reset_in
                },
                headers={
                    "Retry-After": str(reset_in),
                    "X-RateLimit-Limit": str(config["max_requests"]),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_in)
                }
            )
        
        # Añadir headers de rate limit a la respuesta
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(config["max_requests"])
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Registra todas las peticiones (sin información sensible).
    En producción, enviar a sistema de logging centralizado.
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        # Información básica de la request
        method = request.method
        path = request.url.path
        client_ip = request.client.host
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log solo en desarrollo (en producción usar logger profesional)
            if os.getenv("ENV") == "development":
                print(f"📡 {method} {path} - {response.status_code} - {process_time:.3f}s - IP: {client_ip}")
            
            # Añadir header de tiempo de procesamiento
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            
            # Log de error (sin stack trace completo en producción)
            if os.getenv("ENV") == "development":
                print(f"❌ {method} {path} - ERROR - {process_time:.3f}s - {str(e)}")
            else:
                print(f"❌ {method} {path} - ERROR - {process_time:.3f}s")
            
            raise


class SecurityValidationMiddleware(BaseHTTPMiddleware):
    """Valida aspectos de seguridad de las requests."""
    
    BLOCKED_USER_AGENTS = [
        "sqlmap", "nikto", "scanner", "bot", "crawler"
    ]
    
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB
    
    async def dispatch(self, request: Request, call_next: Callable):
        # 1. Verificar User-Agent sospechoso
        user_agent = request.headers.get("user-agent", "").lower()
        for blocked in self.BLOCKED_USER_AGENTS:
            if blocked in user_agent:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Acceso denegado"}
                )
        
        # 2. Verificar tamaño del body
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.MAX_BODY_SIZE:
            return JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={"detail": "Request demasiado grande"}
            )
        
        # 3. Verificar método HTTP permitido
        if request.method not in ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"]:
            return JSONResponse(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                content={"detail": "Método no permitido"}
            )
        
        # 4. En producción, verificar que sea HTTPS
        if os.getenv("ENV") == "production":
            if request.url.scheme != "https":
                return JSONResponse(
                    status_code=status.HTTP_426_UPGRADE_REQUIRED,
                    content={"detail": "HTTPS requerido"}
                )
        
        return await call_next(request)

