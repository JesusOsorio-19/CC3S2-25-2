import json
import access


class AWSIdentityAdapter:
    """Adapter para transformar roles genéricos a recursos AWS IAM."""
    
    # Mapeo de roles a políticas AWS administradas
    POLICY_MAP = {
        'read': 'arn:aws:iam::aws:policy/ReadOnlyAccess',
        'write': 'arn:aws:iam::aws:policy/PowerUserAccess',
        'admin': 'arn:aws:iam::aws:policy/AdministratorAccess'
    }
    
    def __init__(self, metadata, account_id='123456789012'):
        """
        Args:
            metadata: Diccionario con roles y usuarios
            account_id: ID de cuenta AWS (simulado)
        """
        self.account_id = account_id
        self.aws_users = []
        
        for role, users in metadata.items():
            policy_arn = self.POLICY_MAP.get(role)
            if not policy_arn:
                continue
                
            for user in users:
                # Generar ARN del usuario
                user_arn = f"arn:aws:iam::{account_id}:user/{user}"
                # Mantener estructura de tupla (user, arn, policy)
                self.aws_users.append((user, user_arn, policy_arn))
    
    def outputs(self):
        """Retorna lista de tuplas (user, arn, policy)."""
        return self.aws_users


class AWSProjectUsers:
    """Construye recursos null_resource simulando IAM users y policy attachments."""
    
    def __init__(self, users):
        self._users = users
        self.resources = self._build()
    
    def _build(self):
        """Construye recursos simulados de AWS IAM."""
        null_resources = {}
        
        for (user, user_arn, policy_arn) in self._users:
            # Recurso 1: Simular aws_iam_user
            user_res_name = f"aws_user_{user}".replace('-', '_')
            null_resources[user_res_name] = {
                "triggers": {
                    "user_name": user,
                    "arn": user_arn
                }
            }
            
            # Recurso 2: Simular aws_iam_policy_attachment
            # Extraer nombre de política del ARN
            policy_name = policy_arn.split('/')[-1]
            attachment_res_name = f"aws_policy_attachment_{user}_{policy_name}".replace('-', '_')
            null_resources[attachment_res_name] = {
                "triggers": {
                    "user": user,
                    "user_arn": user_arn,
                    "policy_arn": policy_arn
                }
            }
        
        return {
            "resource": {
                "null_resource": null_resources
            }
        }


if __name__ == "__main__":
    # Cargar los roles genéricos
    metadata = access.Infrastructure().resources
    
    # Transformar a identidades AWS
    aws_adapter = AWSIdentityAdapter(metadata, account_id='123456789012')
    users = aws_adapter.outputs()
        
    # Generar configuración Terraform JSON para AWS
    aws_builder = AWSProjectUsers(users)
    
    with open('main_aws.tf.json', 'w') as outfile:
        json.dump(aws_builder.resources, outfile, 
                 sort_keys=True, indent=4)
