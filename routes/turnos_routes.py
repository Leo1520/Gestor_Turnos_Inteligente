from flask import Blueprint, request, jsonify
from services.turnos_service import TurnosService

turnos_bp = Blueprint('turnos', __name__)
service = TurnosService()

@turnos_bp.route('', methods=['GET'])
def listar_turnos():
    filtros = {}
    if request.args.get('fecha_desde'):
        filtros['fecha_desde'] = request.args.get('fecha_desde')
    if request.args.get('fecha_hasta'):
        filtros['fecha_hasta'] = request.args.get('fecha_hasta')
    if request.args.get('id_medico'):
        filtros['id_medico'] = request.args.get('id_medico')
    if request.args.get('estado'):
        filtros['estado'] = request.args.get('estado')

    resultado, status = service.obtener_turnos(filtros if filtros else None)
    return jsonify(resultado), status

@turnos_bp.route('', methods=['POST'])
def crear_turno():
    data = request.get_json()
    campos_requeridos = ['id_paciente', 'id_medico', 'fecha_hora']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({'error': f'El campo {campo} es requerido'}), 400

    resultado, status = service.crear_turno(data)
    return jsonify(resultado), status

@turnos_bp.route('/<id_turno>', methods=['GET'])
def obtener_turno(id_turno):
    resultado, status = service.obtener_turno(id_turno)
    return jsonify(resultado), status

@turnos_bp.route('/<id_turno>', methods=['PUT'])
def actualizar_turno(id_turno):
    data = request.get_json()
    resultado, status = service.actualizar_turno(id_turno, data)
    return jsonify(resultado), status

@turnos_bp.route('/<id_turno>/cancelar', methods=['PUT'])
def cancelar_turno(id_turno):
    resultado, status = service.cancelar_turno(id_turno)
    return jsonify(resultado), status

@turnos_bp.route('/disponibilidad', methods=['GET'])
def consultar_disponibilidad():
    id_medico = request.args.get('id_medico')
    fecha = request.args.get('fecha')

    if not id_medico or not fecha:
        return jsonify({'error': 'Se requiere id_medico y fecha'}), 400

    resultado, status = service.consultar_disponibilidad(id_medico, fecha)
    return jsonify(resultado), status
