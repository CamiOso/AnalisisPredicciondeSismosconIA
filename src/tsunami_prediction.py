"""
Sistema de Predicción de Tsunamis
Analiza eventos sísmicos y predice riesgo de tsunamis
"""

from typing import Dict, Optional, List, Tuple
import numpy as np
from datetime import datetime
import logging
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class TsunamiRiskAssessment:
    """Evaluación de riesgo de tsunami"""
    earthquake_magnitude: float
    earthquake_depth: float
    earthquake_latitude: float
    earthquake_longitude: float
    location_name: str
    
    # Resultados
    tsunami_probability: float  # 0-1
    estimated_wave_height: float  # metros
    travel_time_minutes: int  # Minutos hasta costa
    risk_level: str  # NONE, LOW, MEDIUM, HIGH, CRITICAL
    affected_coasts: List[str]
    recommendation: str


class TsunamiPredictionSystem:
    """Sistema inteligente de predicción de tsunamis"""
    
    # Thresholds
    MAGNITUDE_THRESHOLD = 6.5  # Magnitud mínima para tsunami
    DEPTH_THRESHOLD = 50  # Profundidad máxima en km
    
    # Ubicaciones costeras de referencia (lat, lon, nombre)
    COASTAL_LOCATIONS = {
        "deception_coast": (-62.9723, -60.6477, "Deception Island Coast"),
        "southeast_asia": (5.0, 105.0, "Southeast Asia Coast"),
        "japan_coast": (36.0, 138.0, "Japan Coast"),
        "california_coast": (36.5, -121.5, "California Coast"),
        "chile_coast": (-40.0, -72.0, "Chile Coast"),
        "new_zealand_coast": (-40.0, 174.0, "New Zealand Coast"),
        "indonesia_coast": (-2.0, 113.0, "Indonesia Coast"),
        "mediterranean": (40.0, 15.0, "Mediterranean Coast"),
    }
    
    def __init__(self):
        self.risk_assessments: List[TsunamiRiskAssessment] = []
        self.historical_events = []
    
    def assess_tsunami_risk(
        self,
        magnitude: float,
        depth: float,
        latitude: float,
        longitude: float,
        location_name: str
    ) -> TsunamiRiskAssessment:
        """
        Evalúa riesgo de tsunami para un evento sísmico
        
        Args:
            magnitude: Magnitud del terremoto (Richter)
            depth: Profundidad en km
            latitude: Latitud del epicentro
            longitude: Longitud del epicentro
            location_name: Nombre de la ubicación
        
        Returns:
            TsunamiRiskAssessment con predicción detallada
        """
        
        # Calcular probabilidad basada en magnitud
        if magnitude < self.MAGNITUDE_THRESHOLD:
            tsunami_probability = 0.0
        else:
            # Función sigmoidea para probabilidad
            tsunami_probability = 1.0 / (1.0 + np.exp(-(magnitude - 6.5) * 0.8))
        
        # Ajustar por profundidad (terremotos profundos generan menos tsunamis)
        if depth > self.DEPTH_THRESHOLD:
            depth_factor = max(0.1, 1.0 - (depth - self.DEPTH_THRESHOLD) / 500)
            tsunami_probability *= depth_factor
        
        # Calcular altura estimada de onda
        if tsunami_probability > 0:
            # Fórmula empírica
            estimated_wave_height = 0.5 * (magnitude - 5.0) + 0.3 * np.log(max(1, 50 - depth))
            estimated_wave_height = max(0, estimated_wave_height)
        else:
            estimated_wave_height = 0.0
        
        # Encontrar costas afectadas
        affected_coasts = self._find_affected_coasts(latitude, longitude)
        
        # Calcular tiempo de viaje
        travel_time_minutes = self._calculate_travel_time(
            latitude, longitude, affected_coasts
        ) if affected_coasts else 0
        
        # Determinar nivel de riesgo
        if tsunami_probability == 0:
            risk_level = "NONE"
        elif tsunami_probability < 0.1:
            risk_level = "LOW"
        elif tsunami_probability < 0.3:
            risk_level = "MEDIUM"
        elif tsunami_probability < 0.6:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
        
        # Generar recomendación
        recommendation = self._generate_recommendation(
            risk_level, tsunami_probability, travel_time_minutes
        )
        
        assessment = TsunamiRiskAssessment(
            earthquake_magnitude=magnitude,
            earthquake_depth=depth,
            earthquake_latitude=latitude,
            earthquake_longitude=longitude,
            location_name=location_name,
            tsunami_probability=round(tsunami_probability, 3),
            estimated_wave_height=round(estimated_wave_height, 2),
            travel_time_minutes=travel_time_minutes,
            risk_level=risk_level,
            affected_coasts=affected_coasts,
            recommendation=recommendation
        )
        
        self.risk_assessments.append(assessment)
        return assessment
    
    def _find_affected_coasts(
        self,
        epicenter_lat: float,
        epicenter_lon: float,
        radius_degrees: float = 30.0
    ) -> List[str]:
        """Encuentra costas potencialmente afectadas"""
        affected = []
        
        for location_id, (lat, lon, name) in self.COASTAL_LOCATIONS.items():
            # Distancia aproximada en grados
            distance = np.sqrt(
                (lat - epicenter_lat)**2 + (lon - epicenter_lon)**2
            )
            
            if distance < radius_degrees:
                affected.append(name)
        
        return affected
    
    def _calculate_travel_time(
        self,
        epicenter_lat: float,
        epicenter_lon: float,
        affected_coasts: List[str]
    ) -> int:
        """Calcula tiempo de viaje aproximado en minutos"""
        # Velocidad de tsunami: ~800 km/h
        tsunami_speed_kmh = 800
        
        if not affected_coasts:
            return 0
        
        # Calcular distancia promedio a costas afectadas
        distances = []
        for location_id, (lat, lon, name) in self.COASTAL_LOCATIONS.items():
            if name in affected_coasts:
                # Distancia en grados a km (~111 km por grado)
                distance_degrees = np.sqrt(
                    (lat - epicenter_lat)**2 + (lon - epicenter_lon)**2
                )
                distance_km = distance_degrees * 111
                distances.append(distance_km)
        
        if distances:
            avg_distance = np.mean(distances)
            travel_time_hours = avg_distance / tsunami_speed_kmh
            return max(5, int(travel_time_hours * 60))  # Mínimo 5 minutos
        
        return 0
    
    def _generate_recommendation(
        self,
        risk_level: str,
        probability: float,
        travel_time: int
    ) -> str:
        """Genera recomendación basada en evaluación"""
        recommendations = {
            "NONE": "Riesgo de tsunami inexistente. Continuar monitoreo normal.",
            "LOW": f"Riesgo bajo ({probability:.1%}). Monitoreo activo recomendado.",
            "MEDIUM": f"Riesgo moderado ({probability:.1%}). Alertar a costas cercanas. Tiempo: ~{travel_time}min",
            "HIGH": f"RIESGO ALTO ({probability:.1%}). EVACUAR costas. Onda en ~{travel_time}min.",
            "CRITICAL": f"🚨 RIESGO CRÍTICO ({probability:.1%}). EVACUACIÓN INMEDIATA. Onda en ~{travel_time}min."
        }
        return recommendations.get(risk_level, "Evaluación pendiente")
    
    def get_recent_assessments(self, limit: int = 10) -> List[Dict]:
        """Retorna evaluaciones recientes"""
        return [
            {
                "magnitude": a.earthquake_magnitude,
                "depth": a.earthquake_depth,
                "location": a.location_name,
                "tsunami_probability": a.tsunami_probability,
                "risk_level": a.risk_level,
                "wave_height": a.estimated_wave_height,
                "affected_coasts": a.affected_coasts
            }
            for a in self.risk_assessments[-limit:]
        ]
    
    def get_high_risk_assessments(self) -> List[Dict]:
        """Retorna evaluaciones de alto riesgo"""
        high_risk = [
            a for a in self.risk_assessments 
            if a.risk_level in ["HIGH", "CRITICAL"]
        ]
        return [
            {
                "magnitude": a.earthquake_magnitude,
                "location": a.location_name,
                "tsunami_probability": a.tsunami_probability,
                "risk_level": a.risk_level,
                "wave_height": a.estimated_wave_height,
                "affected_coasts": a.affected_coasts,
                "recommendation": a.recommendation
            }
            for a in high_risk
        ]
    
    def calculate_coast_risk(self, coast_name: str) -> float:
        """Calcula riesgo agregado para una costa"""
        risks = [
            a.tsunami_probability
            for a in self.risk_assessments
            if coast_name in a.affected_coasts
        ]
        
        if not risks:
            return 0.0
        
        return max(risks)
    
    def get_tsunami_statistics(self) -> Dict:
        """Retorna estadísticas de evaluaciones"""
        if not self.risk_assessments:
            return {
                "total_assessments": 0,
                "high_risk_count": 0,
                "avg_probability": 0.0
            }
        
        high_risk_count = sum(
            1 for a in self.risk_assessments 
            if a.risk_level in ["HIGH", "CRITICAL"]
        )
        
        probabilities = [a.tsunami_probability for a in self.risk_assessments]
        
        return {
            "total_assessments": len(self.risk_assessments),
            "high_risk_count": high_risk_count,
            "avg_probability": round(np.mean(probabilities), 3),
            "max_probability": max(probabilities),
            "coastal_risks": {
                coast: self.calculate_coast_risk(coast)
                for coast in set(
                    coast for a in self.risk_assessments
                    for coast in a.affected_coasts
                )
            }
        }


# Instancia global
tsunami_system = TsunamiPredictionSystem()
