"""
Ejemplos de uso de las nuevas funcionalidades
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import SeismicDataLoader
from src.database import SeismicDatabase
from src.statistics import SeismicStatistics
from src.alerts import EmailAlert
from src.forecasting import SeismicForecasting
import pandas as pd


def example_1_basic_workflow():
    """Ejemplo 1: Flujo básico - Cargar, analizar, guardar"""
    
    print("\n" + "="*70)
    print("EJEMPLO 1: Flujo Básico - Cargar, Analizar, Guardar")
    print("="*70 + "\n")
    
    # 1. Generar datos
    print("📊 Generando datos sísmicos...")
    loader = SeismicDataLoader()
    data = loader.generate_sample_data(days=100)
    print(f"✓ {len(data)} eventos generados\n")
    
    # 2. Guardar en base de datos
    print("💾 Guardando en base de datos...")
    db = SeismicDatabase()
    for idx, row in data.iterrows():
        db.add_event(
            magnitude=row['magnitude'],
            depth=row['depth'],
            latitude=row.get('latitude'),
            longitude=row.get('longitude'),
            anomaly_score=0.5,
            risk_level='BAJO'
        )
    print(f"✓ {len(data)} eventos guardados\n")
    
    # 3. Obtener estadísticas
    print("📈 Estadísticas de base de datos:")
    stats = db.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")


def example_2_statistical_analysis():
    """Ejemplo 2: Análisis estadístico avanzado"""
    
    print("\n" + "="*70)
    print("EJEMPLO 2: Análisis Estadístico Avanzado")
    print("="*70 + "\n")
    
    # Generar datos
    loader = SeismicDataLoader()
    data = loader.generate_sample_data(days=365)
    
    # Análisis
    stats = SeismicStatistics(data)
    
    print("📊 Distribución de Magnitudes:")
    dist = stats.calculate_magnitude_distribution()
    print(f"  Media: {dist['mean']:.2f}")
    print(f"  Mediana: {dist['median']:.2f}")
    print(f"  Desv. Est.: {dist['std']:.2f}")
    print(f"  Asimetría: {dist['skewness']:.2f}")
    print(f"  Curtosis: {dist['kurtosis']:.2f}")
    print(f"  ¿Normal?: {'Sí' if dist['is_normal'] else 'No'}\n")
    
    print("📐 Relación Gutenberg-Richter:")
    gr = stats.calculate_gutenberg_richter()
    print(f"  a-value: {gr['a_value']:.2f}")
    print(f"  b-value: {gr['b_value']:.2f}\n")
    
    print("⏱️  Temporales:")
    temporal = stats.calculate_temporal_statistics()
    print(f"  Intervalo medio: {temporal['mean_interval']:.1f} días")
    print(f"  Intervalo máximo: {temporal['max_interval']:.1f} días\n")
    
    print("🎯 Clusters:")
    clusters = stats.detect_clusters(magnitude_threshold=4.0)
    print(f"  Número: {clusters['num_clusters']}")
    print(f"  Tamaño promedio: {clusters['avg_cluster_size']:.1f}\n")


def example_3_forecasting():
    """Ejemplo 3: Predicción con múltiples métodos"""
    
    print("\n" + "="*70)
    print("EJEMPLO 3: Forecasting Avanzado")
    print("="*70 + "\n")
    
    # Generar datos
    loader = SeismicDataLoader()
    data = loader.generate_sample_data(days=180)
    
    # Forecasting
    forecaster = SeismicForecasting()
    
    print("🔮 Comparando métodos de pronóstico...\n")
    
    results = forecaster.compare_forecasts(data, test_size=15)
    
    print("\n📊 Resultados:")
    for method, metrics in results.items():
        print(f"  {method}:")
        for metric, value in metrics.items():
            print(f"    {metric}: {value:.4f}")


def example_4_database_operations():
    """Ejemplo 4: Operaciones avanzadas con base de datos"""
    
    print("\n" + "="*70)
    print("EJEMPLO 4: Operaciones con Base de Datos")
    print("="*70 + "\n")
    
    db = SeismicDatabase()
    
    # Agregar eventos simulados
    print("📝 Agregando eventos simulados...")
    for i in range(10):
        db.add_event(
            magnitude=4.0 + i*0.1,
            depth=30.0 + i*2,
            anomaly_score=0.2 + i*0.05,
            risk_level=['BAJO', 'MODERADO', 'ALTO'][i % 3]
        )
    
    # Agregar predicciones
    print("🎯 Agregando predicciones...")
    for i in range(10):
        db.add_prediction(
            predicted_magnitude=4.5 + i*0.1,
            anomaly_score=0.3,
            risk_level=['BAJO', 'MODERADO'][i % 2],
            confidence=0.85 + i*0.01,
            model_name='LSTM'
        )
    
    # Obtener récientes
    print("\n📊 Últimos eventos:")
    recent = db.get_recent_events(limit=5)
    for event in recent:
        print(f"  M{event[2]:.1f} @ {event[3]:.0f}km - {event[6]}")
    
    # Exportar
    print("\n💾 Exportando a JSON...")
    db.export_to_json('/tmp/seismic_export.json')
    print("✓ Datos exportados a /tmp/seismic_export.json")


def example_5_alert_system():
    """Ejemplo 5: Sistema de alertas (sin envío real)"""
    
    print("\n" + "="*70)
    print("EJEMPLO 5: Sistema de Alertas")
    print("="*70 + "\n")
    
    alert = EmailAlert()
    
    print("📧 Configuración de alertas:")
    print("  Usar variables de entorno:")
    print("    EMAIL_SENDER=tu_email@gmail.com")
    print("    EMAIL_PASSWORD=tu_contraseña_app")
    print("\n  Luego usar:")
    
    # Mostrar código de ejemplo (sin ejecutar)
    example_code = """
    alert.send_anomaly_alert(
        recipient_email='destino@email.com',
        anomaly_data={
            'magnitude': 5.8,
            'depth': 35.2,
            'anomaly_score': 0.92,
            'risk_level': 'MUY ALTO',
            'recommendation': 'Aumentar vigilancia inmediatamente'
        }
    )
    """
    print(example_code)


def example_6_complete_pipeline():
    """Ejemplo 6: Pipeline completo de análisis"""
    
    print("\n" + "="*70)
    print("EJEMPLO 6: Pipeline Completo")
    print("="*70 + "\n")
    
    # 1. Generar datos
    print("[1/5] Generando datos...")
    loader = SeismicDataLoader()
    data = loader.generate_sample_data(days=180)
    print(f"✓ {len(data)} eventos\n")
    
    # 2. Guardar en BD
    print("[2/5] Guardando en base de datos...")
    db = SeismicDatabase()
    for idx, row in data.iterrows():
        db.add_event(
            magnitude=row['magnitude'],
            depth=row['depth'],
            anomaly_score=0.3 + (idx % 10) * 0.05
        )
    stats_db = db.get_statistics()
    print(f"✓ {stats_db['total_events']} eventos en BD\n")
    
    # 3. Análisis estadístico
    print("[3/5] Análisis estadístico...")
    stats = SeismicStatistics(data)
    dist = stats.calculate_magnitude_distribution()
    print(f"✓ Media de magnitud: {dist['mean']:.2f}\n")
    
    # 4. Forecasting
    print("[4/5] Predicciones...")
    forecaster = SeismicForecasting()
    print("✓ Modelos disponibles: Prophet, ARIMA\n")
    
    # 5. Guardar métricas
    print("[5/5] Guardando métricas...")
    db.add_metric('avg_magnitude', dist['mean'], 'ANALYSIS')
    db.add_metric('std_magnitude', dist['std'], 'ANALYSIS')
    print("✓ Métricas guardadas\n")
    
    print("✅ Pipeline completado!\n")


if __name__ == '__main__':
    print("\n\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  🌋 EJEMPLOS DE USO DEL SISTEMA DE ANÁLISIS SÍSMICO  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Ejecutar ejemplos
    example_1_basic_workflow()
    example_2_statistical_analysis()
    example_3_forecasting()
    example_4_database_operations()
    example_5_alert_system()
    example_6_complete_pipeline()
    
    print("\n" + "="*70)
    print("✅ TODOS LOS EJEMPLOS COMPLETADOS")
    print("="*70 + "\n")
    print("💡 Próximos pasos:")
    print("  1. Revisar FEATURES.md para más detalles")
    print("  2. Usar CLI: python cli.py --help")
    print("  3. Ejecutar tests: python -m pytest tests/")
    print("  4. Iniciar dashboard: bash start_dashboard.sh")
    print("\n")
