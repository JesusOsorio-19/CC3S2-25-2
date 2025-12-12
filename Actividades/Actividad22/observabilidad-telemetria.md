# Observabilidad y Telemetría

## 1. Monitoreo vs Observabilidad

### Monitoreo
El monitoreo es un enfoque que responde a la pregunta "¿está funcionando el sistema?". Se basa en métricas predefinidas, umbrales fijos y dashboards estáticos que alertan cuando algo conocido falla. Por ejemplo, una alerta que se dispara cuando el uso de CPU supera el 90% o cuando un servicio deja de responder. El monitoreo es útil para detectar problemas ya conocidos y esperados.

### Observabilidad
La observabilidad es un enfoque proactivo que permite responder "¿por qué no está funcionando?". Un sistema es observable cuando podemos inferir su estado interno a partir de sus salidas (métricas, logs, trazas). A diferencia del monitoreo, la observabilidad permite explorar y correlacionar datos para diagnosticar problemas desconocidos o inesperados. No solo detecta que hay un error 500, sino que permite rastrear exactamente qué petición falló, en qué servicio, con qué parámetros y por qué.

---

## 2. Tipos de Telemetría

### 2.1 Métricas (Prometheus / OpenTelemetry)
Las métricas son valores numéricos agregados que representan el estado del sistema en un momento dado. Se recolectan a intervalos regulares y permiten análisis estadístico y tendencias. En este stack, la aplicación FastAPI está instrumentada con OpenTelemetry, que exporta métricas al OTEL Collector, el cual las expone para que Prometheus las raspe (scrape). Existen tres tipos principales de métricas:
- **Counters**: valores que solo aumentan (ej: total de peticiones).
- **Gauges**: valores que suben y bajan (ej: memoria en uso).
- **Histogramas**: distribuciones de valores (ej: latencias de respuesta).

### 2.2 Logs (Loki)
Los logs son registros textuales de eventos con marca de tiempo que describen qué sucedió en el sistema. Capturan información detallada como mensajes de error, stack traces, datos de contexto y acciones del usuario. En este stack, Promtail recolecta los logs generados por la aplicación (desde archivos o stdout) y los envía a Loki, donde se indexan por etiquetas (labels) y se pueden consultar con LogQL. Los logs son esenciales para debugging y auditoría de seguridad.

### 2.3 Trazas Distribuidas (Tempo)
Las trazas capturan el recorrido completo de una petición a través de múltiples servicios. Cada traza se compone de spans (segmentos) que representan operaciones individuales con su duración, servicio, y relación padre-hijo. OpenTelemetry instrumenta la aplicación para generar trace-id y span-id únicos, propagando el contexto entre servicios. Tempo almacena estas trazas y permite consultarlas con TraceQL. Las trazas son fundamentales para identificar cuellos de botella y entender el flujo de datos en arquitecturas de microservicios.

### 2.4 Otros Tipos de Telemetría
Aunque no están implementados en este stack, existen otros tipos de telemetría relevantes:
- **Eventos**: Ocurrencias discretas significativas (despliegues, cambios de configuración, incidentes).
- **Profiling**: Análisis detallado del rendimiento del código (uso de CPU por función, asignación de memoria).
- **Heartbeats**: Señales periódicas de "estoy vivo" para detectar servicios caídos.
- **Excepciones**: Captura estructurada de errores con contexto completo.

---

## 3. Arquitectura del Stack
```
┌─────────┐      ┌─────────────────┐       ┌────────────┐
│   APP   │─────▶│  OTEL Collector │─────▶│ Prometheus │──┐
│ FastAPI │      │                 │       │ (métricas) │  │
└─────────┘      └─────────────────┘       └────────────┘  │
     │                   │                                 │
     │                   ├───────────────▶┌──────────┐    │
     │                   │                │   Loki   │────┼───▶┌─────────┐
     │                   │                │  (logs)  │    │    │ GRAFANA │
     │                   │                └──────────┘    │    │         │
     │                   │                                │    └────┬────┘
     │                   └───────────────▶┌──────────┐    │         │
     │                                    │  Tempo   │────┘         │
     │                                    │ (trazas) │              │
     │                                    └──────────┘              ▼
     │                                                      ┌────────────┐
     └──────────────────────────────────────────────────────│ MCP Server │
            Promtail (recolección de logs)                  │/api/summary│
                                                            └────────────┘
```

### Flujo de datos:
1. **App FastAPI** genera métricas y trazas vía OpenTelemetry SDK
2. **OTEL Collector** recibe, procesa y exporta telemetría a los backends
3. **Prometheus** almacena métricas y permite consultas PromQL
4. **Loki** almacena logs indexados por labels, consultables con LogQL
5. **Tempo** almacena trazas distribuidas, consultables con TraceQL
6. **Grafana** unifica la visualización de las tres fuentes de datos
7. **MCP Server** expone `/api/summary` con resúmenes para agentes LLM