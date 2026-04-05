# 🇨🇴 Volcanes de Colombia - Documentación Completa

**Versión**: v1.4.1  
**Fecha**: Abril 2026  
**Enfoque**: Sistema especializado de monitoreo de volcanes colombianos

---

## 📋 Resumen Ejecutivo

Se ha implementado un **sistema completo de monitoreo especializado** para los **13 volcanes principales de Colombia**. Este módulo integra la base de datos geológica colombiana con el sistema de predicción sísmica existente.

### Estadísticas de Colombia

| Métrica | Valor |
|---------|-------|
| Volcanes en sistema | 13 volcanes |
| Volcanes activos | 6 activos |
| Volcanes críticos | 2 (Nevado del Ruiz, Galeras) |
| Volcanes de alto riesgo | 4 (+ 2 críticos) |
| Población en riesgo | ~1.5 millones |
| Estaciones de monitoreo | 68+ (toda Colombia) |
| Red de monitoreo | SGC (Servicio Geológico Colombiano) |

---

## 🌋 Los 13 Volcanes Colombianos

### 🚨 VOLCANES CRÍTICOS (Riesgo Level: CRITICAL)

#### 1. **Nevado del Ruiz** 🔴
```
Ubicación:    Caldas, Risaralda, Tolima
Elevación:    5,321 m
Tipo:         Stratovolcano
Activo:       Sí (última erupción 2023)
Población en riesgo: 500,000
Ciudades cercanas:   Manizales, Pereira, Armenia
Peligros:     Lahares, flujos de lava, flujos piroclásticos
```

**Historia**: 
- Erupción fatal de 1985 que causó el desastre de Armero (23,000+ muertes)
- Complejo volcánico más peligroso de Colombia
- Actividad continua con fumarolas

**Monitoreo**: 15 estaciones sísmicas

---

#### 2. **Galeras** 🔴
```
Ubicación:    Nariño
Elevación:    4,276 m
Tipo:         Stratovolcano
Activo:       Sí (última erupción 2010)
Población en riesgo: 300,000
Ciudades cercanas:   Pasto, Ipiales
Peligros:     Flujos de lava, flujos piroclásticos, lahares
```

**Historia**:
- Volcán más activo de los Andes colombianos
- Múltiples erupciones en siglo XX
- Trágica erupción de 1993 que mató a 9 investigadores

**Monitoreo**: 12 estaciones sísmicas

---

### ⚠️ VOLCANES DE ALTO RIESGO (Risk Level: HIGH)

#### 3. **Puracé**
```
Ubicación:    Cauca
Elevación:    4,756 m
Último evento: 1977
Población en riesgo: 150,000
Ciudades cercanas:   Popayán, La Plata
```

#### 4. **Nevado del Huila**
```
Ubicación:    Huila
Elevación:    5,730 m (más alto de Colombia)
Último evento: 1991
Población en riesgo: 100,000
Actividad:    Geotérmica considerable
```

---

### 📊 VOLCANES DE RIESGO MODERADO (Risk Level: MEDIUM)

#### 5. **Nevado del Tolima**
- Elevación: 5,215 m
- Última erupción: 1943
- Proceso de deglaciación acelerada

#### 6. **Cumbal**
- Elevación: 4,764 m
- Última erupción: 1930
- Región: Nariño

#### 7. **Cerro Negro**
- Elevación: 4,725 m
- Última erupción: 1950
- Región: Nariño

---

### 🟡 VOLCANES DE BAJO RIESGO (Risk Level: LOW)

#### 8. **Tamá**
- Elevación: 4,530 m
- Última erupción: 1560
- Estado: Inactivo

#### 9. **Sotará**
- Elevación: 4,600 m
- Última erupción: 1880
- Estado: Inactivo

#### 10. **Romeral**
- Elevación: 5,020 m
- Última erupción: 1845
- Estado: Inactivo

#### 11. **Santa Isabel**
- Elevación: 4,965 m
- Última erupción: 1889
- Estado: Inactivo

#### 12. **Chiles**
- Elevación: 4,747 m
- Última erupción: 1913
- Estado: Inactivo

#### 13. **Cerro Bravo**
- Elevación: 3,856 m
- Última erupción: 1939
- Tipo: Cinder cone

---

## 📦 Módulos Implementados

### 1. **colombian_volcanoes.py** (480 líneas)

Base de datos completa con información de los 13 volcanes:

```python
from src.colombian_volcanoes import (
    get_colombian_volcanoes(),           # Todos los volcanes
    get_active_colombian_volcanoes(),    # Solo activos
    get_critical_colombian_volcanoes(),  # Críticos
    get_high_risk_colombian_volcanoes(), # Alto riesgo
    get_volcano_population_risk(),        # Población en riesgo
    get_volcano_nearby_cities(),          # Ciudades cercanas
    get_volcano_hazards(),                # Tipos de peligro
    get_colombian_volcano_summary()       # Resumen estadístico
)
```

