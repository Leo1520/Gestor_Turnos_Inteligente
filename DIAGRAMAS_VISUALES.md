# 📐 DIAGRAMAS VISUALES DEL SISTEMA

## 1. ARQUITECTURA GENERAL

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIOS FINALES                        │
│  (Recepcionista, Administrador, Personal Médico)                │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                     HTTP/HTTPS │ REST API
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                         │
│                         (Frontend)                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  index.html  │  │  styles.css  │  │    app.js    │          │
│  │              │  │              │  │              │          │
│  │ • Formularios│  │ • Diseño     │  │ • Validación │          │
│  │ • Tablas     │  │ • Responsive │  │ • AJAX calls │          │
│  │ • Modales    │  │ • Animaciones│  │ • Búsqueda   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    JSON/HTTP  │
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     CAPA DE LÓGICA                              │
│                        (Backend)                                 │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                     app.py (Flask)                      │    │
│  │                   Puerto: 5000                          │    │
│  └────────────────────────────────────────────────────────┘    │
│                               │                                  │
│         ┌─────────────────────┼─────────────────────┐           │
│         │                     │                     │           │
│    ┌────▼────┐          ┌────▼────┐          ┌────▼────┐       │
│    │ ROUTES  │          │SERVICES │          │ CONFIG  │       │
│    │         │          │         │          │         │       │
│    │ • /api/ │──calls──▶│Business │          │Database │       │
│    │pacientes│          │ Logic   │          │ Setup   │       │
│    │ • /api/ │          │         │          │         │       │
│    │ medicos │          │Validation│          │Supabase │       │
│    │ • /api/ │          │         │          │ Client  │       │
│    │ turnos  │          │Security │          │         │       │
│    │ • /api/ │          │         │          │         │       │
│    │reportes │          │Queries  │          │         │       │
│    └─────────┘          └─────────┘          └─────────┘       │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                      SQL     │  Supabase Client
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                      CAPA DE DATOS                              │
│                   (PostgreSQL/Supabase)                         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │especialidades│  │   medicos    │  │  pacientes   │          │
│  │      5       │  │              │  │              │          │
│  │   registros  │  │   FK:        │  │  DNI único   │          │
│  │  precargados │  │id_especialid.│  │              │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                   │
│         │    ┌────────────▼─────────────────▼────┐              │
│         └───▶│           turnos                  │              │
│              │                                    │              │
│              │  • Estado (enum)                   │              │
│              │  • Validaciones automáticas        │              │
│              │  • Triggers de actualización       │              │
│              └────────────────────────────────────┘              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 Row Level Security                       │  │
│  │  • 15 políticas activas                                  │  │
│  │  • Acceso restringido por autenticación                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. FLUJO DE CREACIÓN DE TURNO

