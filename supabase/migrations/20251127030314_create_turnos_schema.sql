/*
  # Gestor de Turnos Inteligente - Schema Principal

  ## Descripción General
  Este schema implementa un sistema completo de gestión de turnos para clínicas pequeñas.
  Permite administrar pacientes, médicos, especialidades y turnos con validaciones de negocio.

  ## Nuevas Tablas

  ### 1. `especialidades`
  Catálogo de especialidades médicas disponibles en la clínica
  - `id` (uuid, PK): Identificador único
  - `nombre` (text, UNIQUE): Nombre de la especialidad (ej: "Cardiología")
  - `descripcion` (text): Descripción detallada
  - `activo` (boolean): Estado de la especialidad
  - `created_at` (timestamptz): Fecha de creación

  ### 2. `medicos`
  Registro de médicos que atienden en la clínica
  - `id` (uuid, PK): Identificador único
  - `nombre` (text): Nombre del médico
  - `apellido` (text): Apellido del médico
  - `matricula` (text, UNIQUE): Número de matrícula profesional
  - `id_especialidad` (uuid, FK): Referencia a especialidad
  - `telefono` (text): Teléfono de contacto
  - `email` (text): Email del médico
  - `activo` (boolean): Estado del médico (activo/inactivo)
  - `created_at` (timestamptz): Fecha de registro

  ### 3. `pacientes`
  Registro de pacientes de la clínica
  - `id` (uuid, PK): Identificador único
  - `dni` (text, UNIQUE): Documento de identidad
  - `nombre` (text): Nombre del paciente
  - `apellido` (text): Apellido del paciente
  - `fecha_nacimiento` (date): Fecha de nacimiento
  - `telefono` (text): Teléfono de contacto
  - `email` (text): Email del paciente
  - `direccion` (text): Dirección completa
  - `obra_social` (text): Obra social o prepaga
  - `created_at` (timestamptz): Fecha de registro

  ### 4. `turnos`
  Registro de turnos médicos programados
  - `id` (uuid, PK): Identificador único del turno
  - `id_paciente` (uuid, FK): Referencia al paciente
  - `id_medico` (uuid, FK): Referencia al médico
  - `fecha_hora` (timestamptz): Fecha y hora del turno
  - `duracion_minutos` (integer): Duración en minutos (default: 30)
  - `estado` (text): Estado del turno (pendiente, atendido, cancelado, ausente)
  - `motivo_consulta` (text): Razón de la consulta
  - `observaciones` (text): Notas adicionales
  - `created_at` (timestamptz): Fecha de creación
  - `updated_at` (timestamptz): Última actualización

  ### 5. `horarios_medicos`
  Define los horarios de atención de cada médico por día de la semana
  - `id` (uuid, PK): Identificador único
  - `id_medico` (uuid, FK): Referencia al médico
  - `dia_semana` (integer): Día de la semana (0=Domingo, 6=Sábado)
  - `hora_inicio` (time): Hora de inicio de atención
  - `hora_fin` (time): Hora de fin de atención
  - `activo` (boolean): Estado del horario

  ## Seguridad (RLS)
  - Se habilita Row Level Security en todas las tablas
  - Políticas restrictivas: solo usuarios autenticados pueden acceder
  - Todas las operaciones requieren autenticación

  ## Índices
  - Índices en campos de búsqueda frecuente (DNI, matrícula, fecha_hora)
  - Índices en claves foráneas para optimizar JOINs

  ## Restricciones de Negocio
  1. DNI y matrícula deben ser únicos
  2. Estados de turno limitados a valores específicos
  3. Duración mínima de turno: 15 minutos
  4. Validación de horarios laborales
*/

-- ====================
-- TABLA: especialidades
-- ====================
CREATE TABLE IF NOT EXISTS especialidades (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre text UNIQUE NOT NULL,
  descripcion text DEFAULT '',
  activo boolean DEFAULT true,
  created_at timestamptz DEFAULT now()
);

-- ====================
-- TABLA: medicos
-- ====================
CREATE TABLE IF NOT EXISTS medicos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre text NOT NULL,
  apellido text NOT NULL,
  matricula text UNIQUE NOT NULL,
  id_especialidad uuid REFERENCES especialidades(id) ON DELETE RESTRICT,
  telefono text NOT NULL,
  email text,
  activo boolean DEFAULT true,
  created_at timestamptz DEFAULT now()
);

-- ====================
-- TABLA: pacientes
-- ====================
CREATE TABLE IF NOT EXISTS pacientes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  dni text UNIQUE NOT NULL,
  nombre text NOT NULL,
  apellido text NOT NULL,
  fecha_nacimiento date NOT NULL,
  telefono text NOT NULL,
  email text,
  direccion text DEFAULT '',
  obra_social text DEFAULT 'Particular',
  created_at timestamptz DEFAULT now()
);

-- ====================
-- TABLA: turnos
-- ====================
CREATE TABLE IF NOT EXISTS turnos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  id_paciente uuid REFERENCES pacientes(id) ON DELETE RESTRICT NOT NULL,
  id_medico uuid REFERENCES medicos(id) ON DELETE RESTRICT NOT NULL,
  fecha_hora timestamptz NOT NULL,
  duracion_minutos integer DEFAULT 30 CHECK (duracion_minutos >= 15),
  estado text DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'atendido', 'cancelado', 'ausente')),
  motivo_consulta text DEFAULT '',
  observaciones text DEFAULT '',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- ====================
-- TABLA: horarios_medicos
-- ====================
CREATE TABLE IF NOT EXISTS horarios_medicos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  id_medico uuid REFERENCES medicos(id) ON DELETE CASCADE NOT NULL,
  dia_semana integer CHECK (dia_semana >= 0 AND dia_semana <= 6) NOT NULL,
  hora_inicio time NOT NULL,
  hora_fin time NOT NULL,
  activo boolean DEFAULT true,
  CONSTRAINT horarios_validos CHECK (hora_fin > hora_inicio)
);

-- ====================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ====================
CREATE INDEX IF NOT EXISTS idx_pacientes_dni ON pacientes(dni);
CREATE INDEX IF NOT EXISTS idx_pacientes_nombre ON pacientes(apellido, nombre);
CREATE INDEX IF NOT EXISTS idx_medicos_matricula ON medicos(matricula);
CREATE INDEX IF NOT EXISTS idx_medicos_especialidad ON medicos(id_especialidad);
CREATE INDEX IF NOT EXISTS idx_turnos_fecha ON turnos(fecha_hora);
CREATE INDEX IF NOT EXISTS idx_turnos_medico ON turnos(id_medico);
CREATE INDEX IF NOT EXISTS idx_turnos_paciente ON turnos(id_paciente);
CREATE INDEX IF NOT EXISTS idx_turnos_estado ON turnos(estado);
CREATE INDEX IF NOT EXISTS idx_horarios_medico ON horarios_medicos(id_medico);

-- ====================
-- SEGURIDAD: ROW LEVEL SECURITY
-- ====================
ALTER TABLE especialidades ENABLE ROW LEVEL SECURITY;
ALTER TABLE medicos ENABLE ROW LEVEL SECURITY;
ALTER TABLE pacientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE turnos ENABLE ROW LEVEL SECURITY;
ALTER TABLE horarios_medicos ENABLE ROW LEVEL SECURITY;

-- Políticas para especialidades
CREATE POLICY "Usuarios autenticados pueden ver especialidades"
  ON especialidades FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Usuarios autenticados pueden crear especialidades"
  ON especialidades FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar especialidades"
  ON especialidades FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

-- Políticas para medicos
CREATE POLICY "Usuarios autenticados pueden ver médicos"
  ON medicos FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Usuarios autenticados pueden crear médicos"
  ON medicos FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar médicos"
  ON medicos FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

-- Políticas para pacientes
CREATE POLICY "Usuarios autenticados pueden ver pacientes"
  ON pacientes FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Usuarios autenticados pueden crear pacientes"
  ON pacientes FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar pacientes"
  ON pacientes FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

-- Políticas para turnos
CREATE POLICY "Usuarios autenticados pueden ver turnos"
  ON turnos FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Usuarios autenticados pueden crear turnos"
  ON turnos FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar turnos"
  ON turnos FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden eliminar turnos"
  ON turnos FOR DELETE
  TO authenticated
  USING (true);

-- Políticas para horarios_medicos
CREATE POLICY "Usuarios autenticados pueden ver horarios"
  ON horarios_medicos FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Usuarios autenticados pueden crear horarios"
  ON horarios_medicos FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar horarios"
  ON horarios_medicos FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden eliminar horarios"
  ON horarios_medicos FOR DELETE
  TO authenticated
  USING (true);

-- ====================
-- FUNCIÓN: Actualizar timestamp en turnos
-- ====================
CREATE OR REPLACE FUNCTION actualizar_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_turnos_updated_at
  BEFORE UPDATE ON turnos
  FOR EACH ROW
  EXECUTE FUNCTION actualizar_updated_at();

-- ====================
-- DATOS INICIALES: Especialidades
-- ====================
INSERT INTO especialidades (nombre, descripcion) VALUES
  ('Medicina General', 'Atención médica general y consultas preventivas'),
  ('Cardiología', 'Especialidad enfocada en el sistema cardiovascular'),
  ('Pediatría', 'Atención médica para niños y adolescentes'),
  ('Traumatología', 'Tratamiento de lesiones del sistema musculoesquelético'),
  ('Dermatología', 'Diagnóstico y tratamiento de enfermedades de la piel')
ON CONFLICT (nombre) DO NOTHING;