from flask import Blueprint, request, jsonify
from services.especialidades_service import EspecialidadesService

especialidades_bp = Blueprint('especialidades', __name__)
service = EspecialidadesService()

@especialidades_bp.route('', methods=['GET'])
def listar_especialidades():
    activas = request.args.get('activas', 'true').lower() == 'true'
    resultado, status = service.obtener_especialidades(activas)
    return jsonify(resultado), status

@especialidades_bp.route('', methods=['POST'])
def crear_especialidad():
    data = request.get_json()
    if 'nombre' not in data or not data['nombre']:
        return jsonify({'error': 'El nombre es requerido'}), 400

    resultado, status = service.crear_especialidad(data)
    return jsonify(resultado), status