```
USUARIO                 FRONTEND              BACKEND               BASE DE DATOS
   │                       │                     │                      │
   │ 1. Click "Nuevo       │                     │                      │
   │    Turno"             │                     │                      │
   ├──────────────────────▶│                     │                      │
   │                       │                     │                      │
   │                       │ 2. Carga pacientes  │                      │
   │                       ├────────────────────▶│ GET /api/pacientes   │
   │                       │                     ├─────────────────────▶│
   │                       │                     │                      │
   │                       │                     │      pacientes[]     │
   │                       │   pacientes[]       │◀─────────────────────┤
   │                       │◀────────────────────┤                      │
   │   Selecciona paciente │                     │                      │
   │◀──────────────────────┤                     │                      │
   │                       │                     │                      │
   │ 3. Selecciona         │                     │                      │
   │    especialidad       │                     │                      │
   ├──────────────────────▶│                     │                      │
   │                       │ 4. Filtra médicos   │                      │
   │                       ├────────────────────▶│ GET /api/medicos/    │
   │                       │                     │   especialidad/{id}  │
   │                       │                     ├─────────────────────▶│
   │                       │                     │                      │
   │                       │    medicos[]        │      medicos[]       │
   │                       │◀────────────────────┤◀─────────────────────┤
   │                       │                     │                      │
   │   Selecciona médico   │                     │                      │
   │   y fecha             │                     │                      │
   ├──────────────────────▶│                     │                      │
   │                       │ 5. Consulta disp.   │                      │
   │                       ├────────────────────▶│ GET /turnos/         │
   │                       │                     │   disponibilidad     │
   │                       │                     ├─────────────────────▶│
   │                       │                     │ SELECT turnos WHERE  │
   │                       │                     │  medico + fecha      │
   │                       │                     │                      │
   │                       │   horarios[]        │   turnos_ocupados    │
   │                       │◀────────────────────┤◀─────────────────────┤
   │                       │                     │                      │
   │   Muestra horarios    │                     │                      │
   │   disponibles         │                     │                      │
   │◀──────────────────────┤                     │                      │
   │                       │                     │                      │
   │ 6. Selecciona hora    │                     │                      │
   │    y confirma         │                     │                      │
   ├──────────────────────▶│                     │                      │
   │                       │ 7. Crea turno       │                      │
   │                       ├────────────────────▶│ POST /api/turnos     │
   │                       │                     │                      │
   │                       │                     │ 8. VALIDACIONES:     │
   │                       │                     │  ✓ Horario laboral   │
   │                       │                     │  ✓ No solapamiento   │
   │                       │                     │  ✓ Límite paciente   │
   │                       │                     │                      │
   │                       │                     │ 9. INSERT turno      │
   │                       │                     ├─────────────────────▶│
   │                       │                     │                      │
   │                       │                     │    turno_creado      │
   │                       │   turno_creado      │◀─────────────────────┤
   │                       │◀────────────────────┤                      │
   │                       │                     │                      │
   │   ✅ "Turno creado    │                     │                      │
   │      exitosamente"    │                     │                      │
   │◀──────────────────────┤                     │                      │
   │                       │                     │                      │
   │                       │ 10. Recarga lista   │                      │
   │                       ├────────────────────▶│ GET /api/turnos      │
   │                       │                     ├─────────────────────▶│
   │                       │   turnos[]          │     turnos[]         │
   │   Tabla actualizada   │◀────────────────────┤◀─────────────────────┤
   │◀──────────────────────┤                     │                      │
```

---

## 3. MODELO ENTIDAD-RELACIÓN

```
┌─────────────────────────────────┐
│      ESPECIALIDADES             │
│─────────────────────────────────│
│ • id (PK)                       │
│ • nombre (UNIQUE)               │
│ • descripcion                   │
│ • activo                        │
│ • created_at                    │
└────────────┬────────────────────┘
             │
             │ 1:N
             │
             ▼
┌─────────────────────────────────┐
│          MEDICOS                │
│─────────────────────────────────│
│ • id (PK)                       │
│ • nombre                        │
│ • apellido                      │
│ • matricula (UNIQUE)            │
│ • id_especialidad (FK)  ───────┘
│ • telefono                      │
│ • email                         │
│ • activo                        │
│ • created_at                    │
└────────────┬────────────────────┘
             │
             │ 1:N
             │
             ▼
        ┌────────────────────────────────┐
        │          TURNOS                │
        │────────────────────────────────│
        │ • id (PK)                      │
        │ • id_paciente (FK)  ───────┐   │
        │ • id_medico (FK)           │   │
        │ • fecha_hora               │   │
        │ • duracion_minutos         │   │
        │ • estado (enum)            │   │
        │ • motivo_consulta          │   │
        │ • observaciones            │   │
        │ • created_at               │   │
        │ • updated_at               │   │
        └────────────────────────────┘   │
             ▲                           │
             │                           │
             │ N:1                       │
             │                           │
             │                           │
┌────────────┴────────────────────┐     │
│        PACIENTES                │     │
│─────────────────────────────────│     │
│ • id (PK)     ◀──────────────────────┘
│ • dni (UNIQUE)                  │
│ • nombre                        │
│ • apellido                      │
│ • fecha_nacimiento              │
│ • telefono                      │
│ • email                         │
│ • direccion                     │
│ • obra_social                   │
│ • created_at                    │
└─────────────────────────────────┘

ADICIONAL:
┌─────────────────────────────────┐
│     HORARIOS_MEDICOS            │
│─────────────────────────────────│
│ • id (PK)                       │
│ • id_medico (FK) ────────┐      │
│ • dia_semana              │      │
│ • hora_inicio             │      │
│ • hora_fin                │      │
│ • activo                  │      │
└───────────────────────────┘      │
                                   │
        (Referencia a MEDICOS) ────┘
```

---

## 4. ESTADOS DE TURNO

