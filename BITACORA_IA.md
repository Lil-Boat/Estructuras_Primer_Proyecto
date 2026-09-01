# Bitácora de Uso de Inteligencia Artificial

## Sistema Gestor de Flujos de Trabajo

Este documento registra el uso de herramientas de Inteligencia Artificial durante el desarrollo del proyecto.

La IA fue utilizada como herramienta de apoyo y no como sustituto de la revisión humana.

Todo código sugerido fue revisado, comprendido, ajustado y probado por los integrantes antes de incorporarse al repositorio.

---

## Registro 1 — Diseño general del proyecto

### Área

Arquitectura general del Sistema Gestor de Flujos de Trabajo.

### Prompt utilizado

> Tengo que desarrollar en Python un Sistema Gestor de Flujos de Trabajo para el curso de Estructuras de Datos. Debe utilizar una lista doblemente enlazada para usuarios, pilas para Deshacer/Rehacer, una cola FIFO para tareas regulares, una cola de prioridad para tareas urgentes, un árbol general recursivo para subtareas, tres algoritmos de ordenamiento, persistencia CSV y una interfaz de consola. Ayúdame a diseñar una arquitectura modular que permita dividir el proyecto entre tres integrantes y luego integrarlo mediante Pull Requests.

### Uso de la respuesta

La propuesta se utilizó para identificar módulos independientes y disminuir conflictos durante la integración.

Se definieron carpetas para:

- Modelos.
- Estructuras.
- Algoritmos.
- Persistencia.
- Núcleo.
- CLI.
- Pruebas.

### Validación humana

El equipo revisó que la arquitectura respetara todos los puntos de la rúbrica y que las estructuras principales fueran implementadas manualmente.

También se ajustó la división del trabajo para evitar que varios integrantes modificaran simultáneamente los archivos de integración.

---

## Registro 2 — Lista doblemente enlazada

### Área

Gestión de usuarios.

### Prompt utilizado

> Revisa una implementación manual de una lista doblemente enlazada de usuarios en Python. Debe permitir agregar, buscar por ID, actualizar, eliminar y listar usuarios. No utilices listas de Python como sustituto de la estructura enlazada principal y verifica correctamente los enlaces anterior y siguiente al eliminar cabeza, cola o un nodo intermedio.

### Uso de la respuesta

Se utilizó para revisar casos límite relacionados con la eliminación de nodos.

### Validación humana

Se verificó manualmente:

- Inserción en lista vacía.
- Inserción al final.
- Eliminación de la cabeza.
- Eliminación de la cola.
- Eliminación de un elemento intermedio.
- Prevención de IDs duplicados.

El equipo mantuvo la implementación basada en nodos propios.

---

## Registro 3 — Pila Deshacer/Rehacer

### Área

Historial de modificaciones.

### Prompt utilizado

> Propón una implementación de Deshacer y Rehacer utilizando dos pilas implementadas manualmente en Python. Una acción debe guardar una operación para deshacer y otra para rehacer. Verifica especialmente qué debe ocurrir con la pila de Rehacer cuando se registra una acción nueva después de haber utilizado Deshacer.

### Uso de la respuesta

Se utilizó para validar la lógica de las dos pilas.

### Validación humana

El equipo confirmó que:

- La última acción registrada sea la primera en deshacerse.
- Una acción deshecha pase a la pila de Rehacer.
- Una acción rehecha vuelva a la pila de Deshacer.
- Una operación nueva elimine el historial de Rehacer anterior.
- Deshacer/Rehacer sobre pilas vacías genere errores controlados.

---

## Registro 4 — Cola FIFO

### Área

Procesamiento de tareas regulares.

### Prompt utilizado

> Genera casos de prueba unitarios para una cola FIFO implementada manualmente con nodos enlazados en Python. No utilices collections.deque. Incluye pruebas de encolar, desencolar, orden de salida, cola vacía y varios elementos.

### Uso de la respuesta

Se tomaron los casos de prueba como referencia para QA.

### Validación humana

Se comprobó que la estructura mantuviera correctamente la regla First In, First Out y que el frente y el final se actualizaran al retirar el último elemento.

---

## Registro 5 — Cola de prioridad

### Área

Procesamiento de tareas urgentes.

### Prompt utilizado

> Revisa una cola de prioridad implementada mediante un heap binario máximo propio en Python. Las tareas con valor de prioridad más alto deben salir primero y, cuando dos tareas tengan la misma prioridad, debe conservarse el orden de llegada. No utilices heapq.

### Uso de la respuesta

Se utilizó para revisar el ajuste hacia arriba y hacia abajo del heap.

### Validación humana

El equipo comprobó:

- Inserción de prioridades diferentes.
- Extracción de la prioridad más alta.
- Conservación del orden de llegada en empates.
- Correcta reorganización del heap.
- Manejo controlado de cola vacía.

---

## Registro 6 — Árbol general y recursividad

### Área

