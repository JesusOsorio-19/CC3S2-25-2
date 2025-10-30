import os, json
import click
from shutil import copyfile
from jsonschema import validate, ValidationError

with open("terraform_schema.json", "r") as f:
    SCHEMA = json.load(f)

# Leer api_key desde variable de entorno
API_KEY = os.environ.get("API_KEY", "default-secret-key")

# Parámetros de ejemplo para N entornos
ENVS = [
    {"name": f"app{i}", "network": f"net{i}"} for i in range(1, 11)
]

ENVS.append({
    "name": "env3",
    "network": "net2-peered"  # Depende de net2
})

MODULE_DIR = "modules/simulated_app"
OUT_DIR    = "environments"

def validate_config(config, config_type):
    """Valida un archivo de configuración contra el esquema"""
    try:
        validate(instance=config, schema=SCHEMA)
        click.echo(f"Validación exitosa: {config_type}")
        return True
    except ValidationError as e:
        click.echo(f"Error de validación en {config_type}: {e.message}")
        return False    

def render_and_write(env):
    env_dir = os.path.join(OUT_DIR, env["name"])
    os.makedirs(env_dir, exist_ok=True)

    # 1) Genera network.tf.json dinámicamente con valores del entorno
    network_config = {
        "variable": [
            {
                "name": [
                    {
                        "type": "string",
                        "default": env["name"],
                        "description": "Nombre del servidor local"
                    }
                ]
            },
            {
                "network": [
                    {
                        "type": "string",
                        "default": env["network"],  # Usa el valor específico del entorno
                        "description": "Red de despliegue del servidor"
                    }
                ]
            },
            {
                "port": [
                    {
                        "type": "number",
                        "default": env.get("port", 8080),  # Puerto específico o 8080 por defecto
                        "description": "Puerto de la aplicacion"
                    }
                ]
            },
            {
                "api_key": [
                    {
                        "type": "string",
                        "default": API_KEY,
                        "description": "API key para autenticacion",
                        "sensitive": True
                    }
                ]
            }
        ]
    }
    
    # Validar antes de escribir
    if not validate_config(network_config, f"network.tf.json de {env['name']}"):
        return

    with open(os.path.join(env_dir, "network.tf.json"), "w") as fp:
        json.dump(network_config, fp, indent=4)


    # 2) Genera main.tf.json solo con recursos
    config = {
        "resource": [
            {
                "local_server": [
                    {
                        env["name"]: [
                            {
                                "triggers": {
                                    # Esto genera app1 y net1, etc. hardcodeados
                                    #"name":    env["name"],
                                    #"network": env["network"]
                                    
                                    # Esto genera referencias a variables
                                    "name":    "${var.name}",
                                    "network": "${var.network}",
                                    "port": "${var.port}"
                                },
                                "provisioner": [
                                    {
                                        "local-exec": {
                                            "command": (
                                                "echo 'Arrancando servidor ${var.name} en puerto ${var.port} en red ${var.network}'"
                                            )
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # Validar antes de escribir
    if not validate_config(config, f"main.tf.json de {env['name']}"):
        return

    with open(os.path.join(env_dir, "main.tf.json"), "w") as fp:
        json.dump(config, fp, sort_keys=True, indent=4)

@click.command()
@click.option('--count', default=10, help='Número de entornos a generar')
@click.option('--prefix', default='app', help='Prefijo para nombres de entornos')
@click.option('--port', default=8080, help='Puerto por defecto')
def generate(count, prefix, port):
    """Genera entornos de Terraform con configuración personalizada"""
    
    # Generar lista de entornos
    envs = [
        {
            "name": f"{prefix}{i}",
            "network": f"net{i}",
            "port": port
        }
        for i in range(1, count + 1)
    ]
    
    # Añadir env3 con dependencia
    envs.append({
        "name": "env3",
        "network": "net2-peered",
        "port": port
    })
    
    # Generar entornos
    for env in envs:
        render_and_write(env)
    
    click.echo(f"Generados {len(envs)} entornos en '{OUT_DIR}/'")

if __name__ == "__main__":
    generate()