```
                    ┌─────────────────┐
                    │   PENDIENTE     │◀─── Estado inicial
                    │   (amarillo)    │     al crear turno
                    └────────┬────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
    ┌────────────────┐ ┌──────────┐  ┌────────────┐
    │   ATENDIDO     │ │CANCELADO │  │  AUSENTE   │
    │    (verde)     │ │  (rojo)  │  │  (gris)    │
    └────────────────┘ └──────────┘  └────────────┘
         │                   │               │
         │                   │               │
         ▼                   ▼               ▼
    [Paciente fue]    [Cancelado por]  [No asistió]
    [atendido OK]     [paciente/clín.]  [sin avisar]


TRANSICIONES PERMITIDAS:

PENDIENTE → ATENDIDO   ✅ (click "Atender")
PENDIENTE → CANCELADO  ✅ (click "Cancelar", si >2hs antes)
PENDIENTE → AUSENTE    ✅ (click "Ausente", después de la hora)

ATENDIDO → *          ❌ (final, no se puede cambiar)
CANCELADO → *         ❌ (final, no se puede cambiar)
AUSENTE → *           ❌ (final, no se puede cambiar)
```

---

## 5. FLUJO DE VALIDACIÓN DE TURNOS

```
                    [Solicitud crear turno]
                              │
                              ▼
                    ┌───────────────────┐
                    │ ¿Horario laboral? │
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                   NO                  SI
                    │                   │
                    ▼                   ▼
          ❌ Error: "Fuera    ┌──────────────────┐
             del horario      │ ¿Médico existe   │
             laboral"         │  y está activo?  │
                              └────────┬─────────┘
                                       │
                              ┌────────┴────────┐
                             NO               SI
                              │                │
                              ▼                ▼
                    ❌ Error: "Médico   ┌───────────────┐
                       no disponible"   │ ¿Hay         │
                                        │ solapamiento? │
                                        └───────┬───────┘
                                                │
                                       ┌────────┴────────┐
                                      SI               NO
                                       │                │
                                       ▼                ▼
                             ❌ Error: "Médico  ┌──────────────┐
                                no disponible   │ ¿Paciente    │
                                en ese horario" │ tiene <3     │
                                                │ pendientes?  │
                                                └──────┬───────┘
                                                       │
                                              ┌────────┴────────┐
                                             NO               SI
                                              │                │
                                              ▼                ▼
                                    ❌ Error: "Ya tiene  ✅ TURNO CREADO
                                       3 turnos         └──────────────┘
                                       pendientes"
```

---

## 6. CASOS DE USO PRINCIPALES

```
                        ┌─────────────────────┐
                        │   RECEPCIONISTA     │
                        └──────────┬──────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
        ┌────────────────┐ ┌──────────────┐ ┌──────────────┐
        │   Gestionar    │ │  Gestionar   │ │   Consultar  │
        │   Pacientes    │ │   Turnos     │ │   Reportes   │
        └────────┬───────┘ └──────┬───────┘ └──────┬───────┘
                 │                 │                 │
        ┌────────┴────────┐       │        ┌────────┴────────┐
        │                 │       │        │                 │
        ▼                 ▼       │        ▼                 ▼
   [Registrar]      [Buscar]     │   [Reporte]         [Turnos por]
   [paciente]       [paciente]   │   [diario]          [médico]
                                  │
                     ┌────────────┼────────────┐
                     │            │            │
                     ▼            ▼            ▼
              [Crear turno] [Cancelar]  [Marcar estado]
                            [turno]      [atendido/ausente]


                        ┌─────────────────────┐
                        │   ADMINISTRADOR     │
                        └──────────┬──────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
        ┌────────────────┐ ┌──────────────┐ ┌──────────────┐
        │   Gestionar    │ │  Gestionar   │ │ Configurar   │
        │   Médicos      │ │Especialidades│ │  Horarios    │
        └────────┬───────┘ └──────────────┘ └──────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
   [Registrar]      [Activar/]
   [médico]         [Desactivar]
```

---

## 7. SEGURIDAD - ROW LEVEL SECURITY