Tareas y subtareas.

### Prompt utilizado

> Revisa una estructura de árbol general en Python donde cada tarea puede tener múltiples subtareas. Necesito búsqueda recursiva por ID, recorrido preorden y una representación con sangría. Explica los casos base de la recursividad y verifica que una subtarea pueda contener otras subtareas.

### Uso de la respuesta

Se utilizó para revisar la lógica recursiva.

### Validación humana

El equipo verificó que:

- La tarea actual funcione como caso base.
- La búsqueda continúe recursivamente en todos los hijos.
- El recorrido incluya todos los niveles.
- La persistencia pueda reconstruir subtareas de subtareas.

---

## Registro 7 — Algoritmo Burbuja

### Área

Módulo de reportes.

### Prompt utilizado

> Revisa esta implementación de ordenamiento Burbuja en Python e indica cómo agregar una bandera para detectar que la lista ya está ordenada. No utilices sorted() ni sort(). Incluye el análisis Big-O del mejor, promedio y peor caso.

### Uso de la respuesta

Se incorporó la optimización mediante una bandera de intercambio.

### Validación humana

Se verificaron listas:

- Vacías.
- Con un elemento.
- Ya ordenadas.
- Inversamente ordenadas.
- Con elementos repetidos.

El equipo confirmó el análisis:

- Mejor: O(n).
- Promedio: O(n²).
- Peor: O(n²).

---

## Registro 8 — Merge Sort

### Área

Módulo de reportes.

### Prompt utilizado

> Revisa una implementación manual y recursiva de Merge Sort en Python. No utilices sorted() ni sort(). Verifica el caso base, la división del arreglo y la función que mezcla dos mitades ordenadas. Explica por qué su complejidad temporal es O(n log n).

### Uso de la respuesta

Se utilizó principalmente para revisar la función de combinación.

### Validación humana

El equipo comprobó que el algoritmo:

- Divida hasta listas de tamaño uno.
- Combine correctamente.
- Funcione con duplicados.
- No dependa de métodos automáticos de ordenamiento.

La complejidad O(n log n) fue revisada considerando `log n` niveles de división y trabajo lineal de mezcla por nivel.

---

## Registro 9 — Quicksort

### Área

Módulo de reportes.

### Prompt utilizado

> Genera pruebas unitarias para una implementación manual de Quicksort en Python que utiliza un pivote central. Incluye lista vacía, lista ordenada, lista inversa, valores duplicados y datos repetidos. No reemplaces el algoritmo por sorted().

### Uso de la respuesta

Se utilizaron las sugerencias como referencia para crear pruebas.

### Validación humana

Se verificó que la implementación siguiera siendo recursiva y que el resultado fuera correcto en todos los casos.

Se confirmó:

- Promedio: O(n log n).
- Peor caso: O(n²).

---

## Registro 10 — Validaciones estrictas

### Área

Interfaz CLI y manejo de errores.

### Prompt utilizado

> Revisa estas funciones de captura de datos por consola en Python y propón una forma de evitar que el programa se cierre si el usuario escribe una letra cuando se espera un ID numérico, deja un campo vacío o selecciona una opción inexistente. Utiliza manejo explícito de excepciones y ciclos de reintento.

### Uso de la respuesta

Se utilizaron funciones reutilizables de validación como referencia.

### Validación humana

El equipo probó manualmente:

- Letras en IDs.
- Valores negativos.
- Campos vacíos.
- Opciones inexistentes.
- Prioridades incorrectas.
- Roles incorrectos.

Se confirmó que el programa regresara a solicitar la información en lugar de finalizar inesperadamente.

---

## Registro 11 — Seguridad del login

### Área

Autenticación.

### Prompt utilizado

> En Python necesito solicitar una contraseña desde consola sin mostrar los caracteres escritos. ¿Qué opción de la biblioteca estándar puedo utilizar y cómo integrarla con un inicio de sesión basado en ID y contraseña?

### Uso de la respuesta

Se identificó el módulo estándar `getpass`.

### Validación humana

Se implementó:

```python
from getpass import getpass
```

y se comprobó que la contraseña no apareciera en texto plano durante el ingreso.

---

## Registro 12 — Roles y permisos

### Área

Control de acceso.

### Prompt utilizado

> Revisa un sistema con dos roles: ADMIN y USUARIO. El administrador debe tener acceso total a usuarios y tareas. El usuario normal únicamente debe poder visualizar tareas y cambiar el estado de las tareas que tenga asignadas. Sugiere validaciones de permisos que también protejan el núcleo del programa y no solamente oculten opciones del menú.

### Uso de la respuesta

La recomendación principal fue validar permisos tanto en la interfaz como en el motor.

### Validación humana

El equipo comprobó que un usuario normal no pudiera invocar directamente funciones administrativas aunque intentara evitar el menú.

Se probaron operaciones como:

- Crear tareas.
- Crear usuarios.
- Eliminar registros.
- Cambiar tareas asignadas a otro usuario.

