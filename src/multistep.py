"""
Predicción Multi-paso (Multi-step forecasting)
Predice múltiples pasos en el futuro
"""
import numpy as np
import pandas as pd
from typing import Tuple, List
import warnings
warnings.filterwarnings('ignore')

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model import SeismicLSTM
import tensorflow as tf


class MultiStepForecaster:
    """
    Predicción de múltiples pasos en el futuro
    Soporta dos enfoques: Direct y Recursive
    """
    
    def __init__(self, sequence_length: int = 30):
        self.sequence_length = sequence_length
        self.lstm = SeismicLSTM()
        self.scaler = None
    
    def create_multistep_model(self, input_shape: Tuple, num_steps: int = 7):
        """
        Crea modelo para predictor de múltiples pasos
        
        Args:
            input_shape: Forma del input (sequence_length, features)
            num_steps: Número de pasos a predecir
        
        Returns:
            Modelo Keras compilado
        """
        
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(64, activation='relu', input_shape=input_shape, return_sequences=True),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.LSTM(32, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(num_steps)  # Output: predicciones para N pasos
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model
    
    def prepare_multistep_data(self, 
                              data: np.ndarray,
                              sequence_length: int = 30,
                              num_steps: int = 7) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepara datos para predicción multi-paso
        
        Args:
            data: Serie temporal (1D)
            sequence_length: Longitud de secuencia
            num_steps: Pasos a predecir
        
        Returns:
            X, y preparados para entrenamiento
        """
        
        X, y = [], []
        
        for i in range(len(data) - sequence_length - num_steps + 1):
            # Input: últimos N días
            X.append(data[i:i + sequence_length])
            
            # Output: próximos M días
            y.append(data[i + sequence_length:i + sequence_length + num_steps])
        
        return np.array(X).reshape(-1, sequence_length, 1), np.array(y)
    
    def forecast_direct(self, 
                       model,
                       X_recent: np.ndarray,
                       num_steps: int = 7) -> np.ndarray:
        """
        Predicción DIRECT: Un modelo predice todos los pasos simultaneamente
        Más rápido pero menos flexible
        
        Args:
            model: Modelo entrenado
            X_recent: Secuencia reciente (sequence_length, 1)
            num_steps: Pasos a predecir
        
        Returns:
            Array con predicciones (num_steps,)
        """
        
        X = X_recent.reshape(1, self.sequence_length, 1)
        predictions = model.predict(X, verbose=0)[0]
        
        return predictions
    
    def forecast_recursive(self,
                          model,
                          X_recent: np.ndarray,
                          num_steps: int = 7) -> np.ndarray:
        """
        Predicción RECURSIVE: Usa predicción anterior como input siguiente
        Más flexible pero acumula errores
        
        Args:
            model: Modelo entrenado (predice 1 paso)
            X_recent: Secuencia reciente
            num_steps: Pasos a predecir
        
        Returns:
            Array con predicciones
        """
        
        predictions = []
        current_sequence = X_recent.copy()
        
        for step in range(num_steps):
            # Predecir siguiente paso
            X = current_sequence.reshape(1, self.sequence_length, 1)
            next_pred = model.predict(X, verbose=0)[0][0]
            predictions.append(next_pred)
            
            # Actualizar secuencia (usar predicción como nuevo input)
            current_sequence = np.append(current_sequence[1:], next_pred)
        
        return np.array(predictions)
    
    def forecast_ensemble(self,
                         models: List,
                         X_recent: np.ndarray,
                         num_steps: int = 7,
                         method: str = 'mean') -> np.ndarray:
        """
        Predicción con ENSEMBLE de múltiples modelos
        
        Args:
            models: Lista de modelos entrenados
            X_recent: Secuencia reciente
            num_steps: Pasos a predecir
            method: 'mean', 'median', o 'weighted'
        
        Returns:
            Predicción promediada
        """
        
        all_predictions = []
        
        for model in models:
            pred = self.forecast_recursive(model, X_recent, num_steps)
            all_predictions.append(pred)
        
        all_predictions = np.array(all_predictions)
        
        if method == 'mean':
            return np.mean(all_predictions, axis=0)
        elif method == 'median':
            return np.median(all_predictions, axis=0)
        elif method == 'weighted':
            # Pesos según confianza (ejemplo)
            weights = np.array([1.0, 0.8, 0.6]) / 2.4
            return np.average(all_predictions, axis=0, weights=weights[:len(models)])
    
    def calculate_prediction_intervals(self,
                                      predictions: np.ndarray,
                                      residuals: np.ndarray,
                                      confidence: float = 0.95) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula intervalos de confianza para predicciones
        
        Args:
            predictions: Predicciones punto
            residuals: Residuos históricos
            confidence: Nivel de confianza (0.95 = 95%)
        
        Returns:
            lower_bound, upper_bound
        """
        
        from scipy import stats
        
        # Desviación estándar de residuos
        std_residuals = np.std(residuals)
        
        # Z-score para nivel de confianza
        z_score = stats.norm.ppf((1 + confidence) / 2)
        
        # Intervalos
        margin = z_score * std_residuals
        
        lower = predictions - margin
        upper = predictions + margin
        
        return lower, upper
    
    def evaluate_performance(self,
                            y_true: np.ndarray,
                            y_pred: np.ndarray) -> dict:
        """
        Evalúa rendimiento de predicción multi-paso
        
        Args:
            y_true: Valores reales (n_samples, num_steps)
            y_pred: Predicciones (n_samples, num_steps)
        
        Returns:
            Diccionario con métricas
        """
        
        from sklearn.metrics import mean_absolute_error, mean_squared_error
        
        mae_overall = mean_absolute_error(y_true, y_pred)
        rmse_overall = np.sqrt(mean_squared_error(y_true, y_pred))
        
        # MAE por paso
        mae_per_step = [
            mean_absolute_error(y_true[:, i], y_pred[:, i])
            for i in range(y_true.shape[1])
        ]
        
        # RMSE por paso
        rmse_per_step = [
            np.sqrt(mean_squared_error(y_true[:, i], y_pred[:, i]))
            for i in range(y_true.shape[1])
        ]
        
        return {
            'mae_overall': mae_overall,
            'rmse_overall': rmse_overall,
            'mae_per_step': mae_per_step,
            'rmse_per_step': rmse_per_step
        }


# Ejemplo de uso
if __name__ == '__main__':
    print("\n🔮 PREDICCIÓN MULTI-PASO")
    print("="*60)
    
    # Datos sintéticos
    from src.data_loader import SeismicDataLoader
    
    loader = SeismicDataLoader()
    data = loader.generate_sample_data(days=365)
    normalized = loader.normalize_features(data.copy())
    magnitudes = normalized['magnitude'].values
    
    # Preparar datos
    print("\n📊 Preparando datos...")
    forecaster = MultiStepForecaster()
    X, y = forecaster.prepare_multistep_data(magnitudes, sequence_length=30, num_steps=7)
    
    print(f"✓ X shape: {X.shape}")
    print(f"✓ y shape: {y.shape}\n")
    
    # Split train/test
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Entrenar modelo
    print("🧠 Entrenando modelo multi-paso...")
    model = forecaster.create_multistep_model((30, 1), num_steps=7)
    model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test), verbose=0)
    print("✓ Modelo entrenado\n")
    
    # Predicción
    print("🔮 Haciendo predicción para próximos 7 días...")
    X_recent = X_test[-1]
    predictions = forecaster.forecast_direct(model, X_recent, num_steps=7)
    actual = y_test[-1]
    
    print("\nDía | Predicción | Real  | Error")
    print("-" * 40)
    for i, (pred, real) in enumerate(zip(predictions, actual), 1):
        error = abs(pred - real)
        print(f"{i:3} | {pred:10.4f} | {real:5.4f} | {error:5.4f}")
    
    # Intervalo de confianza
    residuals = y_test.reshape(-1) - model.predict(X_test, verbose=0).reshape(-1)
    lower, upper = forecaster.calculate_prediction_intervals(predictions, residuals)
    
    print("\nIntervalos de confianza (95%):")
    for i, (l, u) in enumerate(zip(lower, upper), 1):
        print(f"Día {i}: [{l:.4f}, {u:.4f}]")
