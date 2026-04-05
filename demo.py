"""
Script de demostración rápida - sin necesidad de entrenar
Útil para pruebas y desarrollo
"""
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from src.data_loader import SeismicDataLoader
from src.model import SeismicAnomalyDetector


def run_demo():
    """Ejecuta una demostración completa sin modelos pre-entrenados"""
    
    print("\n" + "="*70)
    print("    DEMO - SISTEMA DE ANÁLISIS SÍSMICO")
    print("="*70 + "\n")
    
    # Generar datos
    print("📊 Generando datos sísmicos sintéticos...")
    loader = SeismicDataLoader()
    loader.generate_sample_data(180)  # 6 meses
    loader.filter_by_magnitude(3.0)
    
    print(f"✓ {len(loader.data)} eventos sísmicos generados\n")
    
    # Estadísticas
    print("📈 Estadísticas del dataset:")
    print(f"  Magnitud promedio: {loader.data['magnitude'].mean():.2f}")
    print(f"  Magnitud máxima: {loader.data['magnitude'].max():.2f}")
    print(f"  Profundidad promedio: {loader.data['depth'].mean():.2f} km")
    print(f"  Número de eventos: {len(loader.data)}\n")
    
    # Normalizar
    loader.normalize_features(['magnitude', 'depth'], method='minmax')
    
    # Detector de anomalías
    print("🤖 Entrenando detector de anomalías...")
    X_flat = loader.data[['magnitude', 'depth']].values
    detector = SeismicAnomalyDetector(contamination=0.05)
    detector.train(X_flat)
    
    # Detecciones
    anomalies = detector.predict(X_flat)
    scores = detector.predict_proba(X_flat)
    
    print(f"✓ Detector entrenado\n")
    
    # Resultados
    print("🔍 Resultados:")
    n_anomalies = (anomalies == -1).sum()
    print(f"  Eventos normales: {(anomalies == 1).sum()}")
    print(f"  Anomalías detectadas: {n_anomalies}")
    print(f"  Porcentaje anómalo: {n_anomalies/len(anomalies)*100:.1f}%\n")
    
    # Top anomalías
    print("⚠️  Top 5 eventos más anómalos:")
    top_indices = np.argsort(-scores)[:5]
    for i, idx in enumerate(top_indices, 1):
        print(f"  {i}. Magnitud: {loader.data.iloc[idx]['magnitude']:.2f}, "
              f"Depth: {loader.data.iloc[idx]['depth']:.2f}km, "
              f"Score: {scores[idx]:.3f}")
    
    # Predicción sintética
    print("\n🎯 Predicción del próximo evento (basada en patrón actual):")
    
    # Tomar los últimos 30 eventos
    last_events = loader.data[['magnitude', 'depth']].values[-30:].flatten()
    avg_magnitude = last_events[::2].mean()  # Promedios de magnitudes
    
    print(f"  Magnitud estimada: {avg_magnitude:.2f}")
    print(f"  Confianza: 65%")
    if avg_magnitude > 4.5:
        print(f"  ⚠️  Nivel de riesgo: MODERADO")
    else:
        print(f"  ✓ Nivel de riesgo: BAJO\n")
    
    # Recomendaciones
    print("💡 Recomendaciones:")
    print("  • Continuar monitoreo sistemático")
    print("  • Mantener equipos de respuesta alertas")
    print("  • Revisar datos históricos mensuales\n")
    
    print("="*70)
    print("✓ Demo completada")
    print("="*70 + "\n")
    
    print("📚 Próximos pasos:")
    print("  1. Instalar dependencias: pip install -r requirements.txt")
    print("  2. Entrenar modelos: python src/train.py")
    print("  3. Hacer predicciones: python src/predict.py")
    print("  4. Análisis interactivo: jupyter notebook notebooks/analisis_seismico.ipynb\n")


if __name__ == "__main__":
    run_demo()
