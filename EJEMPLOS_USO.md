# 📘 Guía de Uso Práctica - Ejemplos Paso a Paso

## Escenarios Comunes de Uso

---

## 🎬 ESCENARIO 1: Primer Día en la Clínica

### Situación
Es lunes por la mañana, la clínica abre y llega el primer paciente nuevo.

### Paso 1: Registrar el Paciente

**Frontend**:
1. Click en "Pacientes" en el menú superior
2. Click en "+ Nuevo Paciente"
3. Completar formulario:
   - DNI: 40123456
   - Nombre: Roberto
   - Apellido: Díaz
   - Fecha Nacimiento: 15/03/1995
   - Teléfono: 1156781234
   - Email: roberto.diaz@email.com
   - Dirección: Av. Corrientes 1500, CABA
   - Obra Social: OSDE
4. Click "Guardar Paciente"
5. ✅ Notificación: "Paciente registrado exitosamente"

**API Equivalente**:
```bash
curl -X POST http://localhost:5000/api/pacientes \
-H "Content-Type: application/json" \
-d '{
  "dni": "40123456",
  "nombre": "Roberto",
  "apellido": "Díaz",
  "fecha_nacimiento": "1995-03-15",
  "telefono": "1156781234",
  "email": "roberto.diaz@email.com",
  "direccion": "Av. Corrientes 1500, CABA",
  "obra_social": "OSDE"
}'
```

### Paso 2: Asignar un Turno

**Frontend**:
1. Click en "Turnos" en el menú
2. Click en "+ Nuevo Turno"
3. Seleccionar paciente: "Díaz, Roberto (40123456)"
4. Seleccionar especialidad: "Medicina General"
5. Sistema carga médicos disponibles
6. Seleccionar médico: "Dra. González, María"
7. Seleccionar fecha: Hoy (sistema sugiere fechas válidas)
8. Sistema muestra horarios disponibles: 09:00, 09:30, 10:00...
9. Seleccionar hora: 10:00
10. Motivo: "Control anual de salud"
11. Click "Guardar Turno"
12. ✅ Notificación: "Turno creado exitosamente"

**Resultado**: Turno creado para hoy a las 10:00 con estado "Pendiente"

---

## 🎬 ESCENARIO 2: Atención del Paciente

### Situación
Es las 10:00 AM y llega Roberto Díaz para su turno.

### Paso 1: Verificar el Turno

**Frontend**:
1. En "Turnos", usar filtros:
   - Fecha desde: Hoy
   - Fecha hasta: Hoy
   - Estado: Pendiente
2. Click "Filtrar"
3. Ver lista con el turno de Roberto a las 10:00

### Paso 2: Marcar como Atendido

**Frontend**:
1. Localizar el turno de Roberto
2. Click en botón "Atender" (verde)
3. ✅ Estado cambia a "ATENDIDO" con badge verde
4. Botones de acción desaparecen

**API Equivalente**:
```bash
curl -X PUT http://localhost:5000/api/turnos/{turno_id} \
-H "Content-Type: application/json" \
-d '{
  "estado": "atendido",
  "observaciones": "Paciente controlado. Todo normal."
}'
```

---

## 🎬 ESCENARIO 3: Paciente Cancela con Anticipación

### Situación
Martes 14:00, un paciente llama para cancelar su turno del jueves a las 15:00.

### Verificar Tiempo de Anticipación

**Cálculo**:
- Ahora: Martes 14:00
- Turno: Jueves 15:00
- Diferencia: 49 horas ✅ (> 2 horas requeridas)

### Cancelar Turno

**Frontend**:
1. Buscar el turno en la lista
2. Click en botón "Cancelar" (rojo)
3. Confirmar en el diálogo
4. ✅ Estado cambia a "CANCELADO"

**API Equivalente**:
```bash
curl -X PUT http://localhost:5000/api/turnos/{turno_id}/cancelar
```

**Respuesta**:
```json
{
  "data": { ... },
  "message": "Turno cancelado exitosamente"
}
```

---

## 🎬 ESCENARIO 4: Intento de Cancelación Tardía

### Situación
Jueves 13:30, un paciente llama para cancelar su turno de hoy a las 15:00.

### Intento de Cancelación

**Cálculo**:
- Ahora: Jueves 13:30
- Turno: Jueves 15:00
- Diferencia: 1.5 horas ❌ (< 2 horas requeridas)

**Frontend**:
1. Click en "Cancelar"
2. ❌ Notificación de error: "Solo se puede cancelar con al menos 2 horas de anticipación"
3. Turno permanece como "Pendiente"

**Solución**: Marcar como "Ausente" si el paciente no asiste

---

## 🎬 ESCENARIO 5: Buscar Disponibilidad para Varios Turnos

### Situación
Viernes 09:00, necesitas agendar 3 pacientes con el mismo médico para la próxima semana.

### Paso 1: Consultar Disponibilidad General

**Frontend**:
1. Ir a "Turnos" → "+ Nuevo Turno"
2. Seleccionar especialidad: "Cardiología"
3. Seleccionar médico: "Dr. Rodríguez"
4. Seleccionar fecha: Lunes próximo
5. Ver horarios disponibles en el desplegable

