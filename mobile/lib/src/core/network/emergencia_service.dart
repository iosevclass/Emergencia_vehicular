import 'dart:convert';
import 'package:http/http.dart' as http;

class EmergenciaService {
  // OJO: Usa 10.0.2.2 para emulador Android, o la IP de tu PC para dispositivo físico.
  final String baseUrl = 'http://10.0.2.2:8000/emergencias/';

  Future<bool> solicitarAuxilio({
    required int idVehiculo,
    required String ubicacion,
    required String descripcion,
  }) async {
    try {
      final response = await http.post(
        Uri.parse(baseUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          "id_vehiculo": idVehiculo,
          "ubicacion_real": ubicacion,
          "descripcion": descripcion,
          "prioridad": "alta",
        }),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        return true; // Éxito
      } else {
        print("Error del servidor: ${response.body}");
        return false;
      }
    } catch (e) {
      print("Error de conexión: $e");
      return false;
    }
  }
}
