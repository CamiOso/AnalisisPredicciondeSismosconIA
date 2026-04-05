"""
Mapas interactivos con Folium y Streamlit
"""
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SeismicMap:
    """Mapas interactivos para visualización geográfica"""
    
    # Coordenadas del volcán Deception
    DECEPTION_LAT = -62.9723
    DECEPTION_LON = -60.6477
    
    def __init__(self, data: pd.DataFrame = None):
        self.data = data
    
    def create_main_map(self):
        """Crea mapa principal del volcán"""
        
        m = folium.Map(
            location=[self.DECEPTION_LAT, self.DECEPTION_LON],
            zoom_start=10,
            tiles="OpenStreetMap"
        )
        
        # Marcador del volcán
        folium.Marker(
            location=[self.DECEPTION_LAT, self.DECEPTION_LON],
            popup="🌋 Volcán Deception",
            icon=folium.Icon(color='red', icon='volcano'),
            tooltip="Centro del volcán"
        ).add_to(m)
        
        # Agregar círculo de influencia (100 km)
        folium.Circle(
            location=[self.DECEPTION_LAT, self.DECEPTION_LON],
            radius=100000,  # 100 km en metros
            color='red',
            fill=True,
            fillColor='red',
            fillOpacity=0.1,
            popup="Zona de monitoreo (100 km)"
        ).add_to(m)
        
        return m
    
    def create_events_map(self):
        """Crea mapa con eventos sísmicos"""
        
        if self.data is None or len(self.data) == 0:
            st.warning("No hay datos de eventos para mostrar")
            return None
        
        m = self.create_main_map()
        
        # Agregar eventos como puntos
        for idx, row in self.data.iterrows():
            lat = row.get('latitude', self.DECEPTION_LAT)
            lon = row.get('longitude', self.DECEPTION_LON)
            mag = row.get('magnitude', 0)
            
            # Color según magnitud
            if mag < 3:
                color = 'green'
            elif mag < 5:
                color = 'orange'
            else:
                color = 'red'
            
            # Tamaño según magnitud
            radius = max(5, mag * 2)
            
            popup_text = f"""
            <b>Evento Sísmico</b><br>
            Magnitud: {mag:.2f}<br>
            Profundidad: {row.get('depth', 'N/A')} km<br>
            Tiempo: {row.get('time', 'N/A')}
            """
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=radius,
                popup=folium.Popup(popup_text, max_width=300),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)
        
        return m
    
    def create_heatmap(self):
        """Crea mapa de calor de eventos"""
        
        if self.data is None or len(self.data) == 0:
            st.warning("No hay datos para crear heatmap")
            return None
        
        m = self.create_main_map()
        
        # Preparar datos para heatmap
        heat_data = []
        for idx, row in self.data.iterrows():
            lat = row.get('latitude', self.DECEPTION_LAT)
            lon = row.get('longitude', self.DECEPTION_LON)
            magnitude = row.get('magnitude', 0)
            
            # Intensidad basada en magnitud
            intensity = min(1.0, magnitude / 10.0)
            heat_data.append([lat, lon, intensity])
        
        if heat_data:
            from folium.plugins import HeatMap
            HeatMap(heat_data).add_to(m)
        
        return m
    
    def create_cluster_map(self):
        """Crea mapa con clusters de eventos"""
        
        if self.data is None or len(self.data) == 0:
            st.warning("No hay datos para crear clusters")
            return None
        
        m = self.create_main_map()
        
        from folium.plugins import MarkerCluster
        marker_cluster = MarkerCluster().add_to(m)
        
        # Agregar eventos al cluster
        for idx, row in self.data.iterrows():
            lat = row.get('latitude', self.DECEPTION_LAT)
            lon = row.get('longitude', self.DECEPTION_LON)
            mag = row.get('magnitude', 0)
            
            popup_text = f"M {mag:.2f}"
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_text),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(marker_cluster)
        
        return m
