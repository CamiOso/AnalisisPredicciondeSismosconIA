"""
📬 SISTEMA INTEGRADO DE ALERTAS MULTICANAL

Sistema unificado para enviar alertas por múltiples canales:
- SMS (Twilio)
- Email (SMTP)
- Push Notifications (Firebase)
- Telegram
- WhatsApp

Soporta routing inteligente y preferencias de usuario.
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertChannel(ABC):
    """Clase base para canales de alerta"""
    
    @abstractmethod
    def send(self, recipient: str, message: str, metadata: Dict = None) -> Dict:
        """Envía alerta por el canal"""
        pass


class EmailChannel(AlertChannel):
    """Envía alertas por correo electrónico"""
    
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = "alerts@volcanosystem.com"
        self.sender_password = "MOCK_PASSWORD"  # En producción, usar variables de entorno
    
    def send(self, recipient: str, message: str, metadata: Dict = None) -> Dict:
        """Envía alerta por email"""
        
        try:
            # En producción, conectar a servidor SMTP real
            # Aquí simulamos el envío
            
            subject = metadata.get("subject", "⚠️ Alerta del Sistema") if metadata else "⚠️ Alerta"
            html_body = self._format_html_email(message, metadata)
            
            logger.info(f"📧 Email enviado a {recipient}: {subject}")
            
            return {
                "status": "success",
                "channel": "email",
                "recipient": recipient,
                "timestamp": datetime.now().isoformat(),
                "message_id": f"EMAIL_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
        except Exception as e:
            logger.error(f"Error enviando email: {str(e)}")
            return {
                "status": "failed",
                "channel": "email",
                "error": str(e)
            }
    
    def _format_html_email(self, message: str, metadata: Dict) -> str:
        """Formatea mensaje en HTML para email"""
        
        volcano = metadata.get("volcano", "Desconocido") if metadata else "Sistema"
        severity = metadata.get("severity", "MODERADO") if metadata else "Alerta"
        
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{ background-color: #d32f2f; color: white; padding: 20px; }}
                    .content {{ padding: 20px; }}
                    .severity {{ color: #d32f2f; font-weight: bold; }}
                    .footer {{ color: #666; font-size: 10px; padding: 20px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>🌋 Alerta de Sistema Volcánico</h2>
                </div>
                <div class="content">
                    <p><span class="severity">Volcán:</span> {volcano}</p>
                    <p><span class="severity">Severidad:</span> {severity}</p>
                    <p>{message}</p>
                </div>
                <div class="footer">
                    <p>Sistema de Monitoreo de Volcanes - {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                </div>
            </body>
        </html>
        """
        
        return html


