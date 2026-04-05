"""
Monitor Especializado de Volcanes Colombianos
Integración completa con el sistema multi-volcán
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from src.colombian_volcanoes import (
    get_colombian_volcanoes,
    get_active_colombian_volcanoes,
    get_critical_colombian_volcanoes,
    get_high_risk_colombian_volcanoes,
    get_volcano_population_risk,
    get_volcano_nearby_cities,
    get_volcano_hazards,
    get_colombian_volcano_summary
)


logger = logging.getLogger(__name__)


class ColombiaNVolcanoMonitor:
    """Monitor especializado para volcanes de Colombia"""
    
    def __init__(self):
        self.volcanoes = get_colombian_volcanoes()
        self.seismic_data: Dict[str, List[Dict]] = {}
        self.alert_history: Dict[str, List[Dict]] = {}
        
        # Inicializar estructuras de datos
        for volcano_id in self.volcanoes:
            self.seismic_data[volcano_id] = []
            self.alert_history[volcano_id] = []
    
    def get_all_colombian_volcanoes(self) -> List[Dict]:
        """Retorna lista de todos los volcanes colombianos"""
        return [
            {
                "id": v_id,
                "name": volcano.name,
                "elevation": volcano.elevation_m,
                "region": volcano.region,
                "risk_level": volcano.risk_level,
                "active": volcano.active,
                "last_eruption": volcano.last_eruption,
                "population_at_risk": get_volcano_population_risk(v_id),
                "nearby_cities": get_volcano_nearby_cities(v_id)
            }
            for v_id, volcano in self.volcanoes.items()
        ]
    
    def get_active_volcanoes(self) -> List[Dict]:
        """Retorna volcanes activos de Colombia"""
        active = get_active_colombian_volcanoes()
        return [
            {
                "id": v_id,
                "name": volcano.name,
                "elevation": volcano.elevation_m,
                "risk_level": volcano.risk_level,
                "active_status": "Activo" if volcano.active else "Inactivo"
            }
            for v_id, volcano in active.items()
        ]
    
    def get_critical_volcanoes(self) -> List[Dict]:
        """Retorna volcanes de riesgo crítico"""
        critical = get_critical_colombian_volcanoes()
        return [
            {
                "id": v_id,
                "name": volcano.name,
                "elevation": volcano.elevation_m,
                "last_eruption": volcano.last_eruption,
                "population_at_risk": get_volcano_population_risk(v_id),
                "nearby_cities": ", ".join(get_volcano_nearby_cities(v_id)),
                "hazards": get_volcano_hazards(v_id)
            }
            for v_id, volcano in critical.items()
        ]
    
    def get_high_risk_volcanoes(self) -> List[Dict]:
        """Retorna volcanes de alto riesgo (CRITICAL + HIGH)"""
        high_risk = get_high_risk_colombian_volcanoes()
        return [
            {
                "id": v_id,
                "name": volcano.name,
                "risk_level": volcano.risk_level,
                "monitoring_stations": self._get_monitoring_stations(v_id),
                "last_activity": volcano.last_eruption,
                "alert_status": self._get_alert_status(v_id)
            }
            for v_id, volcano in high_risk.items()
        ]
    
    def add_seismic_event(
        self,
        volcano_id: str,
        magnitude: float,
        depth: float,
        latitude: float,
        longitude: float,
        location: str
    ) -> bool:
        """Agrega evento sísmico para volcán colombiano"""
        if volcano_id not in self.seismic_data:
            logger.warning(f"Volcán no existe: {volcano_id}")
            return False
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "magnitude": magnitude,
            "depth": depth,
            "latitude": latitude,
            "longitude": longitude,
            "location": location
        }
        
        self.seismic_data[volcano_id].append(event)
        
        # Generar alerta si es necesario
        self._check_and_generate_alert(volcano_id, magnitude)
        
        logger.info(f"Evento sísmico registrado: {volcano_id} M{magnitude}")
        return True
    
    def get_volcano_activity(self, volcano_id: str, days: int = 7) -> Dict:
        """Obtiene actividad sísmica de los últimos N días"""
        if volcano_id not in self.seismic_data:
            return {}
        
        cutoff = datetime.now() - timedelta(days=days)
        events = [
            e for e in self.seismic_data[volcano_id]
            if datetime.fromisoformat(e["timestamp"]) >= cutoff
        ]
        
        if not events:
            return {
                "volcano_id": volcano_id,
                "period_days": days,
                "total_events": 0,
                "activity_level": "BAJO"
            }
        
        magnitudes = [e["magnitude"] for e in events]
        
        return {
            "volcano_id": volcano_id,
            "period_days": days,
            "total_events": len(events),
            "avg_magnitude": round(np.mean(magnitudes), 2),
            "max_magnitude": round(np.max(magnitudes), 2),
            "min_magnitude": round(np.min(magnitudes), 2),
            "std_deviation": round(np.std(magnitudes), 2),
            "activity_level": self._classify_activity(len(events), np.mean(magnitudes))
        }
    
    def _check_and_generate_alert(self, volcano_id: str, magnitude: float):
        """Genera alerta si el evento cumple criterios"""
        volcano = self.volcanoes.get(volcano_id)
        if not volcano:
            return
        
        # Thresholds por nivel de riesgo
        thresholds = {
            "CRITICAL": 3.5,
            "HIGH": 4.0,
            "MEDIUM": 4.5,
            "LOW": 5.0
        }
        
        threshold = thresholds.get(volcano.risk_level, 4.5)
        
        if magnitude >= threshold:
            alert = {
                "timestamp": datetime.now().isoformat(),
                "volcano": volcano.name,
                "magnitude": magnitude,
                "severity": self._classify_severity(magnitude, volcano.risk_level),
                "message": f"Alerta sísmica en {volcano.name}: Magnitud {magnitude}"
            }
            
            self.alert_history[volcano_id].append(alert)
            logger.warning(f"ALERTA: {alert['message']}")
    
    def _classify_severity(self, magnitude: float, risk_level: str) -> str:
        """Clasifica severidad de evento"""
        if magnitude >= 6.0:
            return "🚨 CRÍTICO"
        elif magnitude >= 5.0:
            return "🔴 SEVERO"
        elif magnitude >= 4.0:
            return "🟠 ALTO"
        elif magnitude >= 3.0:
            return "🟡 MODERADO"
        else:
            return "🟢 BAJO"
    
    def _classify_activity(self, event_count: int, avg_magnitude: float) -> str:
        """Clasifica nivel de actividad sísmica"""
        if event_count > 50 and avg_magnitude > 4.5:
            return "CRÍTICO"
        elif event_count > 30 and avg_magnitude > 4.0:
            return "MUY ALTO"
        elif event_count > 15 and avg_magnitude > 3.5:
            return "ALTO"
        elif event_count > 5:
            return "MODERADO"
        else:
            return "BAJO"
    
    def _get_monitoring_stations(self, volcano_id: str) -> int:
        """Obtiene número de estaciones de monitoreo"""
        stations = {
            "nevado_ruiz": 15,
            "galeras": 12,
            "purace": 8,
            "tolima": 10,
            "huila": 7,
            "cumbal": 5,
            "cerro_negro": 4,
            "tama": 3,
            "sotara": 3,
            "romeral": 2,
            "santa_isabel": 3,
            "chiles": 3,
            "cerro_bravo": 1,
        }
        return stations.get(volcano_id, 0)
    
    def _get_alert_status(self, volcano_id: str) -> str:
        """Obtiene estado de alerta actual"""
        recent_alerts = [
            a for a in self.alert_history.get(volcano_id, [])
            if datetime.fromisoformat(a["timestamp"]) >= 
               datetime.now() - timedelta(hours=24)
        ]
        
        if not recent_alerts:
            return "Sin alertas"
        
        return f"{len(recent_alerts)} alerta(s) en últimas 24h"
    
    def get_regional_summary(self, region: str) -> Dict:
        """Obtiene resumen de actividad por región"""
        region_volcanoes = [
            (v_id, v) for v_id, v in self.volcanoes.items()
            if region.lower() in v.region.lower()
        ]
        
        if not region_volcanoes:
            return {"region": region, "volcanoes": []}
        
        return {
            "region": region,
            "volcanoes_count": len(region_volcanoes),
            "volcanoes": [
                {
                    "id": v_id,
                    "name": volcano.name,
                    "risk_level": volcano.risk_level,
                    "activity": self.get_volcano_activity(v_id).get("activity_level", "BAJO")
                }
                for v_id, volcano in region_volcanoes
            ]
        }
    
    def get_colombia_monitoring_report(self) -> Dict:
        """Genera reporte completo de monitoreo en Colombia"""
        summary = get_colombian_volcano_summary()
        
        return {
            "report_date": datetime.now().isoformat(),
            "country": "Colombia",
            "summary": summary,
            "critical_volcanoes": self.get_critical_volcanoes(),
            "high_risk_volcanoes": self.get_high_risk_volcanoes(),
            "active_volcanoes": self.get_active_volcanoes(),
            "total_population_at_risk": summary["total_population_at_risk"],
            "monitoring_authority": "Servicio Geológico Colombiano (SGC)",
            "recommendation": self._generate_recommendation()
        }
    
    def _generate_recommendation(self) -> str:
        """Genera recomendación general"""
        critical_count = len(self.get_critical_volcanoes())
        
        if critical_count >= 2:
            return "⚠️ Múltiples volcanes en estado crítico. Incrementar vigilancia en regiones volcánicas."
        elif critical_count == 1:
            return "🔴 Un volcán en estado crítico. Monitoreo activo recomendado."
        else:
            return "✓ Situación estable. Continuar con monitoreo rutinario."
    
    def export_regional_data(self, region: str, format: str = "csv") -> Optional[str]:
        """Exporta datos sísmicos por región"""
        region_volcanoes = {
            v_id: v for v_id, v in self.volcanoes.items()
            if region.lower() in v.region.lower()
        }
        
        all_events = []
        for v_id in region_volcanoes:
            for event in self.seismic_data.get(v_id, []):
                event["volcano_id"] = v_id
                all_events.append(event)
        
        if not all_events:
            return None
        
        df = pd.DataFrame(all_events)
        
        if format == "csv":
            return df.to_csv(index=False)
        elif format == "json":
            return df.to_json(orient="records", date_format="iso")
        
        return None


# Instancia global
colombia_monitor = ColombiaNVolcanoMonitor()
