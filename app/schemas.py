from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Esquemas para Comedores
class ComedorBase(BaseModel):
    nombre: str
    barrio: str
    direccion: str
    responsable: str
    telefono: str
    email: EmailStr

class ComedorCreate(ComedorBase):
    pass

class Comedor(ComedorBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para Donaciones
class DonacionBase(BaseModel):
    tipo: str
    descripcion: str
    cantidad: int
    urgencia: str

class DonacionCreate(DonacionBase):
    pass

class Donacion(DonacionBase):
    id: int
    fecha_registro: datetime
    estado: str
    comedor_asignado_id: Optional[int] = None

    class Config:
        from_attributes = True

# Esquemas para Notificaciones
class NotificacionBase(BaseModel):
    comedor_id: int
    donacion_id: int

class NotificacionCreate(NotificacionBase):
    pass

class Notificacion(NotificacionBase):
    id: int
    fecha_envio: datetime
    estado: str

    class Config:
        from_attributes = True 