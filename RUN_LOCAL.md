# Ejecutar localmente - Gestor de Turnos Inteligente

Este documento explica cómo levantar el proyecto localmente desde Windows (PowerShell). Incluye tres opciones: usar Supabase cloud (recomendado), usar Postgres local con Docker y por qué XAMPP (MySQL) en puerto 3307 no es directamente compatible.

---

## Requisitos previos

- Python 3.8+ instalado
- `pip`
- Git (opcional)
- Si usas Docker: Docker Desktop
- Cuenta de Supabase (recomendado)

---

## Opciones

### Opción A (Recomendada): usar Supabase cloud (más sencillo)

1. Crea un proyecto en Supabase (https://app.supabase.com)
2. En **Settings → API** copia:
   - `Project URL` (ej: `https://xxxx.supabase.co`) → ponemos en `VITE_SUPABASE_URL`
   - `anon public` key (anon) → `VITE_SUPABASE_SUPABASE_ANON_KEY` (para frontend)
   - `service_role secret` → `SUPABASE_SERVICE_ROLE` (para backend local y scripts)

3. En la raíz del repo crea/edita `.env` con:

```
VITE_SUPABASE_URL=https://tu-project.supabase.co
VITE_SUPABASE_SUPABASE_ANON_KEY=eyJ... (anon public key)
SUPABASE_SERVICE_ROLE=eyJ... (service_role secret - SOLO en el servidor o local dev)
```

4. Crear y activar venv, instalar deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

5. (Opcional) Ejecutar migración en Supabase: en SQL Editor pega `supabase/migrations/20251127030314_create_turnos_schema.sql` y ejecútalo.

6. Poblar datos de prueba (si tu RLS requiere permisos elevados, usa `SUPABASE_SERVICE_ROLE` definido):

```powershell
python seed_data.py
```

7. Ejecutar backend:

```powershell
python app.py
```

Abre `http://localhost:5000` para la API y abre `static/index.html` (o sirve `static/` con `python -m http.server 8080`).

---

### Opción B: usar PostgreSQL local con Docker

Si no quieres usar Supabase cloud, puedes levantar Postgres localmente y aplicar la migración.

1. Levantar Postgres con Docker (puerto por defecto 5432):

```powershell
docker run --name gt_postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=gestor_turnos -p 5432:5432 -d postgres:15
```

2. Conecta a la DB y crea tablas ejecutando el SQL de `supabase/migrations/20251127030314_create_turnos_schema.sql`. Ten en cuenta que el SQL usa funciones/extensions de Postgres (ej `gen_random_uuid()`), por lo que puede requerir `pgcrypto` o adaptar el SQL.

3. Ajusta `config/database.py` y la librería usada (este proyecto usa cliente de Supabase, por lo que cambiar a conexión directa a Postgres requiere reescribir `services/*` para usar `psycopg2` o `asyncpg`).

> Nota: Opción B requiere cambios no triviales en los servicios; por eso recomendamos Opción A.

---

### Opción C (NO recomendado): intentar usar XAMPP (MySQL) - puerto 3307

- XAMPP proporciona MySQL/MariaDB (usualmente en `3306` o en tu caso `3307`).
- El proyecto actual está escrito para Postgres/Supabase (SQL y funciones específicas). Cambiar a MySQL implica:
  - Convertir `supabase/migrations/*.sql` a sintaxis MySQL
  - Reescribir el acceso a datos en `services/*` (queries, joins, funciones)
  - Cambiar dependencias Python (usar `mysql-connector-python` o `PyMySQL`)
- Por lo tanto no es práctico para levantar el proyecto tal cual.

Si aun así quieres usar XAMPP, dime y te doy una lista de los cambios necesarios, pero no es la opción recomendada.

---

## Notas sobre puertos y XAMPP 3307

- Tu XAMPP usa puerto `3307` para MySQL; eso no interfiere con el puerto `5000` donde corre Flask ni con `5432` (Postgres). Si usas Docker/PG local, asegúrate de mapear puertos para evitar colisiones.

## Servir frontend desde XAMPP (Apache)

Si quieres acceder a la app con la URL `http://localhost/Gestor_Turnos_Inteligente/` usando XAMPP:

1. Asegúrate de que la carpeta del proyecto está en `C:\xampp\htdocs\Gestor_Turnos_Inteligente` (ya lo está).
2. He añadido un `index.html` en la raíz que redirige automáticamente a `static/index.html`. De esa forma `http://localhost/Gestor_Turnos_Inteligente/` abrirá la interfaz.
3. Inicia Apache desde el panel de XAMPP.
4. Inicia el backend Flask como en los pasos previos (`python app.py`). El frontend hará peticiones a `http://localhost:5000/api`.

Nota sobre CORS: la aplicación Flask ya tiene `CORS(app)` configurado; eso permite que el frontend (servido por Apache en `localhost`) haga peticiones al backend en `localhost:5000`.

### Opción avanzada: usar Apache como proxy inverso (evita CORS y mantiene una sola URL)

Si prefieres que la API esté disponible bajo la misma URL (por ejemplo `http://localhost/Gestor_Turnos_Inteligente/api`), habilita `mod_proxy` en Apache y añade algo como esto en `httpd.conf` o en un VirtualHost:

```
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_http_module modules/mod_proxy_http.so

ProxyPass "/Gestor_Turnos_Inteligente/api" "http://127.0.0.1:5000/api"
ProxyPassReverse "/Gestor_Turnos_Inteligente/api" "http://127.0.0.1:5000/api"
```

Después reinicia Apache. Con esto, el frontend puede usar `API_URL = '/Gestor_Turnos_Inteligente/api'` sin problemas de CORS.

---

## Resumen rápido de comandos (PowerShell)

```powershell
# Activar entorno
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar deps
pip install -r requirements.txt

# Ejecutar app
python app.py

# Servir frontend (opcional)
cd static
python -m http.server 8080
```

---

Si quieres, hago una copia de este contenido en `README.md` o lo guardo como `RUN_LOCAL.md` (ya lo agregué al repo). También puedo ayudarte a probar `python app.py` aquí y revisar errores si pegas las credenciales de Supabase (service_role) o si prefieres que use la anon key y ajustamos RLS temporalmente.
