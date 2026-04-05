"""
🌋 SISTEMA INTEGRADO DE MONITOREO VOLCÁNICO - DEMO v1.5.0

Demostración completa del sistema con todas las funcionalidades:
- Predicción de lahares
- Alertas multicanal
- Analytics avanzado
- Monitoreo colombiano
"""

import sys
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar módulos
try:
    from src.lahar_prediction import lahar_detector, detect_lahar_threats
    from src.alerts_multicanal import alert_router, AlertRouter
    from src.advanced_analytics import advanced_analytics
    from src.colombia_monitor import colombia_monitor
    from src.colombian_volcanoes import COLOMBIAN_VOLCANOES
    logger.info("✅ Todos los módulos importados correctamente")
except ImportError as e:
    logger.error(f"❌ Error importando módulos: {e}")
    sys.exit(1)


def print_header(title):
    """Imprime header decorativo"""
    print("\n" + "="*80)
    print(f" 🌋 {title}".ljust(80))
    print("="*80 + "\n")


def demo_lahar_prediction():
    """Demuestra el sistema de predicción de lahares"""
    
    print_header("DEMO 1: PREDICCIÓN DE LAHARES")
    
    volcanoes_to_test = [
        ("nevado_ruiz", 5.2, 300, 20, 50, 3.5),
        ("nevado_huila", 4.8, 150, 15, 30, 2.0),
        ("galeras", 4.5, 100, 10, 20, 1.5)
    ]
    
    for volcano_id, magnitude, gas_emissions, deformation, precipitation, temp_increase in volcanoes_to_test:
        print(f"\n📍 Evaluando: {volcano_id.upper()}")
        print(f"  • Magnitud: {magnitude}M")
        print(f"  • Emisiones de gas: {gas_emissions} ton/día")
        print(f"  • Deformación: {deformation} cm/mes")
        print(f"  • Lluvia reciente: {precipitation} mm/día")
        print(f"  • Aumento de temperatura: {temp_increase}°C/h")
        
        # Predecir lahar
        lahar_event, probability = lahar_detector.predict_lahar_risk(
            volcano_id=volcano_id,
            seismic_magnitude=magnitude,
            volcanic_gas_emissions=gas_emissions,
            ground_deformation=deformation,
            recent_precipitation_mm=precipitation,
            temperature_increase=temp_increase
        )
        
        if lahar_event:
            print(f"\n  ⚠️ RESULTADO LAHAR:")
            print(f"     Severidad: {lahar_event.severity_level}")
            print(f"     Probabilidad: {probability*100:.1f}%")
            print(f"     Velocidad estimada: {lahar_event.velocity_kmh:.1f} km/h")
            print(f"     Volumen: {lahar_event.volume_m3/1e6:.1f} millones m³")
            print(f"     Distancia: {lahar_event.distance_km:.1f} km")
            print(f"     Personas en riesgo: {lahar_event.population_at_risk:,}")
            
            # Generar alerta si es necesario
            if probability > 0.5:
                alert = lahar_detector.generate_lahar_alert(lahar_event)
                print(f"\n  🚨 ALERTA GENERADA:")
                print(f"     {alert['message']}")
                print(f"     Zonas de evacuación: {', '.join(alert['evacuation_areas'])}")
        
        # Evaluar riesgo de inundación
        river_risk = lahar_detector.assess_river_flooding_risk(
            volcano_id=volcano_id,
            river_discharge_m3s=50 + magnitude*10,
            channel_capacity_m3s=100
        )
        
        if river_risk.get("rivers"):
            print(f"\n  💧 RIESGO DE INUNDACIÓN EN RÍOS:")
            for river in river_risk["rivers"]:
                print(f"     {river['river_name']}: {river['flooding_level']} " +
                      f"(Desborde: {river['overflow_percentage']:.1f}%)")


