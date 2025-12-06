# Gestor de Turnos Inteligente

**Resumen:**

Aplicación web para la gestión de turnos médicos pensada para clínicas pequeñas. Backend en Flask (Python) que usa Supabase (Postgres) como base de datos; frontend en HTML/CSS/JavaScript (vanilla). Incluye CRUD de pacientes, médicos y especialidades, gestión de turnos con validaciones de solapamiento y horarios, y reportes básicos.

**Tecnologías principales:**

- Python 3.8+ (Flask)
- Supabase (Postgres + RLS)
- JavaScript (vanilla)
- GitHub Pages (frontend estático)
- Railway / Heroku / similar (backend)

**Estructura del repositorio (resumen):**

- `app.py` — punto de entrada Flask
- `config/database.py` — inicializa cliente Supabase
- `routes/` — blueprints de la API (pacientes, medicos, turnos, especialidades, reportes)
- `services/` — lógica de negocio y consultas a Supabase
- `static/` — frontend (index.html, app.js, styles.css)
- `supabase/migrations/` — script SQL para crear esquema
- `seed_data.py` — script para poblar datos de prueba

**Tablas principales (definidas en `supabase/migrations/*.sql`):**

- `especialidades` (id, nombre, descripcion, activo, created_at)
- `medicos` (id, nombre, apellido, matricula, id_especialidad, telefono, email, activo)
- `pacientes` (id, dni, nombre, apellido, fecha_nacimiento, telefono, email, direccion, obra_social)
- `turnos` (id, id_paciente, id_medico, fecha_hora, duracion_minutos, estado, motivo_consulta, observaciones)
- `horarios_medicos` (id, id_medico, dia_semana, hora_inicio, hora_fin, activo)

> NOTA: La migración incluye índices, triggers para actualizar timestamps y políticas de Row Level Security (RLS). En desarrollo puedes desactivar RLS o ajustar políticas si necesitas accesos sin autenticación.

**Variables de entorno (.env):**

- `VITE_SUPABASE_URL` = `https://<tu-project>.supabase.co` (Project URL)
- `VITE_SUPABASE_SUPABASE_ANON_KEY` = `anon public key` (clave pública para frontend)

Para el backend (operaciones administrativas o scripts que necesitan permisos elevados) usa en el entorno del servidor la `service_role` key (service_role secret) como variable segura, y NUNCA la expongas en frontend.

**Instalación local (rápida):**

1. Crear y activar entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Configurar `.env` con `VITE_SUPABASE_URL` y `VITE_SUPABASE_SUPABASE_ANON_KEY` (y opcionalmente `SERVICE_ROLE_KEY` para scripts locales si lo necesitas).

4. En Supabase → SQL Editor: pegar y ejecutar `supabase/migrations/20251127030314_create_turnos_schema.sql` para crear tablas y datos iniciales.

5. Ejecutar datos de prueba (opcional, requiere service_role si las políticas RLS lo exigen):

```powershell
python seed_data.py
```

6. Levantar backend:

```powershell
python app.py
```

API disponible en `http://localhost:5000` (o en la URL de tu host cuando despliegues).

Frontend: abrir `static/index.html` o servirlo como sitio estático (GitHub Pages o `python -m http.server 8080` dentro de `static/`).

**Endpoints principales (resumen):**

- `GET /api/health` — health check
- `GET/POST /api/pacientes` — listar/crear pacientes
- `GET/PUT /api/pacientes/<id>` — obtener/actualizar paciente
- `GET/POST /api/medicos` — gestión de médicos
- `GET/POST /api/especialidades` — gestión de especialidades
- `GET/POST /api/turnos` — gestión de turnos
- `GET /api/reportes` — generar reportes

(Revisar `routes/` para la implementación exacta y parámetros aceptados.)

**Despliegue recomendado:**

- Backend: Railway (auto-detecta Flask), Heroku o similar.
  - Subir repo a GitHub (ya hecho).
  - Conectar Railway a tu repo y configurar variables de entorno:
    - `VITE_SUPABASE_URL` y `VITE_SUPABASE_SUPABASE_ANON_KEY` o `SERVICE_ROLE_KEY` si el backend necesita permisos elevados.
  - Add `Procfile` con `web: python app.py` (ya incluido en repo).

- Frontend: GitHub Pages
  - Settings → Pages → Branch `main` → Folder `/static`
  - URL resultante: `https://<usuario>.github.io/<repo>/`
  - Update `static/app.js` para apuntar al `API_URL` público del backend desplegado.

**Seguridad y buenas prácticas:**

- Nunca exponer `service_role` key en el frontend. Usar `anon` para cliente público.
- En producción, habilitar HTTPS, logging y backups.
- Implementar autenticación (JWT) para permisos y trazabilidad.

**Comprobaciones y solución de problemas comunes:**

- Error `supabase_url is required` → revisar `.env` y variables en entorno del servidor.
- Error `No module named 'flask'` → ejecutar `pip install -r requirements.txt` en el entorno correcto.
- Error relacionado con RLS → desactivar RLS temporalmente en Supabase o ajustar políticas para desarrollo.

**Siguientes mejoras sugeridas:**

- Añadir autenticación y roles (Administrador / Recepcionista / Médico).
- Implementar tests unitarios e integración (pytest).
- Añadir CI/CD para despliegue automático desde `main`.
- Exportar reportes a PDF y agregar notificaciones por email/SMS.

---

Archivo creado: `PROJECT_DESCRIPTION.md` en la raíz del repositorio.

Si quieres, puedo:
- ajustar el contenido (más/menos detalle),
- generar una versión para `README.md` o reemplazar el existente,
- actualizar `static/app.js` para apuntar al URL público de tu backend desplegado.

Dime qué prefieres y lo hago.