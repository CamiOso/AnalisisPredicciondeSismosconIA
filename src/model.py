"""
Modelos de Machine Learning para predicción sísmica
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Sequential
from sklearn.ensemble import IsolationForest
import joblib
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class SeismicLSTM:
    """Modelo LSTM para predicción de series temporales sísmicas"""
    
    def __init__(self, seq_length: int = 30, features: int = 1):
        self.seq_length = seq_length
        self.features = features
        self.model = self._build_model()
        self.history = None
    
    def _build_model(self):
        """Construye arquitectura LSTM"""
        model = Sequential([
            layers.LSTM(config.LSTM_UNITS, activation='relu', 
                       input_shape=(self.seq_length, self.features)),
            layers.Dropout(config.DROPOUT_RATE),
            layers.Dense(32, activation='relu'),
            layers.Dropout(config.DROPOUT_RATE),
            layers.Dense(self.features)
        ])
        
        optimizer = keras.optimizers.Adam(learning_rate=config.LEARNING_RATE)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        return model
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray,
              X_val: np.ndarray = None, y_val: np.ndarray = None,
              epochs: int = None, batch_size: int = None, verbose: int = 1):
        """Entrena el modelo"""
        if epochs is None:
            epochs = config.EPOCHS
        if batch_size is None:
            batch_size = config.BATCH_SIZE
        
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        
        print(f"🚀 Entrenando LSTM por {epochs} épocas...")
        self.history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=validation_data,
            verbose=verbose,
            callbacks=[
                keras.callbacks.EarlyStopping(
                    monitor='val_loss' if validation_data else 'loss',
                    patience=10,
                    restore_best_weights=True
                )
            ]
        )
        print("✓ Entrenamiento completado")
        return self.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Realiza predicciones"""
        return self.model.predict(X, verbose=0)
    
    def predict_single(self, X: np.ndarray) -> float:
        """Predice un solo valor"""
        prediction = self.model.predict(X.reshape(1, self.seq_length, self.features), verbose=0)
        return prediction[0][0]
    
    def save(self, filepath: str):
        """Guarda el modelo"""
        self.model.save(filepath)
        print(f"✓ Modelo guardado en {filepath}")
    
    def load(self, filepath: str):
        """Carga un modelo"""
        self.model = keras.models.load_model(filepath)
        print(f"✓ Modelo cargado de {filepath}")
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray):
        """Evalúa el modelo"""
        loss, mae = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"\n📊 Métricas de Test:")
        print(f"  Loss (MSE): {loss:.6f}")
        print(f"  MAE: {mae:.6f}")
        return {'loss': loss, 'mae': mae}


class SeismicAnomalyDetector:
    """Detector de anomalías sísmicas con Isolation Forest"""
    
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_trained = False
    
    def train(self, X: np.ndarray):
        """Entrena el detector"""
        print("🚀 Entrenando detector de anomalías...")
        self.model.fit(X)
        self.is_trained = True
        print("✓ Detector entrenado")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Detecta anomalías (-1: anomalía, 1: normal)"""
        return self.model.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Obtiene scores de anomalía"""
        return -self.model.score_samples(X)
    
    def save(self, filepath: str):
        """Guarda el modelo"""
        joblib.dump(self.model, filepath)
        print(f"✓ Modelo guardado en {filepath}")
    
    def load(self, filepath: str):
        """Carga el modelo"""
        self.model = joblib.load(filepath)
        self.is_trained = True
        print(f"✓ Modelo cargado de {filepath}")


class SeismicClassifier:
    """Clasificador de magnitudes de terremotos"""
    
    def __init__(self, seq_length: int = 30):
        self.seq_length = seq_length
        self.model = self._build_model()
    
    def _build_model(self):
        """Construye modelo clasificador"""
        model = Sequential([
            layers.LSTM(64, activation='relu', input_shape=(self.seq_length, 1)),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(3, activation='softmax')  # 3 clases: baja, media, alta
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray,
              X_val: np.ndarray = None, y_val: np.ndarray = None,
              epochs: int = 50):
        """Entrena el clasificador"""
        print("🚀 Entrenando clasificador...")
        
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        
        self.history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=32,
            validation_data=validation_data,
            verbose=1
        )
        print("✓ Clasificador entrenado")


def create_magnitude_labels(magnitudes: np.ndarray, bins: list = [0, 4, 5.5, 10]):
    """Convierte magnitudes continuas a clases discretas"""
    labels = np.digitize(magnitudes, bins) - 1
    labels = np.clip(labels, 0, 2)
    # Convertir a one-hot
    return keras.utils.to_categorical(labels, num_classes=3)
