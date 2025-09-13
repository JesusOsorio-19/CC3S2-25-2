## Actividad 3: Integración de DevOps y DevSecOps con HTTP, DNS, TLS y 12-Factor App

Esta actividad cierra la unidad cubriendo los temas de Introducción a DevOps (qué es y qué no es, del código a producción), el marco CALMS, automatización reproducible con 
Linux/Bash y Make, la visión cultural de DevOps (comunicación y colaboración) y su evolución a DevSecOps, así como los módulos de redes y arquitectura  (HTTP/DNS/TLS, puertos/procesos y metodología 12-Factor App). 

La actividad se divide en una parte teórica (reflexión conceptual) y una parte práctica (ejercicios basados en el laboratorio proporcionado). 

### Parte teórica

1. **Introducción a DevOps: ¿Qué es y qué no es?**
   Explica DevOps desde el código hasta la producción, diferenciándolo de waterfall. Discute "you build it, you run it" en el laboratorio, y separa mitos (ej. solo herramientas) vs realidades (CALMS, feedback, métricas, gates).

   - DevOps es una filosofía de trabajo y conjunto de prácticas que integra el desarrollo y las operaciones para lograr despliegues rápidos, automatizados y confiables para acelerar y mejorar la entrega de software de forma confiable

   - **DevOps vs Waterfall**
      
      - **Waterfall:** Fases secuenciales rígidas -> requisitos -> desarrollo -> pruebas -> operación. Todo estas fases con un feedback tardío.

      - **DevOps:** Iteraciones continuas, equipos integrados, feedback temprano y frecuente.

   - **"You build it, you run it":**  Los equipos que desarrollan el código también operan y mantienen sus aplicaciones en producción.

      - En la actividad: si defines un servicio en `systemd` o un `nginx.conf`, como desarrollador también debes monitorear su estado con `journalctl`y/o `systemctl status`.

   - **Mitos vs Realidades**

      - Mito: DevOps son solo herramientas (Jenkins, Docker, Kubernetes) o elimina las operaciones.
      - Realidad: Es principalmente cultura, colaboración y prácticas. Integra desarrollo y operaciones en equipos multifuncionales
         
2. **Marco CALMS en acción:**
   Describe cada pilar y su integración en el laboratorio (ej. Automation con Makefile, Measurement con endpoints de salud). Propón extender Sharing con runbooks/postmortems en equipo.

      | Pilar CALMS | Descripción |  Ejemplo  |
      |-------------|-------------|------------------|
      | **Culture** | Colaboración entre equipos, responsabilidad compartida, eliminación de silos | `runbooks.md` para que todo el equipo sepa que hacer si un servicio falla. |
      | **Automation** | Procesos repetibles, reproducibles y automatizables, evitando tareas manuales | Makefile con targets (`make run`, `make prepare`, etc) levanta automáticamente la app sin intervención manual |
      | **Lean** | Entrega continua y eliminación de desperdicios| Desplegar solo servicios necesarios, usando el comando `make hosts-setup` configura DNS local vs. múltiples pasos manuales |
      | **Measurement** | Métricas, monitoreo, observabilidad para toma de decisiones | `curl -s http://miapp.local/health` retorna status de la aplicación. También endpoints /health en Flask o usar ss -ltnp para ver puertos activos |
      | **Sharing** | Conocimiento, herramientas y responsabilidades compartidas | postmortems guardados en repositorio (docs/postmortems/) |

   * Propuesta: Extender Sharing con guías rápidas (`runbooks.md`) y análisis de incidentes en equipo.
   
3. **Visión cultural de DevOps y paso a DevSecOps:**
   Analiza colaboración para evitar silos, y evolución a DevSecOps (integrar seguridad como cabeceras TLS, escaneo dependencias en CI/CD).
   Propón escenario retador: fallo certificado y mitigación cultural. Señala 3 controles de seguridad sin contenedores y su lugar en CI/CD.

   - **Colaboración para evitar silos:**
      - Equipos multifuncioanales los cuales comparten objetivos
      - Comunicación constante entre los equipos
      - Responsabilidad ent-to-end del producto

   - **DesSecOps:** Integra seguridad(Sec) como responsabilidad compartida desde el inicio. Escaneando continuamente las vulnerabilidades.

   - **Ejemplo escenario retador: Fallo de certificado**

      - **Incidente:** Certificado TLS caduca
      - **Mitigación cultural:** Los equipos responden juntos, sin culpar al otro.

   - **Tres controles de seguridad sin usar contenedores:**

      1. **Cabeceras TLS/Nginx:** `nginx.conf` con `Strict-Transport-Security`, `X-Frame-Options`

      2. **Escaneo de dependencias:** CI/CD con `pip-audit` o `npm audit`

      3. **Control de procesos/systemd** limitar permisos en `nginx.service` (`User=nginx`, `ProtectSystem=yes`)
         

