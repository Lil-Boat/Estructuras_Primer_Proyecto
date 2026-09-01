# Sistema Gestor de Flujos de Trabajo

Proyecto de Investigación Aplicada del curso **Estructuras de Datos**, desarrollado en **Python** mediante una interfaz de consola (CLI).

El sistema simula la administración, priorización y ejecución de tareas dentro de una organización, aplicando estructuras de datos implementadas desde cero, persistencia en archivos CSV, control de acceso por roles, auditoría, prevención de inanición mediante SLA y funciones de Deshacer/Rehacer.

---

## Objetivo del proyecto

Desarrollar el núcleo computacional de un sistema gestor de flujos de trabajo capaz de:

- Registrar y administrar usuarios.
- Gestionar tareas y subtareas.
- Asignar responsables.
- Priorizar tareas urgentes.
- Procesar tareas regulares mediante una cola FIFO.
- Evitar que las tareas regulares queden esperando indefinidamente.
- Registrar las acciones importantes del sistema.
- Permitir Deshacer y Rehacer modificaciones.
- Recuperar el estado del sistema mediante archivos CSV.
- Generar reportes utilizando diferentes algoritmos de ordenamiento.

---

## Tecnologías utilizadas

- Python 3
- CSV
- `getpass` para ocultar contraseñas
- Git
- GitHub
- GitHub Projects
- Pull Requests
- Pruebas unitarias con `unittest`

No se utilizan implementaciones automáticas de las estructuras principales cuando el objetivo académico es desarrollarlas manualmente.

---

## Estructuras de datos implementadas

### Lista doblemente enlazada

Se utiliza para almacenar los usuarios registrados.

Cada nodo contiene:

- Usuario.
- Referencia al nodo anterior.
- Referencia al nodo siguiente.

Operaciones:

- Agregar.
- Buscar por ID.
- Actualizar.
- Eliminar.
- Listar.

---

### Pila

Se utiliza para implementar el historial de acciones del sistema.

Se mantienen dos pilas:

- Pila de Deshacer.
- Pila de Rehacer.

Cuando se registra una acción nueva después de utilizar Deshacer, la pila de Rehacer se limpia.

---

### Cola FIFO

Se utiliza para almacenar tareas regulares.

La regla aplicada es:

**First In, First Out**

La primera tarea regular que entra será la primera en ser procesada.

---

### Cola de prioridad

Se utiliza para las tareas urgentes.

Fue implementada mediante un **heap binario máximo propio**.

Las tareas de prioridad ALTA son atendidas antes que las tareas regulares.

Cuando existen tareas con la misma prioridad, se conserva el orden de llegada.

---

### Árbol general

Las tareas pueden contener múltiples subtareas.

Cada tarea funciona como un nodo del árbol y puede almacenar una cantidad variable de hijos.

Se utiliza recursividad para:

- Buscar tareas.
- Recorrer el árbol.
- Mostrar la jerarquía.
- Guardar subtareas.
- Reconstruir dependencias.

---

## Roles del sistema

El sistema posee dos tipos de usuario.

### Administrador

Tiene acceso completo.

Puede:

- Agregar usuarios.
- Actualizar usuarios.
- Eliminar usuarios.
- Listar usuarios.
- Buscar usuarios.
- Crear tareas.
- Actualizar tareas.
- Cancelar tareas.
- Eliminar tareas raíz.
- Asignar responsables.
- Crear subtareas.
- Ejecutar tareas.
- Utilizar Deshacer.
- Utilizar Rehacer.
- Generar reportes.

### Usuario normal

Tiene permisos restringidos.

Puede:

- Visualizar la lista general de tareas.
- Visualizar sus tareas asignadas.
- Cambiar el estado de una tarea únicamente si está asignada a él.

No puede administrar usuarios ni modificar tareas de otros responsables.

---

## Inicio de sesión seguro

El sistema solicita:

- ID de usuario.
- Contraseña.

La contraseña se captura mediante un lector especial (`cli.validaciones.leer_contrasena`) que:

- Oculta los caracteres con `getpass` cuando se ejecuta en una consola interactiva real.
- Si la entrada no es una terminal interactiva (IDE, tubería, CI), usa `input()` normal para evitar que el programa se bloquee en Windows.

Para forzar siempre el modo con eco en pantalla, se puede definir la variable de entorno:

```text
FLUJOS_MOSTRAR_CLAVE=1
```

---

## Usuario administrador inicial

Cuando el sistema se ejecuta por primera vez y no existen usuarios registrados, se crea:

```text
ID: 1
Nombre: Administrador
Rol: ADMIN
Contraseña: admin123
```

Se recomienda cambiar esta contraseña después de iniciar el sistema.

