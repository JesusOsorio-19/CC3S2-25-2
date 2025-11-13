import yaml
import access


class YAMLProjectUsers:
    """Construye recursos null_resource para cada usuario/rol y exporta a YAML."""
    
    def __init__(self, users):
        self._users = users
        self.resources = self._build()

    def _build(self):
        """Construye la estructura de recursos."""
        null_resources = {}
        for (user, identity, role) in self._users:
            res_name = f"identity_{user}_{role}".replace('-', '_')
            null_resources[res_name] = {
                "triggers": {
                    "user": user,
                    "identity": identity,
                    "role": role
                }
            }
        return {
            "resource": {
                "null_resource": null_resources
            }
        }
    
    def export(self, filename='main.tf.yaml'):
        """Exporta la configuración a YAML."""
        with open(filename, 'w') as outfile:
            yaml.dump(self.resources, outfile, 
                     default_flow_style=False, 
                     sort_keys=True,
                     indent=2)


if __name__ == "__main__":
    from main import LocalIdentityAdapter  # Reutilizamos el adapter existente
    
    # Cargar roles genéricos
    metadata = access.Infrastructure().resources
    
    # Transformar a identidades locales
    users = LocalIdentityAdapter(metadata).outputs()
    
    # Generar configuración Terraform YAML
    yaml_builder = YAMLProjectUsers(users)
    yaml_builder.export('main.tf.yaml')
    