from config.database import get_supabase_client
from datetime import datetime

class PacientesService:
    def __init__(self):
        self.supabase = get_supabase_client()

    def crear_paciente(self, data):
        try:
            if not self._validar_dni(data.get('dni')):
                return {'error': 'DNI inválido'}, 400

            if not self._validar_fecha_nacimiento(data.get('fecha_nacimiento')):
                return {'error': 'Fecha de nacimiento inválida'}, 400

            existente = self.supabase.table('pacientes').select('id').eq('dni', data['dni']).maybeSingle().execute()
            if existente.data:
                return {'error': 'Ya existe un paciente con ese DNI'}, 409

            resultado = self.supabase.table('pacientes').insert(data).execute()
            return {'data': resultado.data[0], 'message': 'Paciente creado exitosamente'}, 201
        except Exception as e:
            return {'error': str(e)}, 500

    def obtener_pacientes(self, filtro=None):
        try:
            query = self.supabase.table('pacientes').select('*')

            if filtro:
                if 'dni' in filtro:
                    query = query.ilike('dni', f"%{filtro['dni']}%")
                if 'nombre' in filtro:
                    query = query.ilike('nombre', f"%{filtro['nombre']}%")
                if 'apellido' in filtro:
                    query = query.ilike('apellido', f"%{filtro['apellido']}%")

            resultado = query.order('apellido').execute()
            return {'data': resultado.data}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def obtener_paciente(self, id_paciente):
        try:
            resultado = self.supabase.table('pacientes').select('*').eq('id', id_paciente).maybeSingle().execute()
            if not resultado.data:
                return {'error': 'Paciente no encontrado'}, 404
            return {'data': resultado.data}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def actualizar_paciente(self, id_paciente, data):
        try:
            resultado = self.supabase.table('pacientes').update(data).eq('id', id_paciente).execute()
            if not resultado.data:
                return {'error': 'Paciente no encontrado'}, 404
            return {'data': resultado.data[0], 'message': 'Paciente actualizado'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def obtener_historial_turnos(self, id_paciente):
        try:
            resultado = self.supabase.table('turnos').select('''
                *,
                medicos(nombre, apellido, especialidades(nombre))
            ''').eq('id_paciente', id_paciente).order('fecha_hora', desc=True).execute()
            return {'data': resultado.data}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def _validar_dni(self, dni):
        if not dni or not isinstance(dni, str):
            return False
        return len(dni.strip()) >= 7 and dni.strip().isdigit()

    def _validar_fecha_nacimiento(self, fecha_str):
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            if fecha > datetime.now():
                return False
            return True
        except:
            return False
