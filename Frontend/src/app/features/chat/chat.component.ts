import { Component, OnInit, OnDestroy, ViewChild, ElementRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../core/services/chat.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html'
})
export class ChatComponent implements OnInit, OnDestroy {
  private chatService = inject(ChatService);
  
  chatsActivos: any[] = [];
  mensajes: any[] = [];
  chatSeleccionado: any = null;
  nuevoMensaje: string = '';
  myId: number | null = null;
  
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;

  ngOnInit() {
    this.obtenerMiId();
    this.cargarChats();
    this.chatService.conectarTaller();
    
    // Suscribirse a mensajes nuevos vía WebSocket
    this.chatService.messages$.subscribe(payload => {
      this.procesarMensajeWS(payload);
    });
  }

  ngOnDestroy() {
    this.chatService.desconectar();
  }

  obtenerMiId() {
    const token = localStorage.getItem('access_token'); 
    if (token) {
      try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        const decoded = JSON.parse(jsonPayload);
        this.myId = decoded.sub ? parseInt(decoded.sub) : null;
      } catch (e) {
        console.error("Error decodificando token", e);
      }
    }
  }

  cargarChats() {
    this.chatService.getChatsActivos().subscribe(chats => {
      this.chatsActivos = chats;
    });
  }

  seleccionarChat(chat: any) {
    this.chatSeleccionado = chat;
    this.cargarHistorial(chat.nro_emergencia);
    this.marcarComoLeido(chat.nro_emergencia);
    
    // Resetear contador local
    chat.mensajes_pendientes = 0;
  }

  cargarHistorial(nro: number) {
    this.chatService.getHistorial(nro).subscribe(msgs => {
      this.mensajes = msgs;
      this.scrollToBottom();
    });
  }

  marcarComoLeido(nro: number) {
    this.chatService.marcarComoLeidos(nro).subscribe();
  }

  enviar() {
    if (!this.nuevoMensaje.trim() || !this.chatSeleccionado) return;

    const texto = this.nuevoMensaje;
    const nro = this.chatSeleccionado.nro_emergencia;
    
    // Optimistic Update
    this.mensajes.push({
      id_remitente: this.myId,
      mensaje: texto,
      fecha_hora: new Date().toISOString(),
      leido: false
    });
    this.nuevoMensaje = '';
    this.scrollToBottom();

    this.chatService.enviarMensaje(nro, texto).subscribe({
      error: (err) => console.error("Error enviando mensaje", err)
    });
  }

  procesarMensajeWS(payload: any) {
    if (payload.type === 'NEW_MESSAGE') {
      const msg = payload.data;
      
      // Si el mensaje es para el chat que tengo abierto
      if (this.chatSeleccionado && msg.nro_emergencia === this.chatSeleccionado.nro_emergencia) {
        // Evitar duplicar mi propio mensaje (que ya añadí por optimistic update)
        if (msg.id_remitente !== this.myId) {
          this.mensajes.push({
            id_remitente: msg.id_remitente,
            mensaje: msg.mensaje,
            fecha_hora: new Date().toISOString(),
            leido: false
          });
          this.scrollToBottom();
          // Como lo estoy viendo, lo marco como leído
          this.marcarComoLeido(msg.nro_emergencia);
        }
      } else {
        // Si es para otro chat, incrementar contador en la lista
        const chat = this.chatsActivos.find(c => c.nro_emergencia === msg.nro_emergencia);
        if (chat) {
          chat.mensajes_pendientes++;
          chat.ultimo_mensaje = msg.mensaje;
          chat.fecha_ultimo_mensaje = new Date().toISOString();
        } else {
          // Si no existe en la lista (chat nuevo), recargar lista
          this.cargarChats();
        }
      }
    } else if (payload.type === 'MESSAGES_READ') {
      const data = payload.data;
      if (this.chatSeleccionado && data.nro_emergencia === this.chatSeleccionado.nro_emergencia) {
        this.mensajes.forEach(m => {
          if (m.id_remitente === this.myId) m.leido = true;
        });
      }
    }
  }

  esMio(msg: any): boolean {
    return msg.id_remitente === this.myId;
  }

  private scrollToBottom() {
    setTimeout(() => {
      if (this.scrollContainer) {
        this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
      }
    }, 100);
  }
}
