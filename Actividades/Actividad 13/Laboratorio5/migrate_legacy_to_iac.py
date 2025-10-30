import os
import json
import configparser

def parse_legacy_config(config_file):
    """Lee el archivo config.cfg y extrae los parámetros"""
    config = {}
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                config[key] = value
    return config

def generate_terraform_files(config, output_dir):
    """Genera archivos network.tf.json y main.tf.json desde la config legacy"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Generar network.tf.json con variables
    network_config = {
        "variable": [
            {
                "name": [{
                    "type": "string",
                    "default": config.get("APP_NAME", "app"),
                    "description": "Nombre de la aplicación"
                }]
            },
            {
                "network": [{
                    "type": "string",
                    "default": config.get("NETWORK", "default-net"),
                    "description": "Nombre de la red"
                }]
            },
            {
                "port": [{
                    "type": "number",
                    "default": int(config.get("PORT", "8080")),
                    "description": "Puerto de la aplicación"
                }]
            }
        ]
    }
    
    # Generar main.tf.json con recursos
    main_config = {
        "resource": [{
            "null_resource": [{
                config.get("APP_NAME", "app"): [{
                    "triggers": {
                        "name": "${var.name}",
                        "network": "${var.network}",
                        "port": "${var.port}"
                    },
                    "provisioner": [{
                        "local-exec": {
                            "command": "echo 'Arrancando ${var.name} en puerto ${var.port} en red ${var.network}'"
                        }
                    }]
                }]
            }]
        }]
    }
    
    # Escribir archivos
    with open(os.path.join(output_dir, "network.tf.json"), "w") as f:
        json.dump(network_config, f, indent=4)
    
    with open(os.path.join(output_dir, "main.tf.json"), "w") as f:
        json.dump(main_config, f, indent=4)
    
    print(f"Archivos Terraform generados en: {output_dir}")

if __name__ == "__main__":
    # Configuración legacy
    legacy_config = parse_legacy_config("legacy/config.cfg")
    print(f"Configuración legacy: {legacy_config}")
    
    # Generar archivos Terraform
    output_dir = "environments/legacy-migrated"
    generate_terraform_files(legacy_config, output_dir)
    