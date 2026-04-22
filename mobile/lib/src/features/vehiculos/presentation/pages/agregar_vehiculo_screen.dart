import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/network/vehiculo_service.dart'; // Importa el servicio nuevo

class AgregarVehiculoScreen extends StatefulWidget {
  const AgregarVehiculoScreen({super.key});

  @override
  State<AgregarVehiculoScreen> createState() => _AgregarVehiculoScreenState();
}

class _AgregarVehiculoScreenState extends State<AgregarVehiculoScreen> {
  final _formKey = GlobalKey<FormState>();
  final VehiculoService _vehiculoService = VehiculoService();
  bool _isLoading = false;

  final TextEditingController _placaController = TextEditingController();
  final TextEditingController _marcaController = TextEditingController();
  final TextEditingController _modeloController = TextEditingController();
  final TextEditingController _colorController = TextEditingController();
  final TextEditingController _anioController = TextEditingController();

  @override
  void dispose() {
    _placaController.dispose();
    _marcaController.dispose();
    _modeloController.dispose();
    _colorController.dispose();
    _anioController.dispose();
    super.dispose();
  }

  // FUNCIÓN ACTUALIZADA PARA CONECTAR AL BACKEND
  void _guardarVehiculo() async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);

      final vehiculoData = {
        "placa": _placaController.text
            .trim()
            .toUpperCase(), // Recomendado: Placas en mayúsculas
        "marca": _marcaController.text.trim(),
        "modelo": _modeloController.text.trim(),
        "color": _colorController.text.trim(),
        "anio": int.tryParse(_anioController.text) ?? 0,
      };

      try {
        await _vehiculoService.registrarVehiculo(vehiculoData);

        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('✅ Vehículo guardado con éxito')),
          );
          Navigator.pop(context, true);
        }
      } catch (e) {
        // Si el error es por el ROL o el TOKEN, aquí verás el mensaje real
        if (mounted) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text('❌ Error: ${e.toString()}')));
        }
      } finally {
        if (mounted) setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        title: const Text(
          'Agregar Vehículo',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        backgroundColor: AppColors.surface,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              _buildTextField(
                controller: _placaController,
                label: 'Placa',
                hint: 'Ej. 4822-LKN', // Ahora sí pasamos el hint
                icon: Icons.pin,
              ),
              const SizedBox(height: 16),
              _buildTextField(
                controller: _marcaController,
                label: 'Marca',
                hint: 'Ej. Toyota',
                icon: Icons.directions_car,
              ),
              const SizedBox(height: 16),
              _buildTextField(
                controller: _modeloController,
                label: 'Modelo',
                hint: 'Ej. Corsel',
                icon: Icons.category,
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: _buildTextField(
                      controller: _colorController,
                      label: 'Color',
                      hint: 'Ej. Rojo',
                      icon: Icons.color_lens,
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: _buildTextField(
                      controller: _anioController,
                      label: 'Año',
                      hint: 'Ej. 2012',
                      icon: Icons.calendar_today,
                      isNumber: true,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 40),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _guardarVehiculo,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: _isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text('Guardar Vehículo'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required String hint, // 1. Agregamos el parámetro hint
    required IconData icon,
    bool isNumber = false,
  }) {
    return TextFormField(
      controller: controller,
      keyboardType: isNumber ? TextInputType.number : TextInputType.text,
      decoration: InputDecoration(
        labelText: label,
        hintText: hint, // 2. Lo asignamos aquí
        floatingLabelBehavior: FloatingLabelBehavior
            .always, // 3. Forzamos a que el label suba para ver el hint
        prefixIcon: Icon(icon, color: AppColors.outline),
        filled: true,
        fillColor: AppColors.surfaceContainerHighest.withOpacity(0.3),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
      ),
      validator: (value) =>
          (value == null || value.isEmpty) ? 'Requerido' : null,
    );
  }
}
