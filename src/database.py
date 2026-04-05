"""
Base de datos SQLite para logging de predicciones
"""
import sqlite3
from datetime import datetime
import json
import os

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class SeismicDatabase:
    """Base de datos para almacenar predicciones y eventos"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.join(config.DATA_DIR, 'seismic.db')
        self._init_db()
    
    def _init_db(self):
        """Inicializa la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de eventos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                magnitude REAL,
                depth REAL,
                latitude REAL,
                longitude REAL,
                anomaly_score REAL,
                risk_level TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de predicciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                predicted_magnitude REAL,
                anomaly_score REAL,
                risk_level TEXT,
                confidence REAL,
                model_name TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de métricas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT,
                metric_value REAL,
                model_name TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✓ Base de datos inicializada en {self.db_path}")
    
    def add_event(self, magnitude: float, depth: float, latitude: float = None, 
                  longitude: float = None, anomaly_score: float = None, risk_level: str = None):
        """Guarda un evento sísmico"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO events (timestamp, magnitude, depth, latitude, longitude, anomaly_score, risk_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.now(), magnitude, depth, latitude, longitude, anomaly_score, risk_level))
        
        conn.commit()
        event_id = cursor.lastrowid
        conn.close()
        
        return event_id
    
    def add_prediction(self, predicted_magnitude: float, anomaly_score: float, 
                       risk_level: str, confidence: float, model_name: str = "LSTM"):
        """Guarda una predicción"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (predicted_magnitude, anomaly_score, risk_level, confidence, model_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (predicted_magnitude, anomaly_score, risk_level, confidence, model_name))
        
        conn.commit()
        pred_id = cursor.lastrowid
        conn.close()
        
        return pred_id
    
    def add_metric(self, metric_name: str, metric_value: float, model_name: str = None):
        """Guarda una métrica del modelo"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO metrics (metric_name, metric_value, model_name)
            VALUES (?, ?, ?)
        ''', (metric_name, metric_value, model_name))
        
        conn.commit()
        metric_id = cursor.lastrowid
        conn.close()
        
        return metric_id
    
    def get_recent_events(self, limit: int = 10):
        """Obtiene eventos recientes"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM events ORDER BY created_at DESC LIMIT ?
        ''', (limit,))
        
        events = cursor.fetchall()
        conn.close()
        
        return events
    
    def get_recent_predictions(self, limit: int = 10):
        """Obtiene predicciones recientes"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM predictions ORDER BY created_at DESC LIMIT ?
        ''', (limit,))
        
        predictions = cursor.fetchall()
        conn.close()
        
        return predictions
    
    def get_model_metrics(self, model_name: str = None):
        """Obtiene métricas del modelo"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if model_name:
            cursor.execute('''
                SELECT metric_name, AVG(metric_value) as avg_value 
                FROM metrics 
                WHERE model_name = ? 
                GROUP BY metric_name
            ''', (model_name,))
        else:
            cursor.execute('''
                SELECT metric_name, AVG(metric_value) as avg_value 
                FROM metrics 
                GROUP BY metric_name
            ''')
        
        metrics = cursor.fetchall()
        conn.close()
        
        return metrics
    
    def export_to_json(self, filepath: str):
        """Exporta datos a JSON"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Eventos
        cursor.execute('SELECT * FROM events')
        events = cursor.fetchall()
        
        # Predicciones
        cursor.execute('SELECT * FROM predictions')
        predictions = cursor.fetchall()
        
        data = {
            'events': [dict(e) for e in events],
            'predictions': [dict(p) for p in predictions]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        conn.close()
        print(f"✓ Datos exportados a {filepath}")
    
    def get_statistics(self):
        """Obtiene estadísticas generales"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM events')
        total_events = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(magnitude), MAX(magnitude), MIN(magnitude) FROM events')
        mag_stats = cursor.fetchone()
        
        cursor.execute('SELECT AVG(depth) FROM events')
        avg_depth = cursor.fetchone()[0]
        
        stats = {
            'total_events': total_events,
            'avg_magnitude': mag_stats[0],
            'max_magnitude': mag_stats[1],
            'min_magnitude': mag_stats[2],
            'avg_depth': avg_depth
        }
        
        conn.close()
        return stats
