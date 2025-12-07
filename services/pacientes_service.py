import os
from datetime import datetime

# Si USE_MYSQL está activo, utilizamos SQLAlchemy; en caso contrario usamos Supabase
USE_MYSQL = os.getenv('USE_MYSQL', 'false').lower() in ('1', 'true')

if USE_MYSQL:
    from config.mysql_database import SessionLocal
    from config.models import Paciente, Turno, Medico
    from sqlalchemy.exc import IntegrityError
    import uuid

class PacientesService:
    def __init__(self):
        if not USE_MYSQL:
            from config.database import get_supabase_client
            self.supabase = get_supabase_client()

    def crear_paciente(self, data):
        try:
            if not self._validar_dni(data.get('dni')):
                return {'error': 'DNI inválido'}, 400

            if not self._validar_fecha_nacimiento(data.get('fecha_nacimiento')):
                return {'error': 'Fecha de nacimiento inválida'}, 400

            if USE_MYSQL:
                session = SessionLocal()
                try:
                    existente = session.query(Paciente).filter_by(dni=data['dni']).first()
                    if existente:
                        return {'error': 'Ya existe un paciente con ese DNI'}, 409

                    paciente = Paciente(
                        id=str(uuid.uuid4()),
                        dni=data['dni'],
                        nombre=data['nombre'],
                        apellido=data['apellido'],
                        fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date(),
                        telefono=data['telefono'],
                        email=data.get('email'),
                        direccion=data.get('direccion', ''),
                        obra_social=data.get('obra_social', 'Particular')
                    )
                    session.add(paciente)
                    session.commit()
                    return {'data': {'id': paciente.id, 'dni': paciente.dni, 'nombre': paciente.nombre, 'apellido': paciente.apellido}, 'message': 'Paciente creado exitosamente'}, 201
                except IntegrityError:
                    session.rollback()
                    return {'error': 'Ya existe un paciente con ese DNI'}, 409
                except Exception as e:
                    session.rollback()
                    return {'error': str(e)}, 500
                finally:
                    session.close()

            # Supabase path
            existente = self.supabase.table('pacientes').select('id').eq('dni', data['dni']).maybeSingle().execute()
            if existente.data:
                return {'error': 'Ya existe un paciente con ese DNI'}, 409

            resultado = self.supabase.table('pacientes').insert(data).execute()
            return {'data': resultado.data[0], 'message': 'Paciente creado exitosamente'}, 201
        except Exception as e:
            return {'error': str(e)}, 500

    def obtener_pacientes(self, filtro=None):
        try:
            if USE_MYSQL:
                session = SessionLocal()
                try:
                    query = session.query(Paciente)
                    if filtro:
                        if 'dni' in filtro:
                            query = query.filter(Paciente.dni.like(f"%{filtro['dni']}%"))
                        if 'nombre' in filtro:
                            query = query.filter(Paciente.nombre.like(f"%{filtro['nombre']}%"))
                        if 'apellido' in filtro:
                            query = query.filter(Paciente.apellido.like(f"%{filtro['apellido']}%"))

                    results = query.order_by(Paciente.apellido).all()
                    data = [{
                        'id': r.id,
                        'dni': r.dni,
                        'nombre': r.nombre,
                        'apellido': r.apellido,
                        'fecha_nacimiento': r.fecha_nacimiento.isoformat(),
                        'telefono': r.telefono
                    } for r in results]
                    return {'data': data}, 200
                finally:
                    session.close()

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
            if USE_MYSQL:
                session = SessionLocal()
                try:
                    r = session.query(Paciente).filter_by(id=id_paciente).first()
                    if not r:
                        return {'error': 'Paciente no encontrado'}, 404
                    data = {
                        'id': r.id,
                        'dni': r.dni,
                        'nombre': r.nombre,
                        'apellido': r.apellido,
                        'fecha_nacimiento': r.fecha_nacimiento.isoformat(),
                        'telefono': r.telefono
                    }
                    return {'data': data}, 200
                finally:
                    session.close()

            resultado = self.supabase.table('pacientes').select('*').eq('id', id_paciente).maybeSingle().execute()
            if not resultado.data:
                return {'error': 'Paciente no encontrado'}, 404
            return {'data': resultado.data}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def actualizar_paciente(self, id_paciente, data):
        try:
            if USE_MYSQL:
                session = SessionLocal()
                try:
                    paciente = session.query(Paciente).filter_by(id=id_paciente).first()
                    if not paciente:
                        return {'error': 'Paciente no encontrado'}, 404
                    for k, v in data.items():
                        if hasattr(paciente, k):
                            setattr(paciente, k, v)
                    session.commit()
                    return {'data': {'id': paciente.id}, 'message': 'Paciente actualizado'}, 200
                finally:
                    session.close()

            resultado = self.supabase.table('pacientes').update(data).eq('id', id_paciente).execute()
            if not resultado.data:
                return {'error': 'Paciente no encontrado'}, 404
            return {'data': resultado.data[0], 'message': 'Paciente actualizado'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    def obtener_historial_turnos(self, id_paciente):
        try:
            if USE_MYSQL:
                session = SessionLocal()
                try:
                    rows = session.query(Turno).filter_by(id_paciente=id_paciente).order_by(Turno.fecha_hora.desc()).all()
                    data = []
                    for t in rows:
                        medico = session.query(Medico).filter_by(id=t.id_medico).first()
                        data.append({
                            'id': t.id,
                            'fecha_hora': t.fecha_hora.isoformat(),
                            'duracion_minutos': t.duracion_minutos,
                            'estado': t.estado,
                            'medico': {'id': medico.id, 'nombre': medico.nombre, 'apellido': medico.apellido} if medico else None
                        })
                    return {'data': data}, 200
                finally:
                    session.close()

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
