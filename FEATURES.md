# 🚀 Nuevas Funcionalidades - v1.2.0

## Resumen de Cambios

Este documento detalla todas las funcionalidades nuevas agregadas al Sistema de Análisis Sísmico.

---

## 1. 📧 Sistema de Alertas por Email

**Archivo:** `src/alerts.py`

### Características:
- ✅ Alertas automáticas por email cuando se detecten anomalías
- ✅ Reportes periódicos (diarios/semanales)
- ✅ Formato HTML personalizado
- ✅ Integración con Gmail SMTP

### Uso:
```python
from src.alerts import EmailAlert

alert = EmailAlert(
    sender_email="tu_email@gmail.com",
    password="tu_contraseña_app"
)

# Enviar alerta de anomalía
alert.send_anomaly_alert(
    recipient_email="destino@email.com",
    anomaly_data={
        'magnitude': 5.2,
        'depth': 30.5,
        'anomaly_score': 0.85,
        'risk_level': 'ALTO',
        'recommendation': 'Aumentar monitoreo'
    }
)

# Enviar reporte
alert.send_report(
    recipient_email="destino@email.com",
    report_data={
        'total_events': 25,
        'avg_magnitude': 4.2,
        'max_magnitude': 5.8,
        'anomalies': 3,
        'summary': 'Actividad normal con 3 anomalías detectadas'
    }
)
```

---

## 2. 🔮 Forecasting Avanzado

**Archivo:** `src/forecasting.py`

### Características:
- ✅ Predicciones con **Prophet** (Facebook)
- ✅ Predicciones con **ARIMA** (statsmodels)
- ✅ Comparación de métodos
- ✅ Intervalos de confianza

### Uso:
```python
from src.forecasting import SeismicForecasting

forecaster = SeismicForecasting()

# Prophet
prophet_result = forecaster.forecast_with_prophet(data, periods=30)

# ARIMA
arima_result = forecaster.forecast_with_arima(data, periods=30, order=(1,1,1))

# Comparar métodos
comparison = forecaster.compare_forecasts(data, test_size=10)
```

### Modelos Soportados:
| Modelo | Ventajas | Desventajas |
|--------|----------|------------|
| Prophet | Excelente con tendencias, maneja vacíos | Lento para datasets grandes |
| ARIMA | Rápido, clásico | Requiere datos estacionarios |
| LSTM | Aprende patrones complejos | Requiere muchos datos |

---

## 3. 💾 Base de Datos SQLite

**Archivo:** `src/database.py`

### Características:
- ✅ Almacenamiento persistente de eventos
- ✅ Registro de predicciones
- ✅ Métricas del modelo
- ✅ Exportación a JSON
- ✅ Estadísticas agregadas

### Tablas:
- **events**: Eventos sísmicos
- **predictions**: Predicciones realizadas
- **metrics**: Métricas de rendimiento

### Uso:
```python
from src.database import SeismicDatabase

db = SeismicDatabase()

# Guardar evento
db.add_event(magnitude=5.2, depth=30.5, anomaly_score=0.3, risk_level='MODERADO')

# Guardar predicción
db.add_prediction(
    predicted_magnitude=5.5,
    anomaly_score=0.4,
    risk_level='MODERADO',
    confidence=0.95,
    model_name='LSTM'
)

# Obtener estadísticas
stats = db.get_statistics()

# Exportar datos
db.export_to_json('export.json')
```

---

## 4. 📊 Análisis Estadístico Avanzado

**Archivo:** `src/statistics.py`

### Características:
- ✅ **Relación Gutenberg-Richter** (log10(N) = a - b*M)
- ✅ **Análisis temporal** de intervalos
- ✅ **Distribución de magnitudes** (Skewness, Kurtosis)
- ✅ **Correlación** profundidad-magnitud
- ✅ **Detección de clusters** de eventos

### Métricas Calculadas:
- Media, mediana, desviación estándar
- Asimetría (Skewness)
- Curtosis (Kurtosis)
- Test de normalidad Shapiro-Wilk
- Correlación Pearson y Spearman
- b-value sísmico

### Uso:
```python
from src.statistics import SeismicStatistics

stats = SeismicStatistics(data)

# Distribución
dist = stats.calculate_magnitude_distribution()

# Gutenberg-Richter
gr = stats.calculate_gutenberg_richter()

# Clusters
clusters = stats.detect_clusters(magnitude_threshold=4.0, days_window=7)

# Resumen completo
stats.print_summary()
```

---

## 5. 🗺️ Mapas Interactivos

**Archivo:** `src/maps.py`

### Características:
- ✅ Mapa base del volcán Deception
- ✅ Visualización de eventos sísmicos
- ✅ **Heatmap** de intensidad
- ✅ **Clustering** de puntos
- ✅ Integración con Streamlit

### Tipos de Mapas:
1. **Main Map**: Mapa base con zona de monitoreo
2. **Events Map**: Puntos de eventos con color por magnitud
3. **Heatmap**: Distribución de densidad
4. **Cluster Map**: Agrupación automática de eventos

