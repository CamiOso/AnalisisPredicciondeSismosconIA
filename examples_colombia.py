"""
Ejemplos de Uso - Volcanes de Colombia
Sistema de Monitoreo Sísmico Nacional
"""

# ============================================================================
# EJEMPLO 1: Monitoreo de Crisis - Nevado del Ruiz
# ============================================================================

def ejemplo_crisis_nevado_ruiz():
    """Monitorea un evento de crisis en Nevado del Ruiz"""
    from src.colombia_monitor import colombia_monitor
    from src.push_notifications import firebase_system
    from datetime import datetime
    
    print("=" * 70)
    print("EJEMPLO 1: MONITOREO DE CRISIS - NEVADO DEL RUIZ")
    print("=" * 70)
    
    # Agregar evento sísmico de magnitud 5.8
    colombia_monitor.add_seismic_event(
        volcano_id="nevado_ruiz",
        magnitude=5.8,
        depth=42,
        latitude=5.0319,
        longitude=-75.3053,
        location="Nevado del Ruiz - Caldas"
    )
    
    # Obtener actividad recent
    activity = colombia_monitor.get_volcano_activity("nevado_ruiz", days=1)
    print(f"\n📊 Actividad en últimas 24 horas:")
    print(f"   Total de eventos: {activity['total_events']}")
    print(f"   Magnitud promedio: {activity['avg_magnitude']}")
    print(f"   Magnitud máxima: {activity['max_magnitude']}")
    print(f"   Nivel de actividad: {activity['activity_level']}")
    
    # Enviar notificaciones push
    print(f"\n📱 Enviando notificaciones a dispositivos...")
    count = firebase_system.send_alert_notification(
        volcano_id="nevado_ruiz",
        magnitude=5.8,
        depth=42,
        location="Nevado del Ruiz",
        severity="CRITICAL"
    )
    print(f"   Notificaciones enviadas: {count} dispositivos")
    
    # Obtener información de ciudades afectadas
    print(f"\n🏙️ Ciudades en riesgo:")
    for city in ["Manizales", "Pereira", "Armenia"]:
        print(f"   - {city}")


# ============================================================================
# EJEMPLO 2: Análisis Regional - Volcanes de Nariño
# ============================================================================

def ejemplo_analisis_regional_nariño():
    """Analiza volcanes de la región de Nariño"""
    from src.colombia_monitor import colombia_monitor
    from src.colombian_volcanoes import get_volcano_nearby_cities
    
    print("\n" + "=" * 70)
    print("EJEMPLO 2: ANÁLISIS REGIONAL - VOLCANES DE NARIÑO")
    print("=" * 70)
    
    # Obtener resumen de región
    region_report = colombia_monitor.get_regional_summary("Nariño")
    
    print(f"\n🌋 Región: {region_report['region']}")
    print(f"   Volcanes: {region_report['volcanoes_count']}")
    
    print(f"\n   Detalle de volcanes:")
    for volcano in region_report['volcanoes']:
        print(f"\n      {volcano['name']}")
        print(f"      - ID: {volcano['id']}")
        print(f"      - Riesgo: {volcano['risk_level']}")
        print(f"      - Actividad: {volcano['activity']}")
        
        # Ciudades cercanas
        cities = get_volcano_nearby_cities(volcano['id'])
        if cities:
            print(f"      - Ciudades: {', '.join(cities)}")


# ============================================================================
# EJEMPLO 3: Reporte Nacional Completo
# ============================================================================

def ejemplo_reporte_nacional():
    """Genera reporte nacional completo de volcanes"""
    from src.colombia_monitor import colombia_monitor
    from src.reports import report_generator
    
    print("\n" + "=" * 70)
    print("EJEMPLO 3: REPORTE NACIONAL COMPLETO")
    print("=" * 70)
    
    # Obtener reporte nacional
    national_report = colombia_monitor.get_colombia_monitoring_report()
    
    summary = national_report['summary']
    print(f"\n📋 RESUMEN NACIONAL")
    print(f"   Total de volcanes: {summary['total_volcanoes']}")
    print(f"   Volcanes activos: {summary['active_volcanoes']}")
    print(f"   Volcanes críticos: {summary['critical_risk']}")
    print(f"   Poblacion en riesgo: {summary['total_population_at_risk']:,} personas")
    print(f"   Red de monitoreo: {summary['monitoring_network']}")
    
    print(f"\n🚨 VOLCANES CRÍTICOS:")
    for volcano in national_report['critical_volcanoes']:
        print(f"   • {volcano['name']}")
        print(f"     - Población en riesgo: {volcano['population_at_risk']:,}")
        print(f"     - Ciudades: {volcano['nearby_cities']}")
    
    print(f"\n⚠️ VOLCANES DE ALTO RIESGO:")
    for volcano in national_report['high_risk_volcanoes']:
        print(f"   • {volcano['name']}")
        print(f"     - Estaciones de monitoreo: {volcano['monitoring_stations']}")
        print(f"     - Estado de alerta: {volcano['alert_status']}")
    
    print(f"\n💡 RECOMENDACIÓN:")
    print(f"   {national_report['recommendation']}")


