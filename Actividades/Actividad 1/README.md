# Actividad 1: Introducción DevOps - DevSecOps

## Tiempo invertido
- Día 1: 01h:10min

## Desarrollo

## Día 1: Investigación y comparativos

### 1. DevOps vs Metodología Cascada Tradicional

DevOps representa una clara evolución respecto a la metodología cascada tradicional, especialmente para software en la nube. Mientras la cascada sigue un proceso lineal y secuencial donde debe completarse cada etapa antes de que pueda comenzar la siguiente, DevOps integra desarrollo y operaciones en ciclos continuos que permiten entregar aplicaciones y servicios a alta velocidad

#### DevOps acelera y reduce riesgo mediante:

- **Feedback continuo:** Los equipos DevOps obtienen visibilidad inmediata sobre cómo los usuarios en vivo interactúan con un sistema de software y usan esa información para desarrollar mejoras.
- **Automatización:** Los equipos usan un stack tecnológico y herramientas que les ayuda a evolucionar aplicaciones rapidamente y confiablemente.    

**Cascada Tradicional:** Sigue siendo razonable en sistemas con certificaciones regulatorias estrictas (aerospacial, dispositivos médicos) donde se requiere documentación exhaustiva y trazabilidad completa de cambios.

### 2. Ciclo tradicional de dos pasos y silos

#### Limitaciones del ciclo "construcción -> operación"

**1. Grandes cantidades y colas de defectos:**  La metodología cascada carece de adaptabilidad y el enfoque estricto en cumplir los requisitos originales desalienta errores y cambios.

**2. Asimetrías de información:** La falta de comunicación introduce interpretaciones muy variadas de requisitos y documentación entre miembros del equipo.

#### Anti-patrones identificados
**1. Throw over the wall:** Se entrega código sin contexto operativo, causando un ambiente tradicional de "nosotros" y "ellos" entre el equipo de desarrollo y operaciones.

**2. Seguridad como auditoría tardía:** Tradicionalmente las prácticas de seguridad como testing, escaneo de vulnerabilidades tendrían lugar al final, incrementando los costos de integración.

**Incidentes comunes**
- Retrabajos repetitivos: Sin feedback continuo, los mismos problemas de integración se repiten
- Degradaciones repetitivas: Sin integración continua, la estabilidad del código llega a cero muy rápido.

### 3. Principios y beneficios de DevOps

**CI/CD elementos clave:**

- **Tamaño de cambios pequeños:** DevOps promueve integración continua de código actualizado, binarios y dependencias en aplicaciones después de ser liberadas.

- **Pruebas automatizadas cercanas al código:** Se integran herramientas como "SonarQube, PHPStan, y OWASP Zap para análisis SAST y DAST" en el pipeline.

- **Colaboración:** Los equipos de desarrollo y operaciones colaboran cercanamente, comparten muchas responsabilidades y combinan sus flujos de trabajo.

#### Práctica alimentando decisiones del pipeline:
Las retrospectivas informan umbrales de quality gates: si las retrospectivas revelan 40% de bugs por validación insuficiente, se ajusta el umbral de cobertura de pruebas de 70% - 85% o dependiendo del equipo.

**Como recolectarlo:**
- Metadatos de PRs (timestamps de aprobación)
- Logs de CI/CD (timestamps de inicio/fin de despliegue)

### DevOps vs Cascade
![](imagenes/devops-vs-cascada.png)
La metodología Cascada Tradicional representa un proceso lineal y secuencial, donde cada fase se completa una tras otra sin retorno, lo que genera una colaboración limitada y entregas lentas. Por lo contrario, DevOps, simboliza un ciclo continuo e integrado, destacando la colaboración constante entre equipos, la entrega rápida de valor y la automatización de procesos clave, lo que se traduce en mayor agilidad y eficiencia.

### Silos equipos

![](imagenes/silos-equipos.png)

Las secciones separadas simbolizan a los equipos de Desarrollo, QA (control de calidad) y Operaciones, cada uno aislado y enfocado en sus propias tareas, como las líneas de código, la detección de errores y la gestión de servidores. Las barreras en el centro ilustran la falta de comunicación y la desconexión entre ellos, lo que puede causar retrasos en el flujo de trabajo.

## Día 2: Seguridad y despliegue

### Evolución a DevSecOps

#### SAST vs DAST

- **SAST(Static Application Security Testing):** 
    - Estático: Se aplica al código fuente y no ejecuta el código que está escaneando.
    - Análisis de patrones: Las herramientas SAST analizan patrones de código, flujo de datos y puntos de inyección potenciales contra una base de datos de vulnerabilidades conocidas.
    - Ubicación: Pre commit y build stages del pipeline.

