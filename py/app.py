import os
from flask import Flask
from flask_cors import CORS
from database.db import init_db
from routes.upload_route import upload_bp
from routes.download_route import download_bp

# ─── Instância global do Flask (necessária para o Gunicorn) ───────────────────
app = Flask(__name__)
CORS(app)  # Habilita CORS para todos os domínios

# ─── Configuração da pasta de uploads ─────────────────────────────────────────
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cria a pasta de uploads se não existir (filesystem efêmero do Render)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ─── Inicializa o banco de dados (cria tabelas se não existirem) ───────────────
init_db()

# ─── Registro dos Blueprints ───────────────────────────────────────────────────
app.register_blueprint(upload_bp, url_prefix='/uploads')
app.register_blueprint(download_bp, url_prefix='/downloads')

# ─── Execução local ───────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
