#!/bin/bash

clear
echo "🐳 Iniciando Sistema de Análisis Sísmico con Docker Compose..."
echo ""
echo "=" | awk '{for (i = 1; i <= 70; i++) printf "="}'
echo ""
echo "🚀 Servicios disponibles:"
echo "  📊 Dashboard Streamlit: http://localhost:8501"
echo "  🔌 API FastAPI:        http://localhost:8000"
echo "  📚 Swagger Docs:       http://localhost:8000/docs"
echo "  📓 Jupyter Notebook:   http://localhost:8888"
echo "  💾 PostgreSQL:         localhost:5432"
echo ""
echo "=" | awk '{for (i = 1; i <= 70; i++) printf "="}'
echo ""

docker-compose up -d

echo "✓ Contenedores iniciados!"
echo ""
echo "Espera 10 segundos para que se inicialicen los servicios..."
sleep 10

echo ""
echo "📊 Estado de servicios:"
docker-compose ps

echo ""
echo "💡 Útiles comandos:"
echo "  Ver logs:              docker-compose logs -f [servicio]"
echo "  Detener:              docker-compose down"
echo "  Rebuild:              docker-compose build --no-cache"
echo "  Ejecutar comando:      docker-compose exec [servicio] [comando]"
echo ""
echo "🌐 Abre en tu navegador:"
echo "  http://localhost:8501  (Dashboard)"
echo "  http://localhost:8000  (API)"
echo ""
