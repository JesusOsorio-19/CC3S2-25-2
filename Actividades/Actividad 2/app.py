import os
import sys
import logging
from flask import Flask, jsonify
from datetime import datetime

# Configurar logging para stdout (12-Factor)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Configuración desde variables de entorno (12-Factor Config)
PORT = int(os.environ.get('PORT', 5000))
MESSAGE = os.environ.get('MESSAGE', 'Hello World')
RELEASE = os.environ.get('RELEASE', 'v0.1')

@app.route('/', methods=['GET'])
def home():
    response_data = {
        'message': MESSAGE,
        'release': RELEASE,
        'timestamp': datetime.utcnow().isoformat(),
        'method': 'GET'
    }
    
    # Log a stdout
    logger.info(f"GET / - Response: {response_data}")
    
    return jsonify(response_data)

@app.route('/', methods=['POST'])
def home_post():
    response_data = {
        'error': 'Method POST not supported on this endpoint',
        'release': RELEASE,
        'timestamp': datetime.utcnow().isoformat(),
        'method': 'POST'
    }
    
    logger.warning(f"POST / - Method not allowed: {response_data}")
    
    return jsonify(response_data), 405

if __name__ == '__main__':
    logger.info(f"Starting app on port {PORT}, message: '{MESSAGE}', release: {RELEASE}")
    # Port binding (12-Factor)
    app.run(host='0.0.0.0', port=PORT, debug=False)