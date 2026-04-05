"""
🌊 SISTEMA DE PREDICCIÓN DE ALUDES (LAHARES)

Módulo especializado en predicción de lahares (flujos rápidos de barro, rock y agua
que descienden por volcanes). Los lahares son uno de los mayores peligros asociados
a erupciones volcánicas.

Volcanes colombianos con alto riesgo de lahares:
- Nevado del Ruiz (CRÍTICO): 68,000 personas en riesgo directo
- Nevado del Huila: 35,000 personas
- Puracé: 15,000 personas
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LaharEvent:
    """Representa un evento de lahar potencial"""
    
    volcano_id: str
    volcano_name: str
    origin_altitude: int  # Altitud de origen (m)
    peak_altitude: int  # Altitud del volcán (m)
    temperature: float  # Temperatura estimada (°C)
    moisture_content: float  # Contenido de humedad (%)
    velocity_kmh: float  # Velocidad estimada (km/h)
    volume_m3: float  # Volumen estimado (m³)
    distance_km: float  # Distancia recorrida (km)
    duration_hours: float  # Duración estimada (horas)
    population_at_risk: int  # Personas en riesgo
    rivers_affected: List[str]  # Ríos afectados
    severity_level: str  # CRÍTICO, SEVERO, ALTO, MODERADO, BAJO
    risk_score: float  # Score 0-100
    timestamp: str = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class LaharDetector:
    """Detección de lahares usando análisis multi-variable"""
    
    def __init__(self):
        self.lahar_history: List[LaharEvent] = []
        self.volcano_lahar_risk: Dict[str, Dict] = {}
        self._initialize_volcano_data()
    
    def _initialize_volcano_data(self):
        """Inicializa datos de riesgo de lahares por volcán"""
        self.volcano_lahar_risk = {
            "nevado_ruiz": {
                "name": "Nevado del Ruiz",
                "peak_altitude": 5321,
                "lahar_risk": 0.95,  # Muy alto riesgo
                "main_rivers": ["Río Magdalena", "Río Cauca"],
                "population_at_risk": 68000,
                "historical_events": 12,
                "last_major": "1985-11-13"
            },
            "nevado_huila": {
                "name": "Nevado del Huila",
                "peak_altitude": 5750,
                "lahar_risk": 0.85,
                "main_rivers": ["Río Páez", "Río Magdalena"],
                "population_at_risk": 35000,
                "historical_events": 8,
                "last_major": "1994-12-12"
            },
            "purace": {
                "name": "Puracé",
                "peak_altitude": 4646,
                "lahar_risk": 0.70,
                "main_rivers": ["Río Paez", "Río Magdalena"],
                "population_at_risk": 15000,
                "historical_events": 5,
                "last_major": "1977-04-20"
            },
            "galeras": {
                "name": "Galeras",
                "peak_altitude": 4276,
                "lahar_risk": 0.65,
                "main_rivers": ["Río Guáitara"],
                "population_at_risk": 8000,
                "historical_events": 3,
                "last_major": "1988-12-15"
            }
        }
    
    def predict_lahar_risk(
        self,
        volcano_id: str,
        seismic_magnitude: float,
        volcanic_gas_emissions: float,
        ground_deformation: float,
        recent_precipitation_mm: float,
        temperature_increase: float
    ) -> Tuple[LaharEvent, float]:
        """
        Predice riesgo de lahar usando múltiples variables
        
        Args:
            volcano_id: ID del volcán
            seismic_magnitude: Magnitud sísmica (M)
            volcanic_gas_emissions: Emisiones de gas (ton/día)
            ground_deformation: Deformación del suelo (cm/mes)
            recent_precipitation_mm: Lluvia reciente (mm/día)
            temperature_increase: Aumento de temperatura (°C/hora)
        
        Returns:
            (LaharEvent, probability) - Evento y probabilidad
        """
        
        if volcano_id not in self.volcano_lahar_risk:
            logger.warning(f"Volcán {volcano_id} no tiene datos de lahar")
            return None, 0.0
        
        volcano_data = self.volcano_lahar_risk[volcano_id]
        
        # Factores de riesgo normalizados (0-1)
        seismic_factor = min(1.0, seismic_magnitude / 8.0)  # Normalizar por 8.0
        gas_factor = min(1.0, volcanic_gas_emissions / 1000.0)  # Tom/día
        deformation_factor = min(1.0, ground_deformation / 50.0)  # cm/mes
        precipitation_factor = min(1.0, recent_precipitation_mm / 100.0)  # mm
        temperature_factor = min(1.0, temperature_increase / 5.0)  # °C/h
        
        # Cálculo de probabilidad de lahar usando weights
        probability = (
            seismic_factor * 0.25 +
            gas_factor * 0.20 +
            deformation_factor * 0.20 +
            precipitation_factor * 0.20 +
            temperature_factor * 0.15
        ) * volcano_data["lahar_risk"]
        
        # Estimaciones del evento
        if probability > 0.7:
            severity = "CRÍTICO"
            estimated_velocity = 80 + np.random.normal(10, 5)
            estimated_volume = 500e6 + np.random.normal(100e6, 50e6)
        elif probability > 0.5:
            severity = "SEVERO"
            estimated_velocity = 60 + np.random.normal(10, 5)
            estimated_volume = 300e6 + np.random.normal(50e6, 25e6)
        elif probability > 0.3:
            severity = "ALTO"
            estimated_velocity = 40 + np.random.normal(8, 4)
            estimated_volume = 100e6 + np.random.normal(25e6, 15e6)
        else:
            severity = "MODERADO"
            estimated_velocity = 20 + np.random.normal(5, 2)
            estimated_volume = 10e6 + np.random.normal(5e6, 2e6)
        
        # Calcular distancia y duración
        peak_altitude = volcano_data["peak_altitude"]
        origin_altitude = peak_altitude - np.random.randint(200, 1000)
        vertical_drop = peak_altitude - origin_altitude
        distance = vertical_drop / np.sin(np.radians(12))  # Ángulo promedio
        duration = distance / estimated_velocity * 60  # minutos
        
        lahar_event = LaharEvent(
            volcano_id=volcano_id,
            volcano_name=volcano_data["name"],
            origin_altitude=int(origin_altitude),
            peak_altitude=peak_altitude,
            temperature=80 + np.random.normal(20, 10),
            moisture_content=40 + np.random.normal(20, 10),
            velocity_kmh=estimated_velocity,
            volume_m3=int(estimated_volume),
            distance_km=distance / 1000,
            duration_hours=duration / 60,
            population_at_risk=volcano_data["population_at_risk"],
            rivers_affected=volcano_data["main_rivers"],
            severity_level=severity,
            risk_score=probability * 100
        )
        
        self.lahar_history.append(lahar_event)
        return lahar_event, probability
    
    def assess_river_flooding_risk(
        self,
        volcano_id: str,
        river_discharge_m3s: float,
        channel_capacity_m3s: float
    ) -> Dict:
        """
        Evalúa riesgo de inundación en ríos por lahares
        
        Args:
            volcano_id: ID del volcán
            river_discharge_m3s: Caudal actual del río (m³/s)
            channel_capacity_m3s: Capacidad del cauce (m³/s)
        
        Returns:
            Dict con análisis de desborde
        """
        
        if volcano_id not in self.volcano_lahar_risk:
            return {"error": "Volcán desconocido"}
        
        volcano = self.volcano_lahar_risk[volcano_id]
        rivers = volcano["main_rivers"]
        
        results = {
            "volcano_id": volcano_id,
            "volcano_name": volcano["name"],
            "rivers": [],
            "overall_flooding_risk": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
        for river in rivers:
            # Simulación de caudales
            lahar_contribution = river_discharge_m3s * 0.3  # Lahares aumentan 30% caudal
            total_discharge = river_discharge_m3s + lahar_contribution
            
            overflow_percentage = (total_discharge / channel_capacity_m3s - 1) * 100
            
            if overflow_percentage > 50:
                flooding_level = "CRÍTICO"
            elif overflow_percentage > 25:
                flooding_level = "ALTO"
            elif overflow_percentage > 0:
                flooding_level = "MODERADO"
            else:
                flooding_level = "BAJO"
            
            results["rivers"].append({
                "river_name": river,
                "current_discharge_m3s": round(river_discharge_m3s, 2),
                "lahar_contribution_m3s": round(lahar_contribution, 2),
                "total_discharge_m3s": round(total_discharge, 2),
                "channel_capacity_m3s": round(channel_capacity_m3s, 2),
                "overflow_percentage": round(overflow_percentage, 2),
                "flooding_level": flooding_level
            })
        
        # Calcular riesgo general
        flooding_levels = {"CRÍTICO": 1.0, "ALTO": 0.7, "MODERADO": 0.4, "BAJO": 0.1}
        avg_risk = np.mean([
            flooding_levels[r["flooding_level"]]
            for r in results["rivers"]
        ])
        results["overall_flooding_risk"] = round(avg_risk * 100, 2)
        
        return results
    
    def generate_lahar_alert(self, lahar_event: LaharEvent) -> Dict:
        """Genera alerta de lahar con detalles de evacuación"""
        
        alert = {
            "alert_id": f"LAHAR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "volcano": lahar_event.volcano_name,
            "severity": lahar_event.severity_level,
            "risk_score": lahar_event.risk_score,
            "message": f"⚠️ ALERTA DE LAHAR - {lahar_event.severity_level}",
            "details": {
                "estimated_velocity": f"{lahar_event.velocity_kmh:.1f} km/h",
                "estimated_volume": f"{lahar_event.volume_m3/1e6:.1f} millones m³",
                "travel_distance": f"{lahar_event.distance_km:.1f} km",
                "travel_time": f"{lahar_event.duration_hours:.1f} horas",
                "affected_rivers": ", ".join(lahar_event.rivers_affected),
                "population_at_risk": lahar_event.population_at_risk
            },
            "evacuation_areas": self._get_evacuation_zones(lahar_event),
            "recommended_actions": self._get_evacuation_recommendations(lahar_event)
        }
        
        return alert
    
    def _get_evacuation_zones(self, lahar_event: LaharEvent) -> List[str]:
        """Define zonas de evacuación según severidad"""
        
        if lahar_event.severity_level == "CRÍTICO":
            return [
                "Valle del río (0-5 km del cauce)",
                "Pendientes del volcán",
                "Poblaciones en ruta del flujo"
            ]
        elif lahar_event.severity_level == "SEVERO":
            return [
                "Valle del río (0-3 km del cauce)",
                "Poblaciones cercanas"
            ]
        else:
            return ["Áreas bajas del valle"]
    
    def _get_evacuation_recommendations(self, lahar_event: LaharEvent) -> List[str]:
        """Recomendaciones de evacuación según tipo de evento"""
        
        if lahar_event.severity_level == "CRÍTICO":
            return [
                "🚨 EVACUACIÓN INMEDIATA",
                "Salir hacia zonas altas",
                "No permanecer en valles o ríos",
                "Evitar carreteras en zonas bajas",
                "Contactar autoridades locales"
            ]
        elif lahar_event.severity_level == "SEVERO":
            return [
                "⚠️ Prepárese para evacuación rápida",
                "Tenga mochilas de emergencia listas",
                "Identifique rutas de escape",
                "Monitoree alertas constantemente"
            ]
        else:
            return [
                "ℹ️ Manténgase informado",
                "Evite accesos a ríos y quebradas"
            ]
    
    def get_lahar_statistics(self) -> Dict:
        """Retorna estadísticas de lahares detectados"""
        
        if not self.lahar_history:
            return {
                "total_events": 0,
                "message": "Sin eventos de lahar registrados"
            }
        
        df = pd.DataFrame([asdict(e) for e in self.lahar_history])
        
        return {
            "total_events_detected": len(self.lahar_history),
            "critical_events": len(df[df["severity_level"] == "CRÍTICO"]),
            "severe_events": len(df[df["severity_level"] == "SEVERO"]),
            "average_risk_score": float(df["risk_score"].mean()),
            "max_risk_score": float(df["risk_score"].max()),
            "most_affected_volcano": df["volcano_name"].mode()[0] if len(df) > 0 else "N/A",
            "total_population_at_risk": int(df["population_at_risk"].sum()),
            "average_velocity": float(df["velocity_kmh"].mean()),
            "largest_volume": float(df["volume_m3"].max())
        }


# Instancia global
lahar_detector = LaharDetector()


# Funciones de utilidad
def detect_lahar_threats(volcano_id: str, seismic_data: Dict) -> Dict:
    """Función simplificada para detectar amenazas de lahares"""
    
    event, probability = lahar_detector.predict_lahar_risk(
        volcano_id=volcano_id,
        seismic_magnitude=seismic_data.get("magnitude", 4.0),
        volcanic_gas_emissions=seismic_data.get("gas_emissions", 100),
        ground_deformation=seismic_data.get("ground_deformation", 5),
        recent_precipitation_mm=seismic_data.get("precipitation", 20),
        temperature_increase=seismic_data.get("temperature_increase", 1.5)
    )
    
    if event and probability > 0.3:
        alert = lahar_detector.generate_lahar_alert(event)
        return alert
    
    return {"risk_level": "BAJO", "probability": probability}
