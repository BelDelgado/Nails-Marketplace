💅 Nails Marketplace

Plataforma colaborativa para la compra, venta e intercambio de insumos para uñas en comunidades locales.

<p align="center">
  <img src="docs/images/LogoUnasBellas.png" alt="Logo" width="300"/>
</p>


📑 Tabla de Contenidos

Introducción
Tecnologías
Arquitectura
Contribución
Roadmap
Equipo


🎯 Introducción
Nails Marketplace es una plataforma web y móvil diseñada para manicuristas, nail artists y entusiastas de la belleza que deseen:

✅ Vender insumos de uñas (esmaltes, geles, herramientas, decoraciones)
✅ Comprar productos de calidad a precios competitivos
✅ Intercambiar artículos con otros miembros de la comunidad
✅ Conectar con vendedores locales mediante geolocalización
✅ Comunicarse en tiempo real a través de chat integrado

🛠️ Tecnologías
Backend (API REST)

Django 5.2.8 - Framework web robusto
Django REST Framework 3.15.2 - API RESTful
Django Channels 4.2.0 - WebSockets para chat en tiempo real
PostgreSQL - Base de datos relacional (producción)
MongoDB Atlas - Almacenamiento de imágenes y geodatos
Redis - Caché y broker para Celery
Celery - Tareas asíncronas (emails, notificaciones)

Frontend Web

Django Templates - Renderizado del lado del servidor
Bootstrap 5 - Framework CSS responsivo
JavaScript (ES6+) - Interactividad del cliente
Leaflet.js - Mapas interactivos
WebSockets - Chat en tiempo real

Mobile App

Kivy 2.3.0 - Framework multiplataforma para Python
KivyMD 1.2.0 - Material Design para Kivy
Plyer - Acceso a funciones del dispositivo (GPS, cámara)

Servicios Externos

MercadoPago API - Procesamiento de pagos
MongoDB Atlas - Base de datos NoSQL en la nube
Cloudinary (opcional) - CDN para imágenes
Mapbox/Leaflet - Servicios de mapas

🏗️ Arquitectura
nails-marketplace/
│
├── backend/                    # API REST con Django
│   ├── apps/
│   │   ├── users/             # Autenticación y perfiles
│   │   ├── products/          # Catálogo de productos
│   │   ├── chat/              # Mensajería en tiempo real
│   │   ├── payments/          # Integración de pagos
│   │   ├── invoices/          # Facturación
│   │   └── locations/         # Geolocalización
│   ├── config/                # Configuración Django
│   └── manage.py
│
├── frontend/                  # Aplicación web Django
│   ├── templates/             # HTML templates
│   ├── static/                # CSS, JS, imágenes
│   └── manage.py
│
├── mobile/                    # App móvil Kivy
│   ├── app/
│   │   ├── screens/           # Pantallas de la app
│   │   ├── api/               # Cliente API REST
│   │   └── main.py
│   └── buildozer.spec         # Configuración Android
│
└── docs/                      # Documentación

📄 Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

📞 Contacto
Para preguntas, sugerencias o reportar problemas:

Email: contacto@nailsmarketplace.com
GitHub Issues: Crear issue

🔮 Roadmap
✅ Fase 1 (Completada)

 Sistema de autenticación con JWT
 CRUD de productos
 Sistema de categorías
 Favoritos y reseñas
 API REST documentada

🚧 Fase 2 (En desarrollo)

 Chat en tiempo real con WebSockets
 Integración de pagos con MercadoPago
 Geolocalización y mapas
 Sistema de notificaciones

📋 Fase 3 (Planeada)

 App móvil con Kivy
 Panel de analytics para vendedores
 Sistema de cupones y descuentos
 Integración con redes sociales

 <p align="center">
  Hecho con ❤️ por el Bell
</p>