- **DAST (Dynamic Application Security Testing):**
    - Dinámico: Simula ataques del mundo real enviando solicitudes automatizadas y payloads a la aplicación (similar a lo que haría un atacante malicioso).
    - Testing de caja negra: Prueba aplicaciones web mientras están ejecutándose para identificar vulnerabilidades de seguridad.
    - Ubicación: Staging y pre-production stages del pipeline.

### Gate mínimo de seguridad con umbrales cuantitativos:

#### Gate 1 - SAST: Vulnerabilidades Críticas

- **Umbral:** Vulnerabilidades críticas en componentes expuestos bloquea la promoción.
- **Justificación:** Vulnerabilidades críticas como "inyecciones SQL" representan riesgos graves. 

#### Gate 2 - DAST: Cobertura Mínima 

- **Umbral:** >= 80% de cobertura de pruebas dinámicas en rutas críticas de API
- **Justificación:** Cubre la mayoría de funcionalidades, reduciendo riesgos como XSS

### Política de excepción con caducidad:

Se aplica cuando no es posible corregir un hallazgo inmediatamente:

- Autorización: Lead Security + Tech Lead.
- Duración máxima: 7 días calendario.
- Plan de corrección: Implementar mitigación temporal (WAF, rate limiting) + parche definitivo.
- Responsable: Tech Lead asignado debe reportar progreso diario.
- Re-evaluación: Escaneo DAST obligatorio antes del vencimiento.

    > ****Teach Lead***: Desarrollador más experimentado del equipo.*  
    > ****Lead Security***: Encargado de las estrategias, políticas y sistemas de seguridad.*  
    > ****WAF*** (Web application firewall)*

### Evitar "teatro de seguridad"

Señales de eficacia

1. Reducción de hallazgos repetidos
    - Métrica: <= 5% de vulnerabilidades recurrentes entre sprints consecutivos.
    - Medición: Comparar informes de SAST/DAST entre despliegues consecutivos.

2. Tiempo de remediación efectivo
    - Métrica: <= 48hrs para vulnerabilidades críticas (desde detección hasta fix verificado).
    - Medición: Timestamping en pipeline (detección) + commit fix + nuevo escaneo limpio.

## CI/CD y estrategias de despliegue

La estrategia elegida para microservicios de autenticación es **Canary**. El servicio de autenticación es crítico pero permite validación gradual. Canary permite actualizaciones rápidas y mejoras, llevando a mayor eficiencia, gastos reducidos y confiabilidad aumentada.

### Tabla de riesgos vs mitigaciones

| Riesgo | Mitigación | 
| :--- | :--- | 
| Regresión funcional en autenticación | Validación de contrato OAuth2/JWT antes de promover canary | 
| Costo operativo de doble despliegue | Límite temporal: canary máximo 2 horas de convivencia | 
| Manejo de sesiones | Session draining + compatibilidad backward de tokens | 

#### KPI primario para el Gate
- Métrica técnica: Tasa de errores HTTP 5xx <= 0.1% 
- Ventana de observación: 1hr post despliegue canary
- Umbral de rollback: Si >0.1% durante 10min consecutivos -> rollback automático    

#### ¿Por qué coexisten métricas técnicas y de producto?

Aunque el KPI técnico (latencia, errores) se mantenga estable, una caída en métrica de producto como tasa de conversión de login (de 95% a 80%) indica problemas funcionales o de UX que el monitoreo técnico no detecta.

> *Un KPI (Key Performance Indicator), es una metrica medible que se usa para evaluar si un proceso, sistema o equipo esta cumpliendo con un objetivo especifico.*

### Canary en pipeline

![](imagenes/pipeline_canary.png)

Esta imagen ilustra un pipeline de despliegue continuo que incorpora una estrategia de lanzamiento canary para minimizar riesgos. El proceso comienza con la fase de Build (construcción) del software. Una vez construido, pasa por rigurosas pruebas automatizadas que incluyen Unit Tests, Integration Tests y Contract Tests para asegurar su calidad. Solo después de superar estas pruebas, el software se envía a un Deploy Canary (despliegue canario), donde una pequeña porción del tráfico (indicado como 10%) es redirigida a la nueva versión para monitorear su rendimiento en un entorno real. Si esta fase canary es exitosa y estable, se procede al Deploy Production (despliegue a producción), donde la nueva versión se lanza completamente (100% Rollout) a todos los usuarios, completando un ciclo de entrega seguro y eficiente.