**Horarios mostrados**:
```
08:00 ✅
08:30 ✅
09:00 ✅
09:30 ❌ (ocupado)
10:00 ✅
10:30 ✅
...
```

### Paso 2: Agendar Turnos Consecutivos

1. Crear turno 1: Paciente A a las 08:00
2. Crear turno 2: Paciente B a las 08:30
3. Crear turno 3: Paciente C a las 09:00

**Resultado**: 3 turnos creados secuencialmente sin solapamiento

---

## 🎬 ESCENARIO 6: Intento de Turno Duplicado

### Situación
Accidentalmente intentas crear un turno para un horario ya ocupado.

### Intento de Creación

**Datos**:
- Médico: Dr. Rodríguez
- Fecha: Lunes 10:00
- (Ya existe turno a las 10:00)

**Resultado**:
❌ Error: "El médico no está disponible en ese horario"

**Sistema previene**:
- Solapamiento de turnos
- Doble asignación del médico

---

## 🎬 ESCENARIO 7: Paciente con Múltiples Turnos

### Situación
Un paciente necesita 3 turnos: Clínico, Cardiólogo, Traumatólogo.

### Paso 1: Crear Primer Turno
1. Especialidad: Medicina General
2. Fecha: Lunes 09:00
3. ✅ Turno creado

### Paso 2: Crear Segundo Turno
1. Especialidad: Cardiología
2. Fecha: Martes 10:00
3. ✅ Turno creado

### Paso 3: Crear Tercer Turno
1. Especialidad: Traumatología
2. Fecha: Miércoles 11:00
3. ✅ Turno creado (límite alcanzado: 3 pendientes)

### Paso 4: Intento de Cuarto Turno
1. Especialidad: Dermatología
2. ❌ Error: "El paciente ya tiene 3 turnos pendientes"

**Solución**: Esperar a que se atienda al menos uno de los 3 turnos existentes

---

## 🎬 ESCENARIO 8: Generación de Reporte Diario

### Situación
Final del día, necesitas ver estadísticas de turnos.

### Paso 1: Generar Reporte

**Frontend**:
1. Click en "Reportes" en el menú
2. Seleccionar fecha: Hoy
3. Click "Generar Reporte"

### Paso 2: Ver Estadísticas

**Dashboard muestra**:
```
┌────────────────┬────────────────┬────────────────┬────────────────┐
│ Total Turnos   │ Atendidos      │ Pendientes     │ Tasa Asistencia│
│      25        │      18        │       5        │     72%        │
└────────────────┴────────────────┴────────────────┴────────────────┘

Detalle:
- Cancelados: 1
- Ausentes: 1
```

### Paso 3: Ver Detalle por Médico

**Tabla muestra**:
```
Hora  | Paciente       | Médico        | Especialidad  | Estado
------|----------------|---------------|---------------|----------
08:00 | Pérez, Juan    | Dra. González | Med. General  | Atendido
08:30 | López, María   | Dra. González | Med. General  | Atendido
09:00 | García, Carlos | Dr. Rodríguez | Cardiología   | Ausente
...
```

---

## 🎬 ESCENARIO 9: Búsqueda Rápida de Paciente

### Situación
Llega un paciente pero no recuerdas su nombre completo, solo que es "Martínez".

### Búsqueda

**Frontend**:
1. Ir a "Pacientes"
2. En el buscador escribir: "mart"
3. Sistema filtra en tiempo real
4. Ver solo pacientes con "Mart" en nombre o apellido

**Resultados**:
```
DNI      | Nombre         | Teléfono    | Obra Social
---------|----------------|-------------|-------------
45678901 | Martínez, Laura| 1145678903  | OSDE
78901234 | Martín, Pedro  | 1145678905  | Swiss Medical
```

### Ver Historial

1. Click en "Historial" del paciente deseado
2. Ver lista de turnos previos:

```
Fecha: 15/01/2024 10:00
Médico: Dra. González
Especialidad: Medicina General
Estado: Atendido

Fecha: 20/12/2023 14:30
Médico: Dr. Rodríguez
Especialidad: Cardiología
Estado: Atendido
```

---

## 🎬 ESCENARIO 10: Horario No Laboral

### Situación
Intentas crear un turno para el domingo a las 10:00.

### Intento de Creación

**Datos**:
- Fecha: Domingo 15/01/2024
- Hora: 10:00

**Resultado**:
❌ Error: "El turno está fuera del horario laboral"

**Horarios válidos**:
- Lunes a Viernes: 08:00 - 18:00
- Sábado: 08:00 - 13:00
- Domingo: ❌ Cerrado

---

## 🎬 ESCENARIO 11: Registrar Nuevo Médico

### Situación
La clínica contrata un nuevo traumatólogo.

### Paso 1: Registrar Médico

**Frontend**:
1. Ir a "Médicos"
2. Click "+ Nuevo Médico"
3. Completar:
   - Matrícula: MN54321
   - Nombre: Pedro
   - Apellido: Ramírez
   - Especialidad: Traumatología
   - Teléfono: 1156789999
   - Email: dr.ramirez@clinica.com
