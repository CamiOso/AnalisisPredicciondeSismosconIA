"""
Integración con datos sísmicos reales del USGS
"""
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class USGSEarthquakeAPI:
    """Cliente para descargar datos sísmicos del USGS"""
    
    BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    
    # Coordenadas del Volcán Deception (Antártida)
    DECEPTION_VOLCANO = {
        'latitude': -62.9723,
        'longitude': -60.6477,
        'min_latitude': -63.5,
        'max_latitude': -62,
        'min_longitude': -61,
        'max_longitude': -60
    }
    
    def __init__(self, search_radius_km: int = 100, min_magnitude: float = 1.0):
        self.search_radius = search_radius_km
        self.min_magnitude = min_magnitude
        self.timeout = 30
    
    def get_earthquakes(self, 
                       days_back: int = 365,
                       min_magnitude: Optional[float] = None,
                       region: Optional[Dict] = None) -> pd.DataFrame:
        """
        Descarga eventos sísmicos del USGS
        
        Args:
            days_back: Número de días hacia atrás
            min_magnitude: Magnitud mínima (sobreescribe default)
            region: Dict con minlatitude, maxlatitude, minlongitude, maxlongitude
        
        Returns:
            DataFrame con eventos sísmicos
        """
        
        if min_magnitude is None:
            min_magnitude = self.min_magnitude
        
        if region is None:
            region = self.DECEPTION_VOLCANO
        
        # Calcular fechas
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days_back)
        
        # Parámetros de consulta
        params = {
            'format': 'geojson',
            'starttime': start_time.strftime('%Y-%m-%d'),
            'endtime': end_time.strftime('%Y-%m-%d'),
            'minmagnitude': min_magnitude,
            'minlatitude': region['min_latitude'],
            'maxlatitude': region['max_latitude'],
            'minlongitude': region['min_longitude'],
            'maxlongitude': region['max_longitude'],
            'limit': 20000,  # Máximo permitido por USGS
            'orderby': 'time'
        }
        
        try:
            logger.info(f"🌍 Descargando eventos USGS para los últimos {days_back} días...")
            
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data['metadata']['count'] == 0:
                logger.warning("⚠️  No se encontraron eventos")
                return pd.DataFrame()
            
            # Procesar eventos
            events = []
            for feature in data['features']:
                props = feature['properties']
                coords = feature['geometry']['coordinates']
                
                events.append({
                    'time': pd.to_datetime(props['time'], unit='ms'),
                    'magnitude': props.get('mag'),
                    'depth': coords[2],  # Profundidad en km
                    'latitude': coords[1],
                    'longitude': coords[0],
                    'location': props.get('place', 'Unknown'),
                    'usgs_id': props.get('id'),
                    'type': props.get('type'),
                    'felt_reports': props.get('felt'),
                    'tsunami': props.get('tsunami', 0)
                })
            
            df = pd.DataFrame(events)
            df = df.sort_values('time')
            
            logger.info(f"✅ {len(df)} eventos descargados")
            logger.info(f"   Período: {df['time'].min().date()} a {df['time'].max().date()}")
            logger.info(f"   Magnitud: {df['magnitude'].min():.1f} - {df['magnitude'].max():.1f}")
            logger.info(f"   Profundidad: {df['depth'].min():.0f} - {df['depth'].max():.0f} km")
            
            return df
        
        except requests.exceptions.Timeout:
            logger.error("❌ Timeout descargando datos USGS")
            return pd.DataFrame()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error descargando datos: {str(e)}")
            return pd.DataFrame()
    
    def get_recent_earthquakes(self, 
                              hours_back: int = 24,
                              region: Optional[Dict] = None) -> pd.DataFrame:
        """Obtiene eventos de las últimas N horas"""
        
        if region is None:
            region = self.DECEPTION_VOLCANO
        
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours_back)
        
        params = {
            'format': 'geojson',
            'starttime': start_time.isoformat() + 'Z',
            'endtime': end_time.isoformat() + 'Z',
            'minlatitude': region['min_latitude'],
            'maxlatitude': region['max_latitude'],
            'minlongitude': region['min_longitude'],
            'maxlongitude': region['max_longitude'],
            'orderby': 'time-asc'
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if data['metadata']['count'] == 0:
                return pd.DataFrame()
            
            events = []
            for feature in data['features']:
                props = feature['properties']
                coords = feature['geometry']['coordinates']
                
                events.append({
                    'time': pd.to_datetime(props['time'], unit='ms'),
                    'magnitude': props.get('mag'),
                    'depth': coords[2],
                    'latitude': coords[1],
                    'longitude': coords[0],
                    'location': props.get('place'),
                    'usgs_id': props.get('id')
                })
            
            return pd.DataFrame(events)
        
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return pd.DataFrame()
    
    def save_to_csv(self, df: pd.DataFrame, filepath: str) -> bool:
        """Guarda datos a CSV"""
        try:
            df.to_csv(filepath, index=False)
            logger.info(f"✅ Datos guardados en {filepath}")
            return True
        except Exception as e:
            logger.error(f"❌ Error guardando datos: {str(e)}")
            return False
    
    def get_statistics(self, df: pd.DataFrame) -> Dict:
        """Calcula estadísticas de los eventos"""
        
        if df.empty:
            return {}
        
        return {
            'total_events': len(df),
            'date_range': f"{df['time'].min().date()} to {df['time'].max().date()}",
            'magnitude_stats': {
                'mean': df['magnitude'].mean(),
                'median': df['magnitude'].median(),
                'std': df['magnitude'].std(),
                'min': df['magnitude'].min(),
                'max': df['magnitude'].max()
            },
            'depth_stats': {
                'mean': df['depth'].mean(),
                'median': df['depth'].median(),
                'min': df['depth'].min(),
                'max': df['depth'].max()
            },
            'daily_average': len(df) / ((df['time'].max() - df['time'].min()).days + 1),
            'magnitude_distribution': df['magnitude'].value_counts().sort_index().to_dict()
        }


# Script de descarga rápida
if __name__ == '__main__':
    import sys
    
    print("\n🌍 USGS Earthquake Data Downloader")
    print("="*50)
    
    # Descargar datos
    usgs = USGSEarthquakeAPI(min_magnitude=1.0)
    
    # Últimos 365 días
    df = usgs.get_earthquakes(days_back=365)
    
    if not df.empty:
        # Guardar
        usgs.save_to_csv(df, 'data/usgs_deception_1y.csv')
        
        # Estadísticas
        stats = usgs.get_statistics(df)
        print("\n📊 Estadísticas:")
        print(f"Total eventos: {stats['total_events']}")
        print(f"Período: {stats['date_range']}")
        print(f"\nMagnitud:")
        print(f"  Media: {stats['magnitude_stats']['mean']:.2f}")
        print(f"  Rango: {stats['magnitude_stats']['min']:.1f} - {stats['magnitude_stats']['max']:.1f}")
        print(f"\nProfundidad:")
        print(f"  Media: {stats['depth_stats']['mean']:.1f} km")
        print(f"  Rango: {stats['depth_stats']['min']:.0f} - {stats['depth_stats']['max']:.0f} km")
