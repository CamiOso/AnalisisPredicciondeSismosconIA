# Sistema de Análisis y Predicción de Sismos con IA

Sistema de machine learning para análisis de datos sísmicos y predicción de patrones sísmicos usando redes neuronales LSTM.

## 🎯 Objetivo
- Analizar patrones históricos de sismos
- Detectar anomalías en actividad sísmica
- Predecir réplicas y patrones de actividad futura
- Clasificar eventos sísmicos por magnitud

## 📁 Estructura del Proyecto
```
.
├── data/                 # Datos sísmicos (CSV, JSON)
├── models/              # Modelos entrenados (.h5)
├── src/                 # Código fuente
│   ├── data_loader.py   # Carga y preprocesamiento
│   ├── model.py         # Arquitectura LSTM
│   ├── train.py         # Entrenamiento
│   └── predict.py       # Predicciones
├── notebooks/           # Análisis exploratorio
├── requirements.txt     # Dependencias
└── config.py           # Configuración global
```

## 🚀 Inicio Rápido

### 1. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Descargar datos (USGS)
```bash
python src/download_data.py
```

### 4. Entrenar modelo
```bash
python src/train.py
```

### 5. Hacer predicciones
```bash
python src/predict.py
```

## 📊 Modelos Disponibles
- **LSTM**: Predicción de series temporales de magnitud
- **CNN-LSTM**: Detección de patrones complejos
- **Isolation Forest**: Detección de anomalías

## 📈 Métricas
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- F1-Score (para clasificación)

## 🔗 Fuentes de Datos
- USGS (United States Geological Survey)
- EMSC (European-Mediterranean Seismological Centre)
- GFZ (German Research Centre for Geosciences)

## ⚠️ Disclaimer
Este sistema es para **análisis y patrones**, NO para predicción exacta de sismos (no científicamente posible).
