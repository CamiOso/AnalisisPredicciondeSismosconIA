"""
Script de entrenamiento del modelo sísmico
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from src.data_loader import SeismicDataLoader
from src.model import SeismicLSTM, SeismicAnomalyDetector


def main():
    print("=" * 60)
    print("SISTEMA DE PREDICCIÓN SÍSMICA - ENTRENAMIENTO")
    print("=" * 60)
    
    # 1. Cargar datos
    print("\n📊 Paso 1: Cargar datos")
    loader = SeismicDataLoader()
    loader.generate_sample_data(365)
    loader.filter_by_magnitude(config.MIN_MAGNITUDE)
    
    # 2. Preparar features
    print("\n🔧 Paso 2: Preparar features")
    feature_cols = ['magnitude', 'depth']
    
    # Asegurar que las columnas existan
    if 'depth' not in loader.data.columns:
        loader.data['depth'] = np.random.uniform(5, 50, len(loader.data))
    
    loader.normalize_features(feature_cols, method=config.SCALE_METHOD)
    
    # 3. Crear datos para LSTM
    print("\n🧬 Paso 3: Crear secuencias")
    X_train, X_test, y_train, y_test = loader.prepare_for_lstm(
        feature_cols,
        seq_length=config.SEQUENCE_LENGTH,
        split_ratio=config.TRAIN_TEST_SPLIT
    )
    
    # 4. Entrenar modelo LSTM
    print("\n🤖 Paso 4: Entrenar modelo LSTM")
    lstm_model = SeismicLSTM(seq_length=config.SEQUENCE_LENGTH, features=len(feature_cols))
    
    history = lstm_model.train(
        X_train, y_train,
        X_val=X_test, y_val=y_test,
        epochs=config.EPOCHS,
        batch_size=config.BATCH_SIZE
    )
    
    # 5. Evaluar modelo
    print("\n📈 Paso 5: Evaluar modelo")
    metrics = lstm_model.evaluate(X_test, y_test)
    
    # 6. Guardar modelo
    print("\n💾 Paso 6: Guardar modelo")
    os.makedirs(config.MODELS_DIR, exist_ok=True)
    lstm_model.save(os.path.join(config.MODELS_DIR, 'lstm_seismic.h5'))
    
    # 7. Entrenar detector de anomalías
    print("\n🚀 Paso 7: Entrenar detector de anomalías")
    X_train_flat = X_train.reshape(X_train.shape[0], -1)
    anomaly_detector = SeismicAnomalyDetector(contamination=0.1)
    anomaly_detector.train(X_train_flat)
    anomaly_detector.save(os.path.join(config.MODELS_DIR, 'anomaly_detector.pkl'))
    
    # 8. Graficar resultados
    print("\n📉 Paso 8: Generar gráficas")
    plot_results(history, lstm_model, X_test, y_test)
    
    print("\n" + "=" * 60)
    print("✓ ENTRENAMIENTO COMPLETADO")
    print("=" * 60)


def plot_results(history, model, X_test, y_test):
    """Genera gráficas de resultados"""
    os.makedirs(config.NOTEBOOKS_DIR, exist_ok=True)
    
    # Gráfica de pérdida
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    
    axes[0].plot(history.history['loss'], label='Train Loss')
    if 'val_loss' in history.history:
        axes[0].plot(history.history['val_loss'], label='Val Loss')
    axes[0].set_xlabel('Época')
    axes[0].set_ylabel('Pérdida (MSE)')
    axes[0].set_title('Pérdida durante Entrenamiento')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Predicciones vs Reales
    y_pred = model.predict(X_test)
    axes[1].plot(y_test[:100, 0], label='Valores Reales', alpha=0.7)
    axes[1].plot(y_pred[:100, 0], label='Predicciones', alpha=0.7)
    axes[1].set_xlabel('Muestras de Test')
    axes[1].set_ylabel('Valor Normalizado')
    axes[1].set_title('Predicciones vs Valores Reales')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(config.NOTEBOOKS_DIR, 'training_results.png'), dpi=150)
    print(f"✓ Gráfica guardada en {config.NOTEBOOKS_DIR}/training_results.png")
    plt.close()


if __name__ == "__main__":
    main()
