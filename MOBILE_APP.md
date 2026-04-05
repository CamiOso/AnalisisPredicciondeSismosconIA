"""
Documentación para desarrollo de App Móvil Nativa
Orientaciones para Flutter/React Native
"""

# FLUTTER APP - ESTRUCTURA DEL PROYECTO
# ======================================

FLUTTER_STRUCTURE = """
seismic_mobile_app/
├── lib/
│   ├── main.dart                    # Punto de entrada
│   ├── screens/
│   │   ├── home_screen.dart         # Dashboard
│   │   ├── prediction_screen.dart   # Predicción
│   │   ├── alerts_screen.dart       # Alertas
│   │   └── settings_screen.dart     # Configuración
│   ├── models/
│   │   ├── event.dart
│   │   ├── prediction.dart
│   │   └── alert.dart
│   ├── services/
│   │   ├── api_service.dart         # Cliente HTTP
│   │   ├── websocket_service.dart   # WebSocket en tiempo real
│   │   └── notification_service.dart
│   ├── widgets/
│   │   ├── event_card.dart
│   │   ├── metric_card.dart
│   │   └── chart_widget.dart
│   └── utils/
│       ├── constants.dart
│       ├── theme.dart
│       └── validators.dart
├── pubspec.yaml                     # Dependencias
├── ios/                             # Código iOS
└── android/                         # Código Android
"""

FLUTTER_PUBSPEC = """
name: seismic_mobile_app
description: Aplicación móvil para Seismic Analysis

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  http: ^1.1.0              # HTTP client
  dio: ^5.3.0               # HTTP con interceptores
  web_socket_channel: ^2.4.0 # WebSocket
  bloc: ^8.1.1              # State management
  flutter_bloc: ^8.1.3
  get_it: ^7.6.0            # Service locator
  
  # UI
  flutter_animate: ^4.1.0
  lottie: ^2.4.0            # Animaciones
  charts_flutter: ^0.12.0   # Gráficos
  
  # Storage
  hive: ^2.2.3              # Local database
  hive_flutter: ^1.1.0
  
  # Push notifications
  firebase_core: ^2.24.0
  firebase_messaging: ^14.6.0
  
  # Maps
  google_maps_flutter: ^2.5.0

dev_dependencies:
  flutter_lints: ^3.0.0
  build_runner: ^2.4.5
  hive_generator: ^2.0.0
"""

FLUTTER_MAIN = """
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'screens/home_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Inicializar servicios
  await initializeServices();
  
  runApp(const SeismicApp());
}

class SeismicApp extends StatelessWidget {
  const SeismicApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '🌋 Seismic Analysis',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
"""

# REACT NATIVE APP - ESTRUCTURA
# ============================

REACT_NATIVE_STRUCTURE = """
seismic-mobile-app/
├── src/
│   ├── App.tsx                      # Componente raíz
│   ├── screens/
│   │   ├── HomeScreen.tsx
│   │   ├── PredictionScreen.tsx
│   │   ├── AlertsScreen.tsx
│   │   └── SettingsScreen.tsx
│   ├── components/
│   │   ├── EventCard.tsx
│   │   ├── MetricCard.tsx
│   │   ├── Chart.tsx
│   │   └── AlertBanner.tsx
│   ├── services/
│   │   ├── apiService.ts
│   │   ├── websocketService.ts
│   │   └── notificationService.ts
│   ├── redux/
│   │   ├── store.ts
│   │   ├── slices/
│   │   │   ├── eventsSlice.ts
│   │   │   ├── predictionsSlice.ts
│   │   │   └── alertsSlice.ts
│   ├── types/
│   │   └── index.ts
│   └── utils/
│       ├── constants.ts
│       └── theme.ts
├── App.tsx                         # Main App
├── package.json
├── tsconfig.json
└── app.json                        # Config Expo/RN
"""

REACT_NATIVE_PACKAGE = """
{
  "name": "seismic-mobile-app",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "android": "react-native run-android",
    "ios": "react-native run-ios",
    "web": "expo start --web",
    "test": "jest"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-native": "^0.73.0",
    "@react-navigation/native": "^6.1.0",
    "@react-navigation/bottom-tabs": "^6.5.0",
    "axios": "^1.6.0",
    "ws": "^8.14.0",
    "@reduxjs/toolkit": "^1.9.5",
    "react-redux": "^8.1.2",
    "react-native-chart-kit": "^6.12.0",
    "@react-native-async-storage/async-storage": "^1.21.0",
    "react-native-push-notification": "^8.1.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "typescript": "^5.2.0",
    "jest": "^29.7.0"
  }
}
"""

# DESARROLLO RÁPIDO CON EXPO
# ==========================

EXPO_QUICK_START = """
# Instalación
npm install -g expo-cli

# Crear proyecto
expo init SeismicMobileApp
cd SeismicMobileApp

# Seleccionar template: blank (TypeScript)

# Instalar dependencias
npm install axios react-native-chart-kit

# Crear estructura
mkdir src/{screens,components,services}

# Desarrollar
expo start

# En dispositivo:
# - Android: Escanear QR con Expo Go app
# - iOS: Escanear QR con Cámara

# Build
expo build:android
expo build:ios
"""

if __name__ == '__main__':
    print("\\n📱 GUÍA DE DESARROLLO DE APP MÓVIL")
    print("="*60)
    print("\\n1. Flutter")
    print(FLUTTER_STRUCTURE)
    print("\\n2. React Native")
    print(REACT_NATIVE_STRUCTURE)
    print("\\n3. Expo Quick Start")
    print(EXPO_QUICK_START)
