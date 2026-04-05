"""
Sistema de Reportes Automáticos
Genera reportes diarios/semanales en PDF y envía por email
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import json


logger = logging.getLogger(__name__)


@dataclass
class ReportConfig:
    """Configuración de reportes"""
    report_type: str  # daily, weekly, monthly
    recipients: List[str]
    include_metrics: bool = True
    include_charts: bool = True
    include_forecast: bool = True
    include_alerts: bool = True
    include_social_media: bool = True
    language: str = "es"


class ReportGenerator:
    """Genera reportes automáticos en múltiples formatos"""
    
    def __init__(self):
        self.generated_reports: List[Dict] = []
        self.scheduled_reports: Dict[str, ReportConfig] = {}
    
    def generate_daily_report(
        self,
        volcano_id: str,
        seismic_data: Dict,
        metrics: Dict,
        predictions: Dict,
        alerts: List[Dict],
        social_sentiment: Dict
    ) -> Dict:
        """
        Genera reporte diario configuración completo
        
        Args:
            volcano_id: ID del volcán
            seismic_data: Datos sísmicos del día
            metrics: Métricas calculadas
            predictions: Predicciones para 7 días
            alerts: Alertas generadas
            social_sentiment: Análisis de redes sociales
        
        Returns:
            Diccionario con contenido del reporte
        """
        report_date = datetime.now()
        
        content = {
            "title": f"Reporte Diario - {volcano_id.upper()}",
            "date": report_date.isoformat(),
            "volcano_id": volcano_id,
            
            "executive_summary": {
                "report_type": "daily",
                "generated_at": report_date.isoformat(),
                "total_events": seismic_data.get("event_count", 0),
                "avg_magnitude": round(seismic_data.get("avg_magnitude", 0), 2),
                "max_magnitude": round(seismic_data.get("max_magnitude", 0), 2),
                "anomalies_detected": seismic_data.get("anomalies", 0)
            },
            
            "seismic_summary": {
                "total_events_24h": seismic_data.get("event_count", 0),
                "magnitude_distribution": seismic_data.get("magnitude_distribution", {}),
                "depth_stats": {
                    "avg": round(seismic_data.get("avg_depth", 0), 1),
                    "min": round(seismic_data.get("min_depth", 0), 1),
                    "max": round(seismic_data.get("max_depth", 0), 1)
                },
                "event_intensity": self._classify_event_intensity(
                    seismic_data.get("avg_magnitude", 0)
                )
            },
            
            "key_metrics": metrics,
            
            "predictions": {
                "forecast_7days": predictions.get("forecast", []),
                "confidence_level": predictions.get("confidence", 0),
                "probability_increase": predictions.get("probability_increase", False)
            },
            
            "alerts_generated": {
                "total_alerts": len(alerts),
                "critical_count": sum(1 for a in alerts if a.get("severity") == "CRITICAL"),
                "severe_count": sum(1 for a in alerts if a.get("severity") == "SEVERE"),
                "recent_alerts": alerts[-5:] if alerts else []
            },
            
            "social_media_analysis": {
                "total_mentions": social_sentiment.get("total_posts", 0),
                "sentiment_score": social_sentiment.get("avg_sentiment", 0),
                "trending": social_sentiment.get("trending_volcanoes", []),
                "engagement": social_sentiment.get("high_engagement_total", 0)
            },
            
            "recommendations": self._generate_recommendations(
                seismic_data, alerts, social_sentiment
            ),
            
            "next_report": (datetime.now() + timedelta(days=1)).isoformat()
        }
        
        self.generated_reports.append(content)
        logger.info(f"Reporte diario generado: {volcano_id}")
        return content
    
    def generate_weekly_report(
        self,
        volcano_id: str,
        weekly_data: Dict,
        trends: Dict,
        comparative_analysis: Dict
    ) -> Dict:
        """Genera reporte semanal"""
        report_date = datetime.now()
        week_start = report_date - timedelta(days=7)
        
        content = {
            "title": f"Reporte Semanal - {volcano_id.upper()}",
            "date": report_date.isoformat(),
            "period": f"{week_start.isoformat()} a {report_date.isoformat()}",
            "volcano_id": volcano_id,
            
            "summary": {
                "total_events": weekly_data.get("total_events", 0),
                "avg_daily_events": round(
                    weekly_data.get("total_events", 0) / 7, 1
                ),
                "strongest_event": weekly_data.get("max_magnitude", 0),
                "anomalies": weekly_data.get("anomalies", 0)
            },
            
            "trends": {
                "activity_trend": trends.get("trend_direction", "stable"),
                "magnitude_trend": trends.get("magnitude_trend", []),
                "frequency_change": trends.get("frequency_change_percent", 0)
            },
            
            "comparative_analysis": comparative_analysis,
            
            "risk_assessment": {
                "current_risk_level": weekly_data.get("risk_level", "MEDIUM"),
                "risk_change": trends.get("risk_change", "stable"),
                "probability_next_strong_event": trends.get("strong_event_probability", 0)
            },
            
            "recommendations": self._generate_weekly_recommendations(trends),
            
            "next_report": (datetime.now() + timedelta(days=7)).isoformat()
        }
        
        self.generated_reports.append(content)
        logger.info(f"Reporte semanal generado: {volcano_id}")
        return content
    
    def _classify_event_intensity(self, avg_magnitude: float) -> str:
        """Clasifica intensidad de eventos"""
        if avg_magnitude < 3.0:
            return "BAJA (Eventos microsmicos)"
        elif avg_magnitude < 4.0:
            return "MODERADA (Eventos detectables)"
        elif avg_magnitude < 5.0:
            return "ALTA (Eventos de riesgo moderado)"
        elif avg_magnitude < 6.0:
            return "MUY ALTA (Eventos significativos)"
        else:
            return "CRÍTICA (Eventos peligrosos)"
    
    def _generate_recommendations(
        self,
        seismic_data: Dict,
        alerts: List[Dict],
        social_sentiment: Dict
    ) -> List[str]:
        """Genera recomendaciones basadas en datos"""
        recommendations = []
        
        # Basado en actividad sísmica
        event_count = seismic_data.get("event_count", 0)
        if event_count > 50:
            recommendations.append(
                "⚠️ Alta actividad sísmica detectada. Aumentar monitoreo."
            )
        
        if seismic_data.get("anomalies", 0) > 10:
            recommendations.append(
                "🔴 Múltiples anomalías detectadas. Revisar datos en detalle."
            )
        
        # Basado en alertas
        critical_alerts = sum(1 for a in alerts if a.get("severity") == "CRITICAL")
        if critical_alerts > 0:
            recommendations.append(
                f"🚨 {critical_alerts} alerta(s) crítica(s). Acción inmediata recomendada."
            )
        
        # Basado en redes sociales
        if social_sentiment.get("avg_sentiment", 0) < -0.3:
            recommendations.append(
                "📱 Sentimiento negativo en redes. Considerar comunicado público."
            )
        
        # Por defecto
        if not recommendations:
            recommendations.append("✓ Situación estable. Continuar monitoreo normal.")
        
        return recommendations
    
    def _generate_weekly_recommendations(self, trends: Dict) -> List[str]:
        """Genera recomendaciones para reporte semanal"""
        recommendations = []
        
        trend_direction = trends.get("trend_direction", "stable")
        if trend_direction == "increasing":
            recommendations.append(
                "↗️ Tendencia creciente en actividad. Preparar protocolos."
            )
        elif trend_direction == "decreasing":
            recommendations.append(
                "↘️ Actividad en disminución. Mantener vigilancia."
            )
        
        if not recommendations:
            recommendations.append("Continuar monitoreo estándar.")
        
        return recommendations
    
    def export_to_json(self, report: Dict) -> str:
        """Exporta reporte a JSON"""
        return json.dumps(report, indent=2, ensure_ascii=False, default=str)
    
    def export_to_html(self, report: Dict) -> str:
        """
        Exporta reporte a HTML
        En producción, usar jinja2 para templates
        """
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{report['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .header {{ background-color: #d32f2f; color: white; padding: 20px; border-radius: 5px; }}
                .section {{ background-color: white; margin: 20px 0; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                .metric {{ display: inline-block; margin: 10px 20px 10px 0; padding: 15px; background-color: #eee; border-radius: 5px; }}
                .alert {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 10px 0; }}
                .alert.critical {{ background-color: #f8d7da; border-left-color: #dc3545; }}
                .recommendation {{ background-color: #d1ecf1; border-left: 4px solid #17a2b8; padding: 15px; margin: 10px 0; }}
                h2 {{ color: #d32f2f; border-bottom: 2px solid #d32f2f; padding-bottom: 10px; }}
                h3 {{ color: #555; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{report['title']}</h1>
                <p><strong>Fecha:</strong> {report['date']}</p>
                <p><strong>Volcán:</strong> {report['volcano_id'].upper()}</p>
            </div>
            
            <div class="section">
                <h2>Resumen Ejecutivo</h2>
                <div class="metric">
                    <strong>Eventos:</strong> {report['executive_summary']['total_events']}
                </div>
                <div class="metric">
                    <strong>Magnitud Promedio:</strong> {report['executive_summary']['avg_magnitude']}
                </div>
                <div class="metric">
                    <strong>Magnitud Máxima:</strong> {report['executive_summary']['max_magnitude']}
                </div>
                <div class="metric">
                    <strong>Anomalías:</strong> {report['executive_summary']['anomalies_detected']}
                </div>
            </div>
            
            <div class="section">
                <h2>Alertas</h2>
                <p><strong>Total de alertas:</strong> {report['alerts_generated']['total_alerts']}</p>
                <p><strong>Críticas:</strong> {report['alerts_generated']['critical_count']}</p>
                <p><strong>Severas:</strong> {report['alerts_generated']['severe_count']}</p>
            </div>
            
            <div class="section">
                <h2>Recomendaciones</h2>
                {''.join(f'<div class="recommendation">{rec}</div>' for rec in report['recommendations'])}
            </div>
            
            <div class="section" style="text-align: center; color: #999; font-size: 12px;">
                <p>Reporte generado automáticamente</p>
                <p>Próximo reporte: {report['next_report']}</p>
            </div>
        </body>
        </html>
        """
        return html
    
    def schedule_report(
        self,
        report_id: str,
        config: ReportConfig
    ) -> bool:
        """Programa un reporte automático"""
        self.scheduled_reports[report_id] = config
        logger.info(f"Reporte programado: {report_id} ({config.report_type})")
        return True
    
    def get_scheduled_reports(self) -> Dict[str, ReportConfig]:
        """Retorna reportes programados"""
        return self.scheduled_reports
    
    def get_generated_reports(self, limit: int = 10) -> List[Dict]:
        """Retorna reportes generados"""
        return self.generated_reports[-limit:]


# Instancia global
report_generator = ReportGenerator()
