# Estructura del Frontend Móvil (Flutter)

## Árbol del Proyecto (Móvil)

```text
mobile/
├── android/              # Configuración y código nativo Android
├── ios/                  # Configuración y código nativo iOS
├── lib/                  # Código fuente (Dart/Flutter)
│   ├── main.dart         # Punto de entrada de la aplicación
│   └── src/              # Lógica y UI modular
│       ├── core/         # Funcionalidades base y configuración global
│       │   ├── network/  # Cliente HTTP, interceptores, manejo de API
│       │   └── theme/    # Diseño, colores, fuentes, estilos globales
│       ├── features/     # Funcionalidades divididas por dominio
│       │   ├── auth/         # Login, registro, manejo de tokens
│       │   ├── emergencies/  # Reporte y seguimiento de emergencias
│       │   ├── home/         # Pantalla principal / Dashboard
│       │   ├── messages/     # Sistema de notificaciones/mensajería
│       │   ├── vehiculos/    # Gestión de vehículos del usuario
│       │   └── workshops/    # Directorio y asignación de talleres
│       └── shared/       # Componentes reutilizables
│           └── widgets/  # Botones, inputs, tarjetas genéricas
├── pubspec.yaml          # Dependencias (paquetes) y assets
└── web/                  # Soporte para web (PWA)
```

## Detalle de Módulos (Features)

### 1. `auth`
*   **Propósito**: Autenticación de usuario.
*   **Componentes**: Pantallas de Login y Registro.
*   **Lógica**: Gestión de estado de sesión, almacenamiento seguro de tokens (usando `flutter_secure_storage`).

### 2. `emergencies`
*   **Propósito**: Gestión del ciclo de vida de una emergencia.
*   **Componentes**: Formulario de reporte, visualización de estado en tiempo real (mapas/listas).
*   **Lógica**: Integración con servicios de geolocalización, comunicación vía WebSockets para actualizaciones.

### 3. `home`
*   **Propósito**: Pantalla inicial y navegación principal.
*   **Componentes**: Dashboard de control, accesos rápidos.

### 4. `vehiculos`
*   **Propósito**: Inventario personal del usuario.
*   **Componentes**: Listado de vehículos registrados, detalles por placa.

### 5. `workshops`
*   **Propósito**: Interacción con los talleres de servicio.
*   **Componentes**: Directorio de talleres, estado de reparaciones.

## Núcleo (`core`)
*   **`network/`**: Contiene la implementación del cliente API (normalmente usando `Dio` o `http`), manejo de errores globales y autenticación de peticiones (headers con JWT).
*   **`theme/`**: Definición de la identidad visual de la app (paleta de colores, tipografía, estilos de componentes para mantener consistencia).
