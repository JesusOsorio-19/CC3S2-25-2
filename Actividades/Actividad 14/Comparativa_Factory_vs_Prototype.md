# Comparativa: Factory vs Prototype en IaC

Ambos patrones están relacionados con la creación de objetos, pero tienen propósitos y casos de uso distintos en IaC.

## Patrón Factory

### Características
- Encapsula la lógica de creación desde cero
- Crea objetos nuevos con configuración inicial
- Método estático que genera instancias
- No requiere un objeto base existente

### Cuándo usar Factory en IaC
- **Creación estandarizada**: Cuando se necesite generar recursos con configuración consistente
- **Configuraciones iniciales complejas**: Cuando la lógica de inicialización es elaborada (defaults, validaciones)
- **Recursos heterogéneos**: Para crear diferentes tipos de recursos (null_resource, local_file, etc.)
- **Bajo acoplamiento**: No se depende de objetos existentes

### Ejemplo IaC
```python
# Crear recursos desde cero con configuración estándar
vpc = NullResourceFactory.create("vpc", {"cidr": "10.0.0.0/16"})
```

## Patrón Prototype

### Características
- Clona objetos existentes mediante copia profunda
- Permite variaciones del objeto base
- Usa mutators para personalización
- Reutiliza estructura compleja

### Cuándo usar Prototype en IaC
- **Variaciones sobre la base**: Cuando se tiene una configuración base y se necesita múltiples variantes
- **Recursos similares**: Para crear flotas de recursos idénticos con ligeras diferencias
- **Configuraciones complejas**: Cuando copiar es más eficiente que recrear
- **Preservación de estructura**: Mantiene configuraciones anidadas complejas

### Ejemplo IaC
```python
# Clonar configuración base y modificar instancias específicas
base = NullResourceFactory.create("server")
proto = ResourcePrototype(base)
server1 = proto.clone(lambda d: set_zone(d, "us-east-1a"))
server2 = proto.clone(lambda d: set_zone(d, "us-east-1b"))
```

## Costos y Trade-offs

### Factory
- **Ventajas**: Simple, directo, sin overhead de memoria
- **Costos**: Código duplicado si se desarrolla muchos recursos similares
- **Performance**: O(1) - creación constante

### Prototype
- **Ventajas**: Reduce duplicación, reutiliza configuraciones complejas
- **Costos**: Overhead de `deepcopy`, puede ser costoso para objetos grandes
- **Performance**: O(n) donde n es el tamaño del objeto
- **Memoria**: Duplica objetos en memoria

### Serialización y Mantenimiento
- **Factory**: Cada cambio en defaults requiere modificar la factory
- **Prototype**: Cambios en el template se propagan a todos los clones futuros
- **IaC real**: JSON resultante idéntico - la diferencia está en la generación


## Conclusión
En IaC, Factory es ideal para creación directa y Prototype para replicación eficiente. La elección depende del balance entre simplicidad de código y eficiencia de replicación. Para arquitecturas reales, combinar patrones Factory + Prototype + Composite ofrece la mayor flexibilidad.