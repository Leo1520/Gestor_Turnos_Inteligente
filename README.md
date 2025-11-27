# 🏥 Gestor de Turnos Inteligente - Clínica

Sistema completo de gestión de turnos médicos para clínicas pequeñas, desarrollado con arquitectura de 3 capas, Flask (backend), JavaScript vanilla (frontend) y Supabase (base de datos PostgreSQL).

---

## 📋 Características Principales

✅ Gestión completa de pacientes (CRUD)
✅ Gestión de médicos y especialidades
✅ Sistema de turnos con validación de disponibilidad
✅ Prevención de solapamiento de turnos
✅ Horarios laborales configurados (L-V 8-18hs, Sáb 8-13hs)
✅ Límite de 3 turnos pendientes por paciente
✅ Cancelación de turnos con 2 horas de anticipación
✅ Búsqueda y filtrado avanzado
✅ Reportes diarios con estadísticas
✅ Historial de turnos por paciente
✅ Interfaz responsive y moderna
✅ Paginación de resultados

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────┐
│  FRONTEND (HTML/CSS/JS)         │
│  - Interfaz de usuario          │
│  - Validaciones cliente         │
│  - Búsqueda en tiempo real      │
└─────────────────────────────────┘
            ↓ REST API
┌─────────────────────────────────┐
│  BACKEND (Flask/Python)         │
│  - Routes (controladores)       │
│  - Services (lógica negocio)    │
│  - Validaciones servidor        │
└─────────────────────────────────┘
            ↓ Supabase Client
┌─────────────────────────────────┐
│  BASE DE DATOS (Supabase)       │
│  - PostgreSQL                   │
│  - Row Level Security (RLS)     │
│  - Índices optimizados          │
└─────────────────────────────────┘
```

---

## 📊 Modelo de Datos

### Tablas Principales:

1. **especialidades**: Catálogo de especialidades médicas
2. **medicos**: Registro de médicos con especialidad
3. **pacientes**: Datos completos de pacientes
4. **turnos**: Turnos médicos programados
5. **horarios_medicos**: Horarios de atención por médico

### Relaciones:
- Un médico tiene una especialidad
- Un turno pertenece a un paciente y un médico
- Un paciente puede tener múltiples turnos
- Un médico puede tener múltiples turnos

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.8+
- pip
- Cuenta de Supabase (ya configurada)

### Paso 1: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 2: Configurar Variables de Entorno

El archivo `.env` ya está configurado con las credenciales de Supabase.

### Paso 3: Iniciar el Servidor Backend

```bash
python app.py
```

El servidor Flask estará disponible en: `http://localhost:5000`

### Paso 4: Abrir la Aplicación Frontend

Abre el archivo `static/index.html` en tu navegador o usa un servidor web local:

```bash
# Opción 1: Python HTTP Server
cd static
python -m http.server 8080

# Opción 2: Abrir directamente
# Navega a: file:///ruta/al/proyecto/static/index.html
```

La aplicación estará disponible en: `http://localhost:8080`

---

## 📂 Estructura del Proyecto

```
project/
├── app.py                      # Punto de entrada Flask
├── requirements.txt            # Dependencias Python
├── .env                        # Variables de entorno
│
├── config/
│   └── database.py            # Configuración Supabase
│
├── services/                   # Lógica de negocio
│   ├── pacientes_service.py
│   ├── medicos_service.py
│   ├── turnos_service.py
│   ├── especialidades_service.py
│   └── reportes_service.py
│
├── routes/                     # Controladores API
│   ├── pacientes_routes.py
│   ├── medicos_routes.py
│   ├── turnos_routes.py
│   ├── especialidades_routes.py
│   └── reportes_routes.py
│
├── static/                     # Frontend
│   ├── index.html             # Interfaz principal
│   ├── styles.css             # Estilos
│   └── app.js                 # Lógica JavaScript
│
├── supabase/
│   └── migrations/            # Migraciones BD
│
├── API_DOCUMENTATION.md        # Documentación API
├── TESTING_GUIDE.md           # Guía de pruebas
└── README.md                  # Este archivo
```

---

## 🔌 Uso de la API

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Crear un paciente
```bash
curl -X POST http://localhost:5000/api/pacientes \
  -H "Content-Type: application/json" \
  -d '{
    "dni": "12345678",
    "nombre": "Juan",
    "apellido": "Pérez",
    "fecha_nacimiento": "1990-05-15",
    "telefono": "1145678900",
    "email": "juan@email.com",
    "direccion": "Av. Ejemplo 123",
    "obra_social": "OSDE"
  }'
```

### Listar turnos del día
```bash
curl "http://localhost:5000/api/turnos?fecha_desde=2024-01-15T00:00:00&fecha_hasta=2024-01-15T23:59:59"
```

