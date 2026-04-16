class RegisterRequest {
  final String email;
  final String password;
  final String nombreCompleto;
  final String telefono;
  final String ci;
  final String fechaNacimiento;
  final String username; // Añadido para tu controlador _usernameController

  RegisterRequest({
    required this.email,
    required this.password,
    required this.nombreCompleto,
    required this.telefono,
    required this.ci,
    required this.fechaNacimiento,
    required this.username,
  });

  Map<String, dynamic> toJson() => {
    'email': email,
    'password': password,
    'nombre': nombreCompleto,
    'telefono': telefono,
    'ci': ci,
    'fecha_nacimiento': fechaNacimiento,
    'username': username,
  };
}
