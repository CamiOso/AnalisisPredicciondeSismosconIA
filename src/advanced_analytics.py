"""
📊 SISTEMA DE ANALYTICS AVANZADO

Sistema integral de análisis de datos para:
- Tendencias y patrones sísmicos
- Predicciones de mediano/largo plazo
- Análisis comparativo entre volcanes
- Indicadores de riesgo complejos
- Machine Learning insights
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TrendAnalysis:
    """Análisis de tendencias en series de tiempo"""
    
    trend_direction: str  # AUMENTANDO, DISMINUYENDO, ESTABLE
    trend_strength: float  # 0-1
    slope: float
    r_squared: float
    forecast_24h: float  # Predicción para 24h
    confidence: float  # 0-1


class AdvancedAnalytics:
    """Sistema avanzado de análisis de datos sísmicos"""
    
    def __init__(self):
        self.volcano_data_cache: Dict[str, List[Dict]] = {}
        self.analysis_cache: Dict[str, Dict] = {}
        self.ml_models: Dict[str, object] = {}
        self.time_windows = {
            "1h": timedelta(hours=1),
            "24h": timedelta(hours=24),
            "7d": timedelta(days=7),
            "30d": timedelta(days=30),
            "90d": timedelta(days=90)
        }
    
    def analyze_trend(
        self,
        volcano_id: str,
        magnitudes: List[float],
        timestamps: List[str] = None,
        window_hours: int = 24
    ) -> TrendAnalysis:
        """
        Analiza tendencias en magnitud sísmica
        
        Args:
            volcano_id: ID del volcán
            magnitudes: Lista de magnitudes sísmicas
            timestamps: Timestamps de los eventos (opcional)
            window_hours: Ventana de análisis en horas
        
        Returns:
            TrendAnalysis con dirección y pronóstico
        """
        
        if len(magnitudes) < 2:
            return TrendAnalysis(
                trend_direction="INSUFICIENTE_DATOS",
                trend_strength=0.0,
                slope=0.0,
                r_squared=0.0,
                forecast_24h=0.0,
                confidence=0.0
            )
        
        # Convertir a array numpy
        y = np.array(magnitudes, dtype=float)
        x = np.arange(len(y))
        
        # Regresión lineal
        coeffs = np.polyfit(x, y, 1)
        slope = coeffs[0]
        
        # Calcular R²
        y_predict = np.polyval(coeffs, x)
        ss_res = np.sum((y - y_predict) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Determinar dirección
        if abs(slope) < 0.005:
            trend_direction = "ESTABLE"
            trend_strength = 0.0
        elif slope > 0:
            trend_direction = "AUMENTANDO"
            trend_strength = min(1.0, abs(slope) / 0.1)
        else:
            trend_direction = "DISMINUYENDO"
            trend_strength = min(1.0, abs(slope) / 0.1)
        
        # Pronóstico para 24h (asumir 24 eventos más)
        next_x = len(y) + 24
        forecast_24h = np.polyval(coeffs, next_x)
        forecast_24h = max(2.0, min(9.0, forecast_24h))  # Clamp entre 2 y 9
        
        # Confianza basada en R²
        confidence = abs(r_squared)
        
        return TrendAnalysis(
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            slope=slope,
            r_squared=r_squared,
            forecast_24h=forecast_24h,
            confidence=confidence
        )
    
    def calculate_complex_risk_index(
        self,
        volcano_id: str,
        seismic_events: List[Dict],
        deformation_rate: float,
        gas_emissions: float,
        population_at_risk: int
    ) -> Dict:
        """
        Calcula índice de riesgo complejo combinando múltiples factores
        
        Args:
            volcano_id: ID del volcán
            seismic_events: Lista de eventos sísmicos
            deformation_rate: Tasa de deformación (cm/mes)
            gas_emissions: Emisiones de gas (ton/día)
            population_at_risk: Población en riesgo
        
        Returns:
            Dict con componentes del índice de riesgo
        """
        
        components = {}
        
        # 1. Análisis sísmico (30% del peso)
        if seismic_events:
            magnitudes = [e.get("magnitude", 0) for e in seismic_events]
            trend = self.analyze_trend(volcano_id, magnitudes)
            
            # Calcular nivel de actividad
            recent_events = len([e for e in seismic_events 
                               if e.get("hours_ago", 24) < 24])
            avg_magnitude = np.mean(magnitudes) if magnitudes else 0
            
            seismic_score = (
                (min(recent_events / 10, 1.0) * 0.4) +  # 4-5 eventos en 24h = alto
                (min(avg_magnitude / 8.0, 1.0) * 0.3) +  # Magnitud media
                (trend.trend_strength * 0.3)  # Tendencia
            )
            
            components["seismic_score"] = {
                "score": round(seismic_score, 3),
                "recent_events_24h": recent_events,
                "average_magnitude": round(avg_magnitude, 2),
                "trend": trend.trend_direction
            }
        else:
            components["seismic_score"] = {"score": 0.0}
        
        # 2. Deformación (25% del peso)
        deformation_score = min(deformation_rate / 50.0, 1.0)  # >50 cm/mes es crítico
        components["deformation_score"] = {
            "score": round(deformation_score, 3),
            "deformation_rate_cm_month": deformation_rate
        }
        
        # 3. Emisiones de gas (25% del peso)
        gas_score = min(gas_emissions / 5000.0, 1.0)  # >5000 ton/día es crítico
        components["gas_score"] = {
            "score": round(gas_score, 3),
            "emissions_ton_day": gas_emissions
        }
        
        # 4. Población en riesgo (20% del peso, factor de impacto)
        impact_score = min(population_at_risk / 500000.0, 1.0)
        components["impact_score"] = {
            "score": round(impact_score, 3),
            "population_at_risk": population_at_risk
        }
        
        # Calcular índice combinado
        weights = {
            "seismic_score": 0.30,
            "deformation_score": 0.25,
            "gas_score": 0.25,
            "impact_score": 0.20
        }
        
        total_risk_index = sum(
            components.get(key, {}).get("score", 0) * weight
            for key, weight in weights.items()
        )
        
        # Clasificar nivel de riesgo
        if total_risk_index >= 0.75:
            risk_level = "CRÍTICO"
        elif total_risk_index >= 0.50:
            risk_level = "ALTO"
        elif total_risk_index >= 0.30:
            risk_level = "MODERADO"
        elif total_risk_index >= 0.15:
            risk_level = "BAJO"
        else:
            risk_level = "MUY BAJO"
        
        return {
            "volcano_id": volcano_id,
            "risk_index": round(total_risk_index, 3),
            "risk_level": risk_level,
            "timestamp": datetime.now().isoformat(),
            "components": components,
            "recommendations": self._generate_recommendations(total_risk_index, risk_level)
        }
    
    def compare_volcano_activity(self, volcanoes_data: List[Dict]) -> Dict:
        """
        Compara actividad sísmica entre múltiples volcanes
        
        Args:
            volcanoes_data: Lista de diccionarios con datos de volcanes
                {"volcano_id": "...", "magnitudes": [...], "population": ...}
        
        Returns:
            Análisis comparativo
        """
        
        comparison_results = {
            "timestamp": datetime.now().isoformat(),
            "total_volcanoes": len(volcanoes_data),
            "volcanoes": [],
            "ranking": []
        }
        
        volcano_scores = []
        
        for volcano in volcanoes_data:
            volcano_id = volcano.get("volcano_id")
            magnitudes = volcano.get("magnitudes", [])
            
            if not magnitudes:
                continue
            
            # Calcular score de actividad
            recent_events = len([m for m in magnitudes if m > 3.5])
            avg_magnitude = np.mean(magnitudes)
            max_magnitude = np.max(magnitudes)
            
            activity_score = (
                (recent_events / max(1, len(magnitudes))) * 0.4 +
                (avg_magnitude / 8.0) * 0.35 +
                (max_magnitude / 8.0) * 0.25
            )
            
            volcano_scores.append({
                "volcano_id": volcano_id,
                "volcano_name": volcano.get("name", "Unknown"),
                "activity_score": round(activity_score, 3),
                "recent_events_m35": recent_events,
                "avg_magnitude": round(avg_magnitude, 2),
                "max_magnitude": round(max_magnitude, 2)
            })
        
        # Ordenar por score
        volcano_scores.sort(key=lambda x: x["activity_score"], reverse=True)
        
        comparison_results["ranking"] = volcano_scores
        
        return comparison_results
    
    def forecast_activity(
        self,
        volcano_id: str,
        historical_data: List[Tuple[str, float]],
        days_ahead: int = 30
    ) -> Dict:
        """
        Pronóstico de actividad sísmica para días futuros
        
        Args:
            volcano_id: ID del volcán
            historical_data: Lista de (timestamp, magnitud) tuples
            days_ahead: Días a pronosticar
        
        Returns:
            Pronóstico con intervalos de confianza
        """
        
        if len(historical_data) < 10:
            return {
                "status": "insufficient_data",
                "message": "Se necesitan al menos 10 datos históricos"
            }
        
        # Preparar datos
        magnitudes = np.array([m for _, m in historical_data])
        
        # Análisis de tendencia
        trend = self.analyze_trend(volcano_id, magnitudes.tolist())
        
        # Generar pronóstico simple usando tendencia
        forecast_data = []
        current_level = magnitudes[-1]
        
        for day in range(1, days_ahead + 1):
            # Pronóstico lineal con ruido
            predicted_value = current_level + (trend.slope * day)
            predicted_value = max(2.0, min(8.0, predicted_value))
            
            # Intervalo de confianza
            confidence_interval = (
                predicted_value - (0.5 * (1 - trend.confidence)),
                predicted_value + (0.5 * (1 - trend.confidence))
            )
            
            forecast_data.append({
                "day": day,
                "forecast": round(predicted_value, 2),
                "lower_bound": round(confidence_interval[0], 2),
                "upper_bound": round(confidence_interval[1], 2),
                "confidence": round(trend.confidence, 2)
            })
        
        return {
            "volcano_id": volcano_id,
            "forecast_days": days_ahead,
            "trend": trend.trend_direction,
            "forecast_data": forecast_data,
            "timestamp": datetime.now().isoformat()
        }
    
    def detect_anomalies(
        self,
        volcano_id: str,
        magnitudes: List[float],
        threshold_std: float = 2.0
    ) -> Dict:
        """
        Detecta anomalías en serie de magnitudes usando desviación estándar
        
        Args:
            volcano_id: ID del volcán
            magnitudes: Lista de magnitudes
            threshold_std: Número de desviaciones estándar
        
        Returns:
            Diccionario con anomalías detectadas
        """
        
        if len(magnitudes) < 3:
            return {"error": "Dos pocas muestras"}
        
        magnitudes = np.array(magnitudes, dtype=float)
        mean = np.mean(magnitudes)
        std = np.std(magnitudes)
        
        anomalies = []
        
        for i, magnitude in enumerate(magnitudes):
            z_score = abs((magnitude - mean) / std) if std > 0 else 0
            
            if z_score > threshold_std:
                anomalies.append({
                    "index": i,
                    "magnitude": magnitude,
                    "z_score": round(z_score, 2),
                    "deviation": round(magnitude - mean, 2),
                    "anomaly_type": "ALTA" if magnitude > mean else "BAJA"
                })
        
        return {
            "volcano_id": volcano_id,
            "total_points": len(magnitudes),
            "anomalies_detected": len(anomalies),
            "mean_magnitude": round(mean, 2),
            "std_deviation": round(std, 2),
            "threshold_z_score": threshold_std,
            "anomalies": anomalies,
            "timestamp": datetime.now().isoformat()
        }
    
    def calculate_seismic_moment(self, magnitude: float) -> Dict:
        """
        Calcula el momento sísmico (Mo) basado en magnitud
        Usando: log10(Mo) = 1.5*M + 4.8
        """
        
        log_mo = 1.5 * magnitude + 4.8
        moment = 10 ** log_mo
        energy_joules = moment / 1.5e4  # Conversión a energía
        
        return {
            "magnitude": magnitude,
            "seismic_moment_dyne_cm": f"{moment:.2e}",
            "energy_joules": f"{energy_joules:.2e}",
            "energy_equivalent_tnt": f"{energy_joules/4.184e15:.2f} megatones"
        }
    
    def get_statistical_summary(self, magnitudes: List[float]) -> Dict:
        """Retorna resumen estadístico de magnitudes"""
        
        data = np.array(magnitudes, dtype=float)
        
        return {
            "count": len(data),
            "mean": round(np.mean(data), 3),
            "median": round(np.median(data), 3),
            "std_dev": round(np.std(data), 3),
            "min": round(np.min(data), 3),
            "max": round(np.max(data), 3),
            "q25": round(np.percentile(data, 25), 3),
            "q75": round(np.percentile(data, 75), 3),
            "iqr": round(np.percentile(data, 75) - np.percentile(data, 25), 3)
        }
    
    def _generate_recommendations(self, risk_index: float, risk_level: str) -> List[str]:
        """Genera recomendaciones basadas en nivel de riesgo"""
        
        recommendations = {
            "CRÍTICO": [
                "🚨 Activar protocolo de emergencia inmediatamente",
                "Iniciar evacuación de zonas de riesgo",
                "Contactar a autoridades civiles",
                "Monitoreo 24/7 del volcán",
                "Comunicados de prensa cada hora"
            ],
            "ALTO": [
                "⚠️ Aumentar frecuencia de monitoreo 4 veces/día",
                "Alertar a poblaciones potencialmente afectadas",
                "Preparar planes de evacuación",
                "Comunicados diarios al público",
                "Coordinar con autoridades locales"
            ],
            "MODERADO": [
                "ℹ️ Monitoreo normal (2 veces/día)",
                "Mantener comunicación con comunidades cercanas",
                "Revisar planes de contingencia",
                "Comunicados semanales",
                "Análisis de tendencias"
            ],
            "BAJO": [
                "✓ Continuación de monitoreo rutinario",
                "Análisis de nuevos datos",
                "Comunicación periódica (mensual)"
            ],
            "MUY BAJO": [
                "✓ Monitoreo normal",
                "Actividades de investigación científica"
            ]
        }
        
        return recommendations.get(risk_level, [])


# Instancia global
advanced_analytics = AdvancedAnalytics()
