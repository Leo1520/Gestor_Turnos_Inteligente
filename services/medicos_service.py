from config.database import get_supabase_client

class MedicosService:
    def __init__(self):
        self.supabase = get_supabase_client()

    def crear_medico(self, data):
        try:
            existente = self.supabase.table('medicos').select('id').eq('matricula', data['matricula']).maybeSingle().execute()
            if existente.data:
                return {'error': 'Ya existe un médico con esa matrícula'}, 409

            resultado = self.supabase.table('medicos').insert(data).execute()
            return {'data': resultado.data[0], 'message': 'Médico creado exitosamente'}, 201
        except Exception as e:
            return {'error': str(e)}, 500

    def obtener_medicos(self, activos_solo=False):
        try:
            query = self.supabase.table('medicos').select('*, especialidades(nombre)')

            if activos_solo:
                query = query.eq('activo', True)

            resultado = query.order('apellido').execute()
            return {'data': resultado.data}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def obtener_medico(self, id_medico):
        try:
            resultado = self.supabase.table('medicos').select('*, especialidades(*)').eq('id', id_medico).maybeSingle().execute()
            if not resultado.data:
                return {'error': 'Médico no encontrado'}, 404
            return {'data': resultado.data}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def actualizar_medico(self, id_medico, data):
        try:
            resultado = self.supabase.table('medicos').update(data).eq('id', id_medico).execute()
            if not resultado.data:
                return {'error': 'Médico no encontrado'}, 404
            return {'data': resultado.data[0], 'message': 'Médico actualizado'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def obtener_por_especialidad(self, id_especialidad):
        try:
            resultado = self.supabase.table('medicos').select('*').eq('id_especialidad', id_especialidad).eq('activo', True).execute()
            return {'data': resultado.data}, 200
        except Exception as e:
            return {'error': str(e)}, 500
