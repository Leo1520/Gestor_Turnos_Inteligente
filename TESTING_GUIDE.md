# Guía de Pruebas - Gestor de Turnos Inteligente

## 1. CASOS DE PRUEBA UNITARIOS

### Test 1: Validación de DNI en PacientesService

**Objetivo**: Verificar que el sistema rechaza DNIs inválidos

**Datos de entrada**:
- DNI vacío: ""
- DNI con letras: "12345ABC"
- DNI muy corto: "123"

**Resultado esperado**:
- Error: "DNI inválido"
- Código HTTP: 400

**Código de prueba**:
```python
def test_validar_dni_invalido():
    service = PacientesService()

    # DNI vacío
    assert service._validar_dni("") == False

    # DNI con letras
    assert service._validar_dni("12345ABC") == False

    # DNI muy corto
    assert service._validar_dni("123") == False

    # DNI válido
    assert service._validar_dni("12345678") == True
```

---

### Test 2: Validación de Horario Laboral

**Objetivo**: Verificar que el sistema rechaza turnos fuera del horario laboral

**Datos de entrada**:
- Domingo 10:00 AM
- Lunes 19:00 PM (fuera de horario)
- Sábado 15:00 PM (fuera de horario)
- Miércoles 10:00 AM (válido)

**Resultado esperado**:
- Domingos y horarios fuera de rango: False
- Horarios válidos: True

**Código de prueba**:
```python
def test_validar_horario_laboral():
    service = TurnosService()

    # Domingo (no válido)
    assert service._validar_horario_laboral("2024-01-07T10:00:00") == False

    # Lunes 19:00 (fuera de horario)
    assert service._validar_horario_laboral("2024-01-08T19:00:00") == False

    # Sábado 15:00 (fuera de horario)
    assert service._validar_horario_laboral("2024-01-13T15:00:00") == False

    # Miércoles 10:00 (válido)
    assert service._validar_horario_laboral("2024-01-10T10:00:00") == True
```

---

### Test 3: Validación de Solapamiento de Turnos

**Objetivo**: Verificar que no se permitan turnos solapados para el mismo médico

**Precondiciones**:
- Médico ID: "med-123"
- Turno existente: 2024-01-15 10:00 - 10:30

**Datos de entrada**:
- Nuevo turno: 2024-01-15 10:15 - 10:45 (solapado)
- Nuevo turno: 2024-01-15 10:30 - 11:00 (válido)

**Resultado esperado**:
- Turno solapado: False
- Turno válido: True

**Código de prueba**:
```python
def test_validar_disponibilidad():
    service = TurnosService()

    # Turno solapado (debe retornar False)
    disponible = service._validar_disponibilidad(
        "med-123",
        "2024-01-15T10:15:00",
        30
    )
    assert disponible == False

    # Turno válido (debe retornar True)
    disponible = service._validar_disponibilidad(
        "med-123",
        "2024-01-15T10:30:00",
        30
    )
    assert disponible == True
```

---

### Test 4: Límite de Turnos Pendientes por Paciente

**Objetivo**: Verificar que un paciente no pueda tener más de 3 turnos pendientes

**Precondiciones**:
- Paciente ID: "pac-456"
- 3 turnos pendientes existentes

**Datos de entrada**:
- Intentar crear un 4to turno pendiente

**Resultado esperado**:
- Error: "El paciente ya tiene 3 turnos pendientes"
- Código HTTP: 400

**Código de prueba**:
```python
def test_limite_turnos_paciente():
    service = TurnosService()

    # Simular paciente con 3 turnos pendientes
    # (esto debería retornar False)
    puede_crear = service._validar_limite_turnos_paciente("pac-456")
    assert puede_crear == False

    # Paciente con 2 turnos (puede crear uno más)
    puede_crear = service._validar_limite_turnos_paciente("pac-789")
    assert puede_crear == True
```

---

### Test 5: Validación de Cancelación Anticipada

**Objetivo**: Verificar que solo se puedan cancelar turnos con 2 horas de anticipación

**Datos de entrada**:
- Turno programado: Mañana a las 10:00 AM (puede cancelarse)
- Turno programado: Hoy a las 14:00 (1 hora antes, no puede)

**Resultado esperado**:
- Turno con 24hs anticipación: Puede cancelarse
- Turno con 1h anticipación: Error

**Código de prueba**:
```python
from datetime import datetime, timedelta

def test_cancelar_turno_anticipacion():
    service = TurnosService()

    # Simular turno dentro de 24 horas
    turno_id_futuro = crear_turno_prueba(
        fecha_hora=datetime.now() + timedelta(hours=24)
    )
    resultado, status = service.cancelar_turno(turno_id_futuro)
    assert status == 200

    # Simular turno dentro de 1 hora
    turno_id_proximo = crear_turno_prueba(
        fecha_hora=datetime.now() + timedelta(hours=1)
    )
    resultado, status = service.cancelar_turno(turno_id_proximo)
    assert status == 400
    assert "2 horas de anticipación" in resultado['error']
```

---

## 2. CASOS DE PRUEBA FUNCIONALES

### Test Funcional 1: Flujo Completo de Registro de Paciente y Turno

**Objetivo**: Verificar el flujo end-to-end desde el registro de paciente hasta la creación de un turno

**Pasos**:
1. Registrar un nuevo paciente
2. Verificar que aparezca en la lista de pacientes
3. Seleccionar una especialidad
4. Seleccionar un médico de esa especialidad
5. Consultar disponibilidad para una fecha
6. Crear un turno
7. Verificar que el turno aparezca en la lista

**Datos de prueba**:
```json
{
  "paciente": {
    "dni": "40123456",
    "nombre": "Test",
    "apellido": "Usuario",
    "fecha_nacimiento": "1995-06-15",
    "telefono": "1156781234",
    "email": "test@test.com"
  },
  "turno": {
    "especialidad": "Medicina General",
    "fecha": "2024-02-15",
    "hora": "10:00"
  }
}
```

**Resultado esperado**:
- Paciente creado con ID válido
- Turno creado y visible en lista
- Estado inicial: "pendiente"

---

### Test Funcional 2: Validación de Duplicación de Turnos

**Objetivo**: Verificar que el sistema impide crear turnos duplicados

**Pasos**:
1. Crear un turno para Médico A el 15/01 a las 10:00
2. Intentar crear otro turno para Médico A el 15/01 a las 10:00
3. Verificar mensaje de error

**Resultado esperado**:
- Primer turno: Creado exitosamente
- Segundo turno: Error "El médico no está disponible en ese horario"

---

### Test Funcional 3: Marcar Asistencia y Generar Reporte

**Objetivo**: Verificar el flujo de atención y generación de reportes

**Pasos**:
1. Crear 5 turnos para el día actual
2. Marcar 3 como "atendido"
3. Marcar 1 como "ausente"
4. Dejar 1 como "pendiente"
5. Generar reporte diario

**Resultado esperado**:
- Total: 5 turnos
- Atendidos: 3
- Ausentes: 1
- Pendientes: 1
- Tasa de asistencia: 60%

---

## 3. PRUEBAS DE INTEGRACIÓN

### Prueba de Integración con Base de Datos

**Objetivo**: Verificar que todas las operaciones CRUD funcionan correctamente

**Checklist**:
- [ ] Crear paciente → Verificar en BD
- [ ] Leer paciente → Datos correctos
- [ ] Actualizar paciente → Cambios reflejados
- [ ] Crear médico → Verificar en BD
- [ ] Crear turno → Relaciones FK correctas
- [ ] Consultar turnos con JOIN → Datos completos

---

## 4. PRUEBAS DE RENDIMIENTO

### Test de Carga: Consulta de Turnos

**Objetivo**: Verificar que el sistema responde en < 2 segundos con 100 turnos

**Configuración**:
- 100 turnos en BD
- Filtro por fecha (1 mes)
- Medir tiempo de respuesta

**Métrica esperada**: < 2 segundos

**Herramienta**: Apache JMeter o Python `time` module

---

## 5. PRUEBAS DE SEGURIDAD

### Test de Inyección SQL

**Objetivo**: Verificar protección contra SQL injection

**Datos de entrada maliciosos**:
```
dni = "' OR '1'='1"
nombre = "'; DROP TABLE pacientes; --"
```

**Resultado esperado**:
- Datos rechazados o escapados correctamente
- Tablas intactas
- Error de validación

---

## 6. PRUEBAS DE INTERFAZ DE USUARIO

### Test UI 1: Búsqueda en Tiempo Real

**Pasos**:
1. Ir a sección Pacientes
2. Escribir "Pérez" en buscador
3. Verificar filtrado instantáneo

**Resultado esperado**:
- Lista filtrada sin recargar página
- Solo pacientes con apellido "Pérez"

### Test UI 2: Paginación

**Pasos**:
1. Cargar 25 turnos
2. Verificar que se muestren 10 por página
3. Navegar a página 2
4. Verificar 10 turnos siguientes

**Resultado esperado**:
- 3 páginas totales
- Botones de navegación funcionales

### Test UI 3: Validación de Formularios

**Pasos**:
1. Abrir modal "Nuevo Paciente"
2. Intentar guardar sin completar campos obligatorios
3. Verificar mensajes de error

**Resultado esperado**:
- Formulario no se envía
- Campos requeridos marcados
- Mensajes claros

---

## RECOMENDACIONES DE EJECUCIÓN

1. **Orden de pruebas**: Unitarias → Funcionales → Integración → UI
2. **Entorno**: Usar base de datos de prueba separada
3. **Datos de prueba**: Crear dataset consistente
4. **Automatización**: Usar pytest para backend, Selenium para frontend
5. **Cobertura**: Objetivo mínimo 80% de code coverage

## COMANDOS DE PRUEBA

```bash
# Instalar dependencias de testing
pip install pytest pytest-cov

# Ejecutar tests unitarios
pytest tests/unit/ -v

# Ejecutar tests funcionales
pytest tests/functional/ -v

# Cobertura de código
pytest --cov=services --cov-report=html

# Test específico
pytest tests/unit/test_pacientes.py::test_validar_dni_invalido
```
