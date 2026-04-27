import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [],
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent {
  constructor(private router: Router) {}

  // Redirigir al taller al login
  goToLogin() {
    this.router.navigate(['/login']);
  }

  // Redirigir al taller al registro
  goToRegister() {
    this.router.navigate(['/register']);
  }

  // Aquí pondrás el link de descarga de la App más tarde
  downloadApp() {
    window.open('https://drive.google.com/uc?export=download&id=1gwWtu8LXcpxAe4wBMWDwN77bcvL5v7zh', '_blank');
  }
}