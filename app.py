from flask import Flask
from flask_cors import CORS
from routes.pacientes_routes import pacientes_bp
from routes.medicos_routes import medicos_bp
from routes.especialidades_routes import especialidades_bp
from routes.turnos_routes import turnos_bp
from routes.reportes_routes import reportes_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(pacientes_bp, url_prefix='/api/pacientes')
app.register_blueprint(medicos_bp, url_prefix='/api/medicos')
app.register_blueprint(especialidades_bp, url_prefix='/api/especialidades')
app.register_blueprint(turnos_bp, url_prefix='/api/turnos')
app.register_blueprint(reportes_bp, url_prefix='/api/reportes')

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'ok', 'message': 'Gestor de Turnos API v1.0'}, 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
