# Actividad 6

## Resumen de comandos y archivos de logs

- **init:**
  - Comando: `git init` y `git status`
  - Archivo: `git init > logs/init-status.txt; git status >> logs/init-status.txt`
  - Inicializa el repositorio y muestra el estado inicial.
  
- **git config:**
  - Comando: `git config --list`
  - Archivo: `git config --list > logs/config.txt`
  - Muestra la configuración actual de Git.


- **add/commit:**
  - Comando: `git add .` y `git commit -m "mensaje"`
  - Archivo: `git add . > logs/add-commit.txt; git commit -m "mensaje" >> logs/add-commit.txt`
  - Añade archivos y guarda el commit.

- **log:**
  - Comando: `git log --oneline`
  - Archivo: `git log --oneline > logs/log-oneline.txt`
  - Lista los commits en formato breve.

- **ramas (crear/cambiar/merge y resolución):**
  - Crear: `git branch rama-1`
  - Cambiar: `git checkout rama-1`
  - Ver: `git branch`
  - Merge: `git merge rama-1`
  - Archivo: `git merge rama-1 > logs/merge-o-conflicto.txt`
  - Muestra ramas y el resultado del merge sin conflicto.

- **revert/rebase/cherry-pick/stash (si aplica):**
  - **Revert:** `git revert <commit>`, crea un nuevo commit que deshace los cambios de un commit anterior sin modificar el historial, se usa para “revertir” cambios especificos de forma segura.
  - **Rebase:** `git rebase rama`, mueve o combina una secuencia de commits a una nueva base reescribiendo el historial, es util para mantener un historial lineal y limpio, especialmente antes de fusionar ramas.
  - **Cherry-pick:** `git cherry-pick <commit>`, aplica los cambios de un commit especifico de otra rama en la rama actual, permite traer solo los cambios deseados sin fusionar toda la rama.
  - **Stash:** `git stash`, guarda temporalmente los cambios no confirmados en un “stash” para limpiar el area de trabajo.
  

**Pregunta:** ¿Cual es la salida de este comando?

```git
$ git log --graph --pretty=format:'%x09 %h %ar ("%an") %s'
```
Muestra el historial de commits con un formato personalizado y visual.
- `git log`: Comando para mostrar el historial de commits
- `graph`: Muestra una representación gráfica en ASCII de las ramas y merges
- `pretty=format:`: Personaliza el formato de salida
- `%x09`: Inserta un carácter de tabulación
- `%h`: Hash corto del commit 
- `%ar`: Fecha relativa del commit
- `%an`: Nombre del autor del commit
- `%s`: Mensaje del commit

## Trabajar con ramas: La piedra angular de la colaboración

**Preguntas:**

* **¿Cómo te ha ayudado Git a mantener un historial claro y organizado de tus cambios?**

    Git permite registrar cada cambio realizado en el proyecto lo facilita la identificacion de quien, cuando y por que se hicieron modificaciones, esto ayuda a mantener un historial transparente y ordenado, util para auditoria y recuperacion de versiones anteriores.

* **¿Qué beneficios ves en el uso de ramas para desarrollar nuevas características o corregir errores?**

    Las ramas permiten trabajar en nuevas funcionalidades o correcciones de errores de forma aislada sin afectar la version principal, esto fomenta la colaboracion y reduce el riesgo de conflictos entre desarrollos que trabajan de manera simultanea.

* **Realiza una revisión final del historial de commits para asegurarte de que todos los cambios se han registrado correctamente.**

    Utilice `git log` para verificar que cada cambio importante esta documentado y que el historial refleja el desarrollo del proyecto.

* **Revisa el uso de ramas y merges para ver cómo Git maneja múltiples líneas de desarrollo.**

    Analice el grafico de commits y los merges para entender como se integran diferentes lineas de trabajo asegurando que las contribuciones de todos los colaboradores se combinan correctamente.

