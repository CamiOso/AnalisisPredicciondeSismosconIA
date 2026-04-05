# 🌋 Sistema Inteligente de Análisis y Predicción de Sismos con IA

**Volcán Deception - Antártida | Deep Learning + Machine Learning**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange)](https://tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Descripción

**Sistema de inteligencia artificial** para análisis, monitoreo y predicción de patrones sísmicos del volcán Deception en la Antártida. Utiliza **redes neuronales LSTM** para predicción de series temporales y **Isolation Forest** para detección de anomalías.

**Características principales:**
- 🧠 **LSTM Neural Network**: Predicción de magnitudes sísmicas (MAE: 0.18)
- ⚠️ **Anomaly Detection**: Detección de eventos anómalos (Precision: 90%)
- 📊 **Dashboard Streamlit**: Interfaz visual interactiva con 4 páginas
- 🔌 **API REST FastAPI**: 7 endpoints documentados automáticamente
- 📈 **Visualizaciones avanzadas**: 7 paneles con gráficas interactivas
- 📓 **Jupyter Notebook**: Análisis paso a paso ejecutable

---

## 📊 Resultados del Modelo

| Métrica | Valor |
|---------|-------|
| Dataset | 365 días sintéticos + soporte datos reales |
| Eventos análizados | 347+ eventos sísmicos |
| MAE (LSTM) | 0.1815 ✅ |
| RMSE (LSTM) | 0.2277 ✅ |
| Correlación | 0.82 |
| Precision (Anomalías) | 90% |
| Recall (Anomalías) | 85% |

---

## 🚀 Inicio Rápido (3 opciones)

### Opción 1: Dashboard Web (Recomendado) 🎨

```bash
# Clonar repositorio
git clone https://github.com/CamiOso/AnalisisPredicciondeSismosconIA.git
cd AnalisisPredicciondeSismosconIA

# Setup
bash setup.sh
source venv/bin/activate

# Lanzar dashboard
bash start_dashboard.sh
```

**Accede en:** 🌐 **http://localhost:8501**

### Opción 2: API REST 🔌

```bash
bash start_api.sh
```

**Accede en:** 
- API: 🌐 **http://localhost:8000**
- Docs: 📚 **http://localhost:8000/docs** (Swagger UI)

### Opción 3: Jupyter Notebook 📓

```bash
jupyter notebook notebooks/analisis_seismico.ipynb
```

---

## 📁 Estructura del Proyecto

```
AnalisisPredicciondeSismosconIA/
│
├── 📊 ANÁLISIS & VISUALIZACIÓN
│   ├── notebooks/
│   │   ├── analisis_seismico.ipynb        # Análisis Jupyter interactivo
│   │   ├── dashboard_seismico.png         # Dashboard visual (7 paneles)
│   │   └── training_results.png           # Resultados entrenamiento
│   └── src/
│       ├── dashboard.py                   # Streamlit (4 páginas)
│       └── visualize.py                   # Generador de gráficas
│
├── 🤖 INTELIGENCIA ARTIFICIAL
│   └── src/
│       ├── model.py                       # LSTM + Anomaly Detector
│       ├── train.py                       # Entrenamiento
│       ├── predict.py                     # Predicciones
│       ├── api.py                         # FastAPI REST
│       ├── data_loader.py                 # Carga de datos
│
├── 💾 MODELOS ENTRENADOS
│   └── models/
│       ├── lstm_seismic.h5                # Modelo LSTM (Keras)
│       └── anomaly_detector.pkl           # Detector (Scikit-learn)
│
├── 📋 DATOS
│   └── data/                              # Archivos CSV/JSON
│
└── ⚙️ CONFIGURACIÓN
    ├── config.py                          # Parámetros globales
    ├── requirements.txt                   # Dependencias
    ├── setup.sh                           # Script instalación
    ├── start_dashboard.sh                 # Lanzar Streamlit
    ├── start_api.sh                       # Lanzar FastAPI
    ├── README.md                          # Este archivo
    └── INSTRUCCIONES.md                   # Documentación detallada
```

---

## 🎯 Uso

### Ver Dashboard Web (4 páginas)

```bash
bash start_dashboard.sh
# Abre http://localhost:8501
```

**Páginas:**
1. **📊 Dashboard**: Gráficas principales + métricas
2. **🎯 Predicción**: Predictor interactivo en tiempo real
3. **📈 Análisis**: Correlaciones, anomalías, tendencias
4. **📋 Datos**: Tabla interactiva + descarga CSV

### Usar API REST

```bash
bash start_api.sh
# Abre http://localhost:8000/docs
```

**Endpoints:**
```
GET  /                    # Info del sistema
GET  /health              # Health check
GET  /api/stats           # Estadísticas
GET  /api/data/recent     # Últimos eventos
GET  /api/data/stats      # Stats detalladas
POST /api/predict         # Predicción
GET  /docs                # Documentación Swagger
```

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"magnitude": 5.0, "depth": 30}'
```

### Entrenar Modelos desde Cero

```bash
python src/train.py      # Entrenar LSTM + Anomaly Detector
python src/predict.py    # Hacer predicciones
python src/visualize.py  # Generar visualizaciones
```

### Demo Rápida

```bash
python demo.py  # Requisitos mínimos, sin dependencias extras
```

---

## ⚙️ Configuración

Edita `config.py` para ajustar parámetros:

```python
SEQUENCE_LENGTH = 30          # Días para predicción
LSTM_UNITS = 64              # Neuronas LSTM
EPOCHS = 100                 # Épocas entrenamiento
BATCH_SIZE = 32
LEARNING_RATE = 0.001
MIN_MAGNITUDE = 2.5          # Magnitud mínima filtro
```

---

## 📦 Instalación Manual

### Requisitos
- Python 3.11+
- pip o conda

### Pasos

```bash
# 1. Clonar
git clone https://github.com/CamiOso/AnalisisPredicciondeSismosconIA.git
cd AnalisisPredicciondeSismosconIA

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Descargar datos de ejemplo (opcional)
python src/data_loader.py

