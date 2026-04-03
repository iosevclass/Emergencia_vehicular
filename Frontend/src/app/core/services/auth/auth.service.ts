import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = 'http://tu-api.com/auth';

  //   registrarTaller(datos: any, foto?: File) {
  //     const formData = new FormData();

  //     // Pasamos todos los campos al FormData
  //     Object.keys(datos).forEach((key) => {
  //       formData.append(key, datos[key]);
  //     });

  //     if (foto) {
  //       formData.append('foto', foto);
  //     }

  //     return this.http.post('http://localhost:8000/usuarios/register-taller', FormData);
  //   }
  registrarTaller(datos: any) {
    // Por ahora, envía solo el JSON para asegurar que la base de datos reciba todo
    return this.http.post('http://localhost:8000/usuarios/register-taller', datos);
  }
}
