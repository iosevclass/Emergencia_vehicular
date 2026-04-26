import { Component, inject, OnInit, signal } from '@angular/core'; // Añade signal
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms'; // Para reportes/personal
import { AuthService } from '../../core/services/auth/auth.service';
import { EmergenciaWsService } from '../../core/services/emergencia/emergencia-ws.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, ReactiveFormsModule], // Añade ReactiveFormsModule
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  private router = inject(Router);
  private emergenciaWs = inject(EmergenciaWsService);
  private fb = inject(FormBuilder); // Inyecta FormBuilder para el formulario

  tallerNombre: string = 'Taller';
  userRole: string = '';

  // --- Propiedades para Reportes/Personal ---
  personalForm: FormGroup;
  fotoPreview = signal<string | null>(null);
  subiendoFoto = signal<boolean>(false);
  mostrarModal = signal<boolean>(false);

  constructor() {
    // Inicializa el formulario que tenías
    this.personalForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      nombre_completo: ['', Validators.required],
      cargo: ['Mecánico', Validators.required],
      especialidad: [''],
      foto_perfil: [''],
    });
  }

  ngOnInit() {
    this.cargarDatosPerfil();
    this.emergenciaWs.conectar();
  }

  // ... resto de tus métodos (cargarDatosPerfil, logout)
}