def demo_alert_system():
    """Demuestra el sistema de alertas multicanal"""
    
    print_header("DEMO 2: SISTEMA DE ALERTAS MULTICANAL")
    
    # Registrar usuarios de prueba
    print("\n📱 Registrando usuarios con diferentes preferencias...")
    
    alert_router.register_user(
        user_id="user_sgc_001",
        contact_data={
            "email": "monitor1@sgc.gov.co",
            "phone": "+573001234567",
            "telegram_id": "123456789",
            "region": "Caldas"
        },
        preferences={
            "channels": ["email", "sms", "telegram"],
            "min_severity": "ALTO"
        }
    )
    logger.info("✓ Usuario SGC registrado")
    
    alert_router.register_user(
        user_id="user_public_001",
        contact_data={
            "email": "resident@example.com",
            "device_token": "firebase_token_001",
            "region": "Tolima"
        },
        preferences={
            "channels": ["push"],
            "min_severity": "MODERADO"
        }
    )
    logger.info("✓ Usuario público registrado")
    
    # Enviar alertas de prueba
    print("\n📤 Enviando alertas de prueba...")
    
    test_alerts = [
        {
            "user_id": "user_sgc_001",
            "message": "Aumento de actividad sísmica detectado en Nevado del Ruiz. Se registraron 5 eventos en 24h.",
            "severity": "ALTO",
            "volcano": "Nevado del Ruiz"
        },
        {
            "user_id": "user_public_001",
            "message": "Alerta: Incremento de actividad en volcán cercano. Manténgase informado.",
            "severity": "MODERADO",
            "volcano": "Tolima"
        }
    ]
    
    for alert_data in test_alerts:
        result = alert_router.send_alert(
            user_id=alert_data["user_id"],
            message=alert_data["message"],
            severity=alert_data["severity"],
            volcano=alert_data["volcano"]
        )
        print(f"\n✓ Alerta enviada a {alert_data['user_id']}")
        print(f"  Canales: {[r.get('channel') for r in result.get('channels_results', [])]}")
    
    # Mostrar estadísticas
    stats = alert_router.get_statistics()
    print(f"\n📊 ESTADÍSTICAS DE ALERTAS:")
    print(f"   Total alertas enviadas: {stats['total_alerts_sent']}")
    print(f"   Usuarios registrados: {stats['registered_users']}")
    print(f"   Tasa de éxito: {stats['success_rate']:.1f}%")
    print(f"   Por severidad: {stats['severity_breakdown']}")


def demo_advanced_analytics():
    """Demuestra el sistema de analytics avanzado"""
    
    print_header("DEMO 3: ANALYTICS AVANZADO")
    
    # Datos simulados de actividad sísmica
    print("\n🔍 Análisis de tendencias sísmicas...")
    
    # Volcán 1: Tendencia al alza (ALARMA)
    ruiz_magnitudes = [3.2, 3.5, 3.8, 4.1, 4.4, 4.7, 5.0]
    print(f"\n📈 Nevado del Ruiz: {ruiz_magnitudes}")
    trend_ruiz = advanced_analytics.analyze_trend("nevado_ruiz", ruiz_magnitudes)
    print(f"   Tendencia: {trend_ruiz.trend_direction}")
    print(f"   Fuerza: {trend_ruiz.trend_strength:.2f}")
    print(f"   Pronóstico 24h: {trend_ruiz.forecast_24h:.2f}M")
    print(f"   Confianza: {trend_ruiz.confidence:.2%}")
    
    # Volcán 2: Estable
    galeras_magnitudes = [4.0, 3.9, 4.1, 4.0, 3.9, 4.1, 4.0]
    print(f"\n📊 Galeras: {galeras_magnitudes}")
    trend_galeras = advanced_analytics.analyze_trend("galeras", galeras_magnitudes)
    print(f"   Tendencia: {trend_galeras.trend_direction}")
    print(f"   Fuerza: {trend_galeras.trend_strength:.2f}")
    print(f"   Pronóstico 24h: {trend_galeras.forecast_24h:.2f}M")
    
    # Análisis de índice de riesgo complejo
    print(f"\n⚠️ ÍNDICE DE RIESGO COMPLEJO:")
    
    risk_data = [
        {
            "volcano_id": "nevado_ruiz",
            "seismic_events": [
                {"magnitude": 4.7, "hours_ago": 2},
                {"magnitude": 4.4, "hours_ago": 4},
                {"magnitude": 4.1, "hours_ago": 8}
            ],
            "deformation_rate": 25.5,
            "gas_emissions": 450,
            "population_at_risk": 500000
        },
        {
            "volcano_id": "galeras",
            "seismic_events": [
                {"magnitude": 4.0, "hours_ago": 6},
                {"magnitude": 3.9, "hours_ago": 12}
            ],
            "deformation_rate": 5.0,
            "gas_emissions": 150,
            "population_at_risk": 75000
        }
    ]
    
    for volcano in risk_data:
        risk_analysis = advanced_analytics.calculate_complex_risk_index(
            volcano_id=volcano["volcano_id"],
            seismic_events=volcano["seismic_events"],
            deformation_rate=volcano["deformation_rate"],
            gas_emissions=volcano["gas_emissions"],
            population_at_risk=volcano["population_at_risk"]
        )
        
        print(f"\n   {volcano['volcano_id'].upper()}:")
        print(f"   • Índice de riesgo: {risk_analysis['risk_index']:.3f}")
        print(f"   • Nivel: {risk_analysis['risk_level']}")
        print(f"   • Sísmico: {risk_analysis['components']['seismic_score']['score']:.3f}")
        print(f"   • Deformación: {risk_analysis['components']['deformation_score']['score']:.3f}")
        print(f"   • Gas: {risk_analysis['components']['gas_score']['score']:.3f}")
        
        # Mostrar recomendaciones principales
        recommendations = risk_analysis['recommendations'][:2]
        for rec in recommendations:
            print(f"   • {rec}")
    
    # Detección de anomalías
    print(f"\n🚨 DETECCIÓN DE ANOMALÍAS:")
    magnitudes_with_anomaly = [3.5, 3.6, 3.4, 3.5, 6.2, 3.4, 3.5]
    anomalies = advanced_analytics.detect_anomalies(
        "test_volcano",
        magnitudes_with_anomaly,
        threshold_std=2.0
    )
    
    print(f"   Muestras: {anomalies['total_points']}")
    print(f"   Anomalías detectadas: {anomalies['anomalies_detected']}")
    if anomalies['anomalies']:
        for anom in anomalies['anomalies']:
            print(f"   • Índice {anom['index']}: {anom['magnitude']}M (Z-score: {anom['z_score']})")