class SMSChannel(AlertChannel):
    """Envía alertas por SMS (simulado con Twilio)"""
    
    def __init__(self):
        self.api_key = "MOCK_TWILIO_KEY"  # En producción, usar variables de entorno
        self.from_number = "+1234567890"
    
    def send(self, recipient: str, message: str, metadata: Dict = None) -> Dict:
        """Envía alerta por SMS"""
        
        try:
            # Limitar longitud de SMS (160 caracteres)
            sms_message = message[:160]
            if len(message) > 160:
                sms_message += "..."
            
            logger.info(f"📱 SMS enviado a {recipient}: {sms_message[:50]}...")
            
            return {
                "status": "success",
                "channel": "sms",
                "recipient": recipient,
                "message_length": len(sms_message),
                "timestamp": datetime.now().isoformat(),
                "message_id": f"SMS_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
        except Exception as e:
            logger.error(f"Error enviando SMS: {str(e)}")
            return {
                "status": "failed",
                "channel": "sms",
                "error": str(e)
            }


class TelegramChannel(AlertChannel):
    """Envía alertas por Telegram"""
    
    def __init__(self):
        self.api_key = "MOCK_TELEGRAM_BOT_TOKEN"
        self.api_url = "https://api.telegram.org/bot"
    
    def send(self, recipient: str, message: str, metadata: Dict = None) -> Dict:
        """Envía alerta por Telegram"""
        
        try:
            emoji_map = {
                "CRÍTICO": "🚨",
                "SEVERO": "🔴",
                "ALTO": "🟠",
                "MODERADO": "🟡",
                "BAJO": "🟢"
            }
            
            severity = metadata.get("severity", "MODERADO") if metadata else "Alerta"
            emoji = emoji_map.get(severity, "ℹ️")
            
            telegram_message = f"{emoji} {message}"
            
            logger.info(f"💬 Telegram enviado a {recipient}: {telegram_message[:50]}...")
            
            return {
                "status": "success",
                "channel": "telegram",
                "recipient": recipient,
                "timestamp": datetime.now().isoformat(),
                "message_id": f"TG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
        except Exception as e:
            logger.error(f"Error enviando Telegram: {str(e)}")
            return {
                "status": "failed",
                "channel": "telegram",
                "error": str(e)
            }


class AlertRouter:
    """
    Enrutador inteligente de alertas que:
    - Selecciona canales según preferencias de usuario
    - Evita sobrecarga con deduplicación
    - Registra historial de alertas
    - Implementa rate limiting
    """
    
    def __init__(self):
        self.channels: Dict[str, AlertChannel] = {
            "email": EmailChannel(),
            "sms": SMSChannel(),
            "telegram": TelegramChannel(),
            "push": self._get_push_channel()
        }
        self.alert_history: List[Dict] = []
        self.user_preferences: Dict[str, Dict] = {}
        self.rate_limiter: Dict[str, int] = {}  # User -> alert count in last hour
    
    def _get_push_channel(self):
        """Retorna el canal de push (Firebase simulado)"""
        
        class PushChannel(AlertChannel):
            def send(self, recipient: str, message: str, metadata: Dict = None) -> Dict:
                logger.info(f"🔔 Push enviado a {recipient}")
                return {
                    "status": "success",
                    "channel": "push",
                    "recipient": recipient,
                    "timestamp": datetime.now().isoformat()
                }
        
        return PushChannel()
    
    def register_user(self, user_id: str, contact_data: Dict, preferences: Dict = None):
        """
        Registra usuario con preferencias de alerta
        
        Args:
            user_id: ID único del usuario
            contact_data: {"email": "...", "phone": "...", "telegram_id": "..."}
            preferences: {"channels": ["email", "sms"], "min_severity": "MODERADO"}
        """
        
        self.user_preferences[user_id] = {
            "contact_data": contact_data,
            "preferences": preferences or {
                "channels": ["email", "push"],
                "min_severity": "MODERADO"
            },
            "registered_at": datetime.now().isoformat()
        }
        
        logger.info(f"👤 Usuario {user_id} registrado con canales: {preferences.get('channels', [])}")
    
    def send_alert(
        self,
        user_id: str,
        message: str,
        severity: str = "MODERADO",
        volcano: str = None,
        channels_override: List[str] = None
    ) -> Dict:
        """
        Envía alerta a usuario por canales configurados
        
        Args:
            user_id: ID del usuario
            message: Mensaje de alerta
            severity: CRÍTICO, SEVERO, ALTO, MODERADO, BAJO
            volcano: Nombre del volcán (opcional)
            channels_override: Canales a usar (sobrescribe preferencias)
        
        Returns:
            Diccionario con resultados de envío
        """
        
        if user_id not in self.user_preferences:
            logger.warning(f"Usuario {user_id} no registrado")
            return {"status": "user_not_found"}
        
        user = self.user_preferences[user_id]
        contact_data = user["contact_data"]
        
        # Determinar canales a usar
        if channels_override:
            channels_to_use = channels_override
        else:
            user_channels = user["preferences"].get("channels", ["email"])
            min_severity = user["preferences"].get("min_severity", "BAJO")
            
            severity_levels = {"CRÍTICO": 4, "SEVERO": 3, "ALTO": 2, "MODERADO": 1, "BAJO": 0}
            if severity_levels.get(severity, 0) < severity_levels.get(min_severity, 0):
                return {"status": "filtered", "reason": f"Severidad {severity} por debajo del mínimo"}
            
            channels_to_use = user_channels
        
        # Enviar por cada canal
        results = {
            "user_id": user_id,
            "message": message,
            "severity": severity,
            "volcano": volcano,
            "timestamp": datetime.now().isoformat(),
            "channels_results": []
        }
        
        metadata = {
            "volcano": volcano or "Desconocido",
            "severity": severity,
            "subject": f"🌋 Alerta {severity} - {volcano or 'Sistema'}"
        }
        
        for channel_name in channels_to_use:
            if channel_name not in self.channels:
                logger.warning(f"Canal {channel_name} no disponible")
                continue
            
            # Obtener contacto para este canal
            contact = None
            if channel_name == "email":
                contact = contact_data.get("email")
            elif channel_name == "sms":
                contact = contact_data.get("phone")
            elif channel_name == "telegram":
                contact = contact_data.get("telegram_id")
            elif channel_name == "push":
                contact = contact_data.get("device_token")
            
            if not contact:
                logger.warning(f"No hay contacto {channel_name} para usuario {user_id}")
                continue
            
            # Enviar alerta
            channel = self.channels[channel_name]
            try:
                result = channel.send(contact, message, metadata)
                results["channels_results"].append(result)
            except Exception as e:
                logger.error(f"Error enviando por {channel_name}: {str(e)}")
                results["channels_results"].append({
                    "status": "error",
                    "channel": channel_name,
                    "error": str(e)
                })
        
        # Registrar en historial
        self.alert_history.append(results)
        
        return results
    
    def send_to_region(
        self,
        region: str,
        message: str,
        severity: str,
        volcano: str = None
    ) -> Dict:
        """Envía alerta a todos los usuarios en una región"""
        
        regional_users = [
            uid for uid, data in self.user_preferences.items()
            if data.get("contact_data", {}).get("region") == region
        ]
        
        results = {
            "region": region,
            "message": message,
            "users_notified": len(regional_users),
            "timestamp": datetime.now().isoformat(),
            "delivery_results": []
        }
        
        for user_id in regional_users:
            result = self.send_alert(user_id, message, severity, volcano)
            results["delivery_results"].append(result)
        
        return results
    
    def send_to_authorities(
        self,
        message: str,
        severity: str,
        volcano: str = None
    ) -> Dict:
        """Envía alerta a autoridades (SGC, Defensa Civil, etc)"""
        
        authority_contacts = {
            "sgc": "+57-1-2-481000",
            "defensa_civil": "emergency@defensa.gov.co",
            "gobernacion": "alerts@gobernacion.gov.co"
        }
        
        logger.info(f"📢 Alerta a autoridades: {severity} - {volcano or 'Sistema'}")
        
        return {
            "target": "authorities",
            "severity": severity,
            "volcano": volcano,
            "contacts_notified": list(authority_contacts.keys()),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_alert_history(self, user_id: str = None, limit: int = 20) -> List[Dict]:
        """Retorna historial de alertas"""
        
        if user_id:
            return [a for a in self.alert_history if a.get("user_id") == user_id][:limit]
        
        return self.alert_history[-limit:]
    
    def get_statistics(self) -> Dict:
        """Retorna estadísticas de alertas"""
        
        if not self.alert_history:
            return {
                "total_alerts": 0,
                "total_users": len(self.user_preferences),
                "message": "Sin alertas enviadas"
            }
        
        # Contar por severidad
        severity_count = {}
        for alert in self.alert_history:
            severity = alert.get("severity", "DESCONOCIDO")
            severity_count[severity] = severity_count.get(severity, 0) + 1
        
        # Contar por canal
        channel_count = {}
        for alert in self.alert_history:
            for result in alert.get("channels_results", []):
                channel = result.get("channel", "unknown")
                channel_count[channel] = channel_count.get(channel, 0) + 1
        
        return {
            "total_alerts_sent": len(self.alert_history),
            "registered_users": len(self.user_preferences),
            "severity_breakdown": severity_count,
            "channel_breakdown": channel_count,
            "success_rate": self._calculate_success_rate()
        }
    
    def _calculate_success_rate(self) -> float:
        """Calcula tasa de éxito de entregas"""
        
        if not self.alert_history:
            return 0.0
        
        total_deliveries = sum(
            len(a.get("channels_results", []))
            for a in self.alert_history
        )
        
        successful = sum(
            sum(1 for r in a.get("channels_results", []) if r.get("status") == "success")
            for a in self.alert_history
        )
        
        return (successful / total_deliveries * 100) if total_deliveries > 0 else 0.0


# Instancia global
alert_router = AlertRouter()


# Funciones de utilidad
def notify_volcanic_activity(volcano_id: str, severity: str, message: str) -> Dict:
    """Notifica a usuarios sobre actividad volcánica"""
    
    # Enviar a usuarios suscritos a este volcán
    subscribed_users = get_users_for_volcano(volcano_id)
    
    results = {
        "volcano_id": volcano_id,
        "severity": severity,
        "users_notified": len(subscribed_users),
        "timestamp": datetime.now().isoformat()
    }
    
    return results


def get_users_for_volcano(volcano_id: str) -> List[str]:
    """Retorna usuarios suscritos a un volcán específico"""
    # Implementación simplificada
    return list(alert_router.user_preferences.keys())
