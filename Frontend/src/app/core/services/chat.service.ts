import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;
  private socket?: WebSocket;
  
  // Subject para notificar nuevos mensajes a los componentes
  private messageSubject = new Subject<any>();
  public messages$ = this.messageSubject.asObservable();

  constructor() {}

  private getHeaders() {
    const token = localStorage.getItem('access_token');
    return {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    };
  }

  // --- MÉTODOS HTTP ---

  getChatsActivos(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/emergencias/chats/activos`, this.getHeaders());
  }

  getHistorial(nroEmergencia: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/emergencias/${nroEmergencia}/mensajes`, this.getHeaders());
  }

  enviarMensaje(nroEmergencia: number, mensaje: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/emergencias/${nroEmergencia}/mensajes`, { mensaje }, this.getHeaders());
  }

  marcarComoLeidos(nroEmergencia: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/emergencias/${nroEmergencia}/mensajes/leer`, {}, this.getHeaders());
  }

  // --- MÉTODOS WEBSOCKET ---

  conectarTaller() {
    const wsUrl = this.apiUrl.replace('http', 'ws') + '/emergencias/ws/taller';
    this.socket = new WebSocket(wsUrl);

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.messageSubject.next(data);
    };

    this.socket.onclose = () => {
      console.log('WebSocket Chat Taller cerrado. Reintentando...');
      setTimeout(() => this.conectarTaller(), 3000);
    };

    this.socket.onerror = (error) => {
      console.error('Error WebSocket Chat:', error);
    };
  }

  desconectar() {
    this.socket?.close();
  }
}
