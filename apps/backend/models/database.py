from __future__ import annotations

import os
from datetime import datetime, date
from typing import Optional

from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Text, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "storage", "organismo.db"))
DB_PATH = os.path.abspath(DB_PATH)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class EstadoCeroDB(Base):
    __tablename__ = "estado_cero"
    id = Column(String, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.now)
    momento = Column(String, index=True)
    contexto = Column(Text)
    preguntas = Column(Text)
    respuestas = Column(Text)
    direccion = Column(Text)
    accion = Column(Text)
    chat = Column(Text)
    completado = Column(Boolean, default=False)
    archivo_path = Column(Text, nullable=True)


class SesionDB(Base):
    __tablename__ = "sesion"
    id = Column(String, primary_key=True)
    inicio = Column(DateTime, default=datetime.now)
    duracion_minutos = Column(Integer, nullable=True)
    rol = Column(String, nullable=True)
    calidad_flujo = Column(Integer, nullable=True)
    fecha = Column(Date, default=date.today)


class BiometriaDB(Base):
    __tablename__ = "biometria"
    fecha = Column(Date, primary_key=True)
    calidad_sueno = Column(Integer, nullable=True)
    energia_despertar = Column(Integer, nullable=True)
    hrv = Column(Float, nullable=True)
    luz_solar_am = Column(Boolean, default=False)
    luz_solar_am_minutos = Column(Integer, default=0)
    ejercicio = Column(Boolean, default=False)
    tipo_ejercicio = Column(String, nullable=True)
    duracion_ejercicio = Column(Integer, default=0)
    primera_comida = Column(DateTime, nullable=True)
    ultima_comida = Column(DateTime, nullable=True)
    ventana_alimenticia = Column(Float, nullable=True)
    notas = Column(Text, nullable=True)


class NoNegociableTrackingDB(Base):
    __tablename__ = "no_negociable_tracking"
    id = Column(String, primary_key=True)
    fecha = Column(Date, index=True)
    nombre = Column(String)
    tipo = Column(String)
    completado = Column(Boolean, default=False)
    hora_completado = Column(DateTime, nullable=True)


class DocumentoDB(Base):
    __tablename__ = "documento"
    id = Column(String, primary_key=True)
    tipo = Column(String)
    path = Column(Text)
    fecha = Column(DateTime, default=datetime.now)


class CapturaDB(Base):
    __tablename__ = "captura"
    id = Column(String, primary_key=True)
    tipo = Column(String)
    payload = Column(Text)
    procesada = Column(Boolean, default=False)
    creada_en = Column(DateTime, default=datetime.now)


