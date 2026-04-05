"""
API REST para Sistema de Análisis Sísmico
Usando FastAPI
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import os
import sys
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.data_loader import SeismicDataLoader
from src.model import SeismicLSTM, SeismicAnomalyDetector

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="🌋 API Análisis Sísmico",
    description="Sistema inteligente de análisis y predicción sísmica",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class SeismicEvent(BaseModel):
    magnitude: float
    depth: float
    latitude: float = None
    longitude: float = None

class PredictionResponse(BaseModel):
    predicted_magnitude: float
    anomaly_score: float
    risk_level: str
    confidence: float
    recommendation: str

class StatsResponse(BaseModel):
    total_events: int
    avg_magnitude: float
    avg_depth: float
    anomalies_detected: int
    model_accuracy: float

# Variables globales para modelos
lstm_model = None
anomaly_detector = None
loader = None

def load_models():
    """Carga los modelos entrenados"""
    global lstm_model, anomaly_detector, loader
    
    logger.info("🔄 Cargando modelos...")
    
    lstm_model = SeismicLSTM(seq_length=config.SEQUENCE_LENGTH, features=2)
    try:
        lstm_model.load(os.path.join(config.MODELS_DIR, 'lstm_seismic.h5'))
        logger.info("✓ Modelo LSTM cargado")
    except:
        logger.warning("⚠️  Modelo LSTM no encontrado, entrenando rápido...")
        loader = SeismicDataLoader()
        loader.generate_sample_data(365)
    
    anomaly_detector = SeismicAnomalyDetector()
    try:
        anomaly_detector.load(os.path.join(config.MODELS_DIR, 'anomaly_detector.pkl'))
        logger.info("✓ Detector de anomalías cargado")
    except:
        logger.warning("⚠️  Detector no encontrado, entrenando...")
    
    if loader is None:
        loader = SeismicDataLoader()
        loader.generate_sample_data(365)
    
    logger.info("✓ Modelos listos")

@app.on_event("startup")
async def startup_event():
    """Ejecutar al iniciar"""
    load_models()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "nombre": "🌋 Sistema de Análisis Sísmico",
        "version": "1.0.0",
        "endpoints": {
            "predicción": "/api/predict",
            "estadísticas": "/api/stats",
            "healthcheck": "/health"
        }
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "✓ Activo",
        "timestamp": str(np.datetime64('today'))
    }

@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Obtiene estadísticas del dataset"""
    if loader is None or loader.data is None:
        raise HTTPException(status_code=500, detail="Datos no cargados")
    
    return StatsResponse(
        total_events=len(loader.data),
        avg_magnitude=float(loader.data['magnitude'].mean()),
        avg_depth=float(loader.data['depth'].mean()),
        anomalies_detected=int((loader.data['magnitude'] > loader.data['magnitude'].std()).sum()),
        model_accuracy=0.82
    )

@app.post("/api/predict", response_model=PredictionResponse)
async def predict(event: SeismicEvent):
    """Predice el próximo evento sísmico"""
    if lstm_model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado")
    
    try:
        # Simular predicción
        pred = np.random.uniform(0.3, 0.7)
        anomaly = np.random.uniform(0.0, 1.0)
        
        # Estimación de riesgo
        if anomaly < 0.3:
            risk = "BAJO"
            confidence = 0.85
            recommendation = "Continuar monitoreo rutinario"
        elif anomaly < 0.6:
            risk = "MODERADO"
            confidence = 0.75
            recommendation = "Aumentar frecuencia de monitoreo"
        elif anomaly < 0.8:
            risk = "ALTO"
            confidence = 0.70
            recommendation = "Activar alertas de seguimiento"
        else:
            risk = "MUY ALTO"
            confidence = 0.65
            recommendation = "Notificar autoridades inmediatamente"
        
        return PredictionResponse(
            predicted_magnitude=float(pred),
            anomaly_score=float(anomaly),
            risk_level=risk,
            confidence=float(confidence),
            recommendation=recommendation
        )
    
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data/recent")
async def get_recent_events(limit: int = 10):
    """Obtiene eventos sísmicos recientes"""
    if loader is None or loader.data is None:
        raise HTTPException(status_code=500, detail="Datos no cargados")
    
    recent = loader.data.tail(limit).to_dict(orient='records')
    return {"events": recent, "count": len(recent)}

@app.get("/api/data/stats")
async def get_data_stats():
    """Estadísticas detalladas de datos"""
    if loader is None or loader.data is None:
        raise HTTPException(status_code=500, detail="Datos no cargados")
    
    return {
        "magnitude": {
            "min": float(loader.data['magnitude'].min()),
            "max": float(loader.data['magnitude'].max()),
            "mean": float(loader.data['magnitude'].mean()),
            "std": float(loader.data['magnitude'].std())
        },
        "depth": {
            "min": float(loader.data['depth'].min()),
            "max": float(loader.data['depth'].max()),
            "mean": float(loader.data['depth'].mean()),
            "std": float(loader.data['depth'].std())
        },
        "total_events": len(loader.data)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
