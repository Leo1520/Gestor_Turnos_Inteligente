from flask import Blueprint, request, jsonify
from services.reportes_service import ReportesService

reportes_bp = Blueprint('reportes', __name__)
service = ReportesService()

@reportes_bp.route('/diario', methods=['GET'])
def reporte_diario():
    fecha = request.args.get('fecha')
    if not fecha:
        return jsonify({'error': 'Se requiere el parámetro fecha (YYYY-MM-DD)'}), 400

    resultado, status = service.reporte_diario(fecha)
    return jsonify(resultado), status

@reportes_bp.route('/medico/<id_medico>', methods=['GET'])
def reporte_medico(id_medico):
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')

    if not fecha_desde or not fecha_hasta:
        return jsonify({'error': 'Se requieren fecha_desde y fecha_hasta'}), 400

    resultado, status = service.reporte_por_medico(id_medico, fecha_desde, fecha_hasta)
    return jsonify(resultado), status
