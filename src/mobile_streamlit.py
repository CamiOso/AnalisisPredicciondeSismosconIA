"""
Plantilla para crear WebApp con Streamlit
Alternativa ligera a app móvil nativa
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="🌋 Seismic Analysis Mobile",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema
st.markdown("""
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .main { background-color: #f8f9fa; }
        .sidebar .sidebar-content { background-color: #2c3e50; }
        h1, h2, h3 { color: #2c3e50; }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR - CONFIGURACIÓN
# ============================================================

st.sidebar.title("⚙️ Configuración")

api_url = st.sidebar.text_input(
    "URL del API",
    value="http://localhost:8000",
    help="Dirección del servidor API"
)

refresh_rate = st.sidebar.slider(
    "Actualizar cada (segundos)",
    min_value=5,
    max_value=60,
    value=30
)

# Temas
theme = st.sidebar.radio(
    "Tema",
    ["Light", "Dark"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Alertas")
magnitude_threshold = st.sidebar.slider(
    "Umbral magnitud",
    min_value=2.0,
    max_value=8.0,
    value=4.5
)

anomaly_threshold = st.sidebar.slider(
    "Umbral anomalía",
    min_value=0.0,
    max_value=1.0,
    value=0.7
)

# ============================================================
# HEADER
# ============================================================

col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.title("🌋")

with col2:
    st.title("Seismic Analysis Mobile")
    st.caption("Sistema de Monitoreo Sísmico en Tiempo Real")

with col3:
    # Status
    try:
        response = requests.get(f"{api_url}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Online")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")

# ============================================================
# TAB 1: DASHBOARD EN TIEMPO REAL
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "🎯 Predicción",
    "📈 Historial",
    "ℹ️ Información"
])

with tab1:
    st.header("📊 Dashboard en Tiempo Real")
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        # Obtener estadísticas
        response = requests.get(f"{api_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            
            with col1:
                st.metric(
                    "Total Eventos",
                    stats.get('total_events', 0),
                    delta="↑ +5"
                )
            
            with col2:
                st.metric(
                    "Mag. Media",
                    f"{stats.get('mean_magnitude', 0):.2f}",
                    delta="↓ -0.2"
                )
            
            with col3:
                st.metric(
                    "Profundidad Media",
                    f"{stats.get('mean_depth', 0):.0f} km",
                    delta="→ 0"
                )
            
            with col4:
                st.metric(
                    "Anomalías",
                    stats.get('anomalies_count', 0),
                    delta="↑ +1"
                )
    except:
        st.warning("No se puede conectar con el API")
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Últimos 7 días")
        
        # Generar datos de ejemplo
        dates = pd.date_range(start='today', periods=7, freq='D')
        data = pd.DataFrame({
            'Fecha': dates,
            'Magnitud': [3.2, 3.5, 4.1, 3.8, 4.5, 3.9, 4.2]
        })
        
        fig = px.line(
            data,
            x='Fecha',
            y='Magnitud',
            markers=True,
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(
            hovermode='x unified',
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔴 Distribución por Magnitud")
        
        magnitudes = [3.2, 3.5, 4.1, 3.8, 4.5, 3.9, 4.2, 4.0, 3.7, 4.3]
        fig = px.histogram(
            x=magnitudes,
            nbins=8,
            color_discrete_sequence=['#764ba2']
        )
        fig.update_layout(
            hovermode='x',
            height=300,
            showlegend=False,
            xaxis_title="Magnitud",
            yaxis_title="Frecuencia"
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2: PREDICCIÓN INTERACTIVA
# ============================================================

with tab2:
    st.header("🎯 Predicción Interactiva")
    
    col1, col2 = st.columns(2)
    
    with col1:
        magnitude = st.slider(
            "Magnitud",
            min_value=2.0,
            max_value=8.0,
            value=5.0,
            step=0.1
        )
    
    with col2:
        depth = st.slider(
            "Profundidad (km)",
            min_value=0,
            max_value=800,
            value=30,
            step=5
        )
    
    steps = st.slider(
        "Pasos a predecir",
        min_value=1,
        max_value=30,
        value=7,
        help="Número de días a predecir"
    )
    
    if st.button("🔮 Hacer Predicción", key="predict_btn"):
        try:
            response = requests.post(
                f"{api_url}/api/predict",
                json={"magnitude": magnitude, "depth": depth}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                st.success("✅ Predicción completada")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Magnitud Predicha",
                        f"{result.get('predicted_magnitude', 0):.2f}"
                    )
                
                with col2:
                    st.metric(
                        "Confianza",
                        f"{result.get('confidence', 0)*100:.0f}%"
                    )
                
                with col3:
                    risk = result.get('risk_level', 'DESCONOCIDO')
                    risk_colors = {
                        'BAJO': '🟢',
                        'MODERADO': '🟡',
                        'ALTO': '🔴',
                        'MUY ALTO': '🔴🔴'
                    }
                    st.metric(
                        "Nivel de Riesgo",
                        f"{risk_colors.get(risk, '❓')} {risk}"
                    )
                
                st.info(f"**Recomendación:** {result.get('recommendation', 'N/A')}")
            else:
                st.error("Error en la predicción")
        except:
            st.error("No se puede conectar con el API")

# ============================================================
# TAB 3: HISTORIAL
# ============================================================

with tab3:
    st.header("📈 Historial de Eventos")
    
    time_filter = st.radio(
        "Período",
        ["Últimas 24 horas", "Últimos 7 días", "Últimos 30 días"],
        horizontal=True
    )
    
    try:
        response = requests.get(f"{api_url}/api/data/recent?limit=20")
        
        if response.status_code == 200:
            events = response.json()
            
            df = pd.DataFrame(events)
            
            # Filtrar por alertas
            col1, col2 = st.columns(2)
            
            with col1:
                show_anomalies = st.checkbox("Solo anomalías", value=False)
            
            with col2:
                show_strong = st.checkbox("Solo M ≥ 4.0", value=False)
            
            if show_anomalies:
                df = df[df.get('anomaly_score', 0) > anomaly_threshold]
            
            if show_strong:
                df = df[df.get('magnitude', 0) >= 4.0]
            
            st.dataframe(
                df,
                use_container_width=True,
                height=400
            )
        else:
            st.warning("No se pueden obtener eventos")
    except:
        st.error("Error al obtener historial")

# ============================================================
# TAB 4: INFORMACIÓN
# ============================================================

with tab4:
    st.header("ℹ️ Información del Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Estadísticas Globales")
        try:
            response = requests.get(f"{api_url}/api/stats")
            stats = response.json()
            
            st.info(f"""
            **Total Eventos:** {stats.get('total_events', 'N/A')}
            
            **Rango de Magnitudes:** {stats.get('min_magnitude', 0):.1f} - {stats.get('max_magnitude', 0):.1f}
            
            **Período:** {stats.get('date_range', 'N/A')}
            """)
        except:
            st.warning("Datos no disponibles")
    
    with col2:
        st.subheader("🔧 Configuración de Alertas")
        st.info(f"""
        **Umbral Magnitud:** {magnitude_threshold}
        
        **Umbral Anomalía:** {anomaly_threshold}
        
        **Actualización:** Cada {refresh_rate}s
        """)
    
    st.markdown("---")
    
    st.subheader("📚 Documentación")
    st.markdown("""
    - [GitHub Repository](https://github.com/CamiOso/AnalisisPredicciondeSismosconIA)
    - [API Docs](http://localhost:8000/docs)
    - [USGS Earthquake Data](https://earthquake.usgs.gov/)
    """)
    
    st.markdown("---")
    
    st.caption("""
    🌋 **Seismic Analysis System v1.3.0**  
    Sistema de Monitoreo Sísmico con IA  
    Volcán Deception - Antártida  
    © 2026 CamiOso - MIT License
    """)

# ============================================================
# AUTO-REFRESH
# ============================================================

import time
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

placeholder = st.empty()
with placeholder.container():
    st.info(f"⏱️ Última actualización: {datetime.now().strftime('%H:%M:%S')}")

time.sleep(refresh_rate)
st.rerun()
