import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../shared/widgets/custom_text_field.dart';
// --- AÑADE ESTOS DOS ---
import '../../../../core/network/auth_service.dart';
import '../../domian/user_model.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final AuthService _authService = AuthService();
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _idCardController = TextEditingController();
  final TextEditingController _birthDateController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _confirmPasswordController =
      TextEditingController();

  @override
  void dispose() {
    _nameController.dispose();
    _usernameController.dispose();
    _idCardController.dispose();
    _birthDateController.dispose();
    _phoneController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> _selectDate() async {
    DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now().subtract(const Duration(days: 365 * 18)),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
    );
    if (picked != null) {
      setState(() {
        _birthDateController.text = "${picked.toLocal()}".split(' ')[0];
      });
    }
  }

  void _submitForm() async {
    if (_formKey.currentState!.validate()) {
      // Empaquetamos los datos de los controladores
      final request = RegisterRequest(
        email: _emailController.text,
        password: _passwordController.text,
        nombreCompleto: _nameController.text,
        telefono: _phoneController.text,
        ci: _idCardController.text,
        fechaNacimiento: _birthDateController.text,
        username: _usernameController.text,
      );

      // Mostrar círculo de carga (Loading)
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (context) => const Center(child: CircularProgressIndicator()),
      );

      try {
        // Llamada al servicio de red
        bool success = await _authService.registerUser(request);

        // ignore: use_build_context_synchronously
        Navigator.pop(context); // Quitamos el loading

        if (success) {
          // ignore: use_build_context_synchronously
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('¡Registro exitoso! Ya puedes iniciar sesión.'),
            ),
          );
          // ignore: use_build_context_synchronously
          Navigator.pop(context); // Volver al Login automáticamente
        } else {
          // ignore: use_build_context_synchronously
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text(
                'Error al registrar. Revisa tu conexión o los datos.',
              ),
            ),
          );
        }
      } catch (e) {
        // ignore: use_build_context_synchronously
        Navigator.pop(context); // Quitar loading si hay un error fatal
        // ignore: use_build_context_synchronously
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Ocurrió un error inesperado.')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 48),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 450),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Header
                const Center(
                  child: Icon(
                    Icons.security,
                    size: 48,
                    color: AppColors.primary,
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  'Kinetic Trust',
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    color: AppColors.primary,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  'Crea tu cuenta',
                  textAlign: TextAlign.center,
                  style: Theme.of(
                    context,
                  ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 32),

                // Form Container
                Container(
                  padding: const EdgeInsets.all(32),
                  decoration: BoxDecoration(
                    color: AppColors.surfaceContainerLowest,
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: [
                      BoxShadow(
                        color: AppColors.onSurface.withValues(alpha: 0.06),
                        blurRadius: 32,
                        offset: const Offset(0, 12),
                      ),
                    ],
                  ),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Profile Photo
                        Center(
                          child: Column(
                            children: [
                              Stack(
                                children: [
                                  CircleAvatar(
                                    radius: 40,
                                    backgroundColor:
                                        AppColors.surfaceContainerHigh,
                                    child: const Icon(
                                      Icons.person,
                                      size: 40,
                                      color: AppColors.outline,
                                    ),
                                  ),
                                  Positioned(
                                    bottom: 0,
                                    right: 0,
                                    child: Container(
                                      padding: const EdgeInsets.all(4),
                                      decoration: const BoxDecoration(
                                        color: AppColors.primary,
                                        shape: BoxShape.circle,
                                      ),
                                      child: const Icon(
                                        Icons.add_a_photo,
                                        size: 16,
                                        color: AppColors.onPrimary,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 8),
                              Text(
                                'Foto de perfil (Opcional)',
                                style: Theme.of(context).textTheme.labelMedium
                                    ?.copyWith(
                                      color: AppColors.onSurfaceVariant,
                                    ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 32),

                        // Fields
                        CustomTextField(
                          controller: _nameController,
                          label: 'Nombre Completo',
                          hintText: 'Ej. Juan Pérez',
                          prefixIcon: Icons.badge_outlined,
                          validator: (val) =>
                              val == null || val.isEmpty ? 'Requerido' : null,
                        ),
                        const SizedBox(height: 20),
                        CustomTextField(
                          controller: _usernameController,
                          label: 'Nombre de Usuario',
                          hintText: 'juanperez99',
                          prefixIcon: Icons.account_circle_outlined,
                          validator: (val) => val == null || val.length < 3
                              ? 'Mínimo 3 caracteres'
                              : null,
                        ),
                        const SizedBox(height: 20),
                        CustomTextField(
                          controller: _idCardController,
                          label: 'Carnet de Identidad',
                          hintText: '00000000X',
                          prefixIcon: Icons.credit_card,
                          validator: (val) =>
                              val == null || val.isEmpty ? 'Requerido' : null,
                        ),
                        const SizedBox(height: 20),
                        GestureDetector(
                          onTap: _selectDate,
                          child: AbsorbPointer(
                            child: CustomTextField(
                              controller: _birthDateController,
                              label: 'Fecha de Nacimiento',
                              hintText: 'DD/MM/AAAA',
                              prefixIcon: Icons.calendar_today,
                              validator: (val) => val == null || val.isEmpty
                                  ? 'Requerido'
                                  : null,
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        CustomTextField(
                          controller: _phoneController,
                          label: 'Teléfono de Contacto',
                          hintText: '+34 000 000 000',
                          prefixIcon: Icons.phone_outlined,
                          keyboardType: TextInputType.phone,
                          validator: (val) =>
                              val == null || val.isEmpty ? 'Requerido' : null,
                        ),
                        const SizedBox(height: 20),
                        CustomTextField(
                          controller: _emailController,
                          label: 'Correo Electrónico',
                          hintText: 'usuario@ejemplo.com',
                          prefixIcon: Icons.email_outlined,
                          keyboardType: TextInputType.emailAddress,
                          validator: (val) {
                            if (val == null || val.isEmpty) return 'Requerido';
                            if (!val.contains('@')) return 'Correo inválido';
                            return null;
                          },
                        ),
                        const SizedBox(height: 20),
                        CustomTextField(
                          controller: _passwordController,
                          label: 'Contraseña',
                          hintText: '••••••••',
                          prefixIcon: Icons.lock_outline,
                          isPassword: true,
                          validator: (val) => val == null || val.length < 6
                              ? 'Mínimo 6 caracteres'
                              : null,
                        ),
                        const SizedBox(height: 20),
                        CustomTextField(
                          controller: _confirmPasswordController,
                          label: 'Confirmar Contraseña',
                          hintText: '••••••••',
                          prefixIcon: Icons.lock_outline,
                          isPassword: true,
                          validator: (val) {
                            if (val == null || val.isEmpty) return 'Requerido';
                            if (val != _passwordController.text)
                              return 'Las contraseñas no coinciden';
                            return null;
                          },
                        ),
                        const SizedBox(height: 40),

                        SizedBox(
                          width: double.infinity,
                          child: ElevatedButton(
                            onPressed: _submitForm,
                            child: const Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text('Registrarme'),
                                SizedBox(width: 8),
                                Icon(Icons.arrow_forward, size: 20),
                              ],
                            ),
                          ),
                        ),

                        const SizedBox(height: 24),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              '¿Ya tienes una cuenta? ',
                              style: Theme.of(context).textTheme.bodyMedium
                                  ?.copyWith(color: AppColors.onSurfaceVariant),
                            ),
                            GestureDetector(
                              onTap: () {
                                Navigator.pop(context);
                              },
                              child: Text(
                                'Inicia sesión aquí',
                                style: Theme.of(context).textTheme.bodyMedium
                                    ?.copyWith(
                                      color: AppColors.primary,
                                      fontWeight: FontWeight.bold,
                                    ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
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