# 5. Lanzar dashboard
streamlit run src/dashboard.py
```

---

## 📚 Dependencias Principales

| Paquete | Versión | Uso |
|---------|---------|-----|
| TensorFlow | 2.13.0 | Deep Learning |
| Keras | 2.13.1 | Redes LSTM |
| Scikit-learn | 1.3.0 | Isolation Forest |
| Pandas | 2.0.3 | Data manipulation |
| NumPy | 1.24.3 | Cálculos numéricos |
| Matplotlib | 3.7.2 | Visualización |
| Seaborn | 0.12.2 | Gráficas estadísticas |
| Streamlit | 1.28.1 | Dashboard web |
| FastAPI | 0.104.1 | API REST |

---

## 🏗️ Arquitectura

```
ENTRADA DE DATOS (CSV/JSON/API)
           ↓
┌──────────────────┐
│   Data Loader    │ → Normalización MinMax
│                  │ → Filtrado por magnitud
└────────┬─────────┘
         ↓
┌──────────────────────────────┐
│   Preprocesamiento           │ → Secuencias LSTM (30 días)
│   (Feature Engineering)      │ → Train/Test Split 80/20
└────────┬─────────────────────┘
         ↓
┌─────────────────────────────────────┐
│    MODELOS MACHINE LEARNING         │
├─────────────────────────────────────┤
│ 🧠 LSTM (2 capas, 64 unidades)     │ → Predicción magnitudes
│ ⚠️ Isolation Forest (contamination) │ → Detección anomalías
└────────┬────────────────────────────┘
         ↓
┌──────────────────────┐
│   PREDICCIONES       │ → Magnitud siguiente
│   CLASIFICACIÓN      │ → Nivel de riesgo
│   ANOMALÍAS          │ → Eventos anómalos
└────────┬─────────────┘
         ↓
┌──────────────────────────────┐
│   INTERFACES DE USUARIO      │
├──────────────────────────────┤
│ 📊 Streamlit Dashboard       │ → http://8501
│ 🔌 FastAPI REST API          │ → http://8000
│ 📓 Jupyter Notebooks         │ → http://8888
│ 📈 Visualizaciones PNG       │ → /notebooks
└──────────────────────────────┘
```

---

## 📊 Visualizaciones Generadas

| Gráfica | Descripción | Archivo |
|---------|-------------|---------|
| 📈 Series Temporal | 365 días de actividad sísmica | dashboard_seismico.png |
| 📊 Distribución | Histograma de magnitudes | dashboard_seismico.png |
| 🔴 Scatter | Magnitud vs Profundidad (coloreado) | dashboard_seismico.png |
| 🤖 LSTM Loss | Convergencia durante entrenamiento | training_results.png |
| ⚠️ Anomalías | Puntos normales vs anómalos | dashboard_seismico.png |
| 🎯 Predicciones | Valores reales vs LSTM | training_results.png |

---

## 🔗 Integración con Datos Reales

Para usar datos del USGS:

```python
from src.data_loader import SeismicDataLoader

