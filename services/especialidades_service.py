from config.database import get_supabase_client

class EspecialidadesService:
    def __init__(self):
        self.supabase = get_supabase_client()

    def obtener_especialidades(self, activas_solo=True):
        try:
            query = self.supabase.table('especialidades').select('*')
            if activas_solo:
                query = query.eq('activo', True)
            resultado = query.order('nombre').execute()
            return {'data': resultado.data}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def crear_especialidad(self, data):
        try:
            resultado = self.supabase.table('especialidades').insert(data).execute()
            return {'data': resultado.data[0], 'message': 'Especialidad creada'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
