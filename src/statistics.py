"""
Análisis estadístico avanzado de datos sísmicos
"""
import numpy as np
import pandas as pd
from scipy import stats
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SeismicStatistics:
    """Análisis estadístico avanzado"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def calculate_gutenberg_richter(self):
        """Calcula la relación Gutenberg-Richter (log10(N) = a - b*M)"""
        
        magnitudes = sorted(self.data['magnitude'].values, reverse=True)
        
        # Contar eventos >= cada magnitud
        unique_mags = np.unique(magnitudes)
        cumulative_count = [len([m for m in magnitudes if m >= mag]) for mag in unique_mags]
        
        # Ajuste lineal en escala log
        log_count = np.log10(np.array(cumulative_count) + 1)
        
        # Calcular parámetros
        slope, intercept = np.polyfit(unique_mags, log_count, 1)
        
        # b-value (pendiente negativa)
        b_value = -slope
        a_value = intercept
        
        return {
            'a_value': a_value,
            'b_value': b_value,
            'magnitudes': unique_mags,
            'cumulative_count': cumulative_count
        }
    
    def calculate_temporal_statistics(self):
        """Estadísticas temporales (intervalos entre eventos)"""
        
        self.data = self.data.sort_values('time')
        times = pd.to_datetime(self.data['time'])
        
        # Calcular intervalos
        intervals = times.diff().dt.total_seconds() / 86400  # en días
        intervals = intervals.dropna()
        
        return {
            'mean_interval': intervals.mean(),
            'median_interval': intervals.median(),
            'std_interval': intervals.std(),
            'min_interval': intervals.min(),
            'max_interval': intervals.max(),
            'intervals': intervals.values
        }
    
    def calculate_magnitude_distribution(self):
        """Análisis de distribución de magnitudes"""
        
        magnitudes = self.data['magnitude'].values
        
        # Tests de normalidad
        shapiro_stat, shapiro_p = stats.shapiro(magnitudes)
        
        # Kurtosis y Skewness
        kurtosis = stats.kurtosis(magnitudes)
        skewness = stats.skew(magnitudes)
        
        return {
            'mean': magnitudes.mean(),
            'median': np.median(magnitudes),
            'std': magnitudes.std(),
            'kurtosis': kurtosis,
            'skewness': skewness,
            'shapiro_statistic': shapiro_stat,
            'shapiro_pvalue': shapiro_p,
            'is_normal': shapiro_p > 0.05
        }
    
    def calculate_depth_magnitude_correlation(self):
        """Correlación entre profundidad y magnitud"""
        
        if 'depth' not in self.data.columns:
            return None
        
        # Pearson correlation
        pearson_r, pearson_p = stats.pearsonr(
            self.data['magnitude'].values, 
            self.data['depth'].values
        )
        
        # Spearman correlation
        spearman_r, spearman_p = stats.spearmanr(
            self.data['magnitude'].values, 
            self.data['depth'].values
        )
        
        return {
            'pearson_r': pearson_r,
            'pearson_pvalue': pearson_p,
            'spearman_r': spearman_r,
            'spearman_pvalue': spearman_p
        }
    
    def detect_clusters(self, magnitude_threshold: float = 4.0, days_window: int = 7):
        """Detecta clusters de eventos sísmicos"""
        
        strong_events = self.data[self.data['magnitude'] >= magnitude_threshold].copy()
        strong_events['time'] = pd.to_datetime(strong_events['time'])
        strong_events = strong_events.sort_values('time')
        
        clusters = []
        current_cluster = []
        
        for idx, row in strong_events.iterrows():
            if not current_cluster:
                current_cluster = [row]
            else:
                time_diff = (row['time'] - current_cluster[-1]['time']).days
                
                if time_diff <= days_window:
                    current_cluster.append(row)
                else:
                    if len(current_cluster) > 1:
                        clusters.append(current_cluster)
                    current_cluster = [row]
        
        if len(current_cluster) > 1:
            clusters.append(current_cluster)
        
        return {
            'num_clusters': len(clusters),
            'clusters': clusters,
            'avg_cluster_size': np.mean([len(c) for c in clusters]) if clusters else 0
        }
    
    def print_summary(self):
        """Imprime resumen de análisis"""
        
        print("\n" + "="*70)
        print("📊 ANÁLISIS ESTADÍSTICO SÍSMICO")
        print("="*70)
        
        # Distribución de magnitudes
        mag_dist = self.calculate_magnitude_distribution()
        print("\n📈 Distribución de Magnitudes:")
        print(f"  Media: {mag_dist['mean']:.2f}")
        print(f"  Mediana: {mag_dist['median']:.2f}")
        print(f"  Desv. Est.: {mag_dist['std']:.2f}")
        print(f"  Asimetría: {mag_dist['skewness']:.2f}")
        print(f"  Curtosis: {mag_dist['kurtosis']:.2f}")
        print(f"  ¿Distribución Normal?: {'Sí' if mag_dist['is_normal'] else 'No'}")
        
        # Gutenberg-Richter
        gr = self.calculate_gutenberg_richter()
        print(f"\n📐 Relation Gutenberg-Richter:")
        print(f"  a-value: {gr['a_value']:.2f}")
        print(f"  b-value: {gr['b_value']:.2f}")
        
        # Temporal
        temporal = self.calculate_temporal_statistics()
        print(f"\n⏱️  Estadísticas Temporales:")
        print(f"  Intervalo medio: {temporal['mean_interval']:.1f} días")
        print(f"  Intervalo mediano: {temporal['median_interval']:.1f} días")
        print(f"  Intervalo máximo: {temporal['max_interval']:.1f} días")
        
        # Correlacion
        if 'depth' in self.data.columns:
            corr = self.calculate_depth_magnitude_correlation()
            print(f"\n🔗 Correlación Magnitud-Profundidad:")
            print(f"  Pearson r: {corr['pearson_r']:.3f} (p={corr['pearson_pvalue']:.3f})")
            print(f"  Spearman r: {corr['spearman_r']:.3f} (p={corr['spearman_pvalue']:.3f})")
        
        # Clusters
        clusters = self.detect_clusters()
        print(f"\n🎯 Clusters Detectados:")
        print(f"  Número de clusters: {clusters['num_clusters']}")
        print(f"  Tamaño promedio: {clusters['avg_cluster_size']:.1f} eventos")
        
        print("\n" + "="*70 + "\n")
