from flask import Blueprint, request, jsonify
from services.medicos_service import MedicosService

medicos_bp = Blueprint('medicos', __name__)
service = MedicosService()

@medicos_bp.route('', methods=['GET'])
def listar_medicos():
    activos_solo = request.args.get('activos', 'true').lower() == 'true'
    resultado, status = service.obtener_medicos(activos_solo)
    return jsonify(resultado), status

@medicos_bp.route('', methods=['POST'])
def crear_medico():
    data = request.get_json()
    campos_requeridos = ['nombre', 'apellido', 'matricula', 'id_especialidad', 'telefono']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({'error': f'El campo {campo} es requerido'}), 400

    resultado, status = service.crear_medico(data)
    return jsonify(resultado), status

@medicos_bp.route('/<id_medico>', methods=['GET'])
def obtener_medico(id_medico):
    resultado, status = service.obtener_medico(id_medico)
    return jsonify(resultado), status

@medicos_bp.route('/<id_medico>', methods=['PUT'])
def actualizar_medico(id_medico):
    data = request.get_json()
    resultado, status = service.actualizar_medico(id_medico, data)
    return jsonify(resultado), status

@medicos_bp.route('/especialidad/<id_especialidad>', methods=['GET'])
def medicos_por_especialidad(id_especialidad):
    resultado, status = service.obtener_por_especialidad(id_especialidad)
    return jsonify(resultado), status
