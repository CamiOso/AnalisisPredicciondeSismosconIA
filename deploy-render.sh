#!/bin/bash

# Script de despliegue en Render

echo "🚀 Desplegando en Render..."
echo ""

echo "📝 Pasos para desplegar en Render:"
echo ""
echo "1. Ve a https://render.com"
echo "2. Conecta tu repositorio GitHub"
echo "3. Crea nuevo servicio Web"
echo "4. Configuración:"
echo "   - Name: seismic-analysis"
echo "   - Repository: Tu fork"
echo "   - Runtime: Python 3.11"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn src.api:app --bind 0.0.0.0:\$PORT"
echo ""
echo "5. Environment:"
echo "   - PYTHONUNBUFFERED=true"
echo "   - DATABASE_URL=(from PostgreSQL service)"
echo ""
echo "6. Base de datos (opcional):"
echo "   - Crear servicio PostgreSQL"
echo "   - Conectar a Web service"
echo ""
echo "✅ Tu app estará disponible en: https://seismic-analysis.onrender.com"