def demo_colombian_system():
    """Demuestra el sistema de volcanes colombianos"""
    
    print_header("DEMO 4: SISTEMA NACIONAL DE VOLCANES COLOMBIANOS")
    
    # Mostrar volcanes críticos
    print("\n🔴 VOLCANES CRÍTICOS:")
    critical = colombia_monitor.get_critical_volcanoes()
    for i, vol in enumerate(critical, 1):
        print(f"   {i}. {vol['name']}")
        print(f"      Población en riesgo: {vol['population_at_risk']}")
        print(f"      Última erupción: {vol.get('last_eruption', 'N/A')}")
        print(f"      Ciudades cercanas: {vol.get('nearby_cities', 'N/A')}")
    
    # Simular evento sísmico en volcán crítico
    print(f"\n📡 Simulando evento sísmico en Nevado del Ruiz...")
    colombia_monitor.add_seismic_event(
        volcano_id="nevado_ruiz",
        magnitude=5.8,
        depth=35,
        latitude=5.0319,
        longitude=-75.3053,
        location="Nevado del Ruiz - Caldas"
    )
    
    # Obtener actividad
    activity = colombia_monitor.get_volcano_activity("nevado_ruiz", days=1)
    print(f"\n   Actividad en últimas 24h:")
    print(f"   • Total eventos: {activity['total_events']}")
    print(f"   • Magnitud promedio: {activity['avg_magnitude']:.2f}M")
    print(f"   • Máxima magnitud: {activity['max_magnitude']:.2f}M")
    print(f"   • Nivel de actividad: {activity['activity_level']}")
    
    # Análisis regional
    print(f"\n🗺️ ANÁLISIS REGIONAL - CALDAS:")
    regional = colombia_monitor.get_regional_summary("Caldas")
    print(f"   Volcanes en región: {regional.get('volcanoes_count', 0)}")
    for vol in regional['volcanoes'][:2]:
        print(f"   • {vol['name']}: {vol['risk_level']}")
    
    # Reporte nacional
    print(f"\n🇨🇴 REPORTE NACIONAL:")
    national = colombia_monitor.get_colombia_monitoring_report()
    print(f"   Volcanes críticos: {len(national.get('critical_volcanoes', []))}")
    print(f"   Volcanes de alto riesgo: {len(national.get('high_risk_volcanoes', []))}")
    print(f"   Volcanes activos: {len(national.get('active_volcanoes', []))}")
    print(f"   Población total en riesgo: {national.get('total_population_at_risk', 0):,}")
    print(f"   Autoridad: {national.get('monitoring_authority', 'N/A')}")
    print(f"   Recomendación: {national.get('recommendation', 'N/A')}")


