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
<<<<<<< HEAD
<<<<<<< ours
  tallerLat: number = 0; // Coordenadas de tu taller
  tallerLon: number = 0;
  serviciosPendientes: number = 0;
  mostrarModal = signal<boolean>(false);

  // Formulario
  personalForm: FormGroup;
  //para la vista previa de la foto de perfil en el formulario de registro de personal
  fotoPreview = signal<string | null>(null);
  subiendoFoto = signal<boolean>(false);
  constructor() {
    this.personalForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      nombre_completo: ['', Validators.required],
      cargo: ['Mecánico', Validators.required],
      especialidad: [''],
      foto_perfil: [''],
    });
  }
=======
  userRole: string = '';
>>>>>>> theirs
=======

>>>>>>> origin/main
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
<<<<<<< HEAD
<<<<<<< ours
        // Asignamos las coordenadas del taller si existen en tu JSON
        this.tallerLat = userData.latitud || -17.7833; // Ejemplo: Santa Cruz
        this.tallerLon = userData.longitud || -63.1821;
=======
        this.userRole = userData.rol || '';
>>>>>>> theirs
=======
>>>>>>> origin/main
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
