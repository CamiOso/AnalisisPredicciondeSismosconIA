#!/bin/bash

# Script de despliegue en Heroku

echo "🚀 Desplegando en Heroku..."
echo ""

# Verificar si Heroku CLI está instalado
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI no está instalado"
    echo "Descarga desde: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Login en Heroku
echo "🔐 Iniciando sesión en Heroku..."
heroku login

# Crear app
APP_NAME="seismic-analysis-$(date +%s)"
echo "📱 Creando app: $APP_NAME"
heroku create $APP_NAME

# Agregar buildpacks
echo "📦 Configurando buildpacks..."
heroku buildpacks:add heroku/python
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git

# Agregar PostgreSQL
echo "💾 Agregando PostgreSQL..."
heroku addons:create heroku-postgresql:hobby-dev

# Configurar variables de entorno
echo "⚙️  Configurando variables de entorno..."
heroku config:set PYTHON_VERSION=3.11.0
heroku config:set PYTHONUNBUFFERED=true

# Deploy
echo "🔨 Desplegando código..."
git push heroku main

# Abrir app
echo ""
echo "✅ Despliegue completado!"
echo "🌐 Abre tu navegador en: https://$APP_NAME.herokuapp.com"
echo ""
echo "Comandos útiles:"
echo "  Ver logs:     heroku logs -t"
echo "  Escala web:   heroku ps:scale web=1 worker=1"
echo "  Config:       heroku config"
echo "  Abrir app:    heroku open"