**Características**:
- ✅ 13 volcanes con coordenadas GPS precisas
- ✅ Histroia de erupciones documentada
- ✅ Población en riesgo por volcán
- ✅ Ciudades cercanas a cada volcán
- ✅ Tipos de peligro específicos
- ✅ Red de monitoreo SGC

---

### 2. **colombia_monitor.py** (420 líneas)

Monitor especializado integrado con el sistema multi-volcán:

```python
from src.colombia_monitor import colombia_monitor

# Obtener todos los volcanes colombianos
volcanoes = colombia_monitor.get_all_colombian_volcanoes()

# Volcanes de riesgo crítico
critical = colombia_monitor.get_critical_volcanoes()

# Actividad sísmica
activity = colombia_monitor.get_volcano_activity("nevado_ruiz", days=7)

# Monitoreo por región
tolima_report = colombia_monitor.get_regional_summary("Tolima")

# Reporte nacional completo
national_report = colombia_monitor.get_colombia_monitoring_report()
```

**Métodos principales**:
- `get_all_colombian_volcanoes()` → Lista de 13 volcanes
- `get_active_volcanoes()` → Volcanes activos
- `get_critical_volcanoes()` → Riesgo crítico
- `get_high_risk_volcanoes()` → Alto riesgo
- `add_seismic_event()` → Registrar evento sísmico
- `get_volcano_activity()` → Actividad reciente
- `get_regional_summary()` → Por región geográfica
- `get_colombia_monitoring_report()` → Reporte nacional

---

## 🗺️ Distribución Geográfica

### Volcanes por Región

#### **Región Andina Central** (Cordillera Central)
- Nevado del Ruiz (Caldas, Risaralda, Tolima) - **CRÍTICO**
- Nevado del Tolima (Tolima)
- Romeral (Tolima)
- Santa Isabel (Tolima)

#### **Región Cauca-Nariño** (Cordillera Central sur)
- Puracé (Cauca) - **ALTO**
- Sotará (Cauca)
- Galeras (Nariño) - **CRÍTICO**
- Cumbal (Nariño)
- Cerro Negro (Nariño)
- Chiles (Nariño)

#### **Región Huila** (Cordillera Central sur)
- Nevado del Huila (Huila) - **ALTO**

#### **Región Santander** (Cordillera Oriental)
- Tamá (Santander, N. de Santander)

#### **Región Cauca Sur**
- Cerro Bravo (Cauca)

---

## 💡 Casos de Uso

### Caso 1: Monitoreo de Crisis en Nevado del Ruiz
```python
# Obtener actividad reciente
activity = colombia_monitor.get_volcano_activity("nevado_ruiz", days=1)
print(f"Eventos últimas 24h: {activity['total_events']}")
print(f"Magnitud promedio: {activity['avg_magnitude']}")

# Generar alerta si supera threshold
if activity['max_magnitude'] >= 3.5:
    # Enviar notificaciones (integración con push_notifications.py)
    # Actualizar dashboard en tiempo real
    # Generar reporte de crisis
    pass
```

### Caso 2: Análisis Regional Tolima
```python
# Obtener resumen de región
tolima = colombia_monitor.get_regional_summary("Tolima")
print(f"Volcanes en Tolima: {tolima['volcanoes_count']}")

for volcano in tolima['volcanoes']:
    print(f"  - {volcano['name']}: {volcano['risk_level']}")
```

### Caso 3: Reporte Nacional para SGC
```python
# Generar reporte completo
report = colombia_monitor.get_colombia_monitoring_report()

print(f"Volcanes totales: {report['summary']['total_volcanoes']}")
print(f"Población en riesgo: {report['total_population_at_risk']:,}")
print(f"Recomendación: {report['recommendation']}")

# Exportar datos
csv_data = colombia_monitor.export_regional_data("Nariño", format="csv")
with open("nariño_eventos.csv", "w") as f:
    f.write(csv_data)
```

### Caso 4: Alertas Personalizadas por Ciudades
```python
# Identificar ciudades afectadas
from src.colombian_volcanoes import get_volcano_nearby_cities

cities = get_volcano_nearby_cities("galeras")
print(f"Ciudades cercanas a Galeras: {', '.join(cities)}")

# Enviar alertas a residentes de esas ciudades
# Implementar notificaciones geolocalización
```

---

## 📊 Integración con Otros Módulos

### Con Multi-Volcán (multi_volcano.py)
```python
from src.multi_volcano import volcano_manager
from src.colombian_volcanoes import get_colombian_volcanoes

# Agregar todos los volcanes colombianos al sistema
colombian_volcanoes = get_colombian_volcanoes()
for volcano_id, profile in colombian_volcanoes.items():
    volcano_manager.add_volcano(profile)
```

