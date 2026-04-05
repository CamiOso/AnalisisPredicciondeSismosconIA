#!/bin/bash
# Script para iniciar el dashboard Streamlit

echo "🚀 Iniciando Dashboard Streamlit..."
echo ""
echo "📍 Accede en: http://localhost:8501"
echo "Para detener: Ctrl+C"
echo ""

cd /home/cami/Desktop/Software3/TradingAlgoritmico
source venv/bin/activate

# Instalar streamlit si no está
pip install streamlit -q

# Ejecutar dashboard
streamlit run src/dashboard.py --logger.level=warning
