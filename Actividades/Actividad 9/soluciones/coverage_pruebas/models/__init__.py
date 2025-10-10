"""
Modelo de datos
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    if os.environ.get("TESTING"):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return app

# Exponer app y db para los tests / módulos
app = create_app()
db = SQLAlchemy()
# inicializar db con la app y asegurar contexto para llamadas a db.create_all() en import-time
db.init_app(app)
app.app_context().push()