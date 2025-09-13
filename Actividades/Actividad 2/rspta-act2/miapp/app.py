import os, sys, time, json, logging
from flask import Flask, jsonify, request

# Configuración por entorno (12-Factor): se lee al iniciar el proceso
APP_MESSAGE = os.environ.get("MESSAGE", "Hola CC3S2")
APP_RELEASE = os.environ.get("RELEASE", "v1")
APP_PORT    = int(os.environ.get("PORT", "8080"))

app = Flask(__name__)

# Logs estructurados (JSON por línea) a stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
logger = logging.getLogger("miapp")

def jlog(level, **kv):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "level": level, **kv}
    logger.info(json.dumps(rec, ensure_ascii=False))

@app.before_request
def log_request():
    jlog("INFO", event="request",
         method=request.method,
         path=request.path,
         remote=request.headers.get("X-Forwarded-For") or request.remote_addr,
         proto=request.headers.get("X-Forwarded-Proto") or request.environ.get("wsgi.url_scheme"))

@app.route("/", methods=["GET"])
def index():
    # Respuesta JSON incluyendo cabeceras de proxy para observabilidad
    payload = {
        "message": APP_MESSAGE,
        "release": APP_RELEASE,
        "headers": {
            "X-Forwarded-For": request.headers.get("X-Forwarded-For"),
            "X-Forwarded-Proto": request.headers.get("X-Forwarded-Proto"),
            "X-Forwarded-Host": request.headers.get("X-Forwarded-Host"),
        }
    }
    return jsonify(payload), 200

if __name__ == "__main__":
    jlog("INFO", event="startup", port=APP_PORT)
    # Port binding: expone en todas las interfaces
    app.run(host="0.0.0.0", port=APP_PORT)
