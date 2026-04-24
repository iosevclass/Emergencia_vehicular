class Emergencia {
  final int nro;
  final String ubicacionReal;
  final String descripcion;
  final String prioridad;
  final String estado;
  final int idVehiculo;

  Emergencia({
    required this.nro,
    required this.ubicacionReal,
    required this.descripcion,
    required this.prioridad,
    required this.estado,
    required this.idVehiculo,
  });

  factory Emergencia.fromJson(Map<String, dynamic> json) {
    return Emergencia(
      nro: json['nro'],
      ubicacionReal: json['ubicacion_real'],
      descripcion: json['descripcion'],
      prioridad: json['prioridad'],
      estado: json['estado'],
      idVehiculo: json['id_vehiculo'],
    );
  }
}