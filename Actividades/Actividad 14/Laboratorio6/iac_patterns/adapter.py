"""Patrón Adapter
Convierte un null_resource a otros tipos de recursos simulados.
Útil para testing y desarrollo sin dependencias cloud reales.
"""

from typing import Dict, Any


class MockBucketAdapter:
    """
    Adapter simple que transforma un null_resource en un recurso mock_cloud_bucket.
    Mapea los triggers del null_resource como atributos del bucket.
    """
    
    def __init__(self, null_block: Dict[str, Any]) -> None:
        """
        Inicializa el adapter con un bloque null_resource.
        
        Args:
            null_block: Diccionario que contiene un null_resource en formato Terraform JSON.
        """
        self.null = null_block
    
    def to_bucket(self) -> Dict[str, Any]:
        """
        Transforma el null_resource a un mock_cloud_bucket.
        
        Returns:
            Diccionario compatible con formato Terraform JSON para un bucket simulado.
        """
        # Extraer nombre y triggers del null_resource original
        null_res = self.null["resource"][0]["null_resource"][0]
        name = list(null_res.keys())[0]
        triggers = null_res[name][0]["triggers"]
        
        # Retornar estructura adaptada como mock_cloud_bucket
        return {
            "resource": [{
                "mock_cloud_bucket": [{
                    name: [{
                        "name": name,
                        **triggers  # Los triggers se convierten en atributos del bucket
                    }]
                }]
            }]
        }