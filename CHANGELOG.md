# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/es/).

---

## [1.2.0] - 2026-04-05

### 🎉 Nuevas Características Principales

#### 📧 Sistema de Alertas por Email
- Interface `EmailAlert` para enviar notificaciones automáticas
- Alertas HTML personalizadas para anomalías detectadas
- Reportes periódicos con estadísticas
- Soporte para Gmail SMTP
- Variables de entorno para credenciales seguras

#### 🔮 Forecasting Avanzado
- Módulo `SeismicForecasting` con múltiples métodos
- **Prophet** (Facebook) para series temporales
- **ARIMA** (statsmodels) para análisis temporal
- Comparación automática de modelos
- Intervalos de confianza configurable

#### 💾 Base de Datos SQLite
- Módulo `SeismicDatabase` para persistencia
- Almacenamiento de eventos, predicciones y métricas
- Tablas normalizadas (events, predictions, metrics)
- Exportación a JSON
- Estadísticas agregadas

#### 📊 Análisis Estadístico Avanzado
- Módulo `SeismicStatistics` con análisis profundo
- **Relación Gutenberg-Richter** (parámetros a y b)
- **Análisis temporal** de intervalos entre eventos
- **Detección de clusters** automática
- **Test de normalidad** Shapiro-Wilk
- **Correlaciones** Pearson y Spearman

#### 🗺️ Mapas Interactivos
- Módulo `SeismicMap` con Folium
- Mapa base del volcán Deception con zona de monitoreo
- Visualización de eventos con color según magnitud
- **Heatmap** de intensidad sísmica
- **Clustering** automático de eventos
- Integración total con Streamlit

#### 🖥️ CLI Mejorado
- Nuevo archivo `cli.py` con Click framework
- 9 comandos principales:
  - `generate-data`: Generar datos sintéticos
  - `train-models`: Entrenar LSTM + Anomaly Detector
  - `predict`: Predicción interactiva
  - `analyze`: Análisis estadístico
  - `status`: Estado del sistema
  - `test-alert`: Probar alertas por email
  - `export-data`: Exportar en múltiples formatos
  - `test-system`: Prueba completa
  - `version`: Información de versión
- Colores ANSI para mejor legibilidad
- Validación automática de inputs

#### ✅ Unit Tests Completos
- Archivo `tests/test_seismic.py` con pytest
- Cobertura de:
  - Data loader y generación
  - Normalización de features
  - Modelos LSTM y Anomaly Detector
  - Statistiques y análisis
  - Validación de datos
- Ejecutar: `python -m pytest tests/test_seismic.py -v --cov`

#### 🐳 Docker Compose Setup
- `docker-compose.yml` con 4 servicios:
  - Dashboard Streamlit (puerto 8501)
  - API FastAPI (puerto 8000)
  - PostgreSQL opcional (puerto 5432)
  - Jupyter Notebook (puerto 8888)
- `Dockerfile` optimizado con Python 3.11
- Script `docker-compose-up.sh` con instrucciones

#### 🔄 GitHub Actions CI/CD
- Workflow `.github/workflows/tests.yml` automático
- Tests en Python 3.10 y 3.11
- Validación con Black, isort, flake8
- Análisis de seguridad con Bandit
- Reporte de cobertura a Codecov
- Build automático de Docker image

#### 📝 Documentación Ampliada
- **FEATURES.md**: Guía completa de nuevas funcionalidades
- **ADVANCED.md**: Casos de uso avanzados y troubleshooting
- **examples.py**: 6 ejemplos ejecutables
- **.env.example**: Template de variables de entorno
- **CHANGELOG.md**: Este archivo

### 📦 Dependencias Agregadas
```
prophet==1.1.5                  # Forecasting
statsmodels==0.14.0             # ARIMA
folium==0.14.0                  # Mapas
streamlit-folium==0.21.0        # Integración
click==8.1.7                    # CLI
tabulate==0.9.0                 # Tablas
plotly==5.17.0                  # Gráficas
psycopg2-binary==2.9.9          # PostgreSQL
sqlalchemy==2.0.23              # ORM
pytest==7.4.3                   # Testing
scipy==1.11.4                   # Cálculos
```

### 📊 Estadísticas de Cambios
- **Archivos nuevos**: 11
- **Líneas de código**: +2500
- **Módulos ampliados**: 3
- **Dependencias nuevas**: 12

### 🔧 Cambios Técnicos

#### Mejoras de Código
- Refactorización de data_loader para soporte real API
- Modularización de funcionalidades
- Mejor manejo de errores
- Type hints mejorados

#### Seguridad
- Variables de entorno para credenciales
- .env en .gitignore
- CORS configurables en API
- Validación de Pydantic mejorada

#### Performance
- Caché de datos en Streamlit
- Optimización de queries SQLite
- Lazy loading de modelos
- Batch processing en predicciones

### 🎓 Ejemplos y Tests
- `examples.py` con 6 casos de uso completos
- `tests/test_seismic.py` con 10+ tests
- Cobertura mínima 70%
- GitHub Actions automation

### 🚀 Despliegue
- Docker Compose para local
- Dockerfile optimizado
- Instrucciones Heroku
- Nginx reverse proxy config

### ⚡ Performance
- Predicción LSTM: ~50-100ms
- API REST: <200ms
- Análisis estadístico: ~1-5s
- Dashboard Streamlit: <2s load

---

## [1.1.0] - 2026-04-04

### ✨ Características
- Dashboard Streamlit con 4 páginas
- API REST con FastAPI (7 endpoints)
- Visualización con matplotlib/seaborn
- Modelo LSTM personalizado
- Detector de anomalías Isolation Forest

### 📊 Resultados del Modelo
- LSTM MAE: 0.1815
- RMSE: 0.2277
- Anomaly Detection Precision: 90%

---

## [1.0.0] - 2026-04-03

### 🎯 Versión Inicial
- Estructura base del proyecto
- Data loader con soporte sintético
- Archivos de configuración
- Scripts básicos setup.sh
- README.md y documentación inicial
- Publicación en GitHub

### 📁 Estructura Base
```
project/
├── src/          (7 módulos)
├── notebooks/    (Jupyter)
├── data/         (Datos)
├── models/       (Modelos entrenados)
└── config/       (Configuración)
```

---

## Convenciones de Versión

`X.Y.Z` donde:
- **X** (major): Cambios incompatibles / grandes features
- **Y** (minor): Nuevas características compatible
- **Z** (patch): Correcciones de bugs

## Cómo Reportar Problemas

Usa el tab de Issues en GitHub con template:
- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado
- Logs de error

## Próximas Versiones Planeadas

### [1.3.0] - Q2 2026
- [ ] Integración PostgreSQL completa
- [ ] Webhooks para notificaciones
- [ ] Multi-volcano support
- [ ] Gráficas 3D interactivas
- [ ] Mobile app

### [1.4.0] - Q3 2026
- [ ] Predicción multi-paso
- [ ] Sistema de alertas SMS
- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] Análisis de clustering avanzado

### [2.0.0] - Q4 2026
- [ ] Soporte para múltiples regiones volcánicas
- [ ] Integración de datos sísmicos en tiempo real
- [ ] Dashboard personalizable
- [ ] API GraphQL adicional
- [ ] Mobile app nativa

---

## Créditos y Contribuidores

- **Creador**: CamiOso (Cristian López)
- **Email**: cristian.1701421857@ucaldas.edu.co
- **Institución**: Universidad de Caldas

---

## Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles

---

**Última actualización**: 2026-04-05
**Versión actual**: 1.2.0
**Estado**: Estable ✅