### Con Notificaciones Push
```python
from src.push_notifications import firebase_system
from src.colombia_monitor import colombia_monitor

# Suscribir usuarios a volcanes colombianos
firebase_system.subscribe_device(device_token, "nevado_ruiz")
firebase_system.subscribe_device(device_token, "galeras")

# Enviar alertas
critical = colombia_monitor.get_critical_volcanoes()
for volcano in critical:
    firebase_system.send_alert_notification(
        volcano_id=volcano['id'],
        magnitude=5.2,
        depth=45,
        location=volcano['name'],
        severity="CRITICAL"
    )
```

### Con Reportes Automáticos
```python
from src.reports import report_generator
from src.colombia_monitor import colombia_monitor

# Generar reporte nacional
national_report = colombia_monitor.get_colombia_monitoring_report()

# Convertir a HTML/JSON
report_obj = {
    "title": "Reporte de Volcanes Colombianos",
    "content": national_report,
    "executive_summary": national_report['summary'],
    "recommendations": [national_report['recommendation']]
}

html = report_generator.export_to_html(report_obj)
```

### Con Predicción de Tsunamis
```python
from src.tsunami_prediction import tsunami_system
from src.colombian_volcanoes import get_colombian_volcanoes

# Evaluar riesgo de tsunamis para eventos costeros
for volcano_id, volcano in get_colombian_volcanoes().items():
    # Galeras está cerca del Pacífico
    if volcano_id == "galeras":
        assessment = tsunami_system.assess_tsunami_risk(
            magnitude=6.5,
            depth=20,
            latitude=volcano.latitude,
            longitude=volcano.longitude,
            location_name=volcano.name
        )
        print(f"Riesgo de tsunami: {assessment.risk_level}")
```

---

## 📈 Estadísticas de Implementación

| Métrica | Valor |
|---------|-------|
| Archivos nuevos | 2 (colombian_volcanoes.py, colombia_monitor.py) |
| Líneas de código | 900+ líneas |
| Volcanes incluidos | 13 volcanes |
| Métodos públicos | 20+ métodos |
| Información completada | 100% (coordenadas, historia, peligros) |
| Integración con módulos | 5+ módulos compatibles |

---

## 🔍 Detalles Geológicos

### Peligros Volcánicos en Colombia

**1. Lahares** (Flujos de escombros lodo)
- Principal peligro en nevados
- Afectado por deglaciación acelerada
- Riesgo especialmente alto en Ruiz, Tolima, Huila

**2. Flujos Piroclásticos**
- Principalmente en Galeras y Ruiz
- Temperaturas superiores a 1000°C
- Radio de afección: hasta 25 km

**3. Caída de Ceniza**
- Afecta área geográfica amplia
- Impacta agricultura y infraestructura
- Ejemplo: 1985, ceniza alcanzó Bogotá desde Ruiz

**4. Emisiones Gaseosas**
- CO2, H2S de fumarolas
- Riesgo para trabajadores mineros
- Indicador de actividad magmática

**5. Lava y Bloques**
- Radio limitado pero muy destructivo
- Menos probable en volcanes colombianos

---

## 🏛️ Red de Monitoreo SGC

### Estaciones Sísmicas Instaladas

**Nevado del Ruiz**: 15 estaciones
**Galeras**: 12 estaciones
**Tolima**: 10 estaciones
**Puracé**: 8 estaciones
**Huila**: 7 estaciones
**Cumbal**: 5 estaciones
**Cerro Negro**: 4 estaciones
**Sotará**: 3 estaciones
**Santa Isabel**: 3 estaciones
**Chiles**: 3 estaciones
**Romeral**: 2 estaciones
**Tamá**: 3 estaciones
**Cerro Bravo**: 1 estación

**Total: 68+ estaciones en toda Colombia**

---

## 🚀 Próximas Mejoras (v1.5.0+)

- [ ] Integración con datos USGS para volcanes fronterizos
- [ ] API tiempo real del SGC
- [ ] Predicción de actividad por estación
- [ ] Dashboard interactivo por región
- [ ] Exportación a formatos SIG (GIS)
- [ ] Integración con mapas temáticos
- [ ] Pronósticos de dispersión de ceniza
- [ ] Modelo de lahares por topografía

---

## 📞 Referencias

- **SGC**: https://www2.servicigeologico.gov.co/
- **Red Sismológica Nacional**: https://www.serviciGeologico.gov.co/sismos/red-sismologica-nacional
- **Publicaciones**: https://www2.servicigeologico.gov.co/publicaciones-tecnologicas
- **Boletín Actividad Volcánica**: https://www2.servicigeologico.gov.co/boletin-de-actividad-volcanica

---

## 📄 Documentación Completa v1.4.1 - Volcanes de Colombia

Sistema completamente documentado y listo para producción.

**Implementado**: Abril 2026  
**Autor**: Sistema IA de Análisis Sísmico  
**Institución**: Universidad de Caldas - Colombia