---

## Gestión de usuarios

El administrador dispone de un submenú con las siguientes opciones:

1. Agregar usuario.
2. Actualizar usuario.
3. Eliminar usuario.
4. Listar usuarios.
5. Buscar usuario por ID.

Los IDs duplicados no son permitidos.

Además, no se permite eliminar un usuario que todavía tenga tareas pendientes asignadas.

---

## Gestión de tareas

El administrador puede:

1. Crear una tarea.
2. Actualizar una tarea.
3. Cancelar una tarea.
4. Eliminar una tarea raíz.
5. Listar tareas pendientes.
6. Buscar una tarea por ID.
7. Agregar subtareas.

Cada tarea posee:

- ID.
- Descripción.
- Prioridad.
- Responsable.
- Estado.
- Ciclos de espera.
- Subtareas.

Los IDs de tareas y subtareas deben ser únicos.

---

## Prioridades

El sistema utiliza:

```text
BAJA  = 1
MEDIA = 2
ALTA  = 3
```

Las tareas ALTA se almacenan en la cola de prioridad.

Las tareas MEDIA y BAJA se almacenan inicialmente en la cola FIFO regular.

---

## SLA y prevención de inanición

Para evitar que una tarea regular quede esperando indefinidamente mientras se atienden tareas urgentes, se implementó un contador denominado:

```text
ciclos_espera
```

El límite definido por el equipo es:

```text
LIMITE_SLA = 3
```

Cada vez que se procesa una tarea prioritaria, las tareas que continúan esperando en la cola regular aumentan su contador.

Ejemplo:

```text
Tarea regular:
ciclos_espera = 0

Se ejecuta urgente #1
ciclos_espera = 1

Se ejecuta urgente #2
ciclos_espera = 2

Se ejecuta urgente #3
ciclos_espera = 3
```

Al llegar al límite, la tarea:

1. Sale de la cola regular.
2. Cambia a prioridad ALTA.
3. Reinicia su contador.
4. Ingresa a la cola de prioridad.
5. Registra el escalamiento en auditoría.

Esto evita el problema conocido como **starvation o inanición**.

---

## Deshacer y Rehacer

El sistema almacena modificaciones utilizando dos pilas.

Una acción puede contener:

- Descripción.
- Usuario que la realizó.
- Tarea relacionada.
- Función para Deshacer.
- Función para Rehacer.

Ejemplos de acciones reversibles:

- Crear usuario.
- Actualizar usuario.
- Eliminar usuario.
- Crear tarea.
- Actualizar tarea.
- Cancelar tarea.
- Eliminar tarea.
- Cambiar estado.

El uso de Deshacer y Rehacer queda registrado en la auditoría.

---

## Persistencia CSV

El sistema conserva sus datos después de cerrarse.

Archivos utilizados:

```text
data/
├── usuarios.csv
├── tareas.csv
├── subtareas.csv
└── auditoria_log.csv
```

### usuarios.csv

Almacena:

- ID.
- Nombre.
- Contraseña.
- Rol.

### tareas.csv

Almacena:

- ID.
- Prioridad.
- Responsable.
- Descripción.
- Estado.
- Ciclos de espera.

### subtareas.csv

Almacena:

- ID de subtarea.
- ID del padre.
- Prioridad.
- Responsable.
- Descripción.
- Estado.
- Ciclos de espera.

Cada vez que se agrega, actualiza o elimina información relevante, el sistema actualiza los archivos CSV.

Al iniciar el programa se leen nuevamente para reconstruir el estado anterior.

---

## Auditoría transaccional

El archivo:

```text
data/auditoria_log.csv
```

funciona como una bitácora **append-only**.

Esto significa que las entradas anteriores no se modifican ni eliminan.

Formato:

```text
Fecha y Hora | ID Usuario | Acción | ID Tarea
```

Ejemplo:

```text
2026-08-31 20:10:05|2|CAMBIO_ESTADO:PENDIENTE->COMPLETADA|15
2026-08-31 20:12:31|1|ESCALAMIENTO_SLA|8
2026-08-31 20:14:20|1|DESHACER:Crear tarea 20|20
2026-08-31 20:15:03|1|REHACER:Crear tarea 20|20
```

Se registran, como mínimo:

- Cambios de estado.
- Escalamiento por SLA.
- Ejecución de tareas.
- Deshacer.
- Rehacer.

---

## Validaciones y manejo de errores

El programa está diseñado para no cerrarse inesperadamente ante entradas incorrectas.

Se validan:

