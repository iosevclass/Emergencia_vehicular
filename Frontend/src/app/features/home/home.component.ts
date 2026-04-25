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

  ngOnInit() {
    this.cargarDatosPerfil();
    this.emergenciaWs.conectar();
  }

  private cargarDatosPerfil() {
    const userDataJson = localStorage.getItem('user_data');
    if (userDataJson) {
      try {
        const userData = JSON.parse(userDataJson);
        this.tallerNombre = userData.nombre || 'Taller';
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
