## Estrategias de resolución utilizadas:

- **`-X ours`**: Utilizada para resolver conflictos automáticamente favoreciendo los cambios de la rama actual (main). Útil cuando sabemos que nuestra versión base es la correcta.

- **`-X find-renames=90%`**: Como dice el ejercicio configuré Git para detectar archivos renombrados con 90% de similitud. Esto ayuda a mantener el historial cuando se renombran archivos.

- **`-X renormalize`**: Utilizada para normalizar terminadores de línea diferentes durante el merge, evitando conflictos falsos por diferencias de EOL entre sistemas operativos.

**¿Por qué estas opciones?**
Porque en un entorno DevOps/DevSecOps es común tener:
- Equipos mixtos (Windows/Linux/Mac) que generan diferencias de EOL
- Refactorizaciones que incluyen renombrado de archivos
Y estas estrategias nos ayuda a superar estas "barreras".
