from config.database import get_supabase_client
from datetime import datetime, timedelta

class TurnosService:
    def __init__(self):
        self.supabase = get_supabase_client()

    def crear_turno(self, data):
        try:
            if not self._validar_horario_laboral(data['fecha_hora']):
                return {'error': 'El turno está fuera del horario laboral'}, 400

            if not self._validar_disponibilidad(data['id_medico'], data['fecha_hora'], data.get('duracion_minutos', 30)):
                return {'error': 'El médico no está disponible en ese horario'}, 409

            if not self._validar_limite_turnos_paciente(data['id_paciente']):
                return {'error': 'El paciente ya tiene 3 turnos pendientes'}, 400

            resultado = self.supabase.table('turnos').insert(data).execute()
            return {'data': resultado.data[0], 'message': 'Turno creado exitosamente'}, 201
        except Exception as e:
            return {'error': str(e)}, 500

    def obtener_turnos(self, filtros=None):
        try:
            query = self.supabase.table('turnos').select('''
                *,
                pacientes(dni, nombre, apellido, telefono),
                medicos(nombre, apellido, especialidades(nombre))
            ''')

            if filtros:
                if 'fecha_desde' in filtros:
                    query = query.gte('fecha_hora', filtros['fecha_desde'])
                if 'fecha_hasta' in filtros:
                    query = query.lte('fecha_hora', filtros['fecha_hasta'])
                if 'id_medico' in filtros:
                    query = query.eq('id_medico', filtros['id_medico'])
                if 'estado' in filtros:
                    query = query.eq('estado', filtros['estado'])

            resultado = query.order('fecha_hora').execute()
            return {'data': resultado.data}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def obtener_turno(self, id_turno):
        try:
            resultado = self.supabase.table('turnos').select('''
                *,
                pacientes(*),
                medicos(*, especialidades(*))
            ''').eq('id', id_turno).maybeSingle().execute()
            if not resultado.data:
                return {'error': 'Turno no encontrado'}, 404
            return {'data': resultado.data}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def actualizar_turno(self, id_turno, data):
        try:
            resultado = self.supabase.table('turnos').update(data).eq('id', id_turno).execute()
            if not resultado.data:
                return {'error': 'Turno no encontrado'}, 404
            return {'data': resultado.data[0], 'message': 'Turno actualizado'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def cancelar_turno(self, id_turno):
        try:
            turno_actual = self.supabase.table('turnos').select('fecha_hora, estado').eq('id', id_turno).maybeSingle().execute()
            if not turno_actual.data:
                return {'error': 'Turno no encontrado'}, 404

            if turno_actual.data['estado'] != 'pendiente':
                return {'error': 'Solo se pueden cancelar turnos pendientes'}, 400

            fecha_turno = datetime.fromisoformat(turno_actual.data['fecha_hora'].replace('Z', '+00:00'))
            ahora = datetime.now(fecha_turno.tzinfo)
            diferencia = (fecha_turno - ahora).total_seconds() / 3600

            if diferencia < 2:
                return {'error': 'Solo se puede cancelar con al menos 2 horas de anticipación'}, 400

            resultado = self.supabase.table('turnos').update({'estado': 'cancelado'}).eq('id', id_turno).execute()
            return {'data': resultado.data[0], 'message': 'Turno cancelado exitosamente'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def consultar_disponibilidad(self, id_medico, fecha):
        try:
            fecha_inicio = f"{fecha}T00:00:00"
            fecha_fin = f"{fecha}T23:59:59"

            turnos_ocupados = self.supabase.table('turnos').select('fecha_hora, duracion_minutos').eq('id_medico', id_medico).gte('fecha_hora', fecha_inicio).lte('fecha_hora', fecha_fin).in_('estado', ['pendiente', 'atendido']).execute()

            horarios_disponibles = self._generar_horarios_disponibles(fecha, turnos_ocupados.data)
            return {'data': horarios_disponibles}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def _validar_horario_laboral(self, fecha_hora_str):
        try:
            fecha_hora = datetime.fromisoformat(fecha_hora_str.replace('Z', '+00:00'))
            dia_semana = fecha_hora.weekday()
            hora = fecha_hora.hour

            if dia_semana == 6:
                return False

            if dia_semana == 5:
                return 8 <= hora < 13

            return 8 <= hora < 18
        except:
            return False

    def _validar_disponibilidad(self, id_medico, fecha_hora_str, duracion):
        try:
            fecha_hora = datetime.fromisoformat(fecha_hora_str.replace('Z', '+00:00'))
            fecha_fin = fecha_hora + timedelta(minutes=duracion)

            fecha_hora_str_tz = fecha_hora.isoformat()
            fecha_fin_str_tz = fecha_fin.isoformat()

            turnos = self.supabase.table('turnos').select('fecha_hora, duracion_minutos').eq('id_medico', id_medico).in_('estado', ['pendiente', 'atendido']).execute()

            for turno in turnos.data:
                inicio_turno = datetime.fromisoformat(turno['fecha_hora'].replace('Z', '+00:00'))
                fin_turno = inicio_turno + timedelta(minutes=turno['duracion_minutos'])

                if not (fecha_fin <= inicio_turno or fecha_hora >= fin_turno):
                    return False

            return True
        except Exception as e:
            print(f"Error validando disponibilidad: {e}")
            return False

    def _validar_limite_turnos_paciente(self, id_paciente):
        try:
            resultado = self.supabase.table('turnos').select('id', count='exact').eq('id_paciente', id_paciente).eq('estado', 'pendiente').execute()
            return resultado.count < 3
        except:
            return True

    def _generar_horarios_disponibles(self, fecha, turnos_ocupados):
        disponibles = []
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
        dia_semana = fecha_obj.weekday()

        if dia_semana == 5:
            hora_inicio, hora_fin = 8, 13
        elif dia_semana == 6:
            return []
        else:
            hora_inicio, hora_fin = 8, 18

        for hora in range(hora_inicio, hora_fin):
            for minuto in [0, 30]:
                horario = f"{hora:02d}:{minuto:02d}"
                fecha_hora_check = f"{fecha}T{horario}:00"

                ocupado = False
                for turno in turnos_ocupados:
                    inicio_turno = datetime.fromisoformat(turno['fecha_hora'].replace('Z', '+00:00'))
                    if inicio_turno.strftime('%H:%M') == horario:
                        ocupado = True
                        break

                if not ocupado:
                    disponibles.append(horario)

        return disponibles
