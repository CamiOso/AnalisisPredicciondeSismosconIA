#!/bin/bash
# Script para instalar nuevas dependencias

echo "📦 Instalando nuevas dependencias (fastapi, streamlit)..."

cd /home/cami/Desktop/Software3/TradingAlgoritmico
source venv/bin/activate

pip install fastapi uvicorn streamlit pydantic

echo "✓ Dependencias instaladas"
echo ""
echo "Ahora puedes ejecutar:"
echo "  📊 Dashboard: bash start_dashboard.sh"
echo "  🔌 API REST: bash start_api.sh"
