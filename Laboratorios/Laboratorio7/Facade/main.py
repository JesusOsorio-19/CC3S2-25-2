import json
from pathlib import Path
import datetime

class StorageBucketModule:
    def __init__(self, name_base, buckets_dir="./buckets", interpreter_path="python"):
        self.name = f"{name_base}-storage-bucket"
        self.buckets_dir = buckets_dir
        self.interpreter = [interpreter_path, "-c"] # Almacenamos la lista completa

    def resource(self):
        return {
            "null_resource": {
                "storage_bucket": {
                    "triggers": {"name": self.name},
                    "provisioner": [{
                        "local-exec": {
                            # Usamos la variable de instancia
                            "interpreter": self.interpreter,
                            "command": (
                                f"import pathlib; "
                                f"pathlib.Path(r'{self.buckets_dir}/{self.name}').mkdir(parents=True, exist_ok=True)"
                            )
                        }
                    }]
                }
            }
        }

    def outputs(self):
        # Genera una nueva marca de tiempo UTC en formato ISO cada vez que se genera el archivo.
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        return {
            "name": self.name,
            "path": f"{self.buckets_dir}/{self.name}", 
            "created_at": now_utc                     
        }


class StorageBucketAccessModule:
    def __init__(self, bucket_facade, entity, role, interpreter_path="python"):
        self.bucket = bucket_facade
        self.entity = entity
        self.role = role
        self.interpreter = [interpreter_path, "-c"] # Almacenamos la lista completa

    def resource(self):
        # Extraemos los valores del facade
        bucket_name = self.bucket['name']
        bucket_path = self.bucket['path']
        created_at = self.bucket['created_at']

        # Creamos el nuevo comando de impresión
        print_command = (
            f"print(f'Acceso aplicado al bucket: {bucket_name}\\n"
            f"Ruta: {bucket_path}\\n"
            f"Fecha Facade: {created_at}')"
        )    

        return {
            "null_resource": {
                "bucket_access": {
                    "triggers": {
                        "bucket": self.bucket["name"],
                        "path": bucket_path,       
                        "created_at": created_at,
                        "entity": self.entity,
                        "role": self.role
                    },
                    "depends_on": ["null_resource.storage_bucket"],
                    "provisioner": [{
                        "local-exec": {
                            # Usamos la variable de instancia
                            "interpreter": self.interpreter,
                            "command": print_command    # Usamos el nuevo comando
                        }
                    }]
                }
            }
        }

class LoggingModule:
    def __init__(self, log_file="logs/iac.log"):
        self.log_file = log_file
        self.log_dir = str(Path(log_file).parent)
        # Usamos un trigger para que se ejecute en cada apply
        self.run_trigger = datetime.datetime.now(datetime.timezone.utc).isoformat()

    def resource(self):
        command = (
            f"import pathlib; "
            f"pathlib.Path(r'{self.log_dir}').mkdir(parents=True, exist_ok=True); "
            f"f = open(r'{self.log_file}', 'a', encoding='utf-8'); "
            f"f.write(f'LOG: Acceso a bucket verificado en: {self.run_trigger}\\n'); "
            f"f.close()"
        )
        
        return {
            "null_resource": {
                # Un nombre de recurso único para este módulo
                "iac_logging": { 
                    "triggers": {
                        "run_at": self.run_trigger
                    },
                    
                    "depends_on": ["null_resource.bucket_access"],
                    
                    "provisioner": [{
                        "local-exec": {
                            "interpreter": ["python", "-c"],
                            "command": command
                        }
                    }]
                }
            }
        }

if __name__ == "__main__":
    INTERPRETER_TO_USE = "python3"

    bucket_mod = StorageBucketModule(
        "hello-world", 
        interpreter_path=INTERPRETER_TO_USE
    )
    bucket_facade = bucket_mod.outputs()

    access_mod = StorageBucketAccessModule(
        bucket_facade, 
        "allAuthenticatedUsers", 
        "READER",
        interpreter_path=INTERPRETER_TO_USE
    )

    log_mod = LoggingModule()

    Path(".").mkdir(exist_ok=True)

    with open("bucket.tf.json", "w", encoding="utf-8") as f:
        json.dump({"resource": bucket_mod.resource()}, f, indent=2)

    with open("bucket_access.tf.json", "w", encoding="utf-8") as f:
        json.dump({"resource": access_mod.resource()}, f, indent=2)

    with open("logging.tf.json", "w", encoding="utf-8") as f:
        json.dump({"resource": log_mod.resource()}, f, indent=2)

    provider_conf = {
        "terraform": {
            "required_providers": {
                "null": {
                    "source": "hashicorp/null",
                    "version": "~> 3.2"
                }
            }
        },
        "provider": {
            "null": {}
        }
    }
    with open("provider.tf.json", "w", encoding="utf-8") as f:
        json.dump(provider_conf, f, indent=2)
