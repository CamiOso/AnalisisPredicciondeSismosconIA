"""
Sistema de alertas en TIEMPO REAL
WebSocket + Server-Sent Events (SSE) para notificaciones en vivo
"""
import asyncio
import json
from datetime import datetime
from typing import List, Callable, Dict
import logging

logger = logging.getLogger(__name__)

try:
    import websockets
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False


class RealtimeAlertSystem:
    """Sistema de alertas en tiempo real"""
    
    def __init__(self):
        self.subscribers = []
        self.alert_thresholds = {
            'magnitude': 4.5,
            'anomaly_score': 0.7,
            'daily_count': 50
        }
        self.active_alerts = []
    
    def subscribe(self, callback: Callable):
        """Suscribirse a alertas"""
        self.subscribers.append(callback)
        logger.info(f"✓ Suscriptor agregado (total: {len(self.subscribers)})")
    
    def unsubscribe(self, callback: Callable):
        """Desuscribirse de alertas"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
            logger.info(f"✓ Suscriptor removido (total: {len(self.subscribers)})")
    
    def set_thresholds(self, **kwargs):
        """Configura umbrales de alertas"""
        for key, value in kwargs.items():
            if key in self.alert_thresholds:
                self.alert_thresholds[key] = value
                logger.info(f"✓ Umbral {key} actualizado a {value}")
    
    def check_magnitude_alert(self, magnitude: float) -> bool:
        """Verifica alerta por magnitud"""
        if magnitude >= self.alert_thresholds['magnitude']:
            self._trigger_alert({
                'type': 'magnitude_alert',
                'magnitude': magnitude,
                'threshold': self.alert_thresholds['magnitude'],
                'message': f'🚨 Evento sísmico: M{magnitude:.2f}',
                'severity': self._calculate_severity(magnitude)
            })
            return True
        return False
    
    def check_anomaly_alert(self, anomaly_score: float) -> bool:
        """Verifica alerta por anomalía"""
        if anomaly_score >= self.alert_thresholds['anomaly_score']:
            self._trigger_alert({
                'type': 'anomaly_alert',
                'anomaly_score': anomaly_score,
                'threshold': self.alert_thresholds['anomaly_score'],
                'message': f'⚠️  Anomalía detectada: {anomaly_score:.3f}',
                'severity': 'HIGH'
            })
            return True
        return False
    
    def check_activity_alert(self, event_count: int, time_window: str = '24h') -> bool:
        """Verifica alerta por actividad anómala"""
        threshold = self.alert_thresholds['daily_count']
        
        if event_count >= threshold:
            self._trigger_alert({
                'type': 'activity_alert',
                'event_count': event_count,
                'time_window': time_window,
                'threshold': threshold,
                'message': f'📊 Alta actividad: {event_count} eventos en {time_window}',
                'severity': 'MEDIUM'
            })
            return True
        return False
    
    def _calculate_severity(self, magnitude: float) -> str:
        """Calcula severidad basada en magnitud"""
        if magnitude >= 7.0:
            return 'CRITICAL'
        elif magnitude >= 6.0:
            return 'SEVERE'
        elif magnitude >= 5.0:
            return 'HIGH'
        elif magnitude >= 4.0:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _trigger_alert(self, alert_data: Dict):
        """Dispara alerta a todos los suscriptores"""
        alert_data['timestamp'] = datetime.now().isoformat()
        alert_data['id'] = len(self.active_alerts)
        
        self.active_alerts.append(alert_data)
        
        logger.warning(f"🚨 ALERTA: {alert_data['message']}")
        
        # Notificar suscriptores
        for callback in self.subscribers:
            try:
                callback(alert_data)
            except Exception as e:
                logger.error(f"Error en callback: {str(e)}")
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Obtiene alertas recientes"""
        return self.active_alerts[-limit:]
    
    def clear_alerts(self):
        """Limpia alertas"""
        self.active_alerts = []


