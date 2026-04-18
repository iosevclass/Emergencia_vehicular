import 'package:flutter/material.dart';
//import '../../../../core/theme/app_colors.dart';

class EmergencyBubble extends StatefulWidget {
  const EmergencyBubble({super.key});

  @override
  State<EmergencyBubble> createState() => _EmergencyBubbleState();
}

class _EmergencyBubbleState extends State<EmergencyBubble> {
  // Posición inicial de la burbuja
  double _xOffset = 20;
  double _yOffset = 150;

  void _showEmergencySheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true, // Para que el teclado no tape el formulario
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (context) {
        return Padding(
          padding: EdgeInsets.only(
            bottom: MediaQuery.of(
              context,
            ).viewInsets.bottom, // Ajuste para teclado
            left: 24,
            right: 24,
            top: 24,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Encabezado
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: const Color(0xFFD32F2F).withOpacity(0.1),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(
                      Icons.emergency,
                      color: Color(0xFFD32F2F),
                    ),
                  ),
                  const SizedBox(width: 16),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Emergencia en Ruta',
                          style: TextStyle(
                            fontFamily: 'Manrope',
                            fontWeight: FontWeight.bold,
                            fontSize: 20,
                          ),
                        ),
                        Text(
                          'Buscando talleres cercanos...',
                          style: TextStyle(
                            fontFamily: 'Inter',
                            color: Colors.grey,
                            fontSize: 14,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // Campo de Descripción
              TextField(
                maxLines: 3,
                decoration: InputDecoration(
                  hintText:
                      '¿Qué le ocurrió a tu vehículo? (Ej. Llanta pinchada, motor no arranca...)',
                  filled: true,
                  fillColor: Colors.grey,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: BorderSide.none,
                  ),
                ),
              ),
              const SizedBox(height: 16),

              // Botones de Adjuntos (Fotos y Ubicación)
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: () {
                        // Lógica para abrir cámara/galería
                      },
                      icon: const Icon(Icons.camera_alt, size: 20),
                      label: const Text('Añadir Foto'),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: () {
                        // Lógica para capturar GPS
                      },
                      icon: const Icon(Icons.location_on, size: 20),
                      label: const Text('Ubicación'),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // Botón de Envío
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    // Lógica para enviar solicitud por Sockets/Firebase
                    Navigator.pop(context); // Cerrar sheet temporalmente
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text(
                          'Alerta enviada. Esperando a que un taller acepte...',
                        ),
                        backgroundColor: Color(0xFFD32F2F),
                      ),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFFD32F2F),
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text(
                    'SOLICITAR AUXILIO INMEDIATO',
                    style: TextStyle(
                      fontFamily: 'Inter',
                      fontWeight: FontWeight.bold,
                      fontSize: 14,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 32),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Positioned(
      left: _xOffset,
      top: _yOffset,
      child: GestureDetector(
        // Lógica para arrastrar la burbuja
        onPanUpdate: (details) {
          setState(() {
            // Actualizamos la posición sumando el desplazamiento del dedo
            _xOffset += details.delta.dx;
            _yOffset += details.delta.dy;

            // Opcional: Podrías añadir límites aquí usando MediaQuery
            // para que la burbuja no se salga de la pantalla.
          });
        },
        // Lógica al tocar la burbuja
        onTap: () => _showEmergencySheet(context),
        child: Container(
          width: 65,
          height: 65,
          decoration: BoxDecoration(
            color: const Color(0xFFD32F2F), // Rojo alerta
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: const Color(0xFFD32F2F).withOpacity(0.4),
                blurRadius: 15,
                spreadRadius: 5,
                offset: const Offset(0, 5),
              ),
            ],
            border: Border.all(color: Colors.white, width: 2),
          ),
          child: const Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.car_crash, color: Colors.white, size: 28),
                Text(
                  'SOS',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