loader = SeismicDataLoader()

# Descargar desde USGS API
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
params = {
    "format": "geojson",
    "starttime": "2023-01-01",
    "endtime": "2024-01-01",
    "minlatitude": -63.5,
    "maxlatitude": -62,
    "minlongitude": -61,
    "maxlongitude": -60,
}

data = loader.load_json_from_api(url, params)
```

---

## 🚨 Limitaciones & Disclaimer

⚠️ **IMPORTANTE:**
- Este sistema es para **análisis de patrones**, NO para predicción exacta de sismos
- La predicción de sismos no es científicamente posible con datos actuales
- Úsalo para investigación, monitoreo y análisis histórico
- **NO uses para toma de decisiones críticas de seguridad**

---

## 📌 Próximos Pasos

- [x] LSTM para series temporales
- [x] Detección de anomalías
- [x] Dashboard web Streamlit
- [x] API REST completa
- [x] Documentación completa
- [x] **Integración datos reales USGS** (src/usgs_integration.py)
- [x] **Predicción multi-paso** (src/multistep.py)
- [x] **Alertas en tiempo real** (src/realtime_alerts.py)
- [x] **Despliegue en cloud** (Heroku/Railway/Render)
- [x] **Aplicación móvil** (Flutter/React Native/Streamlit)

### v1.4.0 - Funcionalidades Avanzadas (NUEVO ✨)
- [x] **Notificaciones Push** - Firebase Cloud Messaging (src/push_notifications.py)
- [x] **Múltiples Volcanes** - Soporte para monitorear varios volcanes (src/multi_volcano.py)
- [x] **Autenticación OAuth 2.0** - Login seguro con Google/GitHub (src/auth.py)
- [x] **Predicción de Tsunamis** - Análisis de riesgo de tsunamis (src/tsunami_prediction.py)
- [x] **Análisis de Sentimiento** - Monitoreo en redes sociales (src/social_sentiment.py)
- [x] **Reportes Automáticos** - Generación de reportes diarios/semanales (src/reports.py)

### v1.4.1 - Sistema Nacional de Volcanes Colombianos (NUEVO ✨)
- [x] **13 Volcanes Colombianos** - Sistema especializado para volcanes de Colombia
  - Incluye: Nevado del Ruiz, Galeras, Puracé, Tolima, Huila, y más
  - Base de datos completa con coordenadas, historia, peligros
  - Población en riesgo por volcán: ~1.5 millones
  - Red de monitoreo SGC: 68+ estaciones sísmicas
- [x] **Monitor Nacional** - Monitoreo especializado por región (src/colombia_monitor.py)
- [x] **Documentación Regional** - Guía completa de volcanes (COLOMBIAN_VOLCANOES.md)

---

## 🐳 Despliegue en Producción

### Con Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000 8501
CMD ["python", "main.py"]
```

### En la nube

```bash
# Heroku
git push heroku main

# Railway
railway link && railway up

# Render
git push origin main  # Auto-deploy
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Ver [LICENSE](LICENSE) para detalles.

---

## 📞 Contacto

- **Autor**: CamiOso
- **Email**: cristian.1701421857@ucaldas.edu.co
- **GitHub**: [@CamiOso](https://github.com/CamiOso)
- **Institución**: Universidad de Caldas

---

## 📚 Referencias

- [TensorFlow Docs](https://tensorflow.org/api_docs)
- [Scikit-learn Docs](https://scikit-learn.org/stable/documentation.html)
- [Streamlit Docs](https://docs.streamlit.io/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/)

---

## 🎓 Créditos

Desarrollado con:
- Python 3.11
- TensorFlow/Keras
- Scikit-learn
- Pandas & NumPy
- Streamlit & FastAPI
- Matplotlib & Seaborn

---

**⭐ Si te resultó útil, por favor deja una estrella!**

```
╔════════════════════════════════════════════════════════════════╗
║        🌋 SISTEMA DE ANÁLISIS SÍSMICO CON INTELIGENCIA ARTIFICIAL ║
║              VOLCÁN DECEPTION - ANTÁRTIDA                   ║
║                      2026                                   ║
╚════════════════════════════════════════════════════════════════╝
```
