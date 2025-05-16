from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime

# Importaciones locales
from .database import engine, SessionLocal, Base
from .models import Comedor, Donacion, Notificacion
from .schemas import ComedorCreate, DonacionCreate, NotificacionCreate
from .email_service import enviar_notificacion

# Crear la aplicación FastAPI
app = FastAPI(title="Sistema de Gestión de Donaciones para Comedores")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar plantillas
templates = Jinja2Templates(directory="app/templates")

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Dependency para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rutas para la interfaz web
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    comedores = db.query(Comedor).all()
    donaciones = db.query(Donacion).filter(Donacion.estado == "disponible").all()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "comedores": comedores,
        "donaciones": donaciones
    })

# Rutas para comedores
@app.get("/comedores", response_class=HTMLResponse)
async def listar_comedores(request: Request, db: Session = Depends(get_db)):
    comedores = db.query(Comedor).all()
    return templates.TemplateResponse("comedores.html", {
        "request": request, 
        "comedores": comedores
    })

@app.get("/comedores/nuevo", response_class=HTMLResponse)
async def form_nuevo_comedor(request: Request):
    return templates.TemplateResponse("comedor_form.html", {"request": request})

@app.post("/comedores/nuevo")
async def crear_comedor(
    request: Request,
    nombre: str = Form(...),
    barrio: str = Form(...),
    direccion: str = Form(...),
    responsable: str = Form(...),
    telefono: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    comedor = Comedor(
        nombre=nombre,
        barrio=barrio,
        direccion=direccion,
        responsable=responsable,
        telefono=telefono,
        email=email
    )
    db.add(comedor)
    db.commit()
    db.refresh(comedor)
    return RedirectResponse(url="/comedores", status_code=status.HTTP_303_SEE_OTHER)

# Rutas para donaciones
@app.get("/donaciones", response_class=HTMLResponse)
async def listar_donaciones(request: Request, db: Session = Depends(get_db)):
    donaciones = db.query(Donacion).all()
    return templates.TemplateResponse("donaciones.html", {
        "request": request, 
        "donaciones": donaciones
    })

@app.get("/donaciones/nueva", response_class=HTMLResponse)
async def form_nueva_donacion(request: Request):
    return templates.TemplateResponse("donacion_form.html", {"request": request})

@app.post("/donaciones/nueva")
async def crear_donacion(
    request: Request,
    tipo: str = Form(...),
    descripcion: str = Form(...),
    cantidad: int = Form(...),
    urgencia: str = Form(...),
    db: Session = Depends(get_db)
):
    donacion = Donacion(
        tipo=tipo,
        descripcion=descripcion,
        cantidad=cantidad,
        urgencia=urgencia,
        fecha_registro=datetime.now(),
        estado="disponible"
    )
    db.add(donacion)
    db.commit()
    db.refresh(donacion)
    
    # Notificar a todos los comedores sobre la nueva donación
    comedores = db.query(Comedor).all()
    for comedor in comedores:
        notificacion = Notificacion(
            comedor_id=comedor.id,
            donacion_id=donacion.id,
            fecha_envio=datetime.now(),
            estado="enviada"
        )
        db.add(notificacion)
        # Simular envío de correo electrónico
        enviar_notificacion(comedor.email, donacion)
    
    db.commit()
    return RedirectResponse(url="/donaciones", status_code=status.HTTP_303_SEE_OTHER)

# API para aceptar donaciones
@app.post("/api/donaciones/{donacion_id}/aceptar/{comedor_id}")
async def aceptar_donacion(
    donacion_id: int,
    comedor_id: int,
    db: Session = Depends(get_db)
):
    donacion = db.query(Donacion).filter(Donacion.id == donacion_id).first()
    comedor = db.query(Comedor).filter(Comedor.id == comedor_id).first()
    
    if not donacion or not comedor:
        raise HTTPException(status_code=404, detail="Donación o comedor no encontrado")
    
    if donacion.estado != "disponible":
        raise HTTPException(status_code=400, detail="La donación ya no está disponible")
    
    # Actualizar estado de la donación
    donacion.estado = "asignada"
    donacion.comedor_asignado_id = comedor_id
    
    # Actualizar notificación
    notificacion = db.query(Notificacion).filter(
        Notificacion.donacion_id == donacion_id,
        Notificacion.comedor_id == comedor_id
    ).first()
    
    if notificacion:
        notificacion.estado = "aceptada"
    
    db.commit()
    return {"mensaje": "Donación aceptada correctamente"}

# Ruta para ver notificaciones de un comedor
@app.get("/comedores/{comedor_id}/notificaciones", response_class=HTMLResponse)
async def ver_notificaciones(
    request: Request,
    comedor_id: int,
    db: Session = Depends(get_db)
):
    comedor = db.query(Comedor).filter(Comedor.id == comedor_id).first()
    if not comedor:
        raise HTTPException(status_code=404, detail="Comedor no encontrado")
    
    notificaciones = db.query(Notificacion).filter(
        Notificacion.comedor_id == comedor_id,
        Notificacion.estado == "enviada"
    ).join(Donacion).filter(Donacion.estado == "disponible").all()
    
    return templates.TemplateResponse("notificaciones.html", {
        "request": request,
        "comedor": comedor,
        "notificaciones": notificaciones
    }) 