- IDs no numéricos.
- IDs duplicados.
- Opciones de menú inválidas.
- Prioridades inválidas.
- Estados inválidos.
- Roles inválidos.
- Usuarios inexistentes.
- Responsables inexistentes.
- Tareas inexistentes.
- Operaciones no autorizadas.
- Pilas o colas vacías.

Las entradas incorrectas generan mensajes amigables y permiten volver a intentar.

---

## Algoritmos de ordenamiento

Se implementaron tres algoritmos.

### Burbuja optimizada

Complejidad:

- Mejor caso: O(n)
- Promedio: O(n²)
- Peor caso: O(n²)
- Espacio adicional: O(1)

### Merge Sort

Complejidad:

- Mejor caso: O(n log n)
- Promedio: O(n log n)
- Peor caso: O(n log n)
- Espacio adicional: O(n)

### Quicksort

Complejidad:

- Promedio: O(n log n)
- Peor caso: O(n²)
- Espacio promedio por recursión: O(log n)

Los reportes pueden ordenarse por:

- ID.
- Prioridad.
- Descripción.
- Estado.
- Responsable.

---

## Estructura del proyecto

```text
sistema_gestor_flujos/
│
├── main.py
├── README.md
├── BITACORA_IA.md
│
├── modelos/
│   ├── __init__.py
│   ├── usuario.py
│   └── tarea.py
│
├── estructuras/
│   ├── __init__.py
│   ├── pila.py
│   ├── cola.py
│   └── cola_prioridad.py
│
├── algoritmos/
│   ├── __init__.py
│   └── ordenamiento.py
│
├── persistencia/
│   ├── __init__.py
│   ├── csv_manager.py
│   └── auditoria.py
│
├── nucleo/
│   ├── __init__.py
│   └── motor.py
│
├── cli/
│   ├── __init__.py
│   ├── menu.py
│   └── validaciones.py
│
├── data/
│   ├── usuarios.csv
│   ├── tareas.csv
│   ├── subtareas.csv
│   └── auditoria_log.csv
│
├── test/
│   └── test_sistema.py
│
└── docs/
    ├── division_trabajo.md
    └── historias_usuario.md
```

---

## Ejecución

Desde la raíz del proyecto:

```bash
python main.py
```

---

## Ejecución de pruebas

```bash
python -m unittest discover -s test -v
```

Las pruebas verifican, entre otros aspectos:

- Autenticación.
- Credenciales incorrectas.
- Permisos.
- IDs duplicados.
- Restricciones de usuarios normales.
- Cola de prioridad.
- SLA.
- Auditoría.
- Deshacer/Rehacer.
- Persistencia.

---

## Trabajo colaborativo en GitHub

El desarrollo debe realizarse mediante ramas independientes.

Ramas propuestas:

```text
feature/usuarios-seguridad
feature/tareas-colas-sla
feature/historial-persistencia-reportes
```

Se recomienda utilizar adicionalmente:

```text
develop
```

Flujo:

```text
feature/*
    ↓
Pull Request
    ↓
develop
    ↓
Pruebas e integración
    ↓
Pull Request final
    ↓
main
```

No se debe desarrollar todo directamente sobre `main`.

Los commits deben ser pequeños y descriptivos.

Ejemplos:

```text
feat: implementar lista doble de usuarios
feat: agregar autenticacion por roles
feat: implementar cola fifo
feat: agregar escalamiento por sla
feat: agregar auditoria transaccional
test: agregar pruebas de permisos
docs: documentar uso de ia
```

---

## Historias de usuario

Los nuevos requerimientos deben documentarse en GitHub Projects.

Historias sugeridas:

- HU-01 Inicio de sesión seguro.
- HU-02 Control de acceso por roles.
- HU-03 CRUD de usuarios.
- HU-04 CRUD de tareas.
- HU-05 Cambio de estado restringido.
- HU-06 Persistencia automática.
- HU-07 Validaciones estrictas.
- HU-08 SLA anti-starvation.
- HU-09 Auditoría transaccional.
- HU-10 Bitácora de Inteligencia Artificial.

---

# Bitácora de Inteligencia Artificial

Durante el desarrollo se utilizaron herramientas de Inteligencia Artificial únicamente como apoyo para generación de pruebas, revisión, explicación y refactorización.

La decisión final sobre el código fue realizada por los integrantes del equipo.

La bitácora detallada se encuentra en:

```text
BITACORA_IA.md
```

Incluye:

- Función o estructura en la que se utilizó IA.
- Prompt utilizado.
- Resultado esperado.
- Revisión humana.
- Modificaciones realizadas por el equipo.

---

## Integrantes

- Integrante 1: ______________________________
- Integrante 2: ______________________________
- Integrante 3: ______________________________

---

## Curso

**Estructuras de Datos**

Proyecto de Investigación Aplicada.
