// lib/services/websocket_service.dart
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';

class WebSocketService {
  WebSocketChannel? _channel;
  final String wsBaseUrl = "ws://TU_IP_O_DOMINIO:8000/emergencias/ws";

  // Conexión para el TALLER
  void connectTaller(Function(Map<String, dynamic>) onMessage) {
    _channel = WebSocketChannel.connect(Uri.parse("$wsBaseUrl/taller"));
    _listen(onMessage);
  }

  // Conexión para el CLIENTE
  void connectCliente(int clientId, Function(Map<String, dynamic>) onMessage) {
    _channel = WebSocketChannel.connect(
      Uri.parse("$wsBaseUrl/cliente/$clientId"),
    );
    _listen(onMessage);
  }

  void _listen(Function(Map<String, dynamic>) onMessage) {
    _channel?.stream.listen(
      (data) {
        final decodedData = jsonDecode(data);
        onMessage(decodedData);
      },
      onError: (error) => print("Error WS: $error"),
      onDone: () => print("WS Desconectado"),
    );
  }

  void disconnect() {
    _channel?.sink.close();
  }
}
