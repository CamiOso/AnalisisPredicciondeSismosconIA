"""
Aplicación Móvil - API Cliente Python
Compatible con Flutter, React Native, etc.
"""

# Este archivo contiene ejemplos de cómo consumir la API desde una app móvil
# Puede ser usado como referencia para desarrollar clientes en otros lenguajes

import requests
from typing import Dict, Optional
import json


class SeismicMobileClient:
    """Cliente para consumir API desde aplicaciones móviles"""
    
    def __init__(self, base_url: str = "https://api.seismic-analysis.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
    
    def health_check(self) -> bool:
        """Verifica si API está disponible"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_recent_events(self, limit: int = 10) -> list:
        """Obtiene eventos sísmicos recientes"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/data/recent",
                params={"limit": limit}
            )
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error: {str(e)}")
            return []
    
    def predict(self, magnitude: float, depth: float) -> Dict:
        """Hace predicción"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/predict",
                json={"magnitude": magnitude, "depth": depth}
            )
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas"""
        try:
            response = self.session.get(f"{self.base_url}/api/stats")
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}
    
    def multistep_forecast(self, magnitude: float, steps: int = 7) -> list:
        """Obtiene predicción multi-paso"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/multistep_forecast",
                json={"last_magnitude": magnitude, "steps": steps}
            )
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error: {str(e)}")
            return []


# =====================================================================
# EJEMPLOS PARA DIFERENTES PLATAFORMAS MÓVILES
# Ver: src/MOBILE_APP.md para documentación completa
# =====================================================================

FLUTTER_EXAMPLE = '''
import 'package:http/http.dart' as http;
import 'dart:convert';

class SeismicClient {
  final String baseUrl = 'https://api.seismic-analysis.com';
  
  Future<List<dynamic>> getRecentEvents({int limit = 10}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/data/recent?limit=$limit'),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to load events');
  }
}
'''

REACT_NATIVE_EXAMPLE = '''
class SeismicClient {
  constructor(baseUrl = 'https://api.seismic-analysis.com') {
    this.baseUrl = baseUrl;
  }
  
  async getRecentEvents(limit = 10) {
    try {
      const response = await fetch(
        `${this.baseUrl}/api/data/recent?limit=${limit}`
      );
      return await response.json();
    } catch (error) {
      console.error('Error:', error);
      return [];
    }
  }
}
'''

SWIFT_EXAMPLE = '''
import Foundation

class SeismicClient {
    let baseURL = "https://api.seismic-analysis.com"
    
    func getRecentEvents(limit: Int = 10, completion: @escaping ([Any]) -> Void) {
        let urlString = "(baseURL)/api/data/recent?limit=(limit)"
        guard let url = URL(string: urlString) else { return }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data = data else { return }
            let result = try? JSONSerialization.jsonObject(with: data)
            completion(result as? [Any] ?? [])
        }.resume()
    }
}
'''

KOTLIN_EXAMPLE = '''
import okhttp3.*
import com.google.gson.Gson

class SeismicClient {
    private val client = OkHttpClient()
    
    fun getRecentEvents(limit: Int = 10, callback: (List<Any>) -> Unit) {
        val url = "https://api.seismic-analysis.com/api/data/recent?limit=$limit"
        val request = Request.Builder().url(url).build()
        
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) = Unit
            override fun onResponse(call: Call, response: Response) {
                response.body?.string()?.let { body ->
                    val events = Gson().fromJson(body, Array<Any>::class.java).toList()
                    callback(events)
                }
            }
        })
    }
}
'''

# Ejemplos disponibles para referencia
EXAMPLES = {
    'flutter': FLUTTER_EXAMPLE,
    'react_native': REACT_NATIVE_EXAMPLE,
    'swift': SWIFT_EXAMPLE,
    'kotlin': KOTLIN_EXAMPLE,
}


if __name__ == '__main__':
    print("\n📱 Cliente Móvil para Seismic Analysis")
    print("="*60)
    
    # Ejemplo local
    client = SeismicMobileClient(base_url="http://localhost:8000")
    
    print("\n✓ Verificando salud de API...")
    if client.health_check():
        print("✓ API disponible")
        
        print("\n📊 Obteniendo eventos recientes...")
        events = client.get_recent_events(limit=5)
        print(f"✓ {len(events)} eventos obtenidos")
        
        print("\n🎯 Haciendo predicción...")
        pred = client.predict(magnitude=5.0, depth=30)
        if pred:
            print(f"✓ Predicción: {pred.get('predicted_magnitude', 'N/A')}")
    else:
        print("✗ API no disponible")
