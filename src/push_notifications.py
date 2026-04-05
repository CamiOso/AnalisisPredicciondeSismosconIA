"""
Sistema de Notificaciones Push - Firebase Cloud Messaging
Envía alertas sísmicas a dispositivos móviles en tiempo real
"""

import firebase_admin
from firebase_admin import credentials, messaging
import logging
from datetime import datetime
from typing import Dict, List, Optional
import json
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class PushNotification:
    """Estructura de notificación push"""
    title: str
    body: str
    device_token: str
    data: Optional[Dict] = None
    priority: str = "high"
    ttl: int = 3600  # 1 hora


class FirebaseNotificationSystem:
    """Sistema de notificaciones con Firebase Cloud Messaging"""
    
    def __init__(self, credentials_path: str = "firebase-credentials.json"):
        """
        Inicializa Firebase
        Args:
            credentials_path: Ruta al archivo JSON de credenciales de Firebase
        """
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(credentials_path)
                firebase_admin.initialize_app(cred)
            self.subscribers: Dict[str, List[str]] = {}  # volcano_id -> [tokens]
        except Exception as e:
            logger.error(f"Error inicializando Firebase: {e}")
            self.active = False
    
    def subscribe_device(self, device_token: str, volcano_id: str) -> bool:
        """
        Suscribe un dispositivo móvil a alertas de un volcán
        Args:
            device_token: Token FCM del dispositivo
            volcano_id: ID del volcán a monitorear
        Returns:
            True si la suscripción fue exitosa
        """
        try:
            if volcano_id not in self.subscribers:
                self.subscribers[volcano_id] = []
            
            if device_token not in self.subscribers[volcano_id]:
                self.subscribers[volcano_id].append(device_token)
                logger.info(f"Dispositivo suscrito: {volcano_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error al suscribir dispositivo: {e}")
            return False
    
    def unsubscribe_device(self, device_token: str, volcano_id: str) -> bool:
        """Desuscribe un dispositivo"""
        try:
            if volcano_id in self.subscribers and device_token in self.subscribers[volcano_id]:
                self.subscribers[volcano_id].remove(device_token)
                logger.info(f"Dispositivo desuscrito: {volcano_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error al desuscribir: {e}")
            return False
    
    def send_alert_notification(
        self,
        volcano_id: str,
        magnitude: float,
        depth: float,
        location: str,
        severity: str
    ) -> int:
        """
        Envía notificación de alerta sísmica a todos los suscriptores
        Args:
            volcano_id: ID del volcán
            magnitude: Magnitud del evento
            depth: Profundidad en km
            location: Ubicación del epicentro
            severity: Nivel de severidad (CRITICAL, SEVERE, HIGH, MEDIUM, LOW)
        Returns:
            Número de notificaciones enviadas exitosamente
        """
        if volcano_id not in self.subscribers:
            return 0
        
        # Determinar emoji y mensaje según severidad
        severity_map = {
            "CRITICAL": ("🚨", "¡ALERTA CRÍTICA!"),
            "SEVERE": ("⚠️", "Evento severo"),
            "HIGH": ("🔴", "Evento de alto riesgo"),
            "MEDIUM": ("🟠", "Evento moderado"),
            "LOW": ("🟡", "Evento detectable")
        }
        
        emoji, title_prefix = severity_map.get(severity, ("❓", "Evento"))
        
        notification = PushNotification(
            title=f"{emoji} {title_prefix} - {location}",
            body=f"Magnitud {magnitude:.1f} | Profundidad {depth:.0f}km",
            device_token="",  # Se reemplazará por cada token
            data={
                "volcano_id": volcano_id,
                "magnitude": str(magnitude),
                "depth": str(depth),
                "location": location,
                "severity": severity,
                "timestamp": datetime.now().isoformat(),
                "action": "open_alerts"
            }
        )
        
        success_count = 0
        for device_token in self.subscribers[volcano_id]:
            try:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=notification.title,
                        body=notification.body
                    ),
                    data=notification.data,
                    token=device_token,
                    android=messaging.AndroidConfig(
                        priority="high",
                        notification=messaging.AndroidNotification(
                            title=notification.title,
                            body=notification.body,
                            color="#FF0000" if severity == "CRITICAL" else "#FFA500"
                        )
                    ),
                    webpush=messaging.WebpushConfig(
                        notification=messaging.WebpushNotification(
                            title=notification.title,
                            body=notification.body,
                            icon="https://raw.githubusercontent.com/CamiOso/AnalisisPredicciondeSismosconIA/main/assets/icon.png"
                        )
                    )
                )
                
                response = messaging.send(message)
                success_count += 1
                logger.info(f"Notificación enviada: {response}")
            except Exception as e:
                logger.error(f"Error enviando notificación: {e}")
        
        return success_count
    
    def send_forecast_notification(self, volcano_id: str, forecast_data: Dict) -> int:
        """Envía notificación de pronóstico"""
        if volcano_id not in self.subscribers:
            return 0
        
        notification = PushNotification(
            title=f"📊 Pronóstico Sísmico - {volcano_id}",
            body=f"Próximos 7 días: {forecast_data.get('summary', 'Sin cambios significativos')}",
            device_token="",
            data={
                "volcano_id": volcano_id,
                "forecast": json.dumps(forecast_data),
                "type": "forecast",
                "action": "open_forecast"
            }
        )
        
        success_count = 0
        for device_token in self.subscribers[volcano_id]:
            try:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=notification.title,
                        body=notification.body
                    ),
                    data=notification.data,
                    token=device_token
                )
                messaging.send(message)
                success_count += 1
            except Exception as e:
                logger.error(f"Error: {e}")
        
        return success_count
    
    def send_daily_summary(self, volcano_id: str, summary_data: Dict) -> int:
        """Envía resumen diario del volcán"""
        if volcano_id not in self.subscribers:
            return 0
        
        events = summary_data.get('total_events', 0)
        avg_mag = summary_data.get('avg_magnitude', 0)
        
        notification = PushNotification(
            title=f"📈 Resumen Diario - {volcano_id}",
            body=f"{events} eventos, magnitude promedio: {avg_mag:.1f}",
            device_token="",
            data={
                "volcano_id": volcano_id,
                "summary": json.dumps(summary_data),
                "type": "daily_summary",
                "action": "open_stats"
            }
        )
        
        success_count = 0
        for device_token in self.subscribers[volcano_id]:
            try:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=notification.title,
                        body=notification.body
                    ),
                    data=notification.data,
                    token=device_token
                )
                messaging.send(message)
                success_count += 1
            except Exception as e:
                logger.error(f"Error: {e}")
        
        return success_count
    
    def get_subscriber_count(self, volcano_id: str) -> int:
        """Retorna cantidad de suscriptores"""
        return len(self.subscribers.get(volcano_id, []))


