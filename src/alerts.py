"""
Sistema de Alertas por Email para eventos sísmicos anómalos
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)


class EmailAlert:
    """Sistema de alertas por email"""
    
    def __init__(self, sender_email: str = None, password: str = None):
        self.sender_email = sender_email or os.getenv("EMAIL_SENDER")
        self.password = password or os.getenv("EMAIL_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_anomaly_alert(self, recipient_email: str, anomaly_data: dict):
        """Envía alerta de anomalía detectada"""
        
        if not self.sender_email or not self.password:
            logger.warning("⚠️  Email no configurado (variables de entorno faltantes)")
            return False
        
        try:
            subject = "🚨 ALERTA SÍSMICA: Anomalía Detectada en Volcán Deception"
            
            html_body = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; }}
                        .alert {{ background-color: #ff6b6b; color: white; padding: 20px; border-radius: 5px; }}
                        .data {{ background-color: #f0f0f0; padding: 15px; margin: 10px 0; border-left: 4px solid #ff6b6b; }}
                        .safe {{ background-color: #51cf66; color: white; padding: 10px; border-radius: 3px; }}
                    </style>
                </head>
                <body>
                    <div class="alert">
                        <h2>⚠️ ALERTA DE ANOMALÍA SÍSMICA</h2>
                        <p>Se ha detectado un comportamiento anómalo en la actividad sísmica.</p>
                    </div>
                    
                    <div class="data">
                        <h3>Detalles de la Anomalía:</h3>
                        <p><strong>Magnitud:</strong> {anomaly_data.get('magnitude', 'N/A')}</p>
                        <p><strong>Profundidad:</strong> {anomaly_data.get('depth', 'N/A')} km</p>
                        <p><strong>Score de Anomalía:</strong> {anomaly_data.get('anomaly_score', 'N/A'):.3f}</p>
                        <p><strong>Nivel de Riesgo:</strong> {anomaly_data.get('risk_level', 'DESCONOCIDO')}</p>
                        <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    
                    <div class="data">
                        <h3>Recomendacional:</h3>
                        <p>{anomaly_data.get('recommendation', 'N/A')}</p>
                    </div>
                    
                    <p class="safe">✓ Este es un mensaje automático del Sistema de Análisis Sísmico</p>
                </body>
            </html>
            """
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            message.attach(MIMEText(html_body, "html"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            logger.info(f"✓ Email enviado a {recipient_email}")
            return True
        
        except Exception as e:
            logger.error(f"✗ Error enviando email: {str(e)}")
            return False
    
    def send_report(self, recipient_email: str, report_data: dict):
        """Envía reporte diario/semanal"""
        
        try:
            subject = f"📊 Reporte Sísmico Volcán Deception - {datetime.now().strftime('%Y-%m-%d')}"
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>📊 Reporte de Actividad Sísmica</h2>
                    
                    <h3>Estadísticas del período:</h3>
                    <ul>
                        <li>Total de eventos: {report_data.get('total_events', 0)}</li>
                        <li>Magnitud promedio: {report_data.get('avg_magnitude', 0):.2f}</li>
                        <li>Magnitud máxima: {report_data.get('max_magnitude', 0):.2f}</li>
                        <li>Profundidad promedio: {report_data.get('avg_depth', 0):.1f} km</li>
                        <li>Anomalías detectadas: {report_data.get('anomalies', 0)}</li>
                    </ul>
                    
                    <h3>Resumen:</h3>
                    <p>{report_data.get('summary', 'Sin datos disponibles')}</p>
                    
                    <hr>
                    <p><small>Generado automáticamente por Sistema de Análisis Sísmico</small></p>
                </body>
            </html>
            """
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            message.attach(MIMEText(html_body, "html"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            logger.info(f"✓ Reporte enviado a {recipient_email}")
            return True
        
        except Exception as e:
            logger.error(f"✗ Error enviando reporte: {str(e)}")
            return False