4. **Metodología 12-Factor App:**
   Elige 4 factores (incluye config por entorno, port binding, logs como flujos).

   **1. Factor III - Config (Configuración por entorno)**  
      - Configuración separada del código, usando variables de entorno
      - Implementar variables `PORT`, `MESSAGE`, `RELEASE` configurables,

   **2. Factor VII - Port Binding (Enlace de puertos)** 
      - Aplicación autocontenida que exporta servicios vía port binding. La app debe exponer un puerto y no depender de servidor externo
      - Implementar flask app escucha en puerto configurable (host="0.0.0.0", port=5000)

   **3. Factor XI - Logs (Logs como flujos de eventos)**
      - Tratar logs como streams de eventos (`stdout/stderr`), no como archivos locales
      - Implementar logs a stdout/stderr para captura por systemd

   **4. Factor VI - Processes (Procesos stateless)**
      - La aplicación se ejecuta como procesos stateless y share-nothing, no debe guardar estado en disco local
      - 

### Parte práctica

#### 1. **Automatización reproducible con Make y Bash (Automation en CALMS).**
   Ejecuta Makefile para preparar, hosts-setup y correr la app. Agrega un target para verificar idempotencia HTTP (reintentos con curl). Explica cómo Lean minimiza fallos.

   - Ejecutamos `make prepare`
      ![](imgs/1.png)

   - Ejecutamos `make hosts-setup`
      ![](imgs/2.png)

   - Ejecutamos `make run`
      ![](imgs/3.png)

   - Ejecutamos `make check-http` para verificar la conexión
      ![](imgs/4.png)

   - Añadimos el target para verificar idempotencia HTTP.
   
      ![](imgs/5.1.png)

      - Ejecutamos `make check-idempotent` para verificar idempotencia HTTP
      
         ![](imgs/5.png)
         Las 3 respuestas son idénticas (mismo status, contenido, comportamiento). 

   Haz una tabla de rastreo de objetivos con esta cabeceras,  "objetivo -> prepara/verifica -> evidencia" de Instrucciones.md.
   
   **Tabla de rastreo de objetivos (Makefile + Instrucciones.md)**

   | Objetivo (Make) | Prepara / Verifica | Evidencia (captura o salida) |
   |-----------------|--------------------|------------------------------|
   | `make prepare`     | Crea venv 'bdd' con prompt personalizado e instala Flask | ![](imgs/1.png) |
   | `make run`      | Levanta la aplicación Flask en el puerto configurado |![](imgs/3.png) |
   | `make hosts-setup` | Configura resolución local para el dominio de la app | ![](imgs/2.png)  ![](imgs/2.1.png) |
   | `make check-http` | Verifica conectividad HTTP, puertos y sockets | ![](imgs/4.png) |
   | `make check-idempotent` | Confirma comportamiento idempotente con 3 requests | ![](imgs/5.png) |
   | `make cleanup`  | Elimina archivos temporales y detiene servicios | ![](imgs/6.png) |

   **¿Cómo Lean minimiza fallos?**

      1. Eliminación de desperdicios:
         - Un solo comando `make run` automáticamente configura todo, lo cual evita pasos manuales repetitivos.
      
      2. Flujo de valor optimizado:
         - Sin Lean tenemos que ejecutar paso a paso `install python → create venv → install deps → configure hosts → start app`.
         - Con Lean podemos simplificar todo eso en una línea `make prepare && make hosts-setup && make run`.
      
      3. Retroalimentación rápida:
         - Si falta una herramienta, Makefile nos lo hace saber inmediatamente. Con el comando `help` nos muestra el estado de nuestro sistema.

   * *Tip:* Intenta romper el Makefile cambiando una variable y observa si sigue siendo reproducible.

      - Probamos 3 veces, con: `PORT=22 make run`, `PORT=999999 make run` y `PORT=80 make run`

         ![](imgs/7.png)

         - Con `PORT=22 make run` error inmediato y claro, permiso denegado. No corrompe el estado, makefile se detiene limpiamente.
         - Con `PORT=999999 make run` pasa algo interesante, a pesar de que el puerto es inválido Flask lo detecta y asigna uno aleatorio. Se ejecuta pero en un puerto diferente al solicitado.
         - Con `PORT=80 make run` igual que `PORT=22` falla de permisos.

