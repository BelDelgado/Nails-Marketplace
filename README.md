💅 Nails Marketplace

Plataforma colaborativa para la compra, venta e intercambio de insumos para uñas en comunidades locales.

<img width="300" height="300" alt="Image" src="![Image](https://github.com/user-attachments/assets/aea42c54-b8e9-4e7f-8027-52581c85d7be)" />

<img width="300" height="300" alt="Image" src="![Image](https://github.com/user-attachments/assets/a927c785-5dce-401c-aafe-893ee12d1612)" />


📑 Tabla de Contenidos

Introducción
Tecnologías
Contacto
Roadmap
Equipo


🎯 Introducción
"Unas Bellas - Insumos de uñas" es una plataforma web diseñada para manicuristas, nail artists y entusiastas de la belleza que deseen:

✅ Vender insumos de uñas (esmaltes, geles, herramientas, decoraciones)
✅ Comprar productos de calidad a precios competitivos
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

Mobile

Kivy 2.3.0 - Framework multiplataforma para Python
KivyMD 1.2.0 - Material Design para Kivy
Plyer - Acceso a funciones del dispositivo (GPS, cámara)

Servicios Externos

MercadoPago API - Procesamiento de pagos
MongoDB Atlas - Base de datos NoSQL en la nube
Cloudinary - CDN para imágenes
Mapbox/Leaflet - Servicios de mapas


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

🚧 Fase 2 (En desarrollo)

 Chat en tiempo real con WebSockets
 Integración de pagos con MercadoPago
 Geolocalización y mapas
 Sistema de notificaciones

📋 Fase 3 (Planeada)

 App móvil con Kivy
 Panel de analytics para vendedores
 Integración con redes sociales

 <p align="center">
  Hecho con ❤️ por Belén
</p>