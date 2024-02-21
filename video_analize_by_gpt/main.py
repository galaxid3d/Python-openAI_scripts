from flask import Flask
from flask_cors import CORS

from config.settings import FLASK_PORT

from core.api.endpoints import endpoints_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(endpoints_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=False)
