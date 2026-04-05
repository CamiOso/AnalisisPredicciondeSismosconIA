#!/bin/bash
# Script para iniciar la API REST

echo "🚀 Iniciando API REST..."
echo ""
echo "📍 API disponible en: http://localhost:8000"
echo "📚 Documentación en: http://localhost:8000/docs"
echo "Para detener: Ctrl+C"
echo ""

cd /home/cami/Desktop/Software3/TradingAlgoritmico
source venv/bin/activate

# Instalar uvicorn si no está
pip install fastapi uvicorn -q

# Ejecutar API
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
