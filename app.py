import os
from flask import Flask
from config import Config
from routes.main import main_bp
from routes.upload import upload_bp


from routes.analysis import analysis_bp
from routes.history import history_bp

from routes.agent import agent_bp
from routes.settings import settings_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.config.from_object(Config)


app.register_blueprint(main_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(history_bp)
app.register_blueprint(agent_bp)
app.register_blueprint(settings_bp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
