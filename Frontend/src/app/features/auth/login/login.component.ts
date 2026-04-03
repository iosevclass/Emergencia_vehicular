import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, RouterLink], // <--- 2. Agrégalo aquí
  templateUrl: './login.component.html',
  styleUrls: [],
})
export class LoginComponent {}