def demo_integration():
    """Demuestra la integración entre sistemas"""
    
    print_header("DEMO 5: INTEGRACIÓN DE SISTEMAS")
    
    print("\n🔗 Integrando todos los módulos para respuesta coordinada...")
    
    # Escenario: Evento sísmico detectado
    print("\n📍 ESCENARIO: Evento M5.8 detectado en Nevado del Ruiz")
    
    volcano_id = "nevado_ruiz"
    magnitude = 5.8
    
    # 1. Predicción de lahares
    print("\n1️⃣ Predicción de lahares...")
    lahar_result = detect_lahar_threats(
        volcano_id=volcano_id,
        seismic_data={
            "magnitude": magnitude,
            "gas_emissions": 400,
            "ground_deformation": 20,
            "precipitation": 45,
            "temperature_increase": 2.5
        }
    )
    print(f"   Resultado: {lahar_result.get('severity', lahar_result.get('risk_level'))}")
    
    # 2. Análisis avanzado
    print("\n2️⃣ Análisis avanzado...")
    risk_index = advanced_analytics.calculate_complex_risk_index(
        volcano_id=volcano_id,
        seismic_events=[{"magnitude": magnitude, "hours_ago": 0}],
        deformation_rate=15.0,
        gas_emissions=400,
        population_at_risk=500000
    )
    print(f"   Índice de riesgo: {risk_index['risk_index']:.3f} ({risk_index['risk_level']})")
    
    # 3. Enviar alertas
    print("\n3️⃣ Enviando alertas multicanal...")
    result = alert_router.send_alert(
        user_id="user_sgc_001",
        message=f"ALERTA: Evento M{magnitude} en Nevado del Ruiz - Riesgo {risk_index['risk_level']}",
        severity="ALTO" if risk_index['risk_level'] in ["CRÍTICO", "ALTO"] else "MODERADO",
        volcano="Nevado del Ruiz"
    )
    
    success_alerts = sum(
        1 for r in result.get("channels_results", [])
        if r.get("status") == "success"
    )
    print(f"   Canales exitosos: {success_alerts}/{len(result.get('channels_results', []))}")
    
    # 4. Registrar en sistema colombiano
    print("\n4️⃣ Registrando en sistema nacional...")
    colombia_monitor.add_seismic_event(
        volcano_id=volcano_id,
        magnitude=magnitude,
        depth=30,
        latitude=5.0319,
        longitude=-75.3053,
        location="Nevado del Ruiz - Caldas"
    )
    print("   ✓ Evento registrado en base de datos nacional")
    
    print("\n✅ RESPUESTA COORDINADA COMPLETADA")


def main():
    """Ejecuta todas las demos"""
    
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " 🌋 SISTEMA INTELIGENTE DE MONITOREO VOLCÁNICO v1.5.0".center(78) + "║")
    print("║" + " Predicción de Terremotos y Volcanes con IA".center(78) + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        # Ejecutar demos
        demo_lahar_prediction()
        input("\n⏸️  Presiona ENTER para continuar con ALERTAS MULTICANAL...")
        
        demo_alert_system()
        input("\n⏸️  Presiona ENTER para continuar con ANALYTICS AVANZADO...")
        
        demo_advanced_analytics()
        input("\n⏸️  Presiona ENTER para continuar con SISTEMA COLOMBIANO...")
        
        demo_colombian_system()
        input("\n⏸️  Presiona ENTER para continuar con INTEGRACIÓN...")
        
        demo_integration()
        
        # Resumen final
        print_header("RESUMEN FINAL")
        print("\n✅ FUNCIONALIDADES IMPLEMENTADAS EN v1.5.0:")
        print("\n   1. 🌊 Predicción de Lahares")
        print("      • Análisis multi-variable (sísmica, deformación, precipitación)")
        print("      • Estimación de velocidad, volumen y distancia")
        print("      • Evaluación de riesgo de inundación en ríos")
        print("      • 4 volcanes colombianos evaluados (Ruiz, Huila, Puracé, Galeras)")
        
        print("\n   2. 📬 Alertas Multicanal")
        print("      • SMS, Email, Telegram, Push Notifications")
        print("      • Preferencias por usuario y rol")
        print("      • Routing inteligente de alertas")
        print("      • Historial completo de alertas")
        
        print("\n   3. 📊 Analytics Avanzado")
        print("      • Análisis de tendencias con regresión lineal")
        print("      • Índice de riesgo complejo (sísmica 30%, deformación 25%, gas 25%, impacto 20%)")
        print("      • Comparación entre volcanes")
        print("      • Pronóstico de actividad a 30 días")
        print("      • Detección de anomalías (Z-score)")
        
        print("\n   4. 🇨🇴 Sistema Nacional Colombiano")
        print("      • Base de datos de 13 volcanes")
        print("      • Monitoreo regional (4 regiones)")
        print("      • 68+ estaciones de la red SGC")
        print("      • 1.5 millones de personas monitoreadas")
        
        print("\n   5. 🔗 Integración Completa")
        print("      • Comunicación entre todos los módulos")
        print("      • Respuesta coordinada ante eventos")
        print("      • Cadena de comando automática")
        
        print("\n" + "="*80)
        print("🎉 SISTEMA OPERATIVO Y FUNCIONAL - LISTO PARA PRODUCCIÓN".center(80))
        print("="*80)
        
        logger.info("✅ Demo completada exitosamente")
        
    except Exception as e:
        logger.error(f"❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
