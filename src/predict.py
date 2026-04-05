"""
Script de predicción usando modelos entrenados
"""
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from src.data_loader import SeismicDataLoader
from src.model import SeismicLSTM, SeismicAnomalyDetector


def main():
    print("=" * 60)
    print("SISTEMA DE PREDICCIÓN SÍSMICA - INFERENCIA")
    print("=" * 60)
    
    # 1. Cargar modelos
    print("\n📂 Paso 1: Cargar modelos entrenados")
    lstm_model = SeismicLSTM(seq_length=config.SEQUENCE_LENGTH, features=2)
    lstm_model.load(os.path.join(config.MODELS_DIR, 'lstm_seismic.h5'))
    
    anomaly_detector = SeismicAnomalyDetector()
    anomaly_detector.load(os.path.join(config.MODELS_DIR, 'anomaly_detector.pkl'))
    
    # 2. Generar datos de prueba
    print("\n🔄 Paso 2: Generar datos de test")
    loader = SeismicDataLoader()
    loader.generate_sample_data(30)  # Últimos 30 días
    loader.filter_by_magnitude(config.MIN_MAGNITUDE)
    
    feature_cols = ['magnitude', 'depth']
    if 'depth' not in loader.data.columns:
        loader.data['depth'] = np.random.uniform(5, 50, len(loader.data))
    
    loader.normalize_features(feature_cols, method=config.SCALE_METHOD)
    
    # 3. Crear última secuencia para predicción
    print("\n🧬 Paso 3: Preparar secuencia para predicción")
    X_recent = loader.data[feature_cols].values[-config.SEQUENCE_LENGTH:]
    
    if len(X_recent) == config.SEQUENCE_LENGTH:
        # 4. Predicción LSTM
        print("\n🤖 Paso 4: Predicción LSTM")
        X_seq = X_recent.reshape(1, config.SEQUENCE_LENGTH, len(feature_cols))
        prediction = lstm_model.predict_single(X_seq)
        
        print(f"\n✨ PREDICCIÓN PRÓXIMA MAGNITUD (normalizada): {prediction:.4f}")
        
        # 5. Detección de anomalías
        print("\n🎯 Paso 5: Detección de anomalías")
        X_flat = X_recent.reshape(1, -1)
        anomaly_score = anomaly_detector.predict_proba(X_flat)[0]
        is_anomaly = anomaly_detector.predict(X_flat)[0]
        
        print(f"\n⚠️  Anomalía Score: {anomaly_score:.4f}")
        print(f"Clasificación: {'🔴 ANOMALÍA' if is_anomaly == -1 else '🟢 NORMAL'}")
        
        # 6. Resumen
        print_summary(prediction, anomaly_score, is_anomaly)
    else:
        print(f"⚠️  No hay suficientes datos (necesarios {config.SEQUENCE_LENGTH}, disponibles {len(X_recent)})")


def print_summary(prediction, anomaly_score, is_anomaly):
    """Imprime resumen de predicciones"""
    print("\n" + "=" * 60)
    print("RESUMEN DE PREDICCIÓN")
    print("=" * 60)
    
    print(f"\n📊 Magnitud Predicha: {prediction:.4f}")
    print(f"⚠️  Nivel de Anomalía: {anomaly_score:.4f} (0=normal, 1=anomalía)")
    print(f"🟢 Estado: {'ALERTA - Comportamiento Anómalo' if is_anomaly == -1 else 'Normal'}")
    
    risk_level = estimate_risk_level(anomaly_score)
    print(f"\n🎯 Nivel de Riesgo: {risk_level}")
    
    recommendations = get_recommendations(anomaly_score)
    print(f"\n💡 Recomendaciones:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    print("\n" + "=" * 60)


def estimate_risk_level(anomaly_score: float) -> str:
    """Estima nivel de riesgo basado en anomalía"""
    if anomaly_score < 0.3:
        return "🟢 BAJO - Actividad Normal"
    elif anomaly_score < 0.6:
        return "🟡 MODERADO - Comportamiento Inusual"
    elif anomaly_score < 0.8:
        return "🟠 ALTO - Anomalía Significativa"
    else:
        return "🔴 MUY ALTO - Comportamiento Extremo"


def get_recommendations(anomaly_score: float) -> list:
    """Sugiere acciones basadas en riesgo"""
    recommendations = []
    
    if anomaly_score < 0.3:
        recommendations.append("Continuar monitoreo rutinario")
        recommendations.append("No se requiere acción inmediata")
    elif anomaly_score < 0.6:
        recommendations.append("Aumentar frecuencia de monitoreo")
        recommendations.append("Revisar datos históricos recientes")
    elif anomaly_score < 0.8:
        recommendations.append("Active alertas de seguimiento")
        recommendations.append("Contacte a equipos de respuesta")
    else:
        recommendations.append("ALERTA MÁXIMA - Activar protocolos de emergencia")
        recommendations.append("Notifique a autoridades inmediatamente")
    
    return recommendations


if __name__ == "__main__":
    main()
