#!/usr/bin/env python3
"""
Script principal - Ejecuta el pipeline completo
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src import train, predict


def main():
    print("\n" + "="*70)
    print("    SISTEMA INTELIGENTE DE ANÁLISIS SÍSMICO")
    print("    Volcán Deception - Antártida")
    print("="*70 + "\n")
    
    print("Opciones disponibles:")
    print("  1. Entrenar modelos")
    print("  2. Hacer predicción")
    print("  3. Salir")
    
    choice = input("\nSelecciona opción (1-3): ").strip()
    
    if choice == "1":
        train.main()
    elif choice == "2":
        model_path = os.path.join("models", "lstm_seismic.h5")
        if os.path.exists(model_path):
            predict.main()
        else:
            print("⚠️  Primero debes entrenar los modelos (opción 1)")
            print("Ejecutando entrenamiento automático...")
            train.main()
            predict.main()
    elif choice == "3":
        print("Adiós! 👋")
    else:
        print("❌ Opción inválida")


if __name__ == "__main__":
    main()
