import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router'; // 1. Importa esto

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet], // 2. Agrégalo aquí
  templateUrl: './app.html',
})
export class AppComponent {
  title = 'Frontend';
}
