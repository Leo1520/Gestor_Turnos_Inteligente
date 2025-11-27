# Documentación API - Gestor de Turnos Inteligente

## Información General
- **Base URL**: `http://localhost:5000/api`
- **Formato**: JSON
- **Autenticación**: No implementada en v1.0

---

## Endpoints

### 1. PACIENTES

#### Listar pacientes
```
GET /api/pacientes
Query params (opcionales):
  - dni: string
  - nombre: string
  - apellido: string

Response 200:
{
  "data": [
    {
      "id": "uuid",
      "dni": "12345678",
      "nombre": "Juan",
      "apellido": "Pérez",
      "fecha_nacimiento": "1990-05-15",
      "telefono": "1145678900",
      "email": "juan@email.com",
      "direccion": "Av. Ejemplo 123",
      "obra_social": "OSDE",
      "created_at": "2024-01-01T10:00:00"
    }
  ]
}
```

#### Crear paciente
```
POST /api/pacientes
Body:
{
  "dni": "12345678",
  "nombre": "Juan",
  "apellido": "Pérez",
  "fecha_nacimiento": "1990-05-15",
  "telefono": "1145678900",
  "email": "juan@email.com",
  "direccion": "Av. Ejemplo 123",
  "obra_social": "OSDE"
}

Response 201:
{
  "data": { ... },
  "message": "Paciente creado exitosamente"
}

Response 400 (error validación):
{
  "error": "El campo dni es requerido"
}

Response 409 (duplicado):
{
  "error": "Ya existe un paciente con ese DNI"
}
```

#### Obtener paciente específico
```
GET /api/pacientes/{id}

Response 200:
{
  "data": { ... }
}

Response 404:
{
  "error": "Paciente no encontrado"
}
```

#### Actualizar paciente
```
PUT /api/pacientes/{id}
Body: campos a actualizar

Response 200:
{
  "data": { ... },
  "message": "Paciente actualizado"
}
```

#### Historial de turnos
```
GET /api/pacientes/{id}/historial

Response 200:
{
  "data": [
    {
      "id": "uuid",
      "fecha_hora": "2024-01-15T10:00:00",
      "estado": "atendido",
      "medicos": {
        "nombre": "María",
        "apellido": "González",
        "especialidades": {
          "nombre": "Cardiología"
        }
      }
    }
  ]
}
```

---

### 2. MÉDICOS

#### Listar médicos
```
GET /api/medicos?activos=true

Response 200:
{
  "data": [
    {
      "id": "uuid",
      "nombre": "María",
      "apellido": "González",
      "matricula": "MN12345",
      "telefono": "1156789000",
      "email": "dra.gonzalez@email.com",
      "activo": true,
      "especialidades": {
        "nombre": "Cardiología"
      }
    }
  ]
}
```

#### Crear médico
```
POST /api/medicos
Body:
{
  "nombre": "María",
  "apellido": "González",
  "matricula": "MN12345",
  "id_especialidad": "uuid",
  "telefono": "1156789000",
  "email": "dra.gonzalez@email.com"
}

Response 201:
{
  "data": { ... },
  "message": "Médico creado exitosamente"
}

Response 409:
{
  "error": "Ya existe un médico con esa matrícula"
}
```

#### Médicos por especialidad
```
GET /api/medicos/especialidad/{id_especialidad}

Response 200:
{
  "data": [ ... ]
}
```

---

### 3. TURNOS

#### Listar turnos
```
GET /api/turnos?fecha_desde=2024-01-01&fecha_hasta=2024-01-31&id_medico=uuid&estado=pendiente

Response 200:
{
  "data": [
    {
      "id": "uuid",
      "fecha_hora": "2024-01-15T10:00:00",
      "duracion_minutos": 30,
      "estado": "pendiente",
      "motivo_consulta": "Control",
      "observaciones": "",
      "pacientes": {
        "dni": "12345678",
        "nombre": "Juan",
        "apellido": "Pérez",
        "telefono": "1145678900"
      },
      "medicos": {
        "nombre": "María",
        "apellido": "González",
        "especialidades": {
          "nombre": "Cardiología"
        }
      }
    }
  ]
}
```