---

## Registro 13 — SLA y prevención de inanición

### Área

Colas y ejecución.

### Prompt utilizado

> Necesito implementar una regla anti-starvation en un sistema con cola FIFO y cola de prioridad. Cada tarea regular debe llevar un contador de ciclos de espera y, después de un límite X, pasar automáticamente a la cola de prioridad. Propón una lógica sencilla y verificable en Python sin reemplazar las estructuras manuales del proyecto.

### Uso de la respuesta

Se tomó como base el contador de ciclos de espera.

El equipo definió:

```text
LIMITE_SLA = 3
```

### Validación humana

Se creó una prueba donde una tarea regular permanece pendiente mientras se procesan tres tareas urgentes.

Después del tercer ciclo se verificó que:

- Su prioridad cambiara a ALTA.
- Su contador regresara a cero.
- Entrara a la cola de prioridad.
- El evento fuera registrado en auditoría.

---

## Registro 14 — Auditoría transaccional

### Área

Persistencia y trazabilidad.

### Prompt utilizado

> Diseña una forma sencilla de crear en Python una bitácora CSV inmutable o append-only. Cada entrada debe guardar fecha y hora, ID del usuario, acción realizada e ID de tarea afectada. El archivo debe agregar nuevas líneas sin modificar las anteriores.

### Uso de la respuesta

Se utilizó la idea de abrir el archivo mediante modo append.

### Validación humana

El código se revisó para asegurar que utilizara:

```python
open(ruta, "a", encoding="utf-8")
```

y no modo escritura `"w"` para las operaciones de auditoría.

También se comprobó que se registraran:

- Cambio de estado.
- SLA.
- Deshacer.
- Rehacer.

---

## Registro 15 — Persistencia CSV

### Área

Carga y guardado.

### Prompt utilizado

> Revisa una estrategia para persistir usuarios, tareas y subtareas en varios archivos CSV. Al iniciar el programa deben reconstruirse los usuarios, las tareas y las relaciones padre-hijo. Considera que puede haber subtareas de subtareas y evita que una fila inválida cierre todo el programa.

### Uso de la respuesta

Se utilizó como referencia una carga en varias pasadas para las subtareas.

### Validación humana

Se realizaron pruebas de:

- Cierre y reapertura.
- Usuarios.
- Tareas.
- Estados.
- Ciclos de espera.
- Subtareas.
- Jerarquías de varios niveles.

El equipo confirmó que el estado pudiera reconstruirse correctamente.

---

## Registro 16 — Pruebas unitarias integrales

### Área

QA.

### Prompt utilizado

> Propón pruebas unitarias para un Sistema Gestor de Flujos de Trabajo que incluya autenticación, roles, IDs duplicados, cola de prioridad, SLA, auditoría, Deshacer/Rehacer y persistencia CSV.

### Uso de la respuesta

Se utilizaron los casos como guía para crear y ampliar `tests/test_sistema.py`.

### Validación humana

Las pruebas fueron ejecutadas localmente y revisadas por los integrantes.

Se comprobó especialmente:

- Login válido.
- Login inválido.
- Permisos.
- Restricción por responsable.
- IDs duplicados.
- Prioridad.
- Escalamiento SLA.
- Auditoría.
- Deshacer/Rehacer.
- Persistencia.

---

# Criterios de revisión humana

Para cualquier código o sugerencia obtenida con IA se siguió este proceso:

1. Leer y comprender la propuesta.
2. Compararla con el enunciado y la rúbrica.
3. Verificar que no reemplazara las estructuras requeridas por librerías automáticas.
4. Ajustar nombres y arquitectura al proyecto.
5. Ejecutar pruebas.
6. Probar manualmente casos límite.
7. Revisar el código entre integrantes mediante Pull Request.
8. Aceptar únicamente cambios que el equipo pudiera explicar durante la defensa.

---

# Declaración de uso responsable

La Inteligencia Artificial fue utilizada como herramienta de apoyo para:

- Generación de casos de prueba.
- Revisión de estructuras.
- Detección de casos límite.
- Refactorización.
- Documentación.
- Explicación de complejidad asintótica.

No se consideró ninguna respuesta de IA como correcta automáticamente.

Los integrantes del equipo conservaron la responsabilidad sobre la implementación final, las decisiones de diseño, las pruebas, la validación y la comprensión del código entregado.

---

## Integrantes responsables de validación

- Integrante 1: ______________________________
- Integrante 2: ______________________________
- Integrante 3: ______________________________

---

## Evidencia en GitHub

La evidencia de trabajo debe complementarse en el repositorio mediante:

- Branches individuales.
- Commits descriptivos.
- Pull Requests.
- Revisiones de código.
- Historias de usuario.
- Pruebas.
- README.md.
- Esta bitácora de IA.

La incorporación de código asistido por IA debe quedar reflejada en commits y Pull Requests revisados por los integrantes.
