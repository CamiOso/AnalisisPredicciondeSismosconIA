# 🎓 Guía Avanzada

Este documento cubre temas avanzados y casos de uso específicos.

## Tabla de Contenidos

- [Configuración Avanzada](#configuración-avanzada)
- [Integración con Datos Reales](#integración-con-datos-reales)
- [Despliegue en Producción](#despliegue-en-producción)
- [Pipeline Personalizado](#pipeline-personalizado)
- [Optimización de Modelos](#optimización-de-modelos)
- [Troubleshooting](#troubleshooting)

---

## Configuración Avanzada

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Email Alerts
EMAIL_SENDER=tu_email@gmail.com
EMAIL_PASSWORD=tu_contraseña_app

# Database
DATABASE_URL=sqlite:///data/seismic.db
# O para PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/seismic_db

# API
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=False

# Streamlit
STREAMLIT_SERVER_HEADLESS=False
STREAMLIT_LOGGER_LEVEL=warning

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/seismic.log
```

### Configuración de Parámetros

Edita `config.py` para ajustar:

```python
# Model parameters
SEQUENCE_LENGTH = 30              # Ventana temporal para LSTM
LSTM_UNITS = 128                 # Aumentar para modelos más complejos
LSTM_LAYERS = 3                  # Número de capas LSTM
DROPOUT_RATE = 0.3
BATCH_SIZE = 16                  # Reducir si tienes problemas de memoria
LEARNING_RATE = 0.0005          # Ajustar según convergencia
EPOCHS = 200                     # Más épocas para mejor convergencia

# Anomaly Detection
ANOMALY_CONTAMINATION = 0.05    # Porcentaje de anomalías esperadas
ANOMALY_N_ESTIMATORS = 150

# Data
MIN_MAGNITUDE = 1.5              # Umbral mínimo de detección
MAX_DEPTH = 800                  # Profundidad máxima

# Paths
DATA_DIR = 'data/'
MODELS_DIR = 'models/'
LOGS_DIR = 'logs/'
```

---

## Integración con Datos Reales

### USGS Earthquake API

```python
import requests
from src.data_loader import SeismicDataLoader
import json

loader = SeismicDataLoader()

# Parámetros para Volcán Deception
params = {
    'format': 'geojson',
    'starttime': '2024-01-01',
    'endtime': '2024-12-31',
    'minlatitude': -63.5,
    'maxlatitude': -62,
    'minlongitude': -61,
    'maxlongitude': -60,
    'minmagnitude': 1.0
}

# Descargar datos
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
response = requests.get(url, params=params)
data = response.json()

# Procesar
events = []
for feature in data['features']:
    props = feature['properties']
    geometry = feature['geometry']
    
    events.append({
        'time': props['time'],
        'magnitude': props['mag'],
        'depth': geometry['coordinates'][2],
        'latitude': geometry['coordinates'][1],
        'longitude': geometry['coordinates'][0]
    })

# Convertir a DataFrame
import pandas as pd
df = pd.DataFrame(events)
df.to_csv('data/usgs_deception.csv', index=False)

print(f"✓ {len(events)} eventos descargados")
```

### Base de Datos PostgreSQL

```python
from sqlalchemy import create_engine
import pandas as pd

# Conexión
engine = create_engine('postgresql://user:password@localhost/seismic_db')

# Guardar datos
data.to_sql('events', engine, if_exists='append', index=False)

# Leer datos
df = pd.read_sql('SELECT * FROM events', engine)
```

---

## Despliegue en Producción

### Docker en AWS EC2

```bash
# 1. SSH a instancia
ssh -i key.pem ubuntu@your-instance-ip

# 2. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
bash get-docker.sh

# 3. Clonar repo
git clone https://github.com/CamiOso/AnalisisPredicciondeSismosconIA.git
cd AnalisisPredicciondeSismosconIA

# 4. Iniciar con Docker Compose
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 5. Ver logs
docker-compose logs -f api
docker-compose logs -f dashboard
```

### Heroku Deployment

```bash
# 1. Instalar Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 2. Login
heroku login

# 3. Crear app
heroku create seismic-analysis

# 4. Agregar Procfile
cat > Procfile << EOF
web: gunicorn src.api:app
dashboard: streamlit run src/dashboard.py
EOF

# 5. Push
git push heroku main

# 6. Abrir
heroku open
```

### Nginx como Reverse Proxy

```nginx
server {
    listen 80;
    server_name seismic.example.com;
    
    # API FastAPI
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # Streamlit Dashboard
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## Pipeline Personalizado

### Crear un Pipeline Personalizado

```python
from src.data_loader import SeismicDataLoader
from src.model import SeismicLSTM, SeismicAnomalyDetector
from src.statistics import SeismicStatistics
from src.database import SeismicDatabase
import pandas as pd
from sklearn.preprocessing import StandardScaler

class CustomSeismicPipeline:
    """Pipeline personalizado para casos específicos"""
    
    def __init__(self):
        self.loader = SeismicDataLoader()
        self.lstm = SeismicLSTM()
        self.detector = SeismicAnomalyDetector()
        self.db = SeismicDatabase()
    
    def run_deep_analysis(self, data: pd.DataFrame, days_window: int = 30):
        """Análisis profundo con ventana deslizante"""
        
        results = []
        
        # Dividir en ventanas
        data_sorted = data.sort_values('time')
        for i in range(0, len(data_sorted), days_window):
            window = data_sorted.iloc[i:i+days_window]
            
            if len(window) < days_window:
                break
            
            # Análisis de ventana
            stats = SeismicStatistics(window)
            dist = stats.calculate_magnitude_distribution()
            
            results.append({
                'window_start': window.iloc[0]['time'],
                'window_end': window.iloc[-1]['time'],
                'mean_magnitude': dist['mean'],
                'std_magnitude': dist['std'],
                'events': len(window)
            })
        
        return pd.DataFrame(results)
    
    def run_multi_model_ensemble(self, X_test, y_test):
        """Ensemble de múltiples modelos"""
        
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        
        models = {
            'LSTM': self.lstm,
            'RandomForest': RandomForestRegressor(n_estimators=100),
            'GradientBoosting': GradientBoostingRegressor(n_estimators=100)
        }
        
        predictions = {}
        for name, model in models.items():
            pred = model.predict(X_test)
            predictions[name] = pred
        
        # Promedio de predicciones
        ensemble_pred = sum(predictions.values()) / len(predictions)
        
        return predictions, ensemble_pred

# Uso
pipeline = CustomSeismicPipeline()
data = pipeline.loader.generate_sample_data(days=365)

# Ejecutar análisis profundo
analysis = pipeline.run_deep_analysis(data)
print(analysis.head())
```

---

## Optimización de Modelos

### Búsqueda de Hiperparámetros

```python
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasRegressor
from src.model import SeismicLSTM

def create_model(units=64, dropout=0.2):
    lstm = SeismicLSTM()
    model = lstm.create_model((30, 1), units=units, dropout=dropout)
    return model

# Grid Search
param_grid = {
    'units': [32, 64, 128],
    'dropout': [0.1, 0.2, 0.3],
    'epochs': [50, 100],
    'batch_size': [16, 32]
}

model = KerasRegressor(build_fn=create_model, verbose=0)
grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=3)

# Buscar mejores parámetros
grid.fit(X_train, y_train)

print(f"Mejores parámetros: {grid.best_params_}")
print(f"Mejor score: {grid.best_score_}")
```

### Fine-tuning del Modelo

```python
from tensorflow import keras

# Cargar modelo entrenado
model = keras.models.load_model('models/lstm_seismic.h5')

# Congelar capas iniciales
for layer in model.layers[:-2]:
    layer.trainable = False

# Entrenar solo las últimas capas con learning rate bajo
optimizer = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])

# Fine-tune
model.fit(X_new, y_new, epochs=20, batch_size=16)

# Guardar
model.save('models/lstm_seismic_tuned.h5')
```

---

## Monitoreo en Producción

### Logging Avanzado

```python
import logging
from logging.handlers import RotatingFileHandler

# Configurar logger
logger = logging.getLogger('seismic')
logger.setLevel(logging.DEBUG)

# File handler con rotación
file_handler = RotatingFileHandler(
    'logs/seismic.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Usar
logger.info("Sistema iniciado")
logger.warning("Anomalía detectada")
logger.error("Error en predicción", exc_info=True)
```

### Métricas en Tiempo Real

```python
from prometheus_client import Counter, Histogram, start_http_server
import time

# Definir métricas
predictions_counter = Counter(
    'predictions_total',
    'Total de predicciones realizadas',
    ['model_name']
)

prediction_latency = Histogram(
    'prediction_latency_seconds',
    'Latencia de predicción'
)

anomalies_counter = Counter(
    'anomalies_detected',
    'Total de anomalías detectadas'
)

# Usar en código
@prediction_latency.time()
def make_prediction(data):
    result = predictor.predict(data)
    predictions_counter.labels(model_name='LSTM').inc()
    return result

# Iniciar servidor Prometheus
start_http_server(8001)
```

---

## Testing Avanzado

### Test de Integración

```python
import unittest
from src.api import app
from fastapi.testclient import TestClient

class TestAPIIntegration(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_prediction_endpoint(self):
        """Test endpoint de predicción"""
        response = self.client.post(
            "/api/predict",
            json={"magnitude": 5.0, "depth": 30}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('predicted_magnitude', data)
        self.assertIn('risk_level', data)
    
    def test_stats_endpoint(self):
        """Test endpoint de estadísticas"""
        response = self.client.get("/api/stats")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total_events', data)
```

### Benchmarking

```python
import timeit
from src.predict import SeismicPredictor

predictor = SeismicPredictor()

# Tiempo de predicción
time_taken = timeit.timeit(
    lambda: predictor.predict(5.0, 30),
    number=100
)

print(f"Tiempo promedio: {time_taken/100:.4f}s")
print(f"Predicciones por segundo: {100/time_taken:.0f}")
```

---

## Troubleshooting

### Problema: "TensorFlow not found"

```bash
# Solución
pip install --upgrade tensorflow
pip install --upgrade keras
```

### Problema: Memory Error en Entrenamiento

```python
# Reducir batch size
BATCH_SIZE = 8

# Reducir LSTM units
LSTM_UNITS = 32

# Usar mixed precision
from tensorflow.keras.mixed_precision import Policy
policy = Policy('mixed_float16')
tf.keras.mixed_precision.set_global_policy(policy)
```

### Problema: Modelos No Convergen

```python
# Cambiar learning rate
LEARNING_RATE = 0.001  # Aumentar si es muy pequeño

# Usar diferentes optimizadores
optimizer = keras.optimizers.RMSprop(learning_rate=0.001)

# Estandarizar inputs
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
```

### Problema: Docker No Inicia

```bash
# Ver logs
docker-compose logs -f

# Rebuild
docker-compose build --no-cache

# Verificar puertos
netstat -tulpn | grep LISTEN

# Limpiar imágenes
docker system prune -a
```

---

## Recursos Externos

- [TensorFlow Docs](https://tensorflow.org/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [Prophet Docs](https://facebook.github.io/prophet/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [USGS Earthquake Data](https://earthquake.usgs.gov/)

---

**Última actualización:** Abril 2026
