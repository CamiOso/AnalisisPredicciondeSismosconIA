"""
Configuración global del sistema sísmico
"""
import os

# Directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")

# Parámetros de datos
SEQUENCE_LENGTH = 30  # Días para predecir LSTM
TRAIN_TEST_SPLIT = 0.8
BATCH_SIZE = 32
EPOCHS = 100

# Parámetros del modelo
LSTM_UNITS = 64
DROPOUT_RATE = 0.2
LEARNING_RATE = 0.001

# API USGS
USGS_BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Ubicaciones de interés (lat, lon, radio en km)
LOCATIONS = {
    "deception_island": {"lat": -62.9723, "lon": -60.6477, "radius": 100},
    "ring_of_fire": {"lat": 0, "lon": 165, "radius": 5000},
}

# Umbral de magnitud mínima
MIN_MAGNITUDE = 2.5

# Normalización
NORMALIZE = True
SCALE_METHOD = "minmax"  # "minmax" o "standard"
