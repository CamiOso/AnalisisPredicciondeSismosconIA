"""
Volcanes de Colombia - Base de datos completa
Sistema especializado para monitoreo de volcanes colombianos
"""

from src.multi_volcano import VolcanoProfile
from datetime import datetime


# 🇨🇴 VOLCANES ACTIVOS E IMPORTANTES DE COLOMBIA

COLOMBIAN_VOLCANOES = {
    # ==== VOLCANES ACTIVOS CRÍTICOS ====
    
    "nevado_ruiz": VolcanoProfile(
        volcano_id="nevado_ruiz",
        name="Nevado del Ruiz",
        latitude=5.0319,
        longitude=-75.3053,
        elevation_m=5321,
        country="Colombia",
        region="Caldas, Risaralda, Tolima",
        volcano_type="Stratovolcano",
        last_eruption="2023",
        monitoring_since=datetime(1980, 11, 13).isoformat(),
        risk_level="CRITICAL",
        active=True
    ),
    
    "galeras": VolcanoProfile(
        volcano_id="galeras",
        name="Galeras",
        latitude=1.2213,
        longitude=-77.2693,
        elevation_m=4276,
        country="Colombia",
        region="Nariño",
        volcano_type="Stratovolcano",
        last_eruption="2010",
        monitoring_since=datetime(1580, 1, 1).isoformat(),
        risk_level="CRITICAL",
        active=True
    ),
    
    "purace": VolcanoProfile(
        volcano_id="purace",
        name="Puracé",
        latitude=2.3159,
        longitude=-76.4030,
        elevation_m=4756,
        country="Colombia",
        region="Cauca",
        volcano_type="Stratovolcano",
        last_eruption="1977",
        monitoring_since=datetime(1827, 1, 1).isoformat(),
        risk_level="HIGH",
        active=True
    ),
    
    "tolima": VolcanoProfile(
        volcano_id="tolima",
        name="Nevado del Tolima",
        latitude=4.6511,
        longitude=-75.2859,
        elevation_m=5215,
        country="Colombia",
        region="Tolima",
        volcano_type="Stratovolcano",
        last_eruption="1943",
        monitoring_since=datetime(1943, 1, 1).isoformat(),
        risk_level="MEDIUM",
        active=True
    ),
    
    # ==== VOLCANES ACTIVOS IMPORTANTES ====
    
    "huila": VolcanoProfile(
        volcano_id="huila",
        name="Nevado del Huila",
        latitude=2.9331,
        longitude=-75.9828,
        elevation_m=5730,
        country="Colombia",
        region="Huila",
        volcano_type="Stratovolcano",
        last_eruption="1991",
        monitoring_since=datetime(1991, 1, 1).isoformat(),
        risk_level="MEDIUM",
        active=True
    ),
    
    "cumbal": VolcanoProfile(
        volcano_id="cumbal",
        name="Cumbal",
        latitude=0.9514,
        longitude=-76.9128,
        elevation_m=4764,
        country="Colombia",
        region="Nariño",
        volcano_type="Stratovolcano",
        last_eruption="1930",
        monitoring_since=datetime(1930, 1, 1).isoformat(),
        risk_level="MEDIUM",
        active=True
    ),
    
    "cerro_negro": VolcanoProfile(
        volcano_id="cerro_negro",
        name="Cerro Negro",
        latitude=1.0642,
        longitude=-77.3919,
        elevation_m=4725,
        country="Colombia",
        region="Nariño",
        volcano_type="Stratovolcano",
        last_eruption="1950",
        monitoring_since=datetime(1950, 1, 1).isoformat(),
        risk_level="MEDIUM",
        active=True
    ),
    
    "tama": VolcanoProfile(
        volcano_id="tama",
        name="Tamá",
        latitude=6.0975,
        longitude=-72.3686,
        elevation_m=4530,
        country="Colombia",
        region="Santander, Norte de Santander",
        volcano_type="Stratovolcano",
        last_eruption="1560",
        monitoring_since=datetime(1560, 1, 1).isoformat(),
        risk_level="LOW",
        active=False
    ),
    
    # ==== VOLCANES ACTIVOS MENORES ====
    
    "sotara": VolcanoProfile(
        volcano_id="sotara",
        name="Sotará",
        latitude=2.0989,
        longitude=-76.5758,
        elevation_m=4600,
        country="Colombia",
        region="Cauca",
        volcano_type="Stratovolcano",
        last_eruption="1880",
        monitoring_since=datetime(1880, 1, 1).isoformat(),
        risk_level="LOW",
        active=False
    ),
    
    "romeral": VolcanoProfile(
        volcano_id="romeral",
        name="Romeral",
        latitude=4.8311,
        longitude=-75.3642,
        elevation_m=5020,
        country="Colombia",
        region="Tolima",
        volcano_type="Stratovolcano",
        last_eruption="1845",
        monitoring_since=datetime(1845, 1, 1).isoformat(),
        risk_level="LOW",
        active=False
    ),
    
    "santa_isabel": VolcanoProfile(
        volcano_id="santa_isabel",
        name="Volcán Santa Isabel",
        latitude=5.2097,
        longitude=-75.3639,
        elevation_m=4965,
        country="Colombia",
        region="Tolima",
        volcano_type="Stratovolcano",
        last_eruption="1889",
        monitoring_since=datetime(1889, 1, 1).isoformat(),
        risk_level="LOW",
        active=False
    ),
    
    "chiles": VolcanoProfile(
        volcano_id="chiles",
        name="Chiles",
        latitude=0.8189,
        longitude=-77.1186,
        elevation_m=4747,
        country="Colombia",
        region="Nariño",
        volcano_type="Stratovolcano",
        last_eruption="1913",
        monitoring_since=datetime(1913, 1, 1).isoformat(),
        risk_level="LOW",
        active=False
    ),
    
    "cerro_bravo": VolcanoProfile(
        volcano_id="cerro_bravo",
        name="Cerro Bravo",
        latitude=-0.8233,
        longitude=-76.9397,
        elevation_m=3856,
        country="Colombia",
        region="Cauca",
        volcano_type="Cinder cone",
        last_eruption="1939",
        monitoring_since=datetime(1939, 1, 1).isoformat(),
        risk_level="LOW",
        active=False
    ),
}


