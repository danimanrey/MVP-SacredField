"""
Rate Limiter para proteger endpoints de Campo Sagrado
Previene abuso y ataques DDoS
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from collections import defaultdict
import asyncio


class RateLimiter:
    """
    Rate limiter simple basado en memoria.
    Para producción, usar Redis para persistencia distribuida.
    """
    
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.cleanup_task = None
    
    def _cleanup_old_requests(self):
        """Limpia requests antiguos cada minuto."""
        now = datetime.utcnow()
        for ip in list(self.requests.keys()):
            self.requests[ip] = [
                req_time for req_time in self.requests[ip]
                if now - req_time < timedelta(minutes=5)
            ]
            if not self.requests[ip]:
                del self.requests[ip]
    
    def check_rate_limit(
        self, 
        identifier: str, 
        max_requests: int = 100, 
        window_minutes: int = 1
    ) -> tuple[bool, int, int]:
        """
        Verifica si el identificador (IP, user_id) ha excedido el límite.
        
        Args:
            identifier: IP o user_id
            max_requests: Número máximo de requests permitidos
            window_minutes: Ventana de tiempo en minutos
        
        Returns:
            (permitido, requests_restantes, tiempo_hasta_reset)
        """
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)
        
        # Filtrar requests dentro de la ventana
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        current_requests = len(self.requests[identifier])
        
        if current_requests >= max_requests:
            # Calcular tiempo hasta reset
            oldest_request = min(self.requests[identifier])
            reset_time = oldest_request + timedelta(minutes=window_minutes)
            seconds_until_reset = int((reset_time - now).total_seconds())
            
            return False, 0, seconds_until_reset
        
        # Agregar nueva request
        self.requests[identifier].append(now)
        requests_remaining = max_requests - (current_requests + 1)
        
        return True, requests_remaining, 0
    
    async def start_cleanup(self):
        """Inicia tarea de limpieza periódica."""
        while True:
            await asyncio.sleep(60)  # Cada minuto
            self._cleanup_old_requests()


# Instancia global
rate_limiter = RateLimiter()


# Límites por endpoint
RATE_LIMITS = {
    "estado_cero": {"max_requests": 10, "window_minutes": 1},   # 10/min
    "planificar": {"max_requests": 20, "window_minutes": 1},    # 20/min
    "general": {"max_requests": 100, "window_minutes": 1},      # 100/min
    "health": {"max_requests": 300, "window_minutes": 1},       # 300/min
}


def get_rate_limit_for_endpoint(endpoint_type: str = "general") -> dict:
    """Obtiene configuración de rate limit para un endpoint."""
    return RATE_LIMITS.get(endpoint_type, RATE_LIMITS["general"])

