import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { PersonalService } from '../../../core/services/personal/personal.service';
import { MediaService } from '../../../core/services/media.service';
import { EmergenciaWsService, EmergenciaNotificacion } from '../../../core/services/emergencia/emergencia-ws.service';
import { PersonalTaller } from '../../../core/models/personal.model';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['../home.component.css']
})
export class DashboardComponent implements OnInit {
  private personalService = inject(PersonalService);
  private fb = inject(FormBuilder);
  private mediaService = inject(MediaService);
  private emergenciaWs = inject(EmergenciaWsService);
  private http = inject(HttpClient);

  listaPersonal = signal<PersonalTaller[]>([]);
  emergenciasPendientes = signal<EmergenciaNotificacion['data'][]>([]);
  
  mostrarModalDetalle = signal<boolean>(false);
  emergenciaSeleccionada = signal<any | null>(null);
  personalSeleccionadoId = signal<number | null>(null);
  distanciaCalculada = signal<string | null>(null);
  
  tallerLat: number = 0;
  tallerLon: number = 0;
  serviciosPendientes: number = 0;
  mostrarModal = signal<boolean>(false);

  personalForm: FormGroup;
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

  ngOnInit() {
    this.cargarDatosPerfil();
    this.cargarPersonal();

    this.emergenciaWs.emergencias$.subscribe((msg) => {
      if (msg.type === 'NEW_EMERGENCY') {
        this.emergenciasPendientes.update((emergencias) => [msg.data, ...emergencias]);
        this.serviciosPendientes = this.emergenciasPendientes().length;
      }
    });
  }

  private cargarDatosPerfil() {
    const userDataJson = localStorage.getItem('user_data');
    if (userDataJson) {
      try {
        const userData = JSON.parse(userDataJson);
        this.tallerLat = userData.latitud || -17.7833;
        this.tallerLon = userData.longitud || -63.1821;
      } catch (error) {
        console.error('Error al parsear user_data:', error);
      }
    }
  }

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.subiendoFoto.set(true);
      const reader = new FileReader();
      reader.onload = () => this.fotoPreview.set(reader.result as string);
      reader.readAsDataURL(file);

      this.mediaService.uploadImage(file).subscribe({
        next: (response) => {
          this.personalForm.patchValue({ foto_perfil: response.url });
          this.subiendoFoto.set(false);
        },
        error: (err) => {
          console.error('Error al subir imagen:', err);
          this.subiendoFoto.set(false);
          alert('No se pudo subir la imagen, intenta de nuevo.');
        },
      });
    }
  }

  cargarPersonal() {
    this.personalService.getPersonal().subscribe({
      next: (data) => this.listaPersonal.set(data),
      error: (err) => console.error('Error al obtener el personal:', err),
    });
  }

  guardarPersonal() {
    if (this.personalForm.valid) {
      this.personalService.registrarPersonal(this.personalForm.value).subscribe({
        next: () => {
          this.cargarPersonal();
          this.cerrarModal();
        },
        error: (err) => alert(err.error.detail || 'Error al registrar al empleado'),
      });
    }
  }

  abrirModal() { this.mostrarModal.set(true); }
  cerrarModal() {
    this.mostrarModal.set(false);
    this.personalForm.reset({ cargo: 'Mecánico' });
    this.fotoPreview.set(null);
  }

  abrirDetalleEmergencia(emergencia: any) {
    this.emergenciaSeleccionada.set(emergencia);
    this.personalSeleccionadoId.set(null);
    if (emergencia.ubicacion_real && emergencia.ubicacion_real.includes(',')) {
      const coordenadas = emergencia.ubicacion_real.split(',');
      const lat = parseFloat(coordenadas[0].trim());
      const lon = parseFloat(coordenadas[1].trim());
      emergencia.latMap = lat;
      emergencia.lonMap = lon;
      const dist = this.calcularDistancia(this.tallerLat, this.tallerLon, lat, lon);
      this.distanciaCalculada.set(dist.toFixed(2) + ' km');
    } else {
      this.distanciaCalculada.set('Ubicación no disponible');
    }
    this.mostrarModalDetalle.set(true);
  }

  cerrarDetalleEmergencia() {
    this.mostrarModalDetalle.set(false);
    this.emergenciaSeleccionada.set(null);
    this.personalSeleccionadoId.set(null);
  }

  seleccionarPersonal(event: any) {
    this.personalSeleccionadoId.set(Number(event.target.value));
  }

  aceptarEmergencia() {
    const emergencia = this.emergenciaSeleccionada();
    const idPersonal = this.personalSeleccionadoId();
    if (!emergencia || !idPersonal) return;

    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });

    this.http.post(`${environment.apiUrl}/emergencias/${emergencia.nro}/aceptar`, 
      { id_personal: idPersonal }, { headers }).subscribe({
        next: () => {
          alert('¡Emergencia Aceptada y Asignada!');
          this.emergenciasPendientes.update((emergencias) =>
            emergencias.filter((e) => e.nro !== emergencia.nro));
          this.serviciosPendientes = this.emergenciasPendientes().length;
          this.cerrarDetalleEmergencia();
        },
        error: () => alert('Error al aceptar la emergencia'),
      });
  }

  private calcularDistancia(lat1: number, lon1: number, lat2: number, lon2: number): number {
    const R = 6371;
    const dLat = this.deg2rad(lat2 - lat1);
    const dLon = this.deg2rad(lon2 - lon1);
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  }

  private deg2rad(deg: number): number { return deg * (Math.PI / 180); }
  verFotoGrande(url: string) { if (url) window.open(url, '_blank'); }
}
