from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app
)
import sendgrid
from sendgrid.helpers.mail import *

bp = Blueprint('portfolio', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('portfolio/index.html')

@bp.route('/mail', methods=['GET', 'POST'])
def mail():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if request.method == 'POST':
        # Aquí se enviaría el correo usando SendGrid o cualquier otro servicio
        email_sent = send_email(name, email, message)
        if email_sent:
            return render_template('portfolio/sent_mail.html')
        else:
            # Si falla el envío, redirigir al index con un mensaje de error
            return render_template('portfolio/index.html', error="Error al enviar el mensaje. Inténtalo de nuevo.")

    return redirect(url_for('portfolio.index'))

def send_email(name, email, message):
    mi_email = 'maximot0904@outlook.com'
    
    try:
        # Verificar que la API key existe
        api_key = current_app.config.get('SENDGRID_KEY')
        if not api_key:
            print("ERROR: SENDGRID_KEY no está configurada")
            return False
            
        print(f"SendGrid API Key longitud: {len(api_key)} caracteres")
        print(f"SendGrid API Key primeros 10 chars: {api_key[:10]}...")
        
        sg = sendgrid.SendGridAPIClient(api_key=api_key)

        from_email = Email(mi_email)
        # Temporalmente enviar a Gmail para probar si es problema de Outlook
        to_email = To('maximot0904@gmail.com')  # Cambiado temporalmente
        
        html_content = f"""
            <p>Hola Máximo, has recibido un nuevo mensaje desde tu portafolio:</p>
            <p>Nombre: {name}</p>
            <p>Email del remitente: {email}</p>
            <p>Mensaje: {message}</p>
        """
        
        mail = Mail(from_email, to_email, "Nuevo mensaje desde tu portafolio", html_content=html_content)
        
        print("Enviando email...")
        print(f"Enviando desde: {mi_email}")
        print(f"Enviando hacia: maximot0904@gmail.com (TEMPORAL PARA PRUEBA)")
        response = sg.client.mail.send.post(request_body=mail.get())
        
        print(f"Email enviado exitosamente. Status code: {response.status_code}")
        return True
        
    except Exception as e:
        print(f"Error enviando email: {type(e).__name__}: {str(e)}")
        return False
