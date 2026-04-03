export interface RegisterTaller {
  email: string;
  password: string;
  telefono: string;
  nombre_taller: string;
  nit: string;
  ciudad: string;
  direccion: string;
  foto?: File; // Para la imagen opcional
}
