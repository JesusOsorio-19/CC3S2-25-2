"""Patrón Factory
Encapsula la lógica de creación de objetos para recursos Terraform del tipo null_resource.
"""

from typing import Dict, Any
import uuid
from datetime import datetime

class NullResourceFactory:
    """
    Fábrica para crear bloques de recursos `null_resource` en formato Terraform JSON.
    Cada recurso incluye triggers personalizados y valores únicos para garantizar idempotencia.
    """

    @staticmethod
    def create(name: str, triggers: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Crea un bloque de recurso Terraform tipo `null_resource` con triggers personalizados.

        Args:
            name: Nombre del recurso dentro del bloque.
            triggers: Diccionario de valores personalizados que activan recreación del recurso.
                      Si no se proporciona, se inicializa con un UUID y un timestamp.

        Returns:
            Diccionario compatible con la estructura JSON de Terraform para null_resource.
        """
        triggers = triggers or {}

        # Agrega un trigger por defecto: UUID aleatorio para asegurar unicidad
        triggers.setdefault("factory_uuid", str(uuid.uuid4()))

        # Agrega un trigger con timestamp actual en UTC
        triggers.setdefault("timestamp", datetime.utcnow().isoformat())

        # Retorna el recurso estructurado como se espera en archivos .tf.json
        return {
            "resource": [{
                "null_resource": [{
                    name: [{
                        "triggers": triggers
                    }]
                }]
            }]
        }

class TimestampedNullResourceFactory(NullResourceFactory):
    """
    Variación de la Factory que permite personalizar el formato del timestamp.
    Útil para estandarizar timestamps según convenciones organizacionales.
    """
    
    @staticmethod
    def create(name: str, fmt: str = "%Y%m%d", triggers: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Crea un null_resource con un timestamp en formato personalizado.
        
        Args:
            name: Nombre del recurso
            fmt: Formato strftime para el timestamp (por defecto: '%Y%m%d')
            triggers: Triggers adicionales opcionales
            
        Returns:
            Diccionario compatible con Terraform JSON
        """
        triggers = triggers or {}
        
        # Timestamp personalizado con el formato especificado
        triggers.setdefault("timestamp_custom", datetime.utcnow().strftime(fmt))
        
        # Mantiene también el UUID para unicidad
        triggers.setdefault("factory_uuid", str(uuid.uuid4()))
        
        return {
            "resource": [{
                "null_resource": [{
                    name: [{
                        "triggers": triggers
                    }]
                }]
            }]
        }
    