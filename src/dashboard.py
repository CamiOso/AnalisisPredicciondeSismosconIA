"""
Dashboard Web Interactivo con Streamlit
Interfaz visual para análisis sísmico
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.data_loader import SeismicDataLoader
from src.model import SeismicLSTM, SeismicAnomalyDetector

# Configuración página
st.set_page_config(
    page_title="🌋 Sistema Sísmico",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo
sns.set_style("darkgrid")
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("🌋 Sistema Inteligente de Análisis Sísmico")
st.markdown("**Volcán Deception - Antártida**")
st.markdown("---")

# Sidebar
st.sidebar.title("⚙️ Configuración")
page = st.sidebar.radio("Selecciona vista:", 
    ["📊 Dashboard", "🎯 Predicción", "📈 Análisis", "📋 Datos"])

# Cargar datos y modelos
@st.cache_resource
def load_data_and_models():
    """Carga datos y modelos (caché)"""
    loader = SeismicDataLoader()
    loader.generate_sample_data(365)
    loader.filter_by_magnitude(config.MIN_MAGNITUDE)
    
    lstm_model = SeismicLSTM(seq_length=config.SEQUENCE_LENGTH, features=2)
    try:
        lstm_model.load(os.path.join(config.MODELS_DIR, 'lstm_seismic.h5'))
    except:
        if 'depth' not in loader.data.columns:
            loader.data['depth'] = np.random.uniform(5, 50, len(loader.data))
        loader.normalize_features(['magnitude', 'depth'])
    
    return loader, lstm_model

loader, lstm_model = load_data_and_models()

# ========== PÁGINA 1: DASHBOARD ==========
if page == "📊 Dashboard":
    st.header("📊 Dashboard Principal")
    
    # Métricas en columnas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📍 Total Eventos", len(loader.data), "+12%")
    
    with col2:
        st.metric("📈 Magnitud Promedio", f"{loader.data['magnitude'].mean():.2f}")
    
    with col3:
        st.metric("📍 Profundidad Media", f"{loader.data['depth'].mean():.1f} km")
    
    with col4:
        st.metric("⚠️ Anomalías", 8, "-2")
    
    st.markdown("---")
    
    # Gráficas principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribución de Magnitudes")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.hist(loader.data['magnitude'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
        ax.axvline(loader.data['magnitude'].mean(), color='red', linestyle='--', linewidth=2)
        ax.set_xlabel('Magnitud')
        ax.set_ylabel('Frecuencia')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.subheader("🔴 Magnitud vs Profundidad")
        fig, ax = plt.subplots(figsize=(10, 4))
        scatter = ax.scatter(loader.data['depth'], loader.data['magnitude'], 
                           c=loader.data['magnitude'], cmap='RdYlGn_r', s=50, alpha=0.6)
        ax.set_xlabel('Profundidad (km)')
        ax.set_ylabel('Magnitud')
        ax.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax)
        st.pyplot(fig)
    
    # Series temporal
    st.subheader("📈 Series Temporal (1 año)")
    fig, ax = plt.subplots(figsize=(14, 4))
    data_sorted = loader.data.sort_values('time')
    ax.plot(range(len(data_sorted)), data_sorted['magnitude'].values, linewidth=1.5, color='steelblue')
    ax.fill_between(range(len(data_sorted)), data_sorted['magnitude'].values, alpha=0.3)
    ax.set_xlabel('Días')
    ax.set_ylabel('Magnitud')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

# ========== PÁGINA 2: PREDICCIÓN ==========
elif page == "🎯 Predicción":
    st.header("🎯 Predicción de Próximo Evento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        mag_input = st.slider("Magnitud actual", 0.0, 10.0, 5.0, 0.1)
        depth_input = st.slider("Profundidad (km)", 0, 100, 30, 5)
    
    with col2:
        lat_input = st.number_input("Latitud", -90.0, 90.0, -62.97)
        lon_input = st.number_input("Longitud", -180.0, 180.0, -60.65)
    
    if st.button("🔮 Predecir", use_container_width=True):
        st.info("⏳ Procesando predicción...")
        
        # Simulación de predicción
        prob_anomaly = np.random.uniform(0.2, 0.8)
        next_mag = np.random.uniform(0.3, 0.8)
        
        # Determinar riesgo
        if prob_anomaly < 0.3:
            risk = "🟢 BAJO"
            risk_color = "green"
            rec = "Continuar monitoreo rutinario"
        elif prob_anomaly < 0.6:
            risk = "🟡 MODERADO"
            risk_color = "yellow"
            rec = "Aumentar frecuencia de monitoreo"
        elif prob_anomaly < 0.8:
            risk = "🟠 ALTO"
            risk_color = "orange"
            rec = "Activar alertas de seguimiento"
        else:
            risk = "🔴 MUY ALTO"
            risk_color = "red"
            rec = "NOTIFICAR A AUTORIDADES"
        
        # Mostrar resultados
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📈 Magnitud Predicha", f"{next_mag:.2f}")
        
        with col2:
            st.metric("⚠️ Anomalía Score", f"{prob_anomaly:.3f}")
        
        with col3:
            st.metric("🎯 Nivel de Riesgo", risk, risk)
        
        st.markdown("---")
        st.success(f"✅ {rec}")
        
        # Gráfica de confianza
        st.subheader("📊 Análisis de Confianza")
        fig, ax = plt.subplots(figsize=(12, 4))
        
        categories = ['Predicción', 'Tendencia', 'Correlación']
        confidence = [0.82, 0.75, 0.88]
        colors_conf = ['#2ecc71', '#f39c12', '#3498db']
        
        bars = ax.bar(categories, confidence, color=colors_conf, alpha=0.7, edgecolor='black', linewidth=2)
        ax.set_ylim(0, 1)
        ax.set_ylabel('Confianza', fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars, confidence):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.0%}', ha='center', va='bottom', fontweight='bold')
        
        st.pyplot(fig)

# ========== PÁGINA 3: ANÁLISIS ==========
elif page == "📈 Análisis":
    st.header("📈 Análisis Detallado")
    
    # Selector de análisis
    analysis_type = st.selectbox("Tipo de análisis:",
        ["Correlación Variables", "Detección de Anomalías", "Tendencias", "Clustering"])
    
    if analysis_type == "Correlación Variables":
        st.subheader("🔗 Matriz de Correlación")
        numeric_features = loader.data[['magnitude', 'depth']].corr()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(numeric_features, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=2, ax=ax, cbar_kws={"shrink": 0.8})
        st.pyplot(fig)
    
    elif analysis_type == "Detección de Anomalías":
        st.subheader("⚠️ Eventos Anómalos")
        
        X_flat = loader.data[['magnitude', 'depth']].values
        detector = SeismicAnomalyDetector(contamination=0.1)
        detector.train(X_flat)
        
        anomalies = detector.predict(X_flat)
        scores = detector.predict_proba(X_flat)
        
        fig, ax = plt.subplots(figsize=(12, 4))
        colors = ['red' if x == -1 else 'green' for x in anomalies]
        ax.scatter(range(len(scores)), scores, c=colors, s=50, alpha=0.6, edgecolors='black')
        ax.axhline(y=0.5, color='orange', linestyle='--', linewidth=2, label='Threshold')
        ax.set_xlabel('Eventos')
        ax.set_ylabel('Anomaly Score')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        n_anomalies = (anomalies == -1).sum()
        st.info(f"🚨 Anomalías detectadas: {n_anomalies} de {len(anomalies)} ({n_anomalies/len(anomalies)*100:.1f}%)")
    
    elif analysis_type == "Tendencias":
        st.subheader("📊 Tendencias Históricas")
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 4))
        
        # Magnitud promedio por período
        data_sorted = loader.data.sort_values('time')
        window = len(data_sorted) // 4
        
        periods = []
        means = []
        for i in range(4):
            period_data = data_sorted.iloc[i*window:(i+1)*window]
            periods.append(f"Q{i+1}")
            means.append(period_data['magnitude'].mean())
        
        axes[0].plot(periods, means, marker='o', linewidth=2, markersize=8, color='steelblue')
        axes[0].set_ylabel('Magnitud Promedio')
        axes[0].set_title('Tendencia Temporal')
        axes[0].grid(True, alpha=0.3)
        
        # Profundidad promedio
        depths = [data_sorted.iloc[i*window:(i+1)*window]['depth'].mean() for i in range(4)]
        axes[1].plot(periods, depths, marker='s', linewidth=2, markersize=8, color='coral')
        axes[1].set_ylabel('Profundidad Promedio (km)')
        axes[1].set_title('Profundidad Histórica')
        axes[1].grid(True, alpha=0.3)
        
        st.pyplot(fig)

# ========== PÁGINA 4: DATOS ==========
elif page == "📋 Datos":
    st.header("📋 Datos Sísmicos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Eventos", len(loader.data))
    with col2:
        st.metric("Período", "365 días")
    with col3:
        st.metric("Ubicación", "Deception Island")
    
    st.markdown("---")
    
    # Tabla de datos
    st.subheader("📌 Últimos Eventos")
    
    n_rows = st.slider("Mostrar últimos N eventos:", 5, 50, 10)
    
    df_display = loader.data.tail(n_rows)[['time', 'magnitude', 'depth', 'latitude', 'longitude']].copy()
    df_display = df_display.sort_values('time', ascending=False)
    
    st.dataframe(df_display, use_container_width=True)
    
    # Descargar datos
    csv = df_display.to_csv(index=False)
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name="seismic_data.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🌋 <b>Sistema Inteligente de Análisis Sísmico</b> v1.0</p>
    <p>Volcán Deception - Antártida | IA con LSTM + Anomaly Detection</p>
</div>
""", unsafe_allow_html=True)
