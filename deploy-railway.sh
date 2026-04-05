#!/bin/bash

# Script de despliegue en Railway

echo "🚀 Desplegando en Railway..."
echo ""

# Verificar si Railway CLI está instalado
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI no está instalado"
    echo "Instala con: npm install -g @railway/cli"
    echo "O descarga desde: https://railway.app"
    exit 1
fi

# Login en Railway
echo "🔐 Iniciando sesión en Railway..."
railway login

# Crear proyecto
echo "📱 Inicializando proyecto Railway..."
railway init

# Conectar repositorio
echo "📚 Conectando repositorio..."
railway link

# Deploy
echo "🔨 Desplegando código..."
railway up

echo ""
echo "✅ Despliegue completado!"
echo ""
echo "Comandos útiles:"
echo "  Ver status:   railway status"
echo "  Ver logs:     railway logs"
echo "  Config vars:  railway variables"
echo "  Dashboard:    railway open"