```
┌─────────────────────────────────────────────────────────────┐
│                  BASE DE DATOS (PostgreSQL)                 │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ROW LEVEL SECURITY (RLS)               │   │
│  │                 🔒 HABILITADO                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  TABLA: pacientes                                          │
│  ├── Policy: "Ver pacientes" → authenticated ✅            │
│  ├── Policy: "Crear paciente" → authenticated ✅           │
│  └── Policy: "Actualizar paciente" → authenticated ✅      │
│                                                             │
│  TABLA: medicos                                            │
│  ├── Policy: "Ver médicos" → authenticated ✅              │
│  ├── Policy: "Crear médico" → authenticated ✅             │
│  └── Policy: "Actualizar médico" → authenticated ✅        │
│                                                             │
│  TABLA: turnos                                             │
│  ├── Policy: "Ver turnos" → authenticated ✅               │
│  ├── Policy: "Crear turno" → authenticated ✅              │
│  ├── Policy: "Actualizar turno" → authenticated ✅         │
│  └── Policy: "Eliminar turno" → authenticated ✅           │
│                                                             │
│  TABLA: especialidades                                     │
│  ├── Policy: "Ver especialidades" → authenticated ✅       │
│  ├── Policy: "Crear especialidad" → authenticated ✅       │
│  └── Policy: "Actualizar especialidad" → authenticated ✅  │
│                                                             │
│  TOTAL: 15 políticas activas                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. PERFORMANCE - ÍNDICES

```
┌─────────────────────────────────────────────────────────────┐
│                      ÍNDICES OPTIMIZADOS                    │
└─────────────────────────────────────────────────────────────┘

TABLA: pacientes
├── idx_pacientes_dni          → WHERE dni = ?           [UNIQUE]
├── idx_pacientes_nombre       → WHERE apellido LIKE ?   [BTREE]

TABLA: medicos
├── idx_medicos_matricula      → WHERE matricula = ?     [UNIQUE]
├── idx_medicos_especialidad   → WHERE id_especialidad = ? [FK]

TABLA: turnos
├── idx_turnos_fecha          → WHERE fecha_hora >= ?    [BTREE]
├── idx_turnos_medico         → WHERE id_medico = ?      [FK]
├── idx_turnos_paciente       → WHERE id_paciente = ?    [FK]
└── idx_turnos_estado         → WHERE estado = ?         [BTREE]

TABLA: horarios_medicos
└── idx_horarios_medico       → WHERE id_medico = ?      [FK]

TOTAL: 8 índices estratégicos

EFECTO:
✅ Búsqueda por DNI: O(1) - constante
✅ Búsqueda por fecha: O(log n) - logarítmica
✅ Joins: Optimizados con índices en FKs
```

---

## 9. HORARIOS LABORALES

```
┌──────────────────────────────────────────────────────────────┐
│                   SEMANA LABORAL DE LA CLÍNICA               │
└──────────────────────────────────────────────────────────────┘

LUNES a VIERNES
08:00 ─────────────────────────────────── 18:00
├──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┤
│08│09│10│11│12│13│14│15│16│17│18│  │  │  │  │
│✅│✅│✅│✅│✅│✅│✅│✅│✅│✅│❌│  │  │  │  │
└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
 20 turnos posibles por médico (turnos de 30 min)


SÁBADO
08:00 ─────────────── 13:00
├──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┤
│08│09│10│11│12│13│  │  │  │  │  │
│✅│✅│✅│✅│✅│❌│  │  │  │  │  │
└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
 10 turnos posibles por médico


DOMINGO
❌ CERRADO
└──────────────────────────────────────────────┘
 0 turnos


TURNOS SEMANALES POR MÉDICO: 110 turnos máximo
```

---

## 10. REPORTE ESTADÍSTICO

```
┌─────────────────────────────────────────────────────────────┐
│              REPORTE DIARIO - 15 ENE 2024                   │
└─────────────────────────────────────────────────────────────┘

ESTADÍSTICAS GENERALES

     ╔═══════════════╗
     ║ TOTAL: 25     ║  ← Turnos programados
     ╚═══════════════╝

┌──────────────┬──────────────┬──────────────┬──────────────┐
│  ATENDIDOS   │  PENDIENTES  │  CANCELADOS  │   AUSENTES   │
│     18       │      5       │      1       │      1       │
│    72%       │    20%       │     4%       │     4%       │
└──────────────┴──────────────┴──────────────┴──────────────┘

TASA DE ASISTENCIA: 72% (18/25)

DISTRIBUCIÓN POR HORA

08:00  ████████ (4 turnos)
09:00  ████████████ (6 turnos)
10:00  ████████████████ (8 turnos)
11:00  ████ (2 turnos)
14:00  ████████ (4 turnos)
15:00  ████ (1 turno)

DISTRIBUCIÓN POR MÉDICO

Dra. González    ████████████████ (8 turnos)
Dr. Rodríguez    ████████████ (6 turnos)
Dra. Fernández   ████████████ (6 turnos)
Dr. Martínez     ████████ (5 turnos)
```

---

**Fin de los Diagramas Visuales**

Estos diagramas complementan la documentación técnica y facilitan la comprensión del sistema a nivel visual.
