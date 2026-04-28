class WorkshopModel {
  final int id;
  final String nombreTaller;
  final String ciudad;
  final String direccion;
  final String? fotoPerfil;
  final double calificacionPromedio;
  final int totalCalificaciones;
  final double latitud;
  final double longitud;

  WorkshopModel({
    required this.id,
    required this.nombreTaller,
    required this.ciudad,
    required this.direccion,
    this.fotoPerfil,
    required this.calificacionPromedio,
    required this.totalCalificaciones,
    required this.latitud,
    required this.longitud,
  });

  factory WorkshopModel.fromJson(Map<String, dynamic> json) {
    return WorkshopModel(
      id: json['id'],
      nombreTaller: json['nombre_taller'] ?? 'Taller sin nombre',
      ciudad: json['ciudad'] ?? '',
      direccion: json['direccion'] ?? 'Ubicación no disponible',
      fotoPerfil: json['foto_perfil'],
      calificacionPromedio: (json['calificacion_promedio'] ?? 0.0).toDouble(),
      totalCalificaciones: json['total_calificaciones'] ?? 0,
      latitud: (json['latitud'] ?? 0.0).toDouble(),
      longitud: (json['longitud'] ?? 0.0).toDouble(),
    );
  }
}
