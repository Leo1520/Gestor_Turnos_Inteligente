"""
Script de inicialización de datos de prueba
Ejecutar: python seed_data.py
"""

from config.database import get_supabase_client
from datetime import datetime, timedelta

supabase = get_supabase_client()

def seed_medicos():
    """Crear médicos de ejemplo"""
    print("Creando médicos de prueba...")

    especialidades = supabase.table('especialidades').select('id, nombre').execute()
    esp_dict = {e['nombre']: e['id'] for e in especialidades.data}

    medicos = [
        {
            'nombre': 'María',
            'apellido': 'González',
            'matricula': 'MN12345',
            'id_especialidad': esp_dict.get('Medicina General'),
            'telefono': '1156789000',
            'email': 'dra.gonzalez@clinica.com',
            'activo': True
        },
        {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'matricula': 'MN12346',
            'id_especialidad': esp_dict.get('Cardiología'),
            'telefono': '1156789001',
            'email': 'dr.rodriguez@clinica.com',
            'activo': True
        },
        {
            'nombre': 'Ana',
            'apellido': 'Fernández',
            'matricula': 'MN12347',
            'id_especialidad': esp_dict.get('Pediatría'),
            'telefono': '1156789002',
            'email': 'dra.fernandez@clinica.com',
            'activo': True
        },
        {
            'nombre': 'Juan',
            'apellido': 'Martínez',
            'matricula': 'MN12348',
            'id_especialidad': esp_dict.get('Traumatología'),
            'telefono': '1156789003',
            'email': 'dr.martinez@clinica.com',
            'activo': True
        }
    ]

    for medico in medicos:
        try:
            existente = supabase.table('medicos').select('id').eq('matricula', medico['matricula']).maybeSingle().execute()
            if not existente.data:
                supabase.table('medicos').insert(medico).execute()
                print(f"✓ Médico creado: Dr. {medico['apellido']}")
            else:
                print(f"- Médico ya existe: Dr. {medico['apellido']}")
        except Exception as e:
            print(f"✗ Error creando médico {medico['apellido']}: {e}")

def seed_pacientes():
    """Crear pacientes de ejemplo"""
    print("\nCreando pacientes de prueba...")

    pacientes = [
        {
            'dni': '12345678',
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'fecha_nacimiento': '1990-05-15',
            'telefono': '1145678900',
            'email': 'juan.perez@email.com',
            'direccion': 'Av. Corrientes 1234, CABA',
            'obra_social': 'OSDE'
        },
        {
            'dni': '23456789',
            'nombre': 'María',
            'apellido': 'López',
            'fecha_nacimiento': '1985-08-20',
            'telefono': '1145678901',
            'email': 'maria.lopez@email.com',
            'direccion': 'Av. Santa Fe 5678, CABA',
            'obra_social': 'Swiss Medical'
        },
        {
            'dni': '34567890',
            'nombre': 'Carlos',
            'apellido': 'García',
            'fecha_nacimiento': '1978-03-10',
            'telefono': '1145678902',
            'email': 'carlos.garcia@email.com',
            'direccion': 'Av. Rivadavia 910, CABA',
            'obra_social': 'Particular'
        },
        {
            'dni': '45678901',
            'nombre': 'Laura',
            'apellido': 'Martínez',
            'fecha_nacimiento': '1995-11-25',
            'telefono': '1145678903',
            'email': 'laura.martinez@email.com',
            'direccion': 'Av. Cabildo 2345, CABA',
            'obra_social': 'OSDE'
        },
        {
            'dni': '56789012',
            'nombre': 'Roberto',
            'apellido': 'Sánchez',
            'fecha_nacimiento': '1982-07-05',
            'telefono': '1145678904',
            'email': 'roberto.sanchez@email.com',
            'direccion': 'Av. Callao 678, CABA',
            'obra_social': 'Galeno'
        }
    ]

    for paciente in pacientes:
        try:
            existente = supabase.table('pacientes').select('id').eq('dni', paciente['dni']).maybeSingle().execute()
            if not existente.data:
                supabase.table('pacientes').insert(paciente).execute()
                print(f"✓ Paciente creado: {paciente['apellido']}, {paciente['nombre']}")
            else:
                print(f"- Paciente ya existe: {paciente['apellido']}, {paciente['nombre']}")
        except Exception as e:
            print(f"✗ Error creando paciente {paciente['apellido']}: {e}")

def seed_turnos():
    """Crear turnos de ejemplo"""
    print("\nCreando turnos de prueba...")

    pacientes = supabase.table('pacientes').select('id, apellido').limit(5).execute()
    medicos = supabase.table('medicos').select('id, apellido').limit(4).execute()

    if not pacientes.data or not medicos.data:
        print("✗ No hay pacientes o médicos para crear turnos")
        return

    base_date = datetime.now() + timedelta(days=1)
    horas = ['09:00', '10:00', '11:00', '14:00', '15:00']

    turnos_creados = 0
    for i, hora in enumerate(horas):
        if i >= len(pacientes.data):
            break

        fecha_hora = f"{base_date.strftime('%Y-%m-%d')}T{hora}:00"

        turno = {
            'id_paciente': pacientes.data[i]['id'],
            'id_medico': medicos.data[i % len(medicos.data)]['id'],
            'fecha_hora': fecha_hora,
            'duracion_minutos': 30,
            'estado': 'pendiente',
            'motivo_consulta': 'Control de rutina'
        }

        try:
            supabase.table('turnos').insert(turno).execute()
            print(f"✓ Turno creado: {fecha_hora} - {pacientes.data[i]['apellido']}")
            turnos_creados += 1
        except Exception as e:
            print(f"✗ Error creando turno: {e}")

    print(f"\nTotal turnos creados: {turnos_creados}")

def main():
    print("="*60)
    print("INICIALIZACIÓN DE DATOS DE PRUEBA")
    print("="*60)

    try:
        seed_medicos()
        seed_pacientes()
        seed_turnos()

        print("\n" + "="*60)
        print("✓ PROCESO COMPLETADO EXITOSAMENTE")
        print("="*60)
        print("\nPuedes iniciar la aplicación con: python app.py")
        print("Y abrir: http://localhost:8080/static/index.html")

    except Exception as e:
        print(f"\n✗ ERROR GENERAL: {e}")
        print("Verifica tu conexión a Supabase y las credenciales en .env")

if __name__ == '__main__':
    main()
