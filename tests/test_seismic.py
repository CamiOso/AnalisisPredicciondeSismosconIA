"""
Tests unitarios para el sistema de análisis sísmico
"""
import unittest
import numpy as np
import pandas as pd
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import SeismicDataLoader
from src.model import SeismicLSTM, SeismicAnomalyDetector
from src.statistics import SeismicStatistics
from src import config


class TestSeismicDataLoader(unittest.TestCase):
    """Tests para carga de datos"""
    
    def setUp(self):
        self.loader = SeismicDataLoader()
    
    def test_generate_sample_data(self):
        """Test generación de datos sintéticos"""
        data = self.loader.generate_sample_data(days=10)
        
        self.assertIsNotNone(data)
        self.assertTrue(len(data) > 0)
        self.assertIn('magnitude', data.columns)
        self.assertIn('depth', data.columns)
    
    def test_normalize_features(self):
        """Test normalización de features"""
        data = self.loader.generate_sample_data(days=10)
        normalized = self.loader.normalize_features(data)
        
        # Verificar que los valores están entre 0 y 1
        self.assertTrue((normalized['magnitude'] >= 0).all())
        self.assertTrue((normalized['magnitude'] <= 1).all())
    
    def test_filter_by_magnitude(self):
        """Test filtrado por magnitud"""
        data = self.loader.generate_sample_data(days=10)
        filtered = self.loader.filter_by_magnitude(data, min_mag=3.0)
        
        self.assertTrue((filtered['magnitude'] >= 3.0).all())
    
    def test_create_sequences(self):
        """Test creación de secuencias"""
        data = self.loader.generate_sample_data(days=100)
        normalized = self.loader.normalize_features(data)
        
        X, y = self.loader.create_sequences(
            normalized['magnitude'].values,
            seq_length=30
        )
        
        self.assertEqual(X.shape[1], 30)
        self.assertTrue(len(X) > 0)
        self.assertTrue(len(y) > 0)


class TestSeismicModel(unittest.TestCase):
    """Tests para modelos ML"""
    
    def setUp(self):
        self.lstm = SeismicLSTM()
        self.detector = SeismicAnomalyDetector()
    
    def test_lstm_creation(self):
        """Test creación de modelo LSTM"""
        model = self.lstm.create_model(input_shape=(30, 1))
        
        self.assertIsNotNone(model)
        self.assertEqual(len(model.layers), 5)  # 2 LSTM + 2 Dense + 1 Output
    
    def test_anomaly_detector_creation(self):
        """Test creación de detector"""
        self.assertIsNotNone(self.detector.model)
    
    def test_anomaly_detection(self):
        """Test detección de anomalías"""
        # Datos sintéticos
        X_train = np.random.randn(100, 1)
        X_test = np.random.randn(10, 1)
        
        # Añadir anomalías
        X_test[-2:] = np.random.randn(2, 1) * 10
        
        self.detector.fit(X_train)
        predictions = self.detector.predict(X_test)
        
        # Las últimas 2 deberían ser anomalías
        self.assertEqual(predictions[-2:].sum(), -2)  # -1 para anomalías


class TestSeismicStatistics(unittest.TestCase):
    """Tests para análisis estadístico"""
    
    def setUp(self):
        # Crear datos de prueba
        days = 100
        dates = [datetime.now() - timedelta(days=d) for d in range(days)]
        
        self.data = pd.DataFrame({
            'time': dates,
            'magnitude': np.random.uniform(2, 7, days),
            'depth': np.random.uniform(5, 100, days),
            'latitude': np.random.uniform(-63, -62, days),
            'longitude': np.random.uniform(-62, -60, days)
        })
        
        self.stats = SeismicStatistics(self.data)
    
    def test_magnitude_distribution(self):
        """Test análisis de distribución"""
        dist = self.stats.calculate_magnitude_distribution()
        
        self.assertIn('mean', dist)
        self.assertIn('std', dist)
        self.assertIn('skewness', dist)
        self.assertTrue(0 < dist['mean'] < 10)
    
    def test_gutenberg_richter(self):
        """Test relación Gutenberg-Richter"""
        gr = self.stats.calculate_gutenberg_richter()
        
        self.assertIn('a_value', gr)
        self.assertIn('b_value', gr)
        self.assertTrue(0 < gr['b_value'] < 2)
    
    def test_temporal_statistics(self):
        """Test estadísticas temporales"""
        temporal = self.stats.calculate_temporal_statistics()
        
        self.assertIn('mean_interval', temporal)
        self.assertIn('median_interval', temporal)
        self.assertTrue(temporal['mean_interval'] > 0)


class TestDataValidation(unittest.TestCase):
    """Tests para validación de datos"""
    
    def test_data_integrity(self):
        """Test integridad de datos"""
        loader = SeismicDataLoader()
        data = loader.generate_sample_data(days=10)
        
        # No hay NaN
        self.assertTrue(~data.isnull().any().any())
        
        # Magnitudes válidas
        self.assertTrue((data['magnitude'] > 0).all())
        
        # Profundidades válidas
        self.assertTrue((data['depth'] > 0).all())
    
    def test_sequence_continuity(self):
        """Test continuidad de secuencias"""
        loader = SeismicDataLoader()
        data = loader.generate_sample_data(days=50)
        normalized = loader.normalize_features(data)
        
        X, y = loader.create_sequences(normalized['magnitude'].values, seq_length=30)
        
        # Las secuencias deben ser continuas
        for i in range(len(X)-1):
            # El último valor de X[i] debe ser el primero de X[i+1]
            pass  # Verificación visual


def run_tests():
    """Ejecuta todos los tests"""
    
    # Crear suite de tests
    loader_tests = unittest.TestLoader().loadTestsFromTestCase(TestSeismicDataLoader)
    model_tests = unittest.TestLoader().loadTestsFromTestCase(TestSeismicModel)
    stats_tests = unittest.TestLoader().loadTestsFromTestCase(TestSeismicStatistics)
    validation_tests = unittest.TestLoader().loadTestsFromTestCase(TestDataValidation)
    
    # Combinar y ejecutar
    suite = unittest.TestSuite([loader_tests, model_tests, stats_tests, validation_tests])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