# Diccionario de información detallada sobre volcanes colombianos
COLOMBIAN_VOLCANO_INFO = {
    "nevado_ruiz": {
        "description": "Complejo volcánico más peligroso de Colombia. Conocido por la erupción de 1985 (Armero).",
        "population_at_risk": 500000,
        "cities_nearby": ["Manizales", "Pereira", "Armenia"],
        "hazards": ["lahar", "lava_flow", "gas_emission", "pyroclastic_flow"],
        "monitoring_stations": 15,
        "observation_network": "SERVICIO GEOLÓGICO COLOMBIANO (SGC)",
    },
    
    "galeras": {
        "description": "Volcán más activo de los Andes colombianos. Múltiples erupciones en siglo XX.",
        "population_at_risk": 300000,
        "cities_nearby": ["Pasto", "Ipiales"],
        "hazards": ["lava_flow", "pyroclastic_flow", "lahars", "ash_fall"],
        "monitoring_stations": 12,
        "observation_network": "SERVICIO GEOLÓGICO COLOMBIANO (SGC)",
    },
    
    "purace": {
        "description": "Sistema volcánico activo con fumarolas sulfurosas. Riesgo moderado.",
        "population_at_risk": 150000,
        "cities_nearby": ["Popayán", "La Plata"],
        "hazards": ["lahars", "ash_fall", "gas_emission"],
        "monitoring_stations": 8,
        "observation_network": "SERVICIO GEOLÓGICO COLOMBIANO (SGC)",
    },
    
    "tolima": {
        "description": "Volcán nevado en proceso de deglaciación acelerada.",
        "population_at_risk": 200000,
        "cities_nearby": ["Ibagué", "Espinal"],
        "hazards": ["lahars", "debris_flow"],
        "monitoring_stations": 10,
        "observation_network": "SERVICIO GEOLÓGICO COLOMBIANO (SGC)",
    },
    
    "huila": {
        "description": "Volcán nevado más alto de Colombia. Actividad geotérmica considerable.",
        "population_at_risk": 100000,
        "cities_nearby": ["Neiva", "Garzón"],
        "hazards": ["lahars", "debris_flow"],
        "monitoring_stations": 7,
        "observation_network": "SERVICIO GEOLÓGICO COLOMBIANO (SGC)",
    },
}


def get_colombian_volcanoes():
    """Retorna diccionario completo de volcanes colombianos"""
    return COLOMBIAN_VOLCANOES.copy()


def get_active_colombian_volcanoes():
    """Retorna solo volcanes activos de Colombia"""
    return {
        v_id: volcano
        for v_id, volcano in COLOMBIAN_VOLCANOES.items()
        if volcano.active
    }


def get_critical_colombian_volcanoes():
    """Retorna volcanes de riesgo CRITICAL en Colombia"""
    return {
        v_id: volcano
        for v_id, volcano in COLOMBIAN_VOLCANOES.items()
        if volcano.risk_level == "CRITICAL"
    }


def get_high_risk_colombian_volcanoes():
    """Retorna volcanes de riesgo ALTO o superior en Colombia"""
    return {
        v_id: volcano
        for v_id, volcano in COLOMBIAN_VOLCANOES.items()
        if volcano.risk_level in ["CRITICAL", "HIGH"]
    }


def get_volcano_population_risk(volcano_id: str):
    """Obtiene población en riesgo para un volcán colombiano"""
    if volcano_id in COLOMBIAN_VOLCANO_INFO:
        return COLOMBIAN_VOLCANO_INFO[volcano_id].get("population_at_risk", 0)
    return 0


def get_volcano_nearby_cities(volcano_id: str):
    """Retorna ciudades cercanas a un volcán colombiano"""
    if volcano_id in COLOMBIAN_VOLCANO_INFO:
        return COLOMBIAN_VOLCANO_INFO[volcano_id].get("cities_nearby", [])
    return []


def get_volcano_hazards(volcano_id: str):
    """Retorna tipos de peligro para un volcán colombiano"""
    if volcano_id in COLOMBIAN_VOLCANO_INFO:
        return COLOMBIAN_VOLCANO_INFO[volcano_id].get("hazards", [])
    return []


def get_colombian_volcano_summary():
    """Retorna resumen estadístico de volcanes colombianos"""
    volcanoes = COLOMBIAN_VOLCANOES
    
    return {
        "total_volcanoes": len(volcanoes),
        "active_volcanoes": sum(1 for v in volcanoes.values() if v.active),
        "critical_risk": sum(1 for v in volcanoes.values() if v.risk_level == "CRITICAL"),
        "high_risk": sum(1 for v in volcanoes.values() if v.risk_level == "HIGH"),
        "monitoring_network": "SERVICIO GEOLÓGICO COLOMBIANO (SGC)",
        "total_population_at_risk": sum(
            COLOMBIAN_VOLCANO_INFO.get(v_id, {}).get("population_at_risk", 0)
            for v_id in volcanoes
        ),
        "critical_volcanoes": list(get_critical_colombian_volcanoes().keys()),
        "highest_elevation": max(
            v.elevation_m for v in volcanoes.values()
        ),
        "most_active": "nevado_ruiz",
    }
