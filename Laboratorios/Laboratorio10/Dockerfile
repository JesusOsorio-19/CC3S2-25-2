# Etapa de construcción 
FROM python:3.12-slim AS builder

# Evitamos archivos .pyc y forzar salida no bufferizada
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Copiamos dependencias
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa de producción 
FROM python:3.12-slim AS production

# Creamos usuario y grupo de la aplicación
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd -m -r -g ${APP_USER} ${APP_USER}

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/${APP_USER}/.local/bin:${PATH}"

WORKDIR /app

# Copiamos dependencias instaladas desde la etapa builder
COPY --from=builder /root/.local /home/${APP_USER}/.local

# Copiamos el código fuente y dar permisos al usuario (CLAVE para SQLite)
COPY . /app
RUN chown -R ${APP_USER}:${APP_USER} /app

# Ejecutamos como usuario no root
USER ${APP_USER}

# Puerto y comando
EXPOSE 80
CMD ["uvicorn", "microservice.main:app", "--host", "0.0.0.0", "--port", "80"]