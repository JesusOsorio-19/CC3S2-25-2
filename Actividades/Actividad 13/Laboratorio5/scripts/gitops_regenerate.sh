#!/bin/bash

echo "Detectando cambios en modules/simulated_app/..."

# Directorio a monitorear
WATCH_DIR="modules/simulated_app"

# Obtener el hash del último commit que modificó el directorio
LAST_CHANGE=$(git log -1 --format="%H" -- $WATCH_DIR)

if [ -z "$LAST_CHANGE" ]; then
    echo "No se encontraron cambios en $WATCH_DIR"
    exit 0
fi

echo "Último cambio detectado: $LAST_CHANGE"
echo "Regenerando todos los entornos"

# Ejecutar el script de generación
python generate_envs.py --count 10

if [ $? -eq 0 ]; then
    echo "Entornos regenerados exitosamente"
else
    echo "Error al regenerar entornos"
    exit 1
fi