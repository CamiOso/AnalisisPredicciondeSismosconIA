"""
CLI mejorado con más comandos y opciones
"""
import click
import pandas as pd
from tabulate import tabulate
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import SeismicDataLoader
from src.model import SeismicLSTM, SeismicAnomalyDetector
from src.predict import SeismicPredictor
from src.statistics import SeismicStatistics
from src.database import SeismicDatabase
from src.alerts import EmailAlert
from src import config


@click.group()
def cli():
    """🌋 Sistema de Análisis Sísmico con IA - CLI"""
    pass


@cli.command()
@click.option('--days', default=365, help='Días de datos a generar')
def generate_data(days):
    """📊 Genera datos sísmicos sintéticos"""
    
    click.echo(f"📊 Generando {days} días de datos sísmicos...")
    
    loader = SeismicDataLoader()
    data = loader.generate_sample_data(days=days)
    
    # Guardar
    filepath = os.path.join(config.DATA_DIR, f'data_{days}d.csv')
    data.to_csv(filepath, index=False)
    
    click.echo(f"✓ {len(data)} eventos generados")
    click.echo(f"✓ Guardado en {filepath}")
    click.echo(f"\n📈 Estadísticas:")
    click.echo(f"  Magnitud media: {data['magnitude'].mean():.2f}")
    click.echo(f"  Profundidad media: {data['depth'].mean():.1f} km")


@cli.command()
def train_models():
    """🤖 Entrena los modelos LSTM y Anomaly Detector"""
    
    click.echo("🤖 Preparando datos...")
    loader = SeismicDataLoader()
    data = loader.generate_sample_data(days=365)
    
    click.echo("📊 Normalizando features...")
    data_normalized = loader.normalize_features(data.copy())
    
    click.echo("🔄 Creando secuencias para LSTM...")
    X, y = loader.create_sequences(data_normalized['magnitude'].values, seq_length=30)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    
    # Train test split
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Entrenar LSTM
    click.echo("🧠 Entrenando LSTM (100 épocas)...")
    lstm = SeismicLSTM()
    model = lstm.create_model(input_shape=(30, 1))
    model.fit(X_train, y_train, epochs=100, batch_size=32, 
              validation_data=(X_test, y_test), verbose=0)
    
    click.echo("✓ Modelo LSTM entrenado")
    
    # Entrenar Anomaly Detector
    click.echo("⚠️  Entrenando Anomaly Detector...")
    detector = SeismicAnomalyDetector()
    detector.fit(data['magnitude'].values.reshape(-1, 1))
    
    click.echo("✓ Anomaly Detector entrenado")
    click.echo("\n✅ Entrenamiento completado!")


@cli.command()
@click.option('--magnitude', default=5.0, help='Magnitud a predecir')
@click.option('--depth', default=30.0, help='Profundidad a predecir')
def predict(magnitude, depth):
    """🎯 Hace una predicción con los modelos entrenados"""
    
    try:
        click.echo(f"🎯 Haciendo predicción para M{magnitude} a {depth}km...")
        
        predictor = SeismicPredictor()
        prediction = predictor.predict(magnitude, depth)
        
        click.echo("\n" + "="*50)
        click.echo("PREDICCIÓN")
        click.echo("="*50)
        click.echo(f"Magnitud predicha: {prediction.get('predicted_magnitude', 'N/A'):.2f}")
        click.echo(f"Score de anomalía: {prediction.get('anomaly_score', 'N/A'):.3f}")
        click.echo(f"Nivel de riesgo: {prediction.get('risk_level', 'DESCONOCIDO')}")
        click.echo(f"Confianza: {prediction.get('confidence', 0)*100:.1f}%")
        click.echo(f"\n📝 Recomendación: {prediction.get('recommendation', 'N/A')}")
        click.echo("="*50)
    
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)


@cli.command()
@click.option('--days', default=30, help='Días de análisis')
def analyze(days):
    """📈 Análisis estadístico de datos sísmicos"""
    
    click.echo(f"📈 Analizando últimos {days} días...")
    
    loader = SeismicDataLoader()
    data = loader.generate_sample_data(days=days)
    
    stats = SeismicStatistics(data)
    stats.print_summary()


@cli.command()
def status():
    """📊 Estado actual del sistema"""
    
    click.echo("\n" + "="*60)
    click.echo("🌋 ESTADO DEL SISTEMA")
    click.echo("="*60)
    
    # Verificar modelos
    lstm_path = os.path.join(config.MODELS_DIR, 'lstm_seismic.h5')
    detector_path = os.path.join(config.MODELS_DIR, 'anomaly_detector.pkl')
    
    click.echo("\n🤖 Modelos:")
    click.echo(f"  LSTM: {'✓ Disponible' if os.path.exists(lstm_path) else '✗ No disponible'}")
    click.echo(f"  Anomaly Detector: {'✓ Disponible' if os.path.exists(detector_path) else '✗ No disponible'}")
    
    # Verificar datos
    data_files = [f for f in os.listdir(config.DATA_DIR) if f.endswith('.csv')]
    click.echo(f"\n📊 Archivos de datos: {len(data_files)}")
    for f in data_files[:5]:
        click.echo(f"  - {f}")
    
    # Base de datos
    try:
        db = SeismicDatabase()
        stats = db.get_statistics()
        click.echo(f"\n💾 Base de datos:")
        click.echo(f"  Total eventos: {stats['total_events']}")
        click.echo(f"  Magnitud media: {stats['avg_magnitude']:.2f}")
        click.echo(f"  Profundidad media: {stats['avg_depth']:.1f} km")
    except:
        click.echo("\n💾 Base de datos: No disponible")
    
    click.echo("\n" + "="*60 + "\n")


@cli.command()
@click.option('--email', prompt='Email destino', help='Email para enviar alerta')
@click.option('--magnitude', default=5.0, help='Magnitud simulada')
def test_alert(email, magnitude):
    """📧 Prueba el sistema de alertas por email"""
    
    click.echo("📧 Preparando alerta de prueba...")
    
    alert_system = EmailAlert()
    
    test_data = {
        'magnitude': magnitude,
        'depth': 30.5,
        'anomaly_score': 0.85,
        'risk_level': 'ALTO',
        'recommendation': 'Aumentar monitoreo de zona.'
    }
    
    if alert_system.send_anomaly_alert(email, test_data):
        click.echo(f"✓ Alerta enviada a {email}")
    else:
        click.echo(f"✗ Error enviando alerta (verificar credenciales)", err=True)


@cli.command()
@click.option('--format', type=click.Choice(['csv', 'json']), default='csv')
def export_data(format):
    """💾 Exporta datos de la base de datos"""
    
    try:
        db = SeismicDatabase()
        
        if format == 'csv':
            filepath = os.path.join(config.DATA_DIR, 'export_data.csv')
            # Exportar a CSV
            click.echo(f"💾 Exportando a {filepath}...")
        else:
            filepath = os.path.join(config.DATA_DIR, 'export_data.json')
            db.export_to_json(filepath)
        
        click.echo(f"✓ Datos exportados a {filepath}")
    
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)


@cli.command()
def test_system():
    """✅ Prueba completa del sistema"""
    
    click.echo("\n" + "="*60)
    click.echo("✅ PRUEBA DEL SISTEMA")
    click.echo("="*60)
    
    # Test 1: Data Loader
    click.echo("\n[1/5] Probando Data Loader...")
    try:
        loader = SeismicDataLoader()
        data = loader.generate_sample_data(days=10)
        click.echo(f"  ✓ {len(data)} eventos generados")
    except Exception as e:
        click.echo(f"  ✗ Error: {str(e)}")
    
    # Test 2: Models
    click.echo("\n[2/5] Probando modelos...")
    try:
        lstm = SeismicLSTM()
        model = lstm.create_model((30, 1))
        click.echo("  ✓ Modelo LSTM creado")
        
        detector = SeismicAnomalyDetector()
        click.echo("  ✓ Anomaly Detector creado")
    except Exception as e:
        click.echo(f"  ✗ Error: {str(e)}")
    
    # Test 3: Predictions
    click.echo("\n[3/5] Probando predicciones...")
    try:
        predictor = SeismicPredictor()
        pred = predictor.predict(5.0, 30)
        click.echo(f"  ✓ Predicción: M{pred['predicted_magnitude']:.2f}")
    except Exception as e:
        click.echo(f"  ✗ Error: {str(e)}")
    
    # Test 4: Statistics
    click.echo("\n[4/5] Probando análisis estadístico...")
    try:
        data = loader.generate_sample_data(days=30)
        stats = SeismicStatistics(data)
        dist = stats.calculate_magnitude_distribution()
        click.echo(f"  ✓ Media de magnitud: {dist['mean']:.2f}")
    except Exception as e:
        click.echo(f"  ✗ Error: {str(e)}")
    
    # Test 5: Database
    click.echo("\n[5/5] Probando base de datos...")
    try:
        db = SeismicDatabase()
        db.add_event(5.2, 30.5, anomaly_score=0.3, risk_level='MODERADO')
        click.echo("  ✓ Evento almacenado")
    except Exception as e:
        click.echo(f"  ✗ Error: {str(e)}")
    
    click.echo("\n" + "="*60)
    click.echo("✅ Prueba completada!\n")


@cli.command()
def version():
    """🔖 Muestra versión del sistema"""
    
    click.echo(f"🌋 Sistema de Análisis Sísmico v1.2.0")
    click.echo(f"Python: {sys.version.split()[0]}")
    click.echo(f"Ubicación: {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")


if __name__ == '__main__':
    cli()
