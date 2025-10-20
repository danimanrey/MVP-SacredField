#!/usr/bin/env python3
"""
Inicializador de base de datos para Campo Sagrado
Crea todas las tablas y datos iniciales
"""

import os
import sys
from pathlib import Path

# Añadir el directorio padre al path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from sqlalchemy import create_engine, text
from models.database import Base, engine
from models.schemas import MomentoLiturgico, TipoNoNegociable
import json
from datetime import datetime, date

def crear_tablas():
    """Crea todas las tablas de la base de datos"""
    print("🔧 Creando tablas...")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas correctamente")
        return True
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def insertar_datos_iniciales():
    """Inserta datos iniciales necesarios"""
    print("📊 Insertando datos iniciales...")
    
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Aquí podrías insertar datos iniciales si los necesitas
        # Por ejemplo, configuraciones por defecto, usuarios iniciales, etc.
        
        print("✅ Datos iniciales insertados")
        db.commit()
        return True
    except Exception as e:
        print(f"❌ Error insertando datos iniciales: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def verificar_conexion():
    """Verifica que la conexión a la base de datos funcione"""
    print("🔍 Verificando conexión a la base de datos...")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        print("✅ Conexión a base de datos exitosa")
        return True
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False

def mostrar_estado():
    """Muestra el estado actual de la base de datos"""
    print("\n📋 Estado de la base de datos:")
    
    from sqlalchemy.orm import sessionmaker
    from models.database import EstadoCeroDB, SesionDB, NoNegociableTrackingDB, BiometriaDB
    from sqlalchemy import inspect
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Verificar tablas existentes
        inspector = inspect(engine)
        tablas = inspector.get_table_names()
        
        print(f"  📊 Tablas creadas: {len(tablas)}")
        for tabla in tablas:
            print(f"    - {tabla}")
        
        # Contar registros en cada tabla
        print("\n  📈 Registros por tabla:")
        
        if "estado_cero" in tablas:
            count = db.query(EstadoCeroDB).count()
            print(f"    - Estados Cero: {count}")
        
        if "sesiones" in tablas:
            count = db.query(SesionDB).count()
            print(f"    - Sesiones: {count}")
        
        if "no_negociable_tracking" in tablas:
            count = db.query(NoNegociableTrackingDB).count()
            print(f"    - No-negociables: {count}")
        
        if "biometria" in tablas:
            count = db.query(BiometriaDB).count()
            print(f"    - Biometría: {count}")
        
        print("✅ Verificación completada")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estado: {e}")
        return False
    finally:
        db.close()

def main():
    """Función principal"""
    print("🕌 CAMPO SAGRADO - Inicializador de Base de Datos")
    print("=" * 50)
    
    # Verificar configuración
    try:
        from config import validar_configuracion
        validar_configuracion()
        print("✅ Configuración válida")
    except Exception as e:
        print(f"❌ Error de configuración: {e}")
        return False
    
    # Verificar conexión
    if not verificar_conexion():
        return False
    
    # Crear tablas
    if not crear_tablas():
        return False
    
    # Insertar datos iniciales
    if not insertar_datos_iniciales():
        return False
    
    # Mostrar estado final
    if not mostrar_estado():
        return False
    
    print("\n🎉 Base de datos inicializada correctamente")
    print("📍 Ubicación:", Path(__file__).parent.parent.parent / "storage" / "organismo.db")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
