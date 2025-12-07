import uuid
from sqlalchemy import Column, String, Date, Integer, Text, TIMESTAMP, ForeignKey, Time
from sqlalchemy.dialects.mysql import CHAR, TINYINT
from sqlalchemy.sql import func
from config.mysql_database import Base


class Especialidad(Base):
    __tablename__ = 'especialidades'
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(255), unique=True, nullable=False)
    descripcion = Column(Text, default='')
    activo = Column(TINYINT(1), default=1)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Medico(Base):
    __tablename__ = 'medicos'
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    matricula = Column(String(255), unique=True, nullable=False)
    id_especialidad = Column(CHAR(36), ForeignKey('especialidades.id'))
    telefono = Column(String(50), nullable=False)
    email = Column(String(255))
    activo = Column(TINYINT(1), default=1)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Paciente(Base):
    __tablename__ = 'pacientes'
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dni = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    telefono = Column(String(50), nullable=False)
    email = Column(String(255))
    direccion = Column(Text, default='')
    obra_social = Column(String(255), default='Particular')
    created_at = Column(TIMESTAMP, server_default=func.now())


class Turno(Base):
    __tablename__ = 'turnos'
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_paciente = Column(CHAR(36), ForeignKey('pacientes.id'), nullable=False)
    id_medico = Column(CHAR(36), ForeignKey('medicos.id'), nullable=False)
    fecha_hora = Column(TIMESTAMP, nullable=False)
    duracion_minutos = Column(Integer, default=30)
    estado = Column(String(20), default='pendiente')
    motivo_consulta = Column(Text, default='')
    observaciones = Column(Text, default='')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class HorarioMedico(Base):
    __tablename__ = 'horarios_medicos'
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_medico = Column(CHAR(36), ForeignKey('medicos.id'), nullable=False)
    dia_semana = Column(Integer, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    activo = Column(TINYINT(1), default=1)
