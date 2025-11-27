from config.database import get_supabase_client
from datetime import datetime

class ReportesService:
    def __init__(self):
        self.supabase = get_supabase_client()

    def reporte_diario(self, fecha):
        try:
            fecha_inicio = f"{fecha}T00:00:00"
            fecha_fin = f"{fecha}T23:59:59"

            turnos = self.supabase.table('turnos').select('''
                *,
                pacientes(nombre, apellido, dni),
                medicos(nombre, apellido, especialidades(nombre))
            ''').gte('fecha_hora', fecha_inicio).lte('fecha_hora', fecha_fin).order('fecha_hora').execute()

            estadisticas = self._calcular_estadisticas(turnos.data)

            return {
                'data': {
                    'fecha': fecha,
                    'turnos': turnos.data,
                    'estadisticas': estadisticas
                }
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def reporte_por_medico(self, id_medico, fecha_desde, fecha_hasta):
        try:
            turnos = self.supabase.table('turnos').select('''
                *,
                pacientes(nombre, apellido, dni)
            ''').eq('id_medico', id_medico).gte('fecha_hora', fecha_desde).lte('fecha_hora', fecha_hasta).order('fecha_hora').execute()

            estadisticas = self._calcular_estadisticas(turnos.data)

            return {
                'data': {
                    'turnos': turnos.data,
                    'estadisticas': estadisticas
                }
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def _calcular_estadisticas(self, turnos):
        total = len(turnos)
        pendientes = len([t for t in turnos if t['estado'] == 'pendiente'])
        atendidos = len([t for t in turnos if t['estado'] == 'atendido'])
        cancelados = len([t for t in turnos if t['estado'] == 'cancelado'])
        ausentes = len([t for t in turnos if t['estado'] == 'ausente'])

        return {
            'total': total,
            'pendientes': pendientes,
            'atendidos': atendidos,
            'cancelados': cancelados,
            'ausentes': ausentes,
            'tasa_asistencia': round((atendidos / total * 100) if total > 0 else 0, 2)
        }
