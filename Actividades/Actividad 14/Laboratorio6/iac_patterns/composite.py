"""Patrón Composite
Permite tratar múltiples recursos Terraform como una única unidad lógica o módulo compuesto.
Soporta tanto recursos directos como submódulos anidados.
"""

from typing import List, Dict, Any

class CompositeModule:
    """
    Clase que agrega múltiples diccionarios de recursos Terraform como un módulo lógico único.
    Sigue el patrón Composite, donde se unifican estructuras individuales en una sola jerarquía.

    Ahora soporta:
    - Recursos directos (resource)
    - Submódulos (module)
    """

    def __init__(self) -> None:
        """
        Inicializa la estructura compuesta como una lista vacía de recursos hijos.
        Cada hijo será un diccionario que contiene bloques Terraform.
        """
        self._children: List[Dict[str, Any]] = []

    def add(self, resource_dict: Dict[str, Any]) -> None:
        """
        Agrega un diccionario de recurso (por ejemplo, con una clave 'resource') al módulo.

        Args:
            resource_dict: Diccionario que representa un recurso Terraform.
        """
        self._children.append(resource_dict)

    def export(self) -> Dict[str, Any]:
        """
        Exporta todos los recursos agregados a un único diccionario.
        Esta estructura se puede serializar directamente a un archivo Terraform JSON válido.

        Soporta tanto:
        - Bloques "resource" para recursos directos
        - Bloques "module" para submódulos

        Returns:
            Un diccionario con todos los recursos combinados bajo la clave "resource".
        """
        aggregated: Dict[str, Any] = {
            "resource": [],
            "module": {}
        }

        for child in self._children:
            # Combinar recursos directos
            if "resource" in child:
                aggregated["resource"].extend(child.get("resource", []))
            
            # Combinar módulos
            if "module" in child:
                # Los módulos se mergean como diccionarios, no como listas
                for module_name, module_config in child["module"].items():
                    aggregated["module"][module_name] = module_config
        
        # Limpiar claves vacías para mantener JSON limpio
        if not aggregated["resource"]:
            del aggregated["resource"]
        if not aggregated["module"]:
            del aggregated["module"]
        return aggregated