class LocalPushNotificationSystem:
    """Sistema alternativo de notificaciones local (sin Firebase)"""
    
    def __init__(self):
        self.subscribers = {}  # volcano_id -> [devices]
        self.notifications_history = []
    
    def subscribe_device(self, device_id: str, volcano_id: str) -> bool:
        """Suscribe dispositivo local"""
        if volcano_id not in self.subscribers:
            self.subscribers[volcano_id] = []
        if device_id not in self.subscribers[volcano_id]:
            self.subscribers[volcano_id].append(device_id)
            return True
        return False
    
    def send_alert_notification(
        self,
        volcano_id: str,
        magnitude: float,
        depth: float,
        location: str,
        severity: str
    ) -> int:
        """Envía notificación local"""
        notification = {
            "timestamp": datetime.now().isoformat(),
            "volcano_id": volcano_id,
            "magnitude": magnitude,
            "depth": depth,
            "location": location,
            "severity": severity,
            "recipients": self.subscribers.get(volcano_id, [])
        }
        
        self.notifications_history.append(notification)
        logger.info(f"Notificación local enviada: {volcano_id} - {magnitude}")
        return len(notification["recipients"])
    
    def get_notifications_history(self, limit: int = 100) -> List[Dict]:
        """Retorna historial de notificaciones"""
        return self.notifications_history[-limit:]


# Instancia global
firebase_system = FirebaseNotificationSystem() if firebase_admin._apps else LocalPushNotificationSystem()
