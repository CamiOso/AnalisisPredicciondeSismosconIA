#!/bin/bash

# Instalador de dependencias para despliegue en la nube

echo "☁️  Instalando dependencias para despliegue en la nube..."
echo ""

# Heroku
echo "📦 Heroku CLI..."
if command -v brew &> /dev/null; then
    brew tap heroku/brew && brew install heroku
elif command -v apt-get &> /dev/null; then
    curl https://cli-assets.heroku.com/install.sh | sh
else
    echo "⚠️  Descarga desde https://devcenter.heroku.com/articles/heroku-cli"
fi

# Railway
echo ""
echo "📦 Railway CLI..."
npm install -g @railway/cli

# Render
echo ""
echo "📝 Configuración para Render:"
echo "  1. Ve a https://render.com"
echo "  2. Conecta tu repositorio GitHub"
echo "  3. Crea nuevo servicio Web"

# Dependencias Python para producción
echo ""
echo "📦 Dependencias de producción..."
pip install -r requirements.txt
pip install gunicorn
pip install websockets
pip install python-dotenv

echo ""
echo "✅ Instalación completada"
echo ""
echo "Próximos pasos:"
echo "1. Para Heroku:   bash deploy-heroku.sh"
echo "2. Para Railway:  bash deploy-railway.sh"
echo "3. Para Render:   bash deploy-render.sh"
