"""
Data loader y preprocesamiento de datos sísmicos
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class SeismicDataLoader:
    """Cargador y procesador de datos sísmicos"""
    
    def __init__(self):
        self.scaler = None
        self.data = None
        
    def load_csv(self, filepath: str) -> pd.DataFrame:
        """Carga datos desde CSV"""
        print(f"📂 Cargando datos de {filepath}")
        self.data = pd.read_csv(filepath)
        self._validate_columns()
        return self.data
    
    def _validate_columns(self):
        """Valida que existan columnas necesarias"""
        required_cols = ['magnitude', 'depth', 'latitude', 'longitude', 'time']
        missing = [col for col in required_cols if col not in self.data.columns]
        if missing:
            print(f"⚠️  Columnas faltantes: {missing}")
            print(f"Columnas disponibles: {list(self.data.columns)}")
    
    def filter_by_location(self, lat: float, lon: float, radius_km: float) -> pd.DataFrame:
        """Filtra datos por ubicación geográfica"""
        if 'latitude' not in self.data.columns or 'longitude' not in self.data.columns:
            print("No se pueden filtrar sin columnas de coordenadas")
            return self.data
        
        # Cálculo simple de distancia (Haversine simplificada)
        def haversine(lat1, lon1):
            # Aproximación (grados a km: 111 km/grado)
            dist = np.sqrt((lat1 - lat)**2 + (lon1 - lon)**2) * 111
            return dist < radius_km
        
        self.data['in_radius'] = self.data.apply(
            lambda row: haversine(row['latitude'], row['longitude']), 
            axis=1
        )
        self.data = self.data[self.data['in_radius']].drop('in_radius', axis=1)
        print(f"✓ Filtrados a {len(self.data)} eventos en el radio")
        return self.data
    
    def filter_by_magnitude(self, min_magnitude: float) -> pd.DataFrame:
        """Filtra por magnitud mínima"""
        if 'magnitude' in self.data.columns:
            self.data = self.data[self.data['magnitude'] >= min_magnitude]
            print(f"✓ Filtrados a {len(self.data)} eventos con magnitud >= {min_magnitude}")
        return self.data
    
    def normalize_features(self, features: list, method: str = 'minmax'):
        """Normaliza características numéricas"""
        if method == 'minmax':
            self.scaler = MinMaxScaler()
        elif method == 'standard':
            self.scaler = StandardScaler()
        else:
            raise ValueError("Método debe ser 'minmax' o 'standard'")
        
        self.data[features] = self.scaler.fit_transform(self.data[features])
        print(f"✓ Normalizados con método: {method}")
        return self.data
    
    def create_sequences(self, data: np.ndarray, seq_length: int = 30):
        """Crea secuencias para LSTM"""
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)
    
    def prepare_for_lstm(self, feature_cols: list, seq_length: int = 30, 
                         split_ratio: float = 0.8):
        """Prepara datos para modelo LSTM"""
        print(f"\n🔧 Preparando datos para LSTM...")
        
        # Seleccionar características
        X = self.data[feature_cols].values
        
        # Crear secuencias
        X_seq, y_seq = self.create_sequences(X, seq_length)
        print(f"✓ Secuencias creadas: {X_seq.shape}")
        
        # Split train/test
        split_idx = int(len(X_seq) * split_ratio)
        X_train = X_seq[:split_idx]
        X_test = X_seq[split_idx:]
        y_train = y_seq[:split_idx]
        y_test = y_seq[split_idx:]
        
        print(f"✓ Train: {X_train.shape}, Test: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test
    
    def generate_sample_data(self, n_days: int = 365) -> pd.DataFrame:
        """Genera datos sísmicos sintéticos para pruebas"""
        print(f"🔄 Generando {n_days} días de datos sísmicos sintéticos...")
        
        dates = [datetime.now() - timedelta(days=x) for x in range(n_days)]
        
        data = {
            'time': dates,
            'magnitude': np.random.normal(4.5, 1.2, n_days),
            'depth': np.random.uniform(5, 50, n_days),
            'latitude': np.random.uniform(-63, -62.5, n_days),
            'longitude': np.random.uniform(-61, -60, n_days),
            'latitude_error': np.random.uniform(0, 5, n_days),
            'longitude_error': np.random.uniform(0, 5, n_days),
            'depth_error': np.random.uniform(0, 5, n_days),
        }
        
        self.data = pd.DataFrame(data)
        self.data['magnitude'] = np.clip(self.data['magnitude'], 0, 10)
        return self.data


def load_example_data():
    """Función helper para cargar datos de ejemplo"""
    loader = SeismicDataLoader()
    loader.generate_sample_data(365)
    return loader
