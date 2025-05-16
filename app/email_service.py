import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("email_service")

def enviar_notificacion(email_destino, donacion):
    """
    Simula el envío de un correo electrónico de notificación sobre una donación disponible.
    
    En un entorno real, aquí se implementaría la lógica para enviar correos electrónicos
    utilizando una biblioteca como aiosmtplib, pero para este MVP simplemente registramos
    la acción en los logs.
    """
    asunto = f"Nueva donación disponible: {donacion.tipo}"
    mensaje = f"""
    Estimado comedor comunitario,
    
    Nos complace informarle que hay una nueva donación disponible:
    
    Tipo: {donacion.tipo}
    Descripción: {donacion.descripcion}
    Cantidad: {donacion.cantidad}
    Urgencia: {donacion.urgencia}
    
    Para aceptar esta donación, por favor ingrese a nuestro sistema o responda
    a través de la API en la siguiente URL:
    
    /api/donaciones/{donacion.id}/aceptar/[su_id_de_comedor]
    
    Saludos cordiales,
    Sistema de Gestión de Donaciones
    """
    
    # Simulamos el envío del correo electrónico
    logger.info(f"Enviando notificación por correo a {email_destino}")
    logger.info(f"Asunto: {asunto}")
    logger.info(f"Mensaje: {mensaje}")
    
    # En un entorno real, aquí se enviaría el correo electrónico
    return True 