#### 2. **Del código a producción con 12-Factor (Build/Release/Run).**
   Modifica variables de entorno (`PORT`, `MESSAGE`, `RELEASE`) sin tocar código. Crea un artefacto inmutable con `git archive` y verifica paridad dev-prod.
   Documenta en tabla "variable -> efecto observable". Simula un fallo de backing service (puerto equivocado) y resuélvelo con disposability. Relaciona con logs y port binding.

   - Modificamos las variables de entorno.
      ![](imgs/8.png)
   
   - Ejecutamos `make run`
      ![](imgs/9.png)

   - Ahora creamos un artefacto inmutable, usamos `git archive` para crear una copia `.zip` del laboratorio. Luego vamos a descomprimirlo y nombrarlo `app-release`.

      ![](imgs/10.png)

      - Verificamos que se descomprimieron todos los archivos:
      ![](imgs/11.png)

   - Tabla "variable -> efecto observable"
      | Variable   | Efecto observable en la app                                     |
      |------------|------------------------------------------------------------------|
      | `PORT=3000`| La app se expone en `http://localhost:3000` (verificable con `ss -lnt`) |
      | `MESSAGE="Hola Diego Osorio!"` | Al abrir `/` devuelve `Hola Diego Osorio! (release: V2.10)`              |
      | `RELEASE=v2.10` | La ruta `/` muestra `(... release: v1.2.3)` -> indica versiOn desplegada |

   - Fallo de backing service. Haremos que la app dependa de una base de datos en localhost:1234 pero se configure mal.

      - Ejecutamos `export DATABASE_URL="postgres://user:pass@localhost:1234/db"`
      ![](imgs/12.png)

      - Esto falla rápidamente, para solucionarse se debe reiniciar y se encontra en un estado limpio y sin corrupción.

         ![](imgs/13.png)

#### 3. **HTTP como contrato observable.**
   Inspecciona cabeceras como ETag o HSTS. Define qué operaciones son seguras para reintentos. Implementa readiness y liveness simples, y mide latencias con curl.
   Documenta contrato mínimo (campos respuesta, trazabilidad en logs). Explica cómo definirías un **SLO**.

   1. **Operaciones seguras para reintentos**

      - Seguras e idempotentes:
         - GET -> no cambia el estado
         - PUT -> escribe los mismo
         - DELETE -> elimina recurso, mismo resultado aunque se repita
      
      - No idempotente:
         - POST -> cada repetición crea un nuevo recurso

   2. **Readiness y liveness simples**
      - Implementamos en `app.py`:
         ![](imgs/14.png)

      - Ahora medimos latencia con `curl`
         ![](imgs/15.png)

   3. **Service Level Objective (SLO)**

      Un SLO es el objetivo medible del servicio, es una meta específica y medible que define qué tan confiable debe ser tu servicio. Ejemplo:
         - Disponibilidad: 99.9% de las peticiones a `/readyz` deben devolver 200 OK.

         - Latencia: El 95% de las respuestas deben tener `time_total < 200ms`.

         - Errores: Menos del 0.1% de las peticiones a `/api/*` deben devolver `5xx` (error).


#### 4. **DNS y caché en operación.**
   Configura IP estática en Netplan. Usa dig para observar TTL decreciente y getent local para resolución de `miapp.local`.
   Explica cómo opera sin zona pública, el camino stub/recursor/autoritativos y overrides locales. Diferencia respuestas cacheadas y autoritativas.

   1. Observar TTL con dig

      - Domain Information Groper (dig)
         - Sirve para consultar servidores DNS y ver como se resuelve un nombre de dominio.
         - Muestra detalles tecnicos: registros (A, AAAA, MX, NS), el TTL, la seccion autoritativa y si la respuesta viene de cache o no.
            ![](imgs/16.png)

      - getent (get entries)
         - Consulta la base de datos NSS (Name Service Switch) de Linux, que integra varias fuentes de resolucion como `/etc/hosts`, DNS y NIS.

   2. **Camino DNS en operación**

      Cuando consultas un dominio, el flujo es:

      1. **Stub resolver:** la libreria que recibe la query.

      2. **Recursive resolver (recursor):** tu DNS configurado (como 8.8.8.8) busca la respuesta.

      3. **Autoritativos:** servidores responsables del dominio (como .com -> google.com -> www.google.com).

      Para miapp.local:

      * No hay zona publica.

      * El sistema resuelve directamente desde /etc/hosts (override local).

   4. **Cacheadas vs Autoritativas**

      * **Respuesta cacheada:** viene del recursor, TTL decrece con cada consulta (Time To Live).

      * **Respuesta autoritativa:** viene directo del servidor DNS del dominio, TTL se reinicia en su valor original.
