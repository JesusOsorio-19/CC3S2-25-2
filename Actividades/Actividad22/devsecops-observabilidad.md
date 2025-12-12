# Ciclo de vida DevSecOps con Observabilidad y Métricas

## 1. Integración de observabilidad en cada fase del ciclo DevSecOps

### Planificación / Diseño

**Actividades de observabilidad**:
- Definir SLIs (Service Level Indicators) y SLOs (Service Level Objectives) desde el diseño
- Planificar qué métricas, logs y trazas se necesitarán
- Diseñar la arquitectura de instrumentación (OpenTelemetry, agentes, pipelines)

**Ejemplo en esta actividad**:
- Definimos que `demo-app` debe tener:
  - SLI: Error rate < 0.1% (1 error cada 1000 requests)
  - SLI: P95 latencia < 200ms
  - SLI: Disponibilidad > 99.9%

### Construcción y Pruebas (CI)

**Actividades de observabilidad**:
- Instrumentar código con OpenTelemetry (métricas, logs, trazas)
- Tests unitarios que verifican que la instrumentación funciona
- Análisis de logs en tests de integración

**Ejemplo en esta actividad**:
```python
# En main.py agregamos instrumentación OpenTelemetry
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

FastAPIInstrumentor.instrument_app(app)
```

**Gates de calidad**:
```yaml
# Pipeline CI
- name: Verify instrumentation
  run: |
    # Verificar que las métricas se exportan
    curl http://localhost:8080/metrics | grep http_server_requests_total
    if [ $? -ne 0 ]; then
      echo "Métricas no encontradas"
      exit 1
    fi
```

### Despliegue (CD)

**Actividades de observabilidad**:
- Canary deployments monitoreados con métricas en tiempo real
- Blue-Green deployments con comparación de error rates
- Rollback automático basado en métricas

**Ejemplo - Gate pre-deploy**:
```bash
# Verificar que el stack de observabilidad está UP
OTEL_UP=$(curl -s http://prometheus:9090/api/v1/query?query=up{job="otel-collector"} | jq -r '.data.result[0].value[1]')

if [ "$OTEL_UP" != "1" ]; then
  echo "OTEL Collector DOWN - Abortando deploy"
  exit 1
fi
```

**Ejemplo - Gate post-deploy**:
```bash
# Esperar 5 minutos y verificar error rate
sleep 300

ERROR_RATE=$(curl -s 'http://prometheus:9090/api/v1/query?query=sum(rate(http_server_requests_total{status_code=~"5.."}[5m]))' | jq -r '.data.result[0].value[1]')

if (( $(echo "$ERROR_RATE > 0.1" | bc -l) )); then
  echo "Error rate $ERROR_RATE supera umbral - Iniciando rollback"
  kubectl rollout undo deployment/demo-app
  exit 1
fi

echo "Deploy exitoso - Error rate: $ERROR_RATE"
```

### Operación / Respuesta a Incidentes

**Actividades de observabilidad**:
- Monitoreo 24/7 con dashboards en Grafana
- Alertas automáticas vía PagerDuty/Slack cuando se violan SLOs
- Investigación de incidentes usando los 3 pilares (métricas, logs, trazas)

**Flujo de investigación de incidente**:

1. Alerta dispara: "Error rate 5xx > 0.1 req/s durante 5 minutos"
   
2. SRE abre Grafana Dashboard
   
3. Prometheus: Confirma error rate en panel "Error Rate 5xx"
   
4. Loki: {job="demo-app"} |= "ERROR" → ve mensajes específicos
   
5. Tempo: {status = error} -> obtiene trace_id de una petición fallida
   
6. Correlación: Busca en Loki con trace_id para ver logs contextuales
   
7. Root cause: Identifica que el endpoint /api/v1/error tiene bug en línea X
   
8. Fix: Hotfix + deploy + verificación en métricas que error rate vuelve a 0


**Ejemplo real**:
```logql
# En Loki, buscar logs de una traza específica
{job="demo-app"} |= "d9afaff1ee8449b26db06"
```

### Aprendizaje / Mejora Continua

**Actividades de observabilidad**:
- Análisis post-mortem basado en métricas históricas
- Ajuste de SLOs basado en datos reales
- Optimización de costos (reducir retención de logs/trazas innecesarios)
- Mejora de instrumentación (agregar nuevas métricas identificadas como faltantes)

**Ejemplo**:

