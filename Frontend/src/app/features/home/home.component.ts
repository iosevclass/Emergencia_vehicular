import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth/auth.service';
import { EmergenciaWsService } from '../../core/services/emergencia/emergencia-ws.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  private router = inject(Router);
  private emergenciaWs = inject(EmergenciaWsService);
  
  tallerNombre: string = 'Taller';
  userRole: string = ''; // Nueva propiedad para almacenar el rol

  // Getter para verificar fácilmente en el HTML si es el Admin del Sistema
  get isAdminSistema(): boolean {
    return this.userRole === 'admin_sistema';
  }

  ngOnInit() {
    this.cargarDatosPerfil();
    this.emergenciaWs.conectar();
  }

  private cargarDatosPerfil() {
    const userDataJson = localStorage.getItem('user_data');
    if (userDataJson) {
      try {
        const userData = JSON.parse(userDataJson);
        // Si es Admin, tal vez en el backend se llame nombre_completo según tu modelo Administrador
        this.tallerNombre = userData.nombre || userData.nombre_completo || 'Usuario'; 
        this.userRole = userData.rol || ''; // Capturamos el rol que viene de FastAPI
        
      } catch (error) {
        console.error('Error al parsear user_data:', error);
      }
    }
  }

  logout() {
    this.emergenciaWs.desconectar();
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_data');
    this.router.navigate(['/login']);
  }
}

