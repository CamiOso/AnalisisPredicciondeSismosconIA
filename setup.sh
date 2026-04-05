#!/bin/bash

# Script rápido para setup inicial
echo "🚀 Configurando Sistema de Análisis Sísmico..."

# Crear venv
echo "📦 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear directorios necesarios
mkdir -p data models notebooks logs

echo ""
echo "✓ Setup completado!"
echo ""
echo "Para empezar:"
echo "  1. Activa el entorno: source venv/bin/activate"
echo "  2. Entrena el modelo: python src/train.py"
echo "  3. Haz predicciones: python src/predict.py"
echo "  4. O abre el análisis: jupyter notebook notebooks/analisis_seismico.ipynb"