### Uso en Streamlit:
```python
from src.maps import SeismicMap
import streamlit as st

seismic_map = SeismicMap(data)

# Mapa de eventos
map_events = seismic_map.create_events_map()
st.folium_static(map_events)

# Heatmap
map_heat = seismic_map.create_heatmap()
st.folium_static(map_heat)

# Clustered
map_cluster = seismic_map.create_cluster_map()
st.folium_static(map_cluster)
```

---

## 6. ✅ Unit Tests

**Archivo:** `tests/test_seismic.py`

### Cobertura:
- ✅ Tests para Data Loader
- ✅ Tests para Modelos ML
- ✅ Tests para Estadísticas
- ✅ Tests de validación de datos

### Ejecutar:
```bash
# Todos los tests
python -m pytest tests/test_seismic.py -v

# Con cobertura
python -m pytest tests/test_seismic.py --cov=src

# Test específico
python -m pytest tests/test_seismic.py::TestSeismicDataLoader::test_generate_sample_data -v
```

### Cobertura de Pruebas:
- Data generation and normalization
- LSTM model creation and training
- Anomaly detection
- Sequence creation
- Statistics calculations
- Data integrity

---

## 7. 🖥️ CLI Mejorado

**Archivo:** `cli.py`

### Nuevos Comandos:
```bash
# Generar datos
python cli.py generate-data --days 365

# Entrenar modelos
python cli.py train-models

# Hacer predicción
python cli.py predict --magnitude 5.0 --depth 30

# Análisis estadístico
python cli.py analyze --days 30

# Estado del sistema
python cli.py status

# Probar alertas
python cli.py test-alert --email tu@email.com --magnitude 5.2

# Exportar datos
python cli.py export-data --format json

# Prueba completa
python cli.py test-system

# Versión
python cli.py version
```

### Características:
- Colores ANSI para mejor legibilidad
- Validación de inputs
- Mensajes de error descriptivos
- Progreso visual

---

## 8. 🐳 Docker Compose Setup

**Archivos:** 
- `docker-compose.yml`
- `Dockerfile`
- `docker-compose-up.sh`

### Servicios:
```yaml
dashboard:   # Streamlit en 8501
api:         # FastAPI en 8000
postgres:    # PostgreSQL en 5432 (opcional)
jupyter:     # Jupyter en 8888
```

### Uso:
```bash
# Iniciar todos los servicios
bash docker-compose-up.sh

# Ver logs
docker-compose logs -f dashboard

# Detener
docker-compose down

# Rebuilder
docker-compose build --no-cache
```

### Ventajas:
- ✅ Ambiente completamente containerizado
- ✅ No requiere instalación local
- ✅ Reproducible en cualquier máquina
- ✅ Escalable a producción

---

## 9. 🔄 GitHub Actions CI/CD

**Archivo:** `.github/workflows/tests.yml`

### Validaciones Automáticas:
- ✅ **Tests unitarios** en Python 3.10 y 3.11
- ✅ **Linting** con Black, isort
- ✅ **Análisis de seguridad** con Bandit
- ✅ **Cobertura de tests**
- ✅ **Build Docker** automático

### Triggers:
- Push a `main` o `develop`
- Pull requests

### Reportes:
- Codecov coverage reports
- Security scans
- Test results

---

## 10. 📝 Cambios en Dependencias

**Archivo:** `requirements.txt`

### Nuevos Paquetes:
```
prophet==1.1.5              # Forecasting
statsmodels==0.14.0         # Time series
folium==0.14.0              # Mapas interactivos
streamlit-folium==0.21.0    # Integración Streamlit-Folium
click==8.1.7                # CLI elegante
tabulate==0.9.0             # Tablas en terminal
plotly==5.17.0              # Gráficas interactivas
psycopg2-binary==2.9.9      # PostgreSQL
sqlalchemy==2.0.23          # ORM
pytest==7.4.3               # Testing
scipy==1.11.4               # Cálculos científicos
```

---

## 📊 Estadísticas de Cambios

### Archivos Nuevos: 11
```
src/alerts.py
src/forecasting.py
src/database.py
src/statistics.py
src/maps.py
cli.py
tests/test_seismic.py
docker-compose.yml
Dockerfile
docker-compose-up.sh
.github/workflows/tests.yml
```

### Líneas de Código Nuevas: ~2500

### Dependencias Añadidas: 12

---

## 🎯 Próximas Mejoras (v1.3.0)

- [ ] Integración con base de datos PostgreSQL
- [ ] Webhooks para notificaciones
- [ ] Soporte para múltiples volcanes
- [ ] API de machine learning personalizado
- [ ] Gráficas 3D interactivas
- [ ] Mobile app
- [ ] Predicción multi-paso
- [ ] Sistema de alertas SMS
- [ ] Integración con plataformas en la nube
- [ ] Dashboard avanzado con Plotly Dash

---

## 🤝 Contribuir

Para sugerir nuevas funcionalidades:
1. Abre un Issue con etiqueta `enhancement`
2. Describe la funcionalidad deseada
3. Proporciona casos de uso

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

**Última actualización:** Abril 2026
**Versión:** 1.2.0
