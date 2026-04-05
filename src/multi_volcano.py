"""
Sistema Multi-Volcán - Soporte para monitorear múltiples volcanes
Permite gestionar y predecir patrones sísmicos en diferentes ubicaciones
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from dataclasses import dataclass, asdict
import json
import logging


logger = logging.getLogger(__name__)


@dataclass
class VolcanoProfile:
    """Perfil de un volcán monitoreado"""
    volcano_id: str
    name: str
    latitude: float
    longitude: float
    elevation_m: float
    country: str
    region: str
    volcano_type: str  # Stratovolcano, Shield, Caldera, etc.
    last_eruption: Optional[str] = None
    monitoring_since: str = None
    active: bool = True
    risk_level: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    
    def __post_init__(self):
        if self.monitoring_since is None:
            self.monitoring_since = datetime.now().isoformat()


class MultiVolcanoManager:
    """Gestor centralizado de múltiples volcanes"""
    
    # Volcanes predefinidos
    KNOWN_VOLCANOES = {
        "deception": VolcanoProfile(
            volcano_id="deception",
            name="Deception Island",
            latitude=-62.9723,
            longitude=-60.6477,
            elevation_m=602,
            country="Antarctica",
            region="South Shetland Islands",
            volcano_type="Caldera",
            last_eruption="1970",
            risk_level="MEDIUM"
        ),
        "cotopaxi": VolcanoProfile(
            volcano_id="cotopaxi",
            name="Cotopaxi",
            latitude=-0.8628,
            longitude=-78.4409,
            elevation_m=5897,
            country="Ecuador",
            region="Central Cordillera",
            volcano_type="Stratovolcano",
            last_eruption="2015",
            risk_level="HIGH"
        ),
        "villarrica": VolcanoProfile(
            volcano_id="villarrica",
            name="Villarrica",
            latitude=-39.4206,
            longitude=-71.9305,
            elevation_m=2847,
            country="Chile",
            region="Los Ríos Region",
            volcano_type="Stratovolcano",
            last_eruption="2015",
            risk_level="HIGH"
        ),
        "vesuvio": VolcanoProfile(
            volcano_id="vesuvio",
            name="Mount Vesuvius",
            latitude=40.8212,
            longitude=14.4269,
            elevation_m=1281,
            country="Italy",
            region="Campania",
            volcano_type="Stratovolcano",
            last_eruption="1944",
            risk_level="CRITICAL"
        ),
        "sakurajima": VolcanoProfile(
            volcano_id="sakurajima",
            name="Sakurajima",
            latitude=31.5929,
            longitude=130.6571,
            elevation_m=1117,
            country="Japan",
            region="Kyushu",
            volcano_type="Stratovolcano",
            last_eruption="Active",
            risk_level="HIGH"
        ),
        "etna": VolcanoProfile(
            volcano_id="etna",
            name="Mount Etna",
            latitude=37.7510,
            longitude=15.0087,
            elevation_m=3350,
            country="Italy",
            region="Sicily",
            volcano_type="Stratovolcano",
            last_eruption="Active",
            risk_level="MEDIUM"
        ),
    }
    
    def __init__(self):
        """Inicializa el gestor multi-volcán"""
        self.volcanoes: Dict[str, VolcanoProfile] = self.KNOWN_VOLCANOES.copy()
        self.seismic_data: Dict[str, List[Dict]] = {}
        self.models: Dict[str, object] = {}  # Un modelo por volcán
        self.alert_thresholds: Dict[str, Dict] = {}
        
        # Inicializar thresholds por defecto
        for v_id in self.volcanoes:
            self.alert_thresholds[v_id] = {
                "magnitude": 4.5,
                "anomaly_score": 0.7,
                "daily_count": 50
            }
    
    def add_volcano(self, profile: VolcanoProfile) -> bool:
        """Agrega un nuevo volcán al sistema"""
        if profile.volcano_id in self.volcanoes:
            logger.warning(f"Volcán {profile.volcano_id} ya existe")
            return False
        
        self.volcanoes[profile.volcano_id] = profile
        self.seismic_data[profile.volcano_id] = []
        self.alert_thresholds[profile.volcano_id] = {
            "magnitude": 4.5,
            "anomaly_score": 0.7,
            "daily_count": 50
        }
        logger.info(f"Volcán agregado: {profile.name}")
        return True
    
    def get_volcano_info(self, volcano_id: str) -> Optional[Dict]:
        """Obtiene información del volcán"""
        if volcano_id not in self.volcanoes:
            return None
        
        profile = self.volcanoes[volcano_id]
        return asdict(profile)
    
    def get_all_volcanoes(self) -> List[Dict]:
        """Retorna lista de todos los volcanes"""
        return [asdict(v) for v in self.volcanoes.values()]
    
    def set_volcano_threshold(
        self,
        volcano_id: str,
        threshold_type: str,
        value: float
    ) -> bool:
        """Configura threshold de alerta para volcán"""
        if volcano_id not in self.alert_thresholds:
            return False
        
        if threshold_type in self.alert_thresholds[volcano_id]:
            self.alert_thresholds[volcano_id][threshold_type] = value
            logger.info(f"Threshold actualizado: {volcano_id} {threshold_type}={value}")
            return True
        return False
    
    def get_volcano_thresholds(self, volcano_id: str) -> Optional[Dict]:
        """Obtiene thresholds de alerta"""
        return self.alert_thresholds.get(volcano_id)
    
    def add_seismic_data(
        self,
        volcano_id: str,
        magnitude: float,
        depth: float,
        latitude: float,
        longitude: float,
        location: str
    ) -> bool:
        """Agrega dato sísmico a un volcán"""
        if volcano_id not in self.seismic_data:
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
        return True
    
    def get_volcano_seismic_data(
        self,
        volcano_id: str,
        days: int = 30
    ) -> Optional[pd.DataFrame]:
        """Obtiene datos sísmicos recientes de un volcán"""
        if volcano_id not in self.seismic_data:
            return None
        
        if not self.seismic_data[volcano_id]:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.seismic_data[volcano_id])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
        return df[df['timestamp'] >= cutoff]
    
    def get_comparative_statistics(
        self,
        volcano_ids: Optional[List[str]] = None
    ) -> Dict:
        """Compara estadísticas entre múltiples volcanes"""
        if volcano_ids is None:
            volcano_ids = list(self.volcanoes.keys())
        
        stats = {}
        for v_id in volcano_ids:
            if v_id not in self.seismic_data:
                continue
            
            data = self.seismic_data[v_id]
            if not data:
                stats[v_id] = {
                    "total_events": 0,
                    "avg_magnitude": 0,
                    "max_magnitude": 0,
                    "avg_depth": 0
                }
            else:
                magnitudes = [d['magnitude'] for d in data]
                depths = [d['depth'] for d in data]
                
                stats[v_id] = {
                    "total_events": len(data),
                    "avg_magnitude": np.mean(magnitudes),
                    "max_magnitude": np.max(magnitudes),
                    "min_magnitude": np.min(magnitudes),
                    "avg_depth": np.mean(depths),
                    "max_depth": np.max(depths),
                    "last_event": max([d['timestamp'] for d in data])
                }
        
        return stats
    
    def find_volcanoes_by_criteria(
        self,
        country: Optional[str] = None,
        risk_level: Optional[str] = None,
        volcano_type: Optional[str] = None
    ) -> List[Dict]:
        """Busca volcanes por criterios"""
        results = []
        
        for volcano in self.volcanoes.values():
            match = True
            
            if country and volcano.country != country:
                match = False
            if risk_level and volcano.risk_level != risk_level:
                match = False
            if volcano_type and volcano.volcano_type != volcano_type:
                match = False
            
            if match:
                results.append(asdict(volcano))
        
        return results
    
    def get_high_risk_volcanoes(self) -> List[Dict]:
        """Retorna volcanes de alto riesgo"""
        return self.find_volcanoes_by_criteria(risk_level="HIGH") + \
               self.find_volcanoes_by_criteria(risk_level="CRITICAL")
    
    def calculate_global_activity_index(self) -> float:
        """Calcula índice global de actividad sísmica"""
        total_magnitude = 0
        total_events = 0
        
        for data in self.seismic_data.values():
            for event in data:
                total_magnitude += event['magnitude']
                total_events += 1
        
        if total_events == 0:
            return 0.0
        
        return total_magnitude / total_events
    
    def export_volcano_data(self, volcano_id: str, format: str = "csv") -> Optional[str]:
        """Exporta datos de volcán"""
        if volcano_id not in self.seismic_data:
            return None
        
        data = self.seismic_data[volcano_id]
        if not data:
            return None
        
        df = pd.DataFrame(data)
        
        if format == "csv":
            return df.to_csv(index=False)
        elif format == "json":
            return df.to_json(orient="records", date_format="iso")
        
        return None
    
    def get_volcano_comparison_report(self) -> Dict:
        """Genera reporte comparativo completo"""
        stats = self.get_comparative_statistics()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_volcanoes": len(self.volcanoes),
            "high_risk_count": len(self.get_high_risk_volcanoes()),
            "global_activity_index": self.calculate_global_activity_index(),
            "volcano_statistics": stats,
            "top_5_most_active": sorted(
                stats.items(),
                key=lambda x: x[1].get('total_events', 0),
                reverse=True
            )[:5]
        }
        
        return report


# Instancia global
volcano_manager = MultiVolcanoManager()