Ver `API_DOCUMENTATION.md` para la documentación completa de endpoints.

---

## 💻 Uso del Frontend

### 1. Gestión de Turnos
- Click en "Turnos" en el menú
- Click en "+ Nuevo Turno"
- Seleccionar paciente (o crear uno nuevo)
- Seleccionar especialidad
- Seleccionar médico
- Elegir fecha y ver horarios disponibles
- Completar motivo y guardar

### 2. Gestión de Pacientes
- Click en "Pacientes" en el menú
- Click en "+ Nuevo Paciente"
- Completar formulario con datos requeridos
- Usar el buscador para encontrar pacientes
- Click en "Historial" para ver turnos anteriores

### 3. Gestión de Médicos
- Click en "Médicos" en el menú
- Click en "+ Nuevo Médico"
- Asignar especialidad
- Activar/Desactivar médicos según disponibilidad

### 4. Reportes
- Click en "Reportes" en el menú
- Seleccionar fecha
- Click en "Generar Reporte"
- Ver estadísticas y detalle de turnos

---

## 🧪 Ejecutar Pruebas

```bash
# Instalar dependencias de testing
pip install pytest pytest-cov

# Ejecutar tests unitarios
pytest tests/unit/ -v

# Ver cobertura de código
pytest --cov=services --cov-report=html
```

Ver `TESTING_GUIDE.md` para la guía completa de pruebas.

---

## 🔒 Seguridad

El sistema implementa:

✅ Row Level Security (RLS) en todas las tablas
✅ Validación de datos en backend y frontend
✅ Prevención de inyección SQL con Supabase ORM
✅ Validación de DNI y matrícula únicos
✅ Escapado de datos de entrada

**Nota**: Para producción se recomienda implementar:
- Autenticación de usuarios (JWT)
- HTTPS obligatorio
- Rate limiting
- Logs de auditoría

---

## 📈 Rendimiento

- Respuesta API: < 2 segundos
- Índices en campos de búsqueda frecuente
- Paginación de resultados (10 items por página)
- Consultas optimizadas con JOINs eficientes

---

## 🛠️ Tecnologías Utilizadas

**Backend**:
- Python 3.8+
- Flask 3.0.0
- Flask-CORS 4.0.0
- Supabase Client 2.3.0

**Frontend**:
- HTML5
- CSS3 (diseño moderno sin frameworks)
- JavaScript ES6+ (vanilla)

**Base de Datos**:
- PostgreSQL (vía Supabase)
- Row Level Security
- Triggers y funciones

---

## 👥 Roles de Usuario (Fase 1)

Actualmente el sistema no implementa autenticación. Todos los usuarios tienen acceso completo.

**Roles sugeridos para v2.0**:
- **Administrador**: Acceso completo
- **Recepcionista**: Gestión de turnos y pacientes
- **Médico**: Solo visualización de su agenda

---

## 📝 Reglas de Negocio Implementadas

1. ✅ Duración de turno: 30 minutos (configurable)
2. ✅ No solapamiento de turnos por médico
3. ✅ Horario laboral: L-V 8-18hs, Sáb 8-13hs
4. ✅ Máximo 3 turnos pendientes por paciente
5. ✅ Cancelación con 2 horas de anticipación
6. ✅ Estados: pendiente, atendido, cancelado, ausente
7. ✅ DNI único por paciente
8. ✅ Matrícula única por médico

---

## 🚧 Roadmap Futuro (v2.0)

- [ ] Sistema de autenticación (JWT)
- [ ] Notificaciones por email/SMS
- [ ] Recordatorios automáticos
- [ ] Vista de agenda por médico
- [ ] Exportación de reportes a PDF
- [ ] Dashboard con gráficos estadísticos
- [ ] App móvil para pacientes
- [ ] Integración con obras sociales
- [ ] Sistema de pagos online
- [ ] Telemedicina (videollamadas)

---

## 🐛 Solución de Problemas

### Error: "Cannot connect to database"
- Verificar que las credenciales en `.env` sean correctas
- Verificar conexión a internet

### Error: "CORS policy"
- Asegurarse de que Flask-CORS esté instalado
- Verificar que el servidor Flask esté corriendo

### Error: "No module named 'supabase'"
- Ejecutar: `pip install -r requirements.txt`

---

## 📞 Soporte

Para reportar bugs o solicitar funcionalidades, crear un issue en el repositorio.

---

## 📄 Licencia

Este proyecto es software libre para uso en clínicas pequeñas. Desarrollado como demostración educativa.

---

## 👨‍💻 Autor

**Sistema desarrollado por**: Asistente IA
**Fecha**: 2024
**Versión**: 1.0.0

---

## 🙏 Agradecimientos

- Supabase por la infraestructura de base de datos
- Flask por el framework web minimalista
- Comunidad open-source
