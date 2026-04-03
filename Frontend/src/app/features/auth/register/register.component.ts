import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../../core/services/auth/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule], // Asegúrate de importar esto
  templateUrl: './register.component.html',
})
export class RegisterComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  // Definimos el formulario con los nombres que pusimos en el HTML
  registerForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
    telefono: ['', Validators.required],
    nombre_taller: ['', Validators.required],
    nit: ['', Validators.required],
    ciudad: ['', Validators.required],
    direccion: ['', Validators.required],
  });

  onSubmit() {
    console.log('Formulario clickeado');
    if (this.registerForm.invalid) {
      console.log('Formulario inválido:', this.registerForm.errors);
      // Esto te dirá qué campo falta
      return;
    }

    console.log('Enviando datos...', this.registerForm.value);
    this.authService.registrarTaller(this.registerForm.value).subscribe({
      next: (res) => {
        alert('¡Registro exitoso!');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error('Error completo del servidor:', err);
        alert('Error: ' + err.error?.detail || 'Error de conexión');
      },
    });
  }
}