# ============================================================================
# EJEMPLO 4: Integración Multi-Volcán
# ============================================================================

def ejemplo_integracion_multivulcan():
    """Integra todos los volcanes colombianos con sistema multi-volcán"""
    from src.multi_volcano import volcano_manager
    from src.colombian_volcanoes import get_colombian_volcanoes
    
    print("\n" + "=" * 70)
    print("EJEMPLO 4: INTEGRACIÓN CON SISTEMA MULTI-VOLCÁN")
    print("=" * 70)
    
    # Agregar todos los volcanes colombianos
    colombian = get_colombian_volcanoes()
    
    print(f"\n➕ Agregando {len(colombian)} volcanes colombianos...")
    
    added_count = 0
    for volcano_id, profile in colombian.items():
        if volcano_manager.add_volcano(profile):
            added_count += 1
    
    print(f"✅ {added_count} volcanes agregados exitosamente")
    
    # Comparación global
    stats = volcano_manager.get_comparative_statistics()
    
    print(f"\n📊 Estadísticas de actividad global:")
    print(f"   Índice global de actividad: {volcano_manager.calculate_global_activity_index():.2f}")
    
    # Top 5 más activos
    print(f"\n   Top 5 volcanes más activos:")
    top_5 = sorted(
        stats.items(),
        key=lambda x: x[1].get('total_events', 0),
        reverse=True
    )[:5]
    
    for volcano_id, stats_data in top_5:
        print(f"      {volcano_id}: {stats_data.get('total_events', 0)} eventos")


# ============================================================================
# EJEMPLO 5: Predicción de Tsunamis - Galeras
# ============================================================================

def ejemplo_tsunami_galeras():
    """Evalúa riesgo de tsunami para evento en Galeras"""
    from src.tsunami_prediction import tsunami_system
    from src.colombian_volcanoes import get_colombian_volcanoes
    
    print("\n" + "=" * 70)
    print("EJEMPLO 5: EVALUACIÓN DE RIESGO DE TSUNAMI - GALERAS")
    print("=" * 70)
    
    volcanoes = get_colombian_volcanoes()
    galeras = volcanoes['galeras']
    
    # Simular evento de magnitud alta
    assessment = tsunami_system.assess_tsunami_risk(
        magnitude=6.8,
        depth=15,  # Muy superficial
        latitude=galeras.latitude,
        longitude=galeras.longitude,
        location_name=galeras.name
    )
    
    print(f"\n🌊 Evaluación de riesgo de tsunami:")
    print(f"   Magnitud: {assessment.earthquake_magnitude}")
    print(f"   Profundidad: {assessment.earthquake_depth} km")
    print(f"   Probabilidad de tsunami: {assessment.tsunami_probability:.1%}")
    print(f"   Altura estimada de onda: {assessment.estimated_wave_height:.1f} metros")
    print(f"   Nivel de riesgo: {assessment.risk_level}")
    print(f"   Tiempo hasta costa: ~{assessment.travel_time_minutes} minutos")
    
    if assessment.affected_coasts:
        print(f"   Costas potencialmente afectadas:")
        for coast in assessment.affected_coasts:
            print(f"      • {coast}")
    
    print(f"\n   Recomendación:")
    print(f"   {assessment.recommendation}")


# ============================================================================
# EJEMPLO 6: Análisis de Sentimiento Social
# ============================================================================

def ejemplo_sentimiento_social():
    """Analiza sentimiento en redes sobre volcanes colombianos"""
    from src.social_sentiment import sentiment_analyzer
    from datetime import datetime
    
    print("\n" + "=" * 70)
    print("EJEMPLO 6: ANÁLISIS DE SENTIMIENTO SOCIAL")
    print("=" * 70)
    
    # Simular algunos posts en redes
    posts = [
        {
            "id": "tw_001",
            "platform": "twitter",
            "user": "@user1",
            "content": "¡Temblor fuerte en Galeras! Muy peligroso para Pasto",
        },
        {
            "id": "tw_002",
            "platform": "twitter",
            "user": "@user2",
            "content": "SGC monitorea actividad sísminca en región de Nariño",
        },
        {
            "id": "fb_001",
            "platform": "facebook",
            "user": "Usuario Facebook",
            "content": "Evacuación preventiva en Nevado del Ruiz",
        },
    ]
    
    print(f"\n📱 Analizando {len(posts)} posts en redes sociales...")
    
    for post in posts:
        analyzed = sentiment_analyzer.analyze_post(
            post_id=post["id"],
            platform=post["platform"],
            username=post["user"],
            content=post["content"],
            timestamp=datetime.now(),
            engagement=50
        )
        
        print(f"\n   {post['platform'].upper()} - {post['user']}")
        print(f"   Contenido: {post['content']}")
        print(f"   Sentimiento: {analyzed.sentiment_label} ({analyzed.sentiment_score:.2f})")
        print(f"   Volcanes mencionados: {', '.join(analyzed.volcano_mentions) or 'Ninguno'}")
    
    # Análisis de tendencias
    print(f"\n📊 Análisis de tendencias:")
    trending = sentiment_analyzer.get_trending_volcanoes()
    print(f"   Volcanes en tendencia: {len(trending)}")
    
    for volcano in trending[:3]:
        print(f"      • {volcano['volcano_id']}: {volcano['mentions']} menciones")


# ============================================================================
# EJEMPLO 7: Generación de Reportes
# ============================================================================

def ejemplo_generacion_reportes():
    """Genera reportes automáticos para volcanes colombianos"""
    from src.reports import report_generator, ReportConfig
    
    print("\n" + "=" * 70)
    print("EJEMPLO 7: GENERACIÓN DE REPORTES AUTOMÁTICOS")
    print("=" * 70)
    
    # Crear configuración de reportes
    config = ReportConfig(
        report_type="daily",
        recipients=[
            "sgc@servicigeologico.gov.co",
            "proteccion@colombia.gov.co",
            "defensa_civil@local.gov.co"
        ],
        include_metrics=True,
        include_charts=True,
        include_forecast=True,
        include_alerts=True,
        include_social_media=True,
        language="es"
    )
    
    # Programar reportes
    print(f"\n📅 Programando reportes automáticos:")
    
    volcanoes_to_monitor = [
        "nevado_ruiz",
        "galeras",
        "purace",
        "tolima"
    ]
    
    for volcano_id in volcanoes_to_monitor:
        success = report_generator.schedule_report(
            f"daily_{volcano_id}",
            config
        )
        if success:
            print(f"   ✅ Reporte programado: {volcano_id}")
    
    # Generar reporte ejemplo
    daily_report = report_generator.generate_daily_report(
        volcano_id="nevado_ruiz",
        seismic_data={
            "event_count": 12,
            "avg_magnitude": 4.1,
            "max_magnitude": 5.2,
            "anomalies": 2,
            "avg_depth": 45,
            "min_depth": 30,
            "max_depth": 60
        },
        metrics={"correlation": 0.82},
        predictions={"forecast": [4.0, 4.1, 4.2, 4.3, 4.1, 4.0, 3.9]},
        alerts=[{"severity": "HIGH", "magnitude": 5.2}],
        social_sentiment={
            "total_posts": 145,
            "avg_sentiment": -0.15,
            "trending_volcanoes": ["nevado_ruiz"]
        }
    )
    
    print(f"\n📄 Reporte generado:")
    print(f"   Título: {daily_report['title']}")
    print(f"   Fecha: {daily_report['date']}")
    print(f"   Eventos sísmicos: {daily_report['executive_summary']['total_events']}")
    print(f"   Magnitud máxima: {daily_report['executive_summary']['max_magnitude']}")
    print(f"   Recomendaciones: {len(daily_report['recommendations'])}")


# ============================================================================
# EJECUTAR TODOS LOS EJEMPLOS
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "EJEMPLOS DE USO - VOLCANES DE COLOMBIA" + " " * 16 + "║")
    print("║" + " " * 20 + "Sistema de Monitoreo Sísmico Nacional" + " " * 12 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Ejecutar ejemplos
    ejemplo_crisis_nevado_ruiz()
    ejemplo_analisis_regional_nariño()
    ejemplo_reporte_nacional()
    ejemplo_integracion_multivulcan()
    ejemplo_tsunami_galeras()
    ejemplo_sentimiento_social()
    ejemplo_generacion_reportes()
    
    print("\n" + "=" * 70)
    print("✅ EJEMPLOS COMPLETADOS EXITOSAMENTE")
    print("=" * 70)
    print("\nPara más información, ver:")
    print("  • COLOMBIAN_VOLCANOES.md - Documentación completa")
    print("  • src/colombian_volcanoes.py - Base de datos")
    print("  • src/colombia_monitor.py - Monitor especializado")
    print("\n")
