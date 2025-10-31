"""Patrón Builder
Construye de manera fluida configuraciones Terraform locales combinando los patrones Factory, Prototype y Composite.
"""

from typing import Dict, Any
import os
import json

from .factory import NullResourceFactory
from .composite import CompositeModule
from .prototype import ResourcePrototype

class InfrastructureBuilder:
    """Builder fluido que combina los patrones Factory, Prototype y Composite para crear módulos Terraform."""

    def __init__(self, env_name: str) -> None:
        """
        Inicializa el builder con un nombre de entorno y una instancia de módulo compuesto.
        """
        self.env_name = env_name
        self._module = CompositeModule()

    #  Métodos de construcción (steps) 

    def build_null_fleet(self, count: int = 5) -> "InfrastructureBuilder":
        """
        Construye una flota de `null_resource` clonados a partir de un prototipo base.
        Cada recurso tiene un trigger que lo identifica por índice, y un nombre válido.
        """
        # Se crea un prototipo reutilizable a partir de un recurso null de fábrica
        base_proto = ResourcePrototype(
            NullResourceFactory.create("placeholder")
        )

        for i in range(count):
            def mutator(d: Dict[str, Any], idx=i) -> None:
                """
                Función mutadora: modifica el nombre del recurso clonado
                e inserta un trigger identificador con el índice correspondiente.
                """
                res_block = d["resource"][0]["null_resource"][0]
                # Nombre original del recurso (por defecto "placeholder")
                original_name = next(iter(res_block.keys()))
                # Nuevo nombre válido: empieza con letra y contiene índice
                new_name = f"{original_name}_{idx}"
                # Renombramos la clave en el dict
                res_block[new_name] = res_block.pop(original_name)
                # Añadimos el trigger de índice
                res_block[new_name][0]["triggers"]["index"] = idx

            # Clonamos el prototipo y aplicamos la mutación
            clone = base_proto.clone(mutator).data
            # Agregamos el recurso clonado al módulo compuesto
            self._module.add(clone)

        return self

    def add_custom_resource(self, name: str, triggers: Dict[str, Any]) -> "InfrastructureBuilder":
        """
        Agrega un recurso null personalizado al módulo compuesto.

        Args:
            name: nombre del recurso.
            triggers: diccionario de triggers personalizados.
        Returns:
            self: permite encadenar llamadas.
        """
        self._module.add(NullResourceFactory.create(name, triggers))
        return self

    #  Método final (exportación) 

    def export(self, path: str) -> None:
        """
        Exporta el módulo compuesto a un archivo JSON compatible con Terraform.

        Args:
            path: ruta de destino del archivo `.tf.json`.
        """
        data = self._module.export()

        # Asegura que el directorio destino exista
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Escribe el archivo con indentación legible
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"[Builder] Terraform JSON escrito en: {path}")

    def build_group(self, name: str, size: int) -> "InfrastructureBuilder":
        """
        Construye un grupo de recursos relacionados con un nombre base.
        Cada recurso del grupo tiene un sufijo numérico y comparte metadata del grupo.
        
        Args:
            name: Nombre base del grupo (e.g., "webserver", "database")
            size: Número de recursos en el grupo
            
        Returns:
            self: Permite encadenar llamadas (fluent interface)
        """
        # Crear un prototipo base para el grupo
        base_proto = ResourcePrototype(
            NullResourceFactory.create(name, triggers={"group": name})
        )
        
        # Composite para almacenar los recursos del grupo
        group_composite = CompositeModule()
        
        for i in range(size):
            def mutator(d: Dict[str, Any], idx=i, group_name=name) -> None:
                """
                Mutator que personaliza cada recurso del grupo:
                - Renombra con sufijo numérico
                - Añade metadata de grupo
                - Asigna índice dentro del grupo
                """
                res_block = d["resource"][0]["null_resource"][0]
                
                # Obtener nombre original del recurso
                original_name = next(iter(res_block.keys()))
                
                # Nuevo nombre: <grupo>_<índice>
                new_name = f"{group_name}_{idx}"
                
                # Renombrar la clave en el diccionario
                res_block[new_name] = res_block.pop(original_name)
                
                # Añadir metadata del grupo
                res_block[new_name][0]["triggers"]["group_index"] = idx
                res_block[new_name][0]["triggers"]["group_size"] = size
                res_block[new_name][0]["triggers"]["group_name"] = group_name
            
            # Clonar el prototipo y aplicar mutación
            clone = base_proto.clone(mutator).data
            
            # Agregar el recurso clonado al composite del grupo
            group_composite.add(clone)
        
        # Exportar el grupo y añadirlo al módulo principal
        # Nota: Como no podemos usar módulos Terraform reales sin source,
        # simplemente agregamos todos los recursos del grupo al módulo principal
        for child in group_composite._children:
            self._module.add(child)
        
        return self
