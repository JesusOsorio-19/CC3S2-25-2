"""
counter.py
Servicio Flask que implementa un contador in-memory.
Provee rutas para crear, leer, actualizar e eliminar contadores.
"""

import status
from functools import wraps
from flask import Flask, request

app = Flask(__name__)

# Diccionario global que guarda el nombre de cada contador y su valor.
COUNTERS = {}

def require_counter(f):
    @wraps(f)
    def wrapper(name, *args, **kwargs):
        if name not in COUNTERS:
            return {"message": f"El contador '{name}' no existe"}, status.HTTP_404_NOT_FOUND
        return f(name, *args, **kwargs)
    return wrapper


def change_counter(name, delta):
    COUNTERS[name] += delta
    return {name: COUNTERS[name]}

@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """
    Crea un nuevo contador con valor inicial = 0.
    Retorna 201 (CREATED) si se crea correctamente.
    Retorna 409 (CONFLICT) si el contador ya existía.
    """
    app.logger.info(f"Solicitud para crear el contador: {name}")

    if name in COUNTERS:
        return {"message": f"El contador '{name}' ya existe"}, status.HTTP_409_CONFLICT

    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED


@app.route("/counters/<name>", methods=["PUT"])
@require_counter
def update_counter(name):
    """
    Actualiza (p.e. incrementa) el contador <name>.
    Retorna 200 (OK) si se actualiza correctamente.
    Retorna 404 (NOT FOUND) si el contador no existe.
    """
    app.logger.info(f"Solicitud para actualizar el contador: {name}")

    if name not in COUNTERS:
        return {"message": f"El contador '{name}' no existe"}, status.HTTP_404_NOT_FOUND

    # Ejemplo de actualización: incrementar en 1
    COUNTERS[name] += 1
    return {name: COUNTERS[name]}, status.HTTP_200_OK


@app.route("/counters/<name>", methods=["GET"])
@require_counter
def read_counter(name):
    """
    Lee el valor actual del contador <name>.
    Retorna 200 (OK) si el contador existe.
    Retorna 404 (NOT FOUND) si el contador no existe.
    """
    app.logger.info(f"Solicitud para leer el contador: {name}")

    if name not in COUNTERS:
        return {"message": f"El contador '{name}' no existe"}, status.HTTP_404_NOT_FOUND

    return {name: COUNTERS[name]}, status.HTTP_200_OK


@app.route("/counters/<name>", methods=["DELETE"])
@require_counter
def delete_counter(name):
    """
    Elimina el contador <name>.
    Retorna 204 (NO CONTENT) si la eliminación es exitosa.
    Retorna 404 (NOT FOUND) si el contador no existe.
    """
    app.logger.info(f"Solicitud para eliminar el contador: {name}")

    if name not in COUNTERS:
        return {"message": f"El contador '{name}' no existe"}, status.HTTP_404_NOT_FOUND

    del COUNTERS[name]
    # 204 NO CONTENT suele devolver un cuerpo vacío
    return "", status.HTTP_204_NO_CONTENT

# Nuevas rutas para las funcionalidades adicionales

@app.route("/counters/<name>/increment", methods=["PUT"])
@require_counter
def increment_counter(name):
    return change_counter(name, +1), status.HTTP_200_OK

@app.route("/counters/<name>/set", methods=["PUT"])
@require_counter
def set_counter(name):
    body = request.get_json(silent=True) or {}
    # Si no viene 'value', mantener el valor actual
    try:
        value = body.get("value", COUNTERS[name])
    except AttributeError:
        value = COUNTERS[name]
    COUNTERS[name] = value
    return {name: COUNTERS[name]}, status.HTTP_200_OK


@app.route("/counters", methods=["GET"])
def list_counters():
    return COUNTERS, status.HTTP_200_OK


@app.route("/counters/<name>/reset", methods=["PUT"])
@require_counter
def reset_counter(name):
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_200_OK