class WebSocketAlertServer:
    """Servidor WebSocket para alertas en tiempo real"""
    
    def __init__(self, host: str = 'localhost', port: int = 8765):
        self.host = host
        self.port = port
        self.connected_clients = set()
        self.alert_system = RealtimeAlertSystem()
        
        if WEBSOCKET_AVAILABLE:
            self.alert_system.subscribe(self._broadcast_alert)
    
    async def _broadcast_alert(self, alert_data: Dict):
        """Envía alerta a todos los clientes conectados"""
        if not self.connected_clients:
            return
        
        message = json.dumps(alert_data)
        
        # Enviar a todos los clientes
        for client in list(self.connected_clients):
            try:
                await client.send(message)
            except Exception as e:
                logger.error(f"Error enviando alerta: {str(e)}")
                self.connected_clients.discard(client)
    
    async def handle_connection(self, websocket, path):
        """Maneja conexión de cliente"""
        self.connected_clients.add(websocket)
        client_ip = websocket.remote_address[0]
        logger.info(f"✓ Cliente conectado: {client_ip} (total: {len(self.connected_clients)})")
        
        try:
            async for message in websocket:
                # Procesar mensajes del cliente
                try:
                    data = json.loads(message)
                    await self._process_client_message(websocket, data)
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({'error': 'Invalid JSON'}))
        
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected_clients.discard(websocket)
            logger.info(f"✗ Cliente desconectado: {client_ip} (total: {len(self.connected_clients)})")
    
    async def _process_client_message(self, websocket, data: Dict):
        """Procesa comandos del cliente"""
        
        command = data.get('command')
        
        if command == 'get_thresholds':
            await websocket.send(json.dumps({
                'type': 'thresholds',
                'data': self.alert_system.alert_thresholds
            }))
        
        elif command == 'set_threshold':
            key = data.get('key')
            value = data.get('value')
            self.alert_system.set_thresholds(**{key: value})
            await websocket.send(json.dumps({'type': 'success'}))
        
        elif command == 'get_alerts':
            alerts = self.alert_system.get_recent_alerts(limit=10)
            await websocket.send(json.dumps({
                'type': 'alert_history',
                'data': alerts
            }))
    
    async def start(self):
        """Inicia servidor WebSocket"""
        if not WEBSOCKET_AVAILABLE:
            logger.error("websockets no instalado: pip install websockets")
            return
        
        async with websockets.serve(self.handle_connection, self.host, self.port):
            logger.info(f"✓ WebSocket server ejecutándose en ws://{self.host}:{self.port}")
            await asyncio.Future()  # Ejecutar indefinidamente


class ServerSentEventsAlertSystem:
    """Sistema de alertas con SSE (Server-Sent Events)"""
    
    def __init__(self):
        self.alert_system = RealtimeAlertSystem()
        self.streaming_clients = []
        
        # Suscribir a alertas
        self.alert_system.subscribe(self._format_sse_alert)
    
    def _format_sse_alert(self, alert_data: Dict):
        """Formatea alerta para SSE"""
        message = f"data: {json.dumps(alert_data)}\n\n"
        return message
    
    def get_sse_stream_endpoint(self):
        """Retorna función para endpoint SSE"""
        
        async def stream():
            alert_queue = asyncio.Queue()
            
            # Suscribirse
            self.alert_system.subscribe(lambda alert: alert_queue.put_nowait(alert))
            
            try:
                while True:
                    alert = await asyncio.wait_for(alert_queue.get(), timeout=30)
                    yield f"data: {json.dumps(alert)}\n\n"
            except asyncio.TimeoutError:
                yield f": keepalive\n\n"
        
        return stream


# Ejemplo de uso
if __name__ == '__main__':
    print("\n⚡ SISTEMA DE ALERTAS EN TIEMPO REAL")
    print("="*60 + "\n")
    
    # Crear sistema
    alerts = RealtimeAlertSystem()
    
    # Suscriptor de ejemplo
    def my_alert_handler(alert):
        print(f"[{alert['timestamp']}] {alert['message']}")
        print(f"  Tipo: {alert['type']}")
        print(f"  Severidad: {alert['severity']}\n")
    
    alerts.subscribe(my_alert_handler)
    
    # Configurar umbrales
    alerts.set_thresholds(
        magnitude=4.5,
        anomaly_score=0.7,
        daily_count=50
    )
    
    # Simular eventos
    print("📊 Simulando eventos sísmicos...\n")
    
    events = [
        (3.5, 0.2, "Normal", "Evento pequeño"),
        (5.2, 0.3, "Magnitud media", ""),
        (4.8, 0.85, "Anomalía detectada", ""),
        (6.1, 0.4, "Evento fuerte", ""),
    ]
    
    for mag, anom, desc, _ in events:
        print(f"🌍 Evento: {desc} (M{mag:.1f})")
        
        if mag >= 5.0:
            alerts.check_magnitude_alert(mag)
        
        if anom > 0.7:
            alerts.check_anomaly_alert(anom)
        
        print()
    
    # Mostrar alertas activas
    print("\n📋 Alertas activas:")
    for alert in alerts.get_recent_alerts():
        print(f"  - [{alert['severity']}] {alert['message']}")
