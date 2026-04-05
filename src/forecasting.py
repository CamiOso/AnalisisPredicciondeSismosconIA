"""
Forecasting avanzado con Prophet y ARIMA
"""
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

try:
    from statsmodels.tsa.arima.model import ARIMA
    ARIMA_AVAILABLE = True
except ImportError:
    ARIMA_AVAILABLE = False

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False


class SeismicForecasting:
    """Forecasting de series temporales sísmicas"""
    
    def __init__(self):
        self.prophet_model = None
        self.arima_model = None
    
    def forecast_with_prophet(self, data: pd.DataFrame, periods: int = 30):
        """Pronostica con Prophet (FB)"""
        
        if not PROPHET_AVAILABLE:
            print("⚠️  Prophet no instalado. pip install prophet")
            return None
        
        try:
            # Preparar datos
            forecast_data = data[['time', 'magnitude']].rename(
                columns={'time': 'ds', 'magnitude': 'y'}
            )
            forecast_data['ds'] = pd.to_datetime(forecast_data['ds'])
            
            # Crear modelo
            print("🔮 Entrenando modelo Prophet...")
            self.prophet_model = Prophet(yearly_seasonality=False, daily_seasonality=False)
            self.prophet_model.fit(forecast_data)
            
            # Hacer predicción
            future = self.prophet_model.make_future_dataframe(periods=periods)
            forecast = self.prophet_model.predict(future)
            
            print(f"✓ Pronóstico generado para {periods} días")
            
            return {
                'forecast': forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
                'model': self.prophet_model
            }
        
        except Exception as e:
            print(f"✗ Error en Prophet: {str(e)}")
            return None
    
    def forecast_with_arima(self, data: pd.DataFrame, periods: int = 30, order: tuple = (1, 1, 1)):
        """Pronostica con ARIMA"""
        
        if not ARIMA_AVAILABLE:
            print("⚠️  ARIMA no instalado. pip install statsmodels")
            return None
        
        try:
            magnitudes = data['magnitude'].values
            
            print("🔮 Entrenando modelo ARIMA...")
            self.arima_model = ARIMA(magnitudes, order=order)
            results = self.arima_model.fit()
            
            # Hacer predicción
            forecast = results.get_forecast(steps=periods)
            forecast_df = forecast.conf_int(alpha=0.05)
            forecast_df['forecast'] = forecast.predicted_mean
            
            print(f"✓ Pronóstico ARIMA generado para {periods} días")
            
            return {
                'forecast': forecast_df,
                'summary': results.summary()
            }
        
        except Exception as e:
            print(f"✗ Error en ARIMA: {str(e)}")
            return None
    
    def compare_forecasts(self, data: pd.DataFrame, test_size: int = 10):
        """Compara diferentes métodos de pronóstico"""
        
        print("\n📊 Comparando métodos de pronóstico...")
        
        # Dividir datos
        train_data = data[:-test_size]
        test_data = data[-test_size:]
        actual_values = test_data['magnitude'].values
        
        results = {}
        
        # Prophet
        if PROPHET_AVAILABLE:
            prophet_pred = self.forecast_with_prophet(train_data, periods=test_size)
            if prophet_pred:
                y_pred = prophet_pred['forecast']['yhat'].values[-test_size:]
                mae = mean_absolute_error(actual_values, y_pred)
                rmse = np.sqrt(mean_squared_error(actual_values, y_pred))
                results['Prophet'] = {'MAE': mae, 'RMSE': rmse}
                print(f"  Prophet - MAE: {mae:.4f}, RMSE: {rmse:.4f}")
        
        # ARIMA
        if ARIMA_AVAILABLE:
            arima_pred = self.forecast_with_arima(train_data, periods=test_size)
            if arima_pred:
                y_pred = arima_pred['forecast']['forecast'].values
                mae = mean_absolute_error(actual_values, y_pred)
                rmse = np.sqrt(mean_squared_error(actual_values, y_pred))
                results['ARIMA'] = {'MAE': mae, 'RMSE': rmse}
                print(f"  ARIMA - MAE: {mae:.4f}, RMSE: {rmse:.4f}")
        
        return results