#### Crear turno
```
POST /api/turnos
Body:
{
  "id_paciente": "uuid",
  "id_medico": "uuid",
  "fecha_hora": "2024-01-15T10:00:00",
  "duracion_minutos": 30,
  "motivo_consulta": "Control anual"
}

Response 201:
{
  "data": { ... },
  "message": "Turno creado exitosamente"
}

Response 400:
{
  "error": "El turno está fuera del horario laboral"
}

Response 409:
{
  "error": "El médico no está disponible en ese horario"
}
```

#### Consultar disponibilidad
```
GET /api/turnos/disponibilidad?id_medico=uuid&fecha=2024-01-15

Response 200:
{
  "data": ["08:00", "08:30", "09:00", "09:30", ...]
}
```

#### Actualizar turno
```
PUT /api/turnos/{id}
Body:
{
  "estado": "atendido",
  "observaciones": "Paciente atendido correctamente"
}

Response 200:
{
  "data": { ... },
  "message": "Turno actualizado"
}
```

#### Cancelar turno
```
PUT /api/turnos/{id}/cancelar

Response 200:
{
  "data": { ... },
  "message": "Turno cancelado exitosamente"
}

Response 400:
{
  "error": "Solo se puede cancelar con al menos 2 horas de anticipación"
}
```

---

### 4. ESPECIALIDADES

#### Listar especialidades
```
GET /api/especialidades?activas=true

Response 200:
{
  "data": [
    {
      "id": "uuid",
      "nombre": "Cardiología",
      "descripcion": "Especialidad enfocada en el sistema cardiovascular",
      "activo": true
    }
  ]
}
```

#### Crear especialidad
```
POST /api/especialidades
Body:
{
  "nombre": "Neurología",
  "descripcion": "Diagnóstico y tratamiento del sistema nervioso"
}

Response 201:
{
  "data": { ... },
  "message": "Especialidad creada"
}
```

---

### 5. REPORTES

#### Reporte diario
```
GET /api/reportes/diario?fecha=2024-01-15

Response 200:
{
  "data": {
    "fecha": "2024-01-15",
    "turnos": [ ... ],
    "estadisticas": {
      "total": 25,
      "pendientes": 5,
      "atendidos": 18,
      "cancelados": 1,
      "ausentes": 1,
      "tasa_asistencia": 72.0
    }
  }
}
```

#### Reporte por médico
```
GET /api/reportes/medico/{id_medico}?fecha_desde=2024-01-01&fecha_hasta=2024-01-31

Response 200:
{
  "data": {
    "turnos": [ ... ],
    "estadisticas": { ... }
  }
}
```

---

## Códigos de Estado HTTP

- **200 OK**: Solicitud exitosa
- **201 Created**: Recurso creado exitosamente
- **400 Bad Request**: Error en validación de datos
- **404 Not Found**: Recurso no encontrado
- **409 Conflict**: Conflicto (duplicado, solapamiento)
- **500 Internal Server Error**: Error del servidor

---

## Manejo de Errores

Todos los errores retornan un objeto JSON:
```json
{
  "error": "Descripción del error"
}
```

---

## Notas de Implementación

1. **Validaciones del Backend**:
   - DNI único por paciente
   - Matrícula única por médico
   - No solapamiento de turnos
   - Horarios laborales válidos
   - Máximo 3 turnos pendientes por paciente
   - Cancelación con 2 horas de anticipación

2. **Estados de Turno**:
   - `pendiente`: Turno programado
   - `atendido`: Paciente fue atendido
   - `cancelado`: Turno cancelado
   - `ausente`: Paciente no asistió

3. **Horarios Laborales**:
   - Lunes a Viernes: 08:00 - 18:00
   - Sábados: 08:00 - 13:00
   - Domingos: Cerrado