Hallazgo: El P95 de latencia del endpoint /api/v1/items es 148ms, 
          pero el SLO es <200ms. Hay margen de mejora.

Acción: 
1. Crear traza detallada para ver qué operación interna es lenta
2. Optimizar query a base de datos
3. Verificar en métricas que el P95 baja a <100ms
4. Actualizar SLO a <100ms para mejorar experiencia de usuario

## 2. Gates DevSecOps con métricas/logs/trazas

### Gate 1: Pre-Merge (Code Review + CI)

**Objetivo**: Verificar que el código nuevo no rompe la instrumentación.

**Implementación**:
```yaml
# .github/workflows/ci.yml
- name: Test instrumentation
  run: |
    docker-compose up -d app otel-collector prometheus
    sleep 10
    
    # Generar tráfico
    curl http://localhost:8080/api/v1/items
    
    # Verificar que métricas llegan a Prometheus
    METRICS=$(curl -s 'http://localhost:9090/api/v1/query?query=http_server_requests_total' | jq '.data.result | length')
    
    if [ "$METRICS" -eq 0 ]; then
      echo "No se generaron métricas - PR bloqueado"
      exit 1
    fi
    
    echo "Instrumentación funcional - $METRICS series generadas"
```

**Métricas/Logs/Trazas usadas**:
- Métricas: `http_server_requests_total` debe existir
- Logs: No debe haber logs de ERROR en logs de OTEL Collector
- Trazas: Al menos 1 traza debe llegar a Tempo

### Gate 2: Pre-Deploy a Producción (Staging)

**Objetivo**: Validar que en staging no hay errores antes de pasar a producción.

**Implementación**:
```bash
#!/bin/bash
# scripts/staging-gate.sh

echo "Verificando staging antes de deploy a producción..."

# 1. Verificar error rate en últimos 15 minutos
ERROR_RATE=$(curl -s 'http://prometheus-staging:9090/api/v1/query?query=sum(rate(http_server_requests_total{status_code=~"5..",env="staging"}[15m]))' | jq -r '.data.result[0].value[1] // 0')

if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
  echo "Error rate en staging: $ERROR_RATE req/s (umbral: 0.01)"
  echo "   No se permite deploy a producción"
  exit 1
fi

# 2. Verificar que no hay logs de ERROR en últimos 15 minutos
ERROR_LOGS=$(curl -s -G 'http://loki-staging:3100/loki/api/v1/query' \
  --data-urlencode 'query={job="demo-app",env="staging"} |= "ERROR"' \
  --data-urlencode 'time=now' | jq '.data.result | length')

if [ "$ERROR_LOGS" -gt 0 ]; then
  echo "Se encontraron $ERROR_LOGS logs de ERROR en staging"
  exit 1
fi

# 3. Verificar latencia P95 < 200ms
LATENCY_P95=$(curl -s 'http://prometheus-staging:9090/api/v1/query?query=histogram_quantile(0.95,sum(rate(http_server_duration_milliseconds_bucket{env="staging"}[15m]))by(le))' | jq -r '.data.result[0].value[1] // 0')

if (( $(echo "$LATENCY_P95 > 200" | bc -l) )); then
  echo "Latencia P95: ${LATENCY_P95}ms (umbral: 200ms)"
  exit 1
fi

echo "Todas las verificaciones pasaron"
echo "   - Error rate: $ERROR_RATE req/s"
echo "   - Error logs: $ERROR_LOGS"
echo "   - Latency P95: ${LATENCY_P95}ms"
echo "Autorizado deploy a producción"
```

### Gate 3: Post-Deploy (Smoke Tests)

**Objetivo**: Verificar salud inmediata después del deploy.

**Implementación**:
```bash
#!/bin/bash
# scripts/post-deploy-gate.sh

echo "Ejecutando smoke tests post-deploy..."

# Esperar que el servicio esté UP
kubectl wait --for=condition=ready pod -l app=demo-app --timeout=120s

# Generar tráfico de prueba
for i in {1..10}; do
  curl -s http://demo-app/api/v1/items > /dev/null
  curl -s http://demo-app/healthz > /dev/null
done

sleep 60  # Esperar a que métricas se agreguen

# Verificar que el servicio responde
UP=$(curl -s 'http://prometheus:9090/api/v1/query?query=up{job="demo-app"}' | jq -r '.data.result[0].value[1]')

if [ "$UP" != "1" ]; then
  echo "Servicio DOWN - Iniciando rollback automático"
  kubectl rollout undo deployment/demo-app
  exit 1
fi

# Verificar que no hay errores 5xx en los primeros 2 minutos
ERROR_COUNT=$(curl -s 'http://prometheus:9090/api/v1/query?query=increase(http_server_requests_total{job="demo-app",status_code=~"5.."}[2m])' | jq -r '.data.result[0].value[1] // 0')

if (( $(echo "$ERROR_COUNT > 0" | bc -l) )); then
  echo "Se detectaron $ERROR_COUNT errores 5xx - Rollback"
  kubectl rollout undo deployment/demo-app
  exit 1
fi

echo "Smoke tests pasaron - Deploy estable"
```

### Gate 4: Seguridad - Detección de patrones sospechosos

**Objetivo**: Detectar comportamientos anómalos que puedan indicar ataques.

**Implementación**:
```promql
# Alerta en Grafana: Picos sospechosos de errores 4xx (posible brute force)
(
  sum(rate(http_server_requests_total{status_code=~"4.."}[5m]))
  /
  sum(rate(http_server_requests_total[5m]))
) > 0.3  # Más del 30% son 4xx
```

```logql
# Buscar patrones de SQL injection en logs
{job="demo-app"} |~ "(?i)(select.*from|union.*select|drop.*table)"
```

```traceql
# Detectar trazas con latencia anómala (posible DoS)
{.service.name = "demo-app" && duration > 5s}
```

## 3. Integración del servidor MCP

### ¿Qué es MCP?

El **MCP Server** (Model Context Protocol) actúa como una capa de abstracción que:
- Expone recursos de observabilidad (métricas, logs, trazas) como recursos consultables
- Permite a agentes LLM/IA consultar y analizar telemetría de forma estructurada
- Facilita la automatización de análisis de incidentes

### Casos de uso del MCP Server

#### Uso 1: Asistente SRE con IA

**Escenario**: Un SRE pregunta a un agente IA: *"¿Por qué subió la latencia en la última hora?"*

**Flujo con MCP**:

1. Agente consulta MCP Server: GET /resources/prometheus/latency-p95

2. MCP ejecuta query en Prometheus y devuelve JSON estructurado

3. Agente correlaciona con logs: GET /resources/loki/recent-errors

4. Agente identifica que hay logs "Slow request simulated" en Loki

5. Agente sugiere: "La latencia subió por el endpoint /api/v1/work.
   Ver traza <trace_id> para más detalle"


**Ejemplo de recurso MCP**:
```json
{
  "uri": "mcp://observability/metrics/error-rate",
  "mimeType": "application/json",
  "description": "Error rate 5xx de demo-app",
  "metadata": {
    "query": "sum(rate(http_server_requests_total{status_code=~\"5..\"}[5m]))",
    "value": 0.05,
    "unit": "req/s",
    "threshold": 0.1,
    "status": "normal"
  }
}
```

#### Uso 2: Consolidación de señales para análisis

**Problema**: SRE necesita ver métricas + logs + trazas correlacionadas, pero están en 3 sistemas distintos.

**Solución con MCP**:
```bash
# MCP Server expone endpoint consolidado
curl http://mcp-server:8000/api/incident-context?trace_id=d9afaff1ee8449b26db06

# Respuesta JSON con todo correlacionado:
{
  "trace_id": "d9afaff1ee8449b26db06",
  "metrics": {
    "error_rate": 0.05,
    "latency_p95": 145,
    "rps": 250
  },
  "logs": [
    "2025-12-12 11:31:45 ERROR Simulated error endpoint called"
  ],
  "trace": {
    "duration_ms": 3,
    "spans": [
      {"name": "GET /api/v1/error", "status": "error"}
    ]
  },
  "recommendation": "El error es simulado en el endpoint /api/v1/error. No requiere acción."
}
```

#### Uso 3: Gates automáticos con IA

**Escenario**: Pipeline CI/CD pregunta a MCP si es seguro hacer deploy.

```python
# scripts/ai-gate.py
import requests

response = requests.get("http://mcp-server:8000/api/deployment-readiness")
data = response.json()

if data["status"] == "ready":
    print(f"{data['message']}")
    print(f"Métricas OK: {data['checks_passed']}")
    exit(0)
else:
    print(f"{data['message']}")
    print(f"Problemas detectados: {data['issues']}")
    exit(1)
```

**MCP Server analiza** (con LLM opcional):
- Error rate < umbral
- Latencia normal
- Sin logs de ERROR recientes
- Sin trazas con status=error
