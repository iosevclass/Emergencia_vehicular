import { Injectable, signal } from '@angular/core';
import { Observable, Subject } from 'rxjs';

export interface EmergenciaNotificacion {
  type: string;
  data: {
    nro: number;
    ubicacion_real: string;
    descripcion: string;
    fotos: string[] | null;
    vehiculo: string;
  };
}

@Injectable({
  providedIn: 'root',
})
export class EmergenciaWsService {
  private socket: WebSocket | null = null;
  private readonly WS_URL = 'ws://127.0.0.1:8000/emergencias/ws/taller';
  private emergenciaSubject = new Subject<EmergenciaNotificacion>();

  public emergencias$ = this.emergenciaSubject.asObservable();

  constructor() {}

  conectar() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      return;
    }

    this.socket = new WebSocket(this.WS_URL);

    this.socket.onopen = () => {
      console.log('🔌 Conectado al WebSocket de Emergencias (Taller)');
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('🚨 Nueva notificación recibida:', data);
        this.emergenciaSubject.next(data);
      } catch (e) {
        console.error('Error parseando mensaje WS:', e);
      }
    };

    this.socket.onclose = () => {
      console.log('🔴 Desconectado del WebSocket. Reintentando en 5s...');
      setTimeout(() => this.conectar(), 5000);
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket Error:', error);
      this.socket?.close();
    };
  }

  desconectar() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}
