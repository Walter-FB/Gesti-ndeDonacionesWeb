from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .database import Base

class Comedor(Base):
    __tablename__ = "comedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    barrio = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    responsable = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    
    # Relaciones
    notificaciones = relationship("Notificacion", back_populates="comedor")
    donaciones_recibidas = relationship("Donacion", back_populates="comedor_asignado")

class Donacion(Base):
    __tablename__ = "donaciones"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)  # Alimentos, Ropa, Útiles, etc.
    descripcion = Column(Text, nullable=False)
    cantidad = Column(Integer, nullable=False)
    urgencia = Column(String(20), nullable=False)  # Alta, Media, Baja
    fecha_registro = Column(DateTime, nullable=False)
    estado = Column(String(20), nullable=False)  # disponible, asignada, entregada
    comedor_asignado_id = Column(Integer, ForeignKey("comedores.id"), nullable=True)
    
    # Relaciones
    comedor_asignado = relationship("Comedor", back_populates="donaciones_recibidas")
    notificaciones = relationship("Notificacion", back_populates="donacion")

class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    comedor_id = Column(Integer, ForeignKey("comedores.id"), nullable=False)
    donacion_id = Column(Integer, ForeignKey("donaciones.id"), nullable=False)
    fecha_envio = Column(DateTime, nullable=False)
    estado = Column(String(20), nullable=False)  # enviada, leida, aceptada, rechazada
    
    # Relaciones
    comedor = relationship("Comedor", back_populates="notificaciones")
    donacion = relationship("Donacion", back_populates="notificaciones") 