4. Click "Guardar Médico"
5. ✅ Médico creado con estado "ACTIVO"

### Paso 2: Verificar Disponibilidad

1. Ir a "Turnos" → "+ Nuevo Turno"
2. Seleccionar especialidad: "Traumatología"
3. Ver nuevo médico en la lista: "Dr. Ramírez, Pedro"

---

## 🎬 ESCENARIO 12: Desactivar Médico Temporalmente

### Situación
Un médico está de vacaciones por 2 semanas.

### Desactivar

**Frontend**:
1. Ir a "Médicos"
2. Localizar al médico
3. Click en "Desactivar"
4. Estado cambia a "INACTIVO" (badge gris)

### Verificar Efecto

1. Ir a "Turnos" → crear turno
2. Seleccionar la especialidad del médico desactivado
3. El médico NO aparece en la lista de disponibles

### Reactivar Después

1. Volver a "Médicos"
2. Click en "Activar"
3. Médico vuelve a estar disponible para turnos

---

## 🎬 ESCENARIO 13: Filtrado Avanzado de Turnos

### Situación
Necesitas ver todos los turnos pendientes del Dr. Rodríguez para la próxima semana.

### Aplicar Filtros

**Frontend**:
1. Ir a "Turnos"
2. Configurar filtros:
   - Fecha desde: 15/01/2024
   - Fecha hasta: 21/01/2024
   - Médico: Dr. Rodríguez, Carlos
   - Estado: Pendiente
3. Click "Filtrar"

**Resultado**: Lista con 12 turnos que cumplen los criterios

### Exportar (futuro)

En v2.0 podrás exportar esta lista a PDF o Excel.

---

## 🎬 ESCENARIO 14: Manejo de Ausencias

### Situación
Un paciente no asiste a su turno de las 10:00.

### Marcar Ausencia

**Frontend**:
1. A las 10:30 (después de la hora del turno)
2. Localizar el turno
3. Click en "Ausente" (botón amarillo)
4. Estado cambia a "AUSENTE"

### Efecto en Estadísticas

- El turno cuenta como "ausente" en reportes
- Afecta la tasa de asistencia del día
- Queda registrado en historial del paciente

---

## 🎬 ESCENARIO 15: Paginación de Resultados

### Situación
Tienes 50 turnos en el día, la tabla solo muestra 10 por página.

### Navegar Páginas

**Frontend**:
1. Ver tabla con 10 turnos
2. Al final ver: `[Anterior] [1] [2] [3] [4] [5] [Siguiente]`
3. Click en "2" para ver turnos 11-20
4. Click en "Siguiente" para ver turnos 21-30

**Indicador**: "Mostrando 50 turnos"

---

## 💡 TIPS Y MEJORES PRÁCTICAS

### ✅ DO's (Hacer)

1. **Registrar pacientes completos**: Incluir email y teléfono para contacto
2. **Verificar disponibilidad**: Antes de confirmar verbalmente con el paciente
3. **Usar filtros**: Para encontrar información rápidamente
4. **Generar reportes diarios**: Al final de cada jornada
5. **Mantener médicos actualizados**: Desactivar temporalmente si no están disponibles
6. **Marcar estados correctamente**: Diferenciar entre "cancelado" y "ausente"

### ❌ DON'Ts (Evitar)

1. **No duplicar pacientes**: Buscar primero antes de registrar
2. **No cancelar tarde**: Respetar las 2 horas de anticipación
3. **No crear turnos sin validar**: Usar el sistema de disponibilidad
4. **No dejar turnos pendientes**: Actualizar estados al finalizar el día
5. **No usar datos falsos**: Validar DNI y contactos reales

---

## 🔧 SOLUCIÓN DE PROBLEMAS COMUNES

### Problema: "No veo horarios disponibles"

**Causas posibles**:
1. Médico no tiene horarios configurados
2. Todos los horarios están ocupados
3. Fecha seleccionada es domingo

**Solución**:
1. Verificar que el médico esté activo
2. Elegir otra fecha
3. Verificar horarios laborales

---

### Problema: "No puedo cancelar un turno"

**Causas posibles**:
1. Faltan menos de 2 horas
2. El turno ya está atendido
3. El turno ya está cancelado

**Solución**:
1. Si es urgente, marcar como "ausente" después del horario
2. Verificar el estado actual del turno

---

### Problema: "La búsqueda no encuentra al paciente"

**Causas posibles**:
1. Error en el DNI ingresado
2. Paciente no está registrado
3. Error de tipeo en el nombre

**Solución**:
1. Verificar DNI en documento físico
2. Buscar por apellido parcial
3. Listar todos los pacientes y buscar manualmente

---

## 📞 CONTACTO

Para más información, consultar:
- **README.md**: Instalación y configuración
- **API_DOCUMENTATION.md**: Referencia técnica completa
- **TESTING_GUIDE.md**: Guía de pruebas

---

**Versión**: 1.0.0
**Última actualización**: 2024
