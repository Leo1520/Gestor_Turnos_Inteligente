from flask import Blueprint, request, jsonify
from services.pacientes_service import PacientesService

pacientes_bp = Blueprint('pacientes', __name__)
service = PacientesService()

@pacientes_bp.route('', methods=['GET'])
def listar_pacientes():
    filtros = {}
    if request.args.get('dni'):
        filtros['dni'] = request.args.get('dni')
    if request.args.get('nombre'):
        filtros['nombre'] = request.args.get('nombre')
    if request.args.get('apellido'):
        filtros['apellido'] = request.args.get('apellido')

    resultado, status = service.obtener_pacientes(filtros if filtros else None)
    return jsonify(resultado), status

@pacientes_bp.route('', methods=['POST'])
def crear_paciente():
    data = request.get_json()
    campos_requeridos = ['dni', 'nombre', 'apellido', 'fecha_nacimiento', 'telefono']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({'error': f'El campo {campo} es requerido'}), 400

    resultado, status = service.crear_paciente(data)
    return jsonify(resultado), status

@pacientes_bp.route('/<id_paciente>', methods=['GET'])
def obtener_paciente(id_paciente):
    resultado, status = service.obtener_paciente(id_paciente)
    return jsonify(resultado), status

@pacientes_bp.route('/<id_paciente>', methods=['PUT'])
def actualizar_paciente(id_paciente):
    data = request.get_json()
    resultado, status = service.actualizar_paciente(id_paciente, data)
    return jsonify(resultado), status

@pacientes_bp.route('/<id_paciente>/historial', methods=['GET'])
def historial_turnos(id_paciente):
    resultado, status = service.obtener_historial_turnos(id_paciente)
    return jsonify(resultado), status
