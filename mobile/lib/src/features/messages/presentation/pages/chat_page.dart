import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:jwt_decoder/jwt_decoder.dart';
import '../../../../core/network/websocket_service.dart';

class ChatPage extends StatefulWidget {
  final int nroEmergencia;
  final String nombreReceptor;

  const ChatPage({
    super.key, 
    required this.nroEmergencia, 
    required this.nombreReceptor
  });

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final TextEditingController _messageController = TextEditingController();
  final WebSocketService _wsService = WebSocketService();
  final List<Map<String, dynamic>> _messages = [];
  final ScrollController _scrollController = ScrollController();
  int? _myId;
  bool _isLoadingHistory = true;

  @override
  void initState() {
    super.initState();
    _initChat();
  }

  Future<void> _initChat() async {
    try {
      const storage = FlutterSecureStorage();
      String? token = await storage.read(key: 'jwt_token');

      if (token != null) {
        Map<String, dynamic> decodedToken = JwtDecoder.decode(token);
        String? sub = decodedToken['sub']?.toString();
        _myId = int.tryParse(sub ?? '');

        if (_myId != null) {
          // 1. Marcar como leídos
          _marcarComoLeidos(token);

          // 2. Escuchar WebSocket
          _wsService.connectCliente(_myId!, (payload) {
            if (mounted) {
              // A. Nuevo Mensaje
              if (payload['type'] == 'NEW_MESSAGE') {
                final Map<String, dynamic> msgData = payload['data'];
                if (msgData['nro_emergencia'] == widget.nroEmergencia) {
                  // Si soy yo quien lo envió, el mensaje ya lo añadí localmente (opcional)
                  // Pero para evitar duplicados si el backend no me lo envía a mí,
                  // verificamos si ya existe o simplemente lo añadimos si el remitente no soy yo.
                  if (msgData['id_remitente'] != _myId) {
                    setState(() {
                      _messages.add({
                        'id_remitente': msgData['id_remitente'],
                        'mensaje': msgData['mensaje'],
                        'fecha_hora': DateTime.now().toIso8601String(),
                        'leido': false,
                      });
                    });
                    _scrollToBottom();
                  }
                }
              }
              // B. Mensajes Leídos por la otra parte
              else if (payload['type'] == 'MESSAGES_READ') {
                if (payload['data']['nro_emergencia'] == widget.nroEmergencia) {
                  setState(() {
                    for (var msg in _messages) {
                      if (msg['id_remitente'] == _myId) {
                        msg['leido'] = true;
                      }
                    }
                  });
                }
              }
            }
          });

          await _loadHistory(token);
        }
      }
    } catch (e) {
      print("Error inicializando chat: $e");
    } finally {
      if (mounted) setState(() => _isLoadingHistory = false);
    }
  }

  Future<void> _marcarComoLeidos(String token) async {
    try {
      final baseUrl = dotenv.env['API_URL'] ?? 'http://10.0.2.2:8000';
      final url = Uri.parse('$baseUrl/emergencias/${widget.nroEmergencia}/mensajes/leer');
      await http.put(url, headers: {'Authorization': 'Bearer $token'});
    } catch (e) {
      print("Error marcando como leídos: $e");
    }
  }

  Future<void> _loadHistory(String token) async {
    try {
      final baseUrl = dotenv.env['API_URL'] ?? 'http://10.0.2.2:8000';
      final url = Uri.parse('$baseUrl/emergencias/${widget.nroEmergencia}/mensajes');

      final response = await http.get(
        url,
        headers: {'Authorization': 'Bearer $token'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> history = jsonDecode(response.body);
        if (mounted) {
          setState(() {
            _messages.clear();
            _messages.addAll(history.map((m) => {
              'id_remitente': m['id_remitente'],
              'mensaje': m['mensaje'],
              'fecha_hora': m['fecha_hora'],
              'leido': m['leido'] ?? false,
            }));
          });
          _scrollToBottom();
        }
      }
    } catch (e) {
      print("Error cargando historial: $e");
    }
  }

  Future<void> _sendMessage() async {
    if (_messageController.text.trim().isEmpty) return;

    final String texto = _messageController.text.trim();
    _messageController.clear();

    // Actualización optimista: Añadir a la lista antes de que el servidor responda
    setState(() {
      _messages.add({
        'id_remitente': _myId,
        'mensaje': texto,
        'fecha_hora': DateTime.now().toIso8601String(),
        'leido': false,
      });
    });
    _scrollToBottom();

    try {
      final baseUrl = dotenv.env['API_URL'] ?? 'http://10.0.2.2:8000';
      final url = Uri.parse('$baseUrl/emergencias/${widget.nroEmergencia}/mensajes');
      
      const storage = FlutterSecureStorage();
      String? token = await storage.read(key: 'jwt_token');

      await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
        body: jsonEncode({'mensaje': texto}),
      );
    } catch (e) {
      print("Error enviando mensaje: $e");
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _wsService.disconnect();
    _messageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(widget.nombreReceptor),
            Text(
              'Emergencia #${widget.nroEmergencia}',
              style: const TextStyle(fontSize: 12, color: Colors.white70),
            ),
          ],
        ),
        backgroundColor: const Color(0xFFB91C1C),
      ),
      body: Column(
        children: [
          Expanded(
            child: _isLoadingHistory 
              ? const Center(child: CircularProgressIndicator())
              : ListView.builder(
                  controller: _scrollController,
                  padding: const EdgeInsets.all(16),
                  itemCount: _messages.length,
                  itemBuilder: (context, index) {
                    final msg = _messages[index];
                    final isMe = msg['id_remitente'] == _myId;
                    
                    return _buildMessageBubble(msg['mensaje'], isMe, msg['leido']);
                  },
                ),
          ),
          _buildInputArea(),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(String text, bool isMe, bool leido) {
    return Align(
      alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
        decoration: BoxDecoration(
          color: isMe ? const Color(0xFFB91C1C) : Colors.grey[200],
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: Radius.circular(isMe ? 16 : 0),
            bottomRight: Radius.circular(isMe ? 0 : 16),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(
              text,
              style: TextStyle(color: isMe ? Colors.white : Colors.black87),
            ),
            if (isMe)
              Padding(
                padding: const EdgeInsets.only(top: 4.0),
                child: Icon(
                  Icons.done_all,
                  size: 14,
                  color: leido ? Colors.blueAccent : Colors.white60,
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildInputArea() {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 4)],
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _messageController,
              decoration: const InputDecoration(
                hintText: 'Escribe un mensaje...',
                border: InputBorder.none,
                contentPadding: EdgeInsets.symmetric(horizontal: 16),
              ),
              onSubmitted: (_) => _sendMessage(),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.send, color: Color(0xFFB91C1C)),
            onPressed: _sendMessage,
          ),
        ],
      ),
    );
  }
}
