from modelos.usuario import (
    Usuario,
    ListaDobleUsuarios
)

from modelos.tarea import (
    Tarea
)

from estructuras.cola import (
    ColaFIFO
)

from estructuras.cola_prioridad import (
    ColaPrioridad
)

from estructuras.pila import (
    Historial,
    Accion
)

from algoritmos.ordenamiento import (
    burbuja,
    merge_sort,
    quicksort
)


class MotorFlujos:
    """
    Es el núcleo principal del sistema.

    Coordina:
    - Usuarios.
    - Roles y permisos.
    - Tareas.
    - Colas.
    - SLA.
    - Árbol de subtareas.
    - Deshacer/Rehacer.
    - Auditoría.
    - Reportes.
    """

    # Una tarea regular se escala automáticamente
    # después de 3 ciclos de espera.
    LIMITE_SLA = 3

    def __init__(
        self,
        auditoria=None
    ):
        """
        Inicializa todas las estructuras necesarias.
        """

        # Lista doblemente enlazada.
        self.usuarios = (
            ListaDobleUsuarios()
        )

        # Lista que guarda las tareas raíz.
        self.tareas_raiz = []

        # Cola FIFO para tareas regulares.
        self.cola_regular = (
            ColaFIFO()
        )

        # Cola de prioridad para tareas urgentes.
        self.cola_prioridad = (
            ColaPrioridad()
        )

        # Sistema Deshacer/Rehacer.
        self.historial = (
            Historial()
        )

        # Sistema de bitácora.
        self.auditoria = auditoria

    # ==================================================
    # AUTENTICACIÓN Y PERMISOS
    # ==================================================

    def autenticar(
        self,
        id_usuario,
        contrasena
    ):
        """
        Comprueba las credenciales de inicio de sesión.

        Si el ID o contraseña son incorrectos,
        se genera una excepción controlada.
        """

        usuario = self.usuarios.buscar(
            id_usuario
        )

        if (
            usuario is None
            or
            usuario.contrasena != contrasena
        ):

            raise ValueError(
                "Credenciales incorrectas."
            )

        return usuario

    def _exigir_admin(
        self,
        actor_id
    ):
        """
        Verifica que la persona que intenta ejecutar
        una acción tenga rol ADMIN.

        actor_id = 0 se utiliza únicamente para
        operaciones internas como cargar archivos.
        """

        if actor_id == 0:
            return

        actor = self.usuarios.buscar(
            actor_id
        )

        if (
            actor is None
            or
            actor.rol != "ADMIN"
        ):

            raise PermissionError(
                "Esta acción requiere rol ADMIN."
            )

    # ==================================================
    # GESTIÓN DE USUARIOS
    # ==================================================

    def agregar_usuario(
        self,
        id_usuario,
        nombre,
        contrasena,
        rol,
        actor_id,
        registrar=True
    ):
        """
        Crea un nuevo usuario.

        Solo un administrador puede hacerlo.
        También se registra la acción para permitir
        Deshacer/Rehacer.
        """

        if registrar:

            self._exigir_admin(
                actor_id
            )

        usuario = Usuario(
            id_usuario,
            nombre,
            contrasena,
            rol
        )

        self.usuarios.agregar(
            usuario
        )

        # Registrar la operación.
        if registrar:

            self.historial.registrar(
                Accion(
                    descripcion=(
                        f"Agregar usuario "
                        f"{id_usuario}"
                    ),
                    id_usuario=actor_id,
                    id_tarea="-",

                    # Para deshacer:
                    deshacer=lambda:
                    self.usuarios.eliminar(
                        id_usuario
                    ),

                    # Para rehacer:
                    rehacer=lambda:
                    self.usuarios.agregar(
                        usuario
                    )
                )
            )

        return usuario

    def actualizar_usuario(
        self,
        id_usuario,
        actor_id,
        nombre=None,
        contrasena=None,
        rol=None
    ):
        """
        Modifica datos de un usuario existente.

        Se guarda una copia de los datos anteriores
        para poder deshacer la modificación.
        """

        self._exigir_admin(
            actor_id
        )

        usuario = self.usuarios.buscar(
            id_usuario
        )

        if usuario is None:

            raise ValueError(
                "Usuario no encontrado."
            )

        # Datos antes de modificar.
        anterior = (
            usuario.nombre,
            usuario.contrasena,
            usuario.rol
        )

        # Realizar actualización.
        self.usuarios.actualizar(
            id_usuario,
            nombre,
            contrasena,
            rol
        )

        # Datos después de modificar.
        nuevo = (
            usuario.nombre,
            usuario.contrasena,
            usuario.rol
        )

        self.historial.registrar(
            Accion(
                descripcion=(
                    f"Actualizar usuario "
                    f"{id_usuario}"
                ),
                id_usuario=actor_id,
                id_tarea="-",

                deshacer=lambda:
                self.usuarios.actualizar(
                    id_usuario,
                    anterior[0],
                    anterior[1],
                    anterior[2]
                ),

                rehacer=lambda:
                self.usuarios.actualizar(
                    id_usuario,
                    nuevo[0],
                    nuevo[1],
                    nuevo[2]
                )
            )
        )

        return usuario

    def eliminar_usuario(
        self,
        id_usuario,
        actor_id
    ):
        """
        Elimina un usuario.

        Por seguridad no se permite eliminar un usuario
        que todavía tenga tareas pendientes asignadas.
        """

        self._exigir_admin(
            actor_id
        )

        # Revisar todas las tareas.
        for tarea in self._todas_tareas():

            if (
                tarea.id_usuario
                ==
                int(id_usuario)
                and
                tarea.estado
                ==
                "PENDIENTE"
            ):

                raise ValueError(
                    "No se puede eliminar: "
                    "el usuario tiene tareas pendientes."
                )

        usuario = self.usuarios.eliminar(
            id_usuario
        )

        self.historial.registrar(
            Accion(
                descripcion=(
                    f"Eliminar usuario "
                    f"{id_usuario}"
                ),
                id_usuario=actor_id,
                id_tarea="-",

                deshacer=lambda:
                self.usuarios.agregar(
                    usuario
                ),

                rehacer=lambda:
                self.usuarios.eliminar(
                    id_usuario
                )
            )
        )

        return usuario

    # ==================================================
    # GESTIÓN DE TAREAS
    # ==================================================

    def crear_tarea(
        self,
        id_tarea,
        prioridad,
        id_usuario,
        descripcion,
        actor_id,
        estado="PENDIENTE",
        ciclos_espera=0,
        registrar=True
    ):
        """
        Crea una nueva tarea principal.

        Valida:
        - ID duplicado.
        - Usuario responsable existente.
        - Permisos administrativos.
        """

        if registrar:

            self._exigir_admin(
                actor_id
            )

        # Evitar IDs repetidos.
        if self.buscar_tarea(
            id_tarea
        ) is not None:

            raise ValueError(
                "Ya existe una tarea con ese ID."
            )

        # Verificar responsable.
        if self.usuarios.buscar(
            id_usuario
        ) is None:

            raise ValueError(
                "El usuario responsable no existe."
            )

        tarea = Tarea(
            id_tarea,
            prioridad,
            id_usuario,
            descripcion,
            estado,
            ciclos_espera
        )

        self.tareas_raiz.append(
            tarea
        )

        # Actualizar colas.
        self._reconstruir_colas()

        if registrar:

            self.historial.registrar(
                Accion(
                    descripcion=(
                        f"Crear tarea "
                        f"{id_tarea}"
                    ),
                    id_usuario=actor_id,
                    id_tarea=id_tarea,

                    deshacer=lambda:
                    self._eliminar_raiz_sin_historial(
                        id_tarea
                    ),

                    rehacer=lambda:
                    self._restaurar_raiz_sin_historial(
                        tarea
                    )
                )
            )

        return tarea

    def actualizar_tarea(
        self,
        id_tarea,
        actor_id,
        descripcion=None,
        prioridad=None,
        responsable=None
    ):
        """
        Permite modificar:
        - Descripción.
        - Prioridad.
        - Responsable.
        """

        self._exigir_admin(
            actor_id
        )

        tarea = self.buscar_tarea(
            id_tarea
        )

        if tarea is None:

            raise ValueError(
                "Tarea no encontrada."
            )

        # Guardar estado anterior.
        anterior = (
            tarea.descripcion,
            tarea.prioridad,
            tarea.id_usuario
        )

        # Cambiar descripción.
        if (
            descripcion is not None
            and
            descripcion.strip()
        ):

            tarea.descripcion = (
                descripcion.strip()
            )

        # Cambiar prioridad.
        if (
            prioridad is not None
            and
            prioridad.strip()
        ):

            prioridad = (
                prioridad.upper()
            )

            if prioridad not in {
                "BAJA",
                "MEDIA",
                "ALTA"
            }:

                raise ValueError(
                    "Prioridad inválida."
                )

            tarea.prioridad = (
                prioridad
            )

        # Cambiar responsable.
        if responsable is not None:

            if self.usuarios.buscar(
                responsable
            ) is None:

                raise ValueError(
                    "El responsable no existe."
                )

            tarea.id_usuario = int(
                responsable
            )

        # Guardar nuevo estado.
        nuevo = (
            tarea.descripcion,
            tarea.prioridad,
            tarea.id_usuario
        )

        # Si cambia prioridad,
        # podría cambiar de cola.
        self._reconstruir_colas()

        self.historial.registrar(
            Accion(
                descripcion=(
                    f"Actualizar tarea "
                    f"{id_tarea}"
                ),
                id_usuario=actor_id,
                id_tarea=id_tarea,

                deshacer=lambda:
                self._aplicar_datos_tarea(
                    tarea,
                    anterior
                ),

                rehacer=lambda:
                self._aplicar_datos_tarea(
                    tarea,
                    nuevo
                )
            )
        )

        return tarea

    def cancelar_tarea(
        self,
        id_tarea,
        actor_id
    ):
        """
        Cancela una tarea sin borrarla físicamente.

        Esto conserva su registro histórico.
        """

        self._exigir_admin(
            actor_id
        )

        tarea = self.buscar_tarea(
            id_tarea
        )

        if tarea is None:

            raise ValueError(
                "Tarea no encontrada."
            )

        estado_anterior = (
            tarea.estado
        )

        tarea.estado = (
            "CANCELADA"
        )

        self._reconstruir_colas()

        self.historial.registrar(
            Accion(
                descripcion=(
                    f"Cancelar tarea "
                    f"{id_tarea}"
                ),
                id_usuario=actor_id,
                id_tarea=id_tarea,

                deshacer=lambda:
                self._cambiar_estado_directo(
                    tarea,
                    estado_anterior
                ),

                rehacer=lambda:
                self._cambiar_estado_directo(
                    tarea,
                    "CANCELADA"
                )
            )
        )

        return tarea

    def eliminar_tarea(
        self,
        id_tarea,
        actor_id
    ):
        """
        Elimina físicamente una tarea raíz.

        Las subtareas se manejan principalmente
        mediante cancelación para evitar romper el árbol.
        """

        self._exigir_admin(
            actor_id
        )

        tarea = self.buscar_tarea(
            id_tarea
        )

        if tarea is None:

            raise ValueError(
                "Tarea no encontrada."
            )

        # Solamente eliminamos físicamente
        # tareas que estén en la raíz.
        if tarea not in self.tareas_raiz:

            raise ValueError(
                "La eliminación física solo aplica "
                "a tareas raíz."
            )

        indice = (
            self.tareas_raiz
            .index(tarea)
        )

        self.tareas_raiz.pop(
            indice
        )

        self._reconstruir_colas()

        self.historial.registrar(
            Accion(
                descripcion=(
                    f"Eliminar tarea "
                    f"{id_tarea}"
                ),
                id_usuario=actor_id,
                id_tarea=id_tarea,

                deshacer=lambda:
                self._insertar_raiz(
                    indice,
                    tarea
                ),

                rehacer=lambda:
                self._eliminar_raiz_sin_historial(
                    id_tarea
                )
            )
        )

        return tarea

    def agregar_subtarea(
        self,
        id_subtarea,
        id_padre,
        descripcion,
        actor_id,
        prioridad="MEDIA",
        id_usuario=None,
        estado="PENDIENTE",
        ciclos_espera=0,
        registrar=True
    ):
        """
        Agrega una nueva subtarea dentro del árbol.

        Puede agregarse debajo de una tarea o debajo
        de otra subtarea.
        """

        if registrar:

            self._exigir_admin(
                actor_id
            )

        # Evitar IDs duplicados.
        if self.buscar_tarea(
            id_subtarea
        ) is not None:

            raise ValueError(
                "ID de tarea/subtarea duplicado."
            )

        padre = self.buscar_tarea(
            id_padre
        )

        if padre is None:

            raise ValueError(
                "Tarea padre no encontrada."
            )

        # Si no se indica responsable,
        # hereda el responsable del padre.
        if id_usuario is None:

            id_usuario = (
                padre.id_usuario
            )

        if self.usuarios.buscar(
            id_usuario
        ) is None:

            raise ValueError(
                "Responsable no encontrado."
            )

        subtarea = Tarea(
            id_subtarea,
            prioridad,
            id_usuario,
            descripcion,
            estado,
            ciclos_espera
        )

        padre.agregar_subtarea(
            subtarea
        )

        if registrar:

            self.historial.registrar(
                Accion(
                    descripcion=(
                        f"Agregar subtarea "
                        f"{id_subtarea}"
                    ),
                    id_usuario=actor_id,
                    id_tarea=id_subtarea,

                    deshacer=lambda:
                    padre.subtareas.remove(
                        subtarea
                    ),

                    rehacer=lambda:
                    padre.subtareas.append(
                        subtarea
                    )
                )
            )

        return subtarea

    # ==================================================
    # CAMBIO DE ESTADO
    # ==================================================

    def cambiar_estado_tarea(
        self,
        id_tarea,
        nuevo_estado,
        actor_id
    ):
        """
        Cambia el estado de una tarea.

        ADMIN:
        Puede cambiar cualquier tarea.

        USUARIO:
        Solo puede cambiar tareas asignadas a él.
        """

        tarea = self.buscar_tarea(
            id_tarea
        )

        if tarea is None:

            raise ValueError(
                "Tarea no encontrada."
            )

        actor = self.usuarios.buscar(
            actor_id
        )

        if actor is None:

            raise PermissionError(
                "Usuario no válido."
            )

        # Usuario normal solo modifica sus tareas.
        if (
            actor.rol != "ADMIN"
            and
            tarea.id_usuario
            !=
            actor.id_usuario
        ):

            raise PermissionError(
                "Solo puede modificar tareas "
                "asignadas a usted."
            )

        nuevo_estado = (
            nuevo_estado.upper()
        )

        if nuevo_estado not in {
            "PENDIENTE",
            "COMPLETADA",
            "CANCELADA"
        }:

            raise ValueError(
                "Estado inválido."
            )

        estado_anterior = (
            tarea.estado
        )

        tarea.estado = (
            nuevo_estado
        )

        self._reconstruir_colas()

        # Registrar auditoría.
        if self.auditoria is not None:

            self.auditoria.registrar(
                actor_id,
                (
                    "CAMBIO_ESTADO:"
                    f"{estado_anterior}"
                    "->"
                    f"{nuevo_estado}"
                ),
                id_tarea
            )

        # Registrar para Deshacer/Rehacer.
        self.historial.registrar(
            Accion(
                descripcion=(
                    f"Cambiar estado tarea "
                    f"{id_tarea}"
                ),
                id_usuario=actor_id,
                id_tarea=id_tarea,

                deshacer=lambda:
                self._cambiar_estado_directo(
                    tarea,
                    estado_anterior
                ),

                rehacer=lambda:
                self._cambiar_estado_directo(
                    tarea,
                    nuevo_estado
                )
            )
        )

        return tarea

    # ==================================================
    # EJECUCIÓN Y SLA
    # ==================================================

    def ejecutar_siguiente(
        self,
        actor_id
    ):
        """
        Ejecuta la siguiente tarea pendiente.

        Orden:
        1. Cola de prioridad.
        2. Cola FIFO regular.

        Si se ejecuta una tarea prioritaria,
        las tareas regulares aumentan su contador SLA.
        """

        self._exigir_admin(
            actor_id
        )

        # Primero revisar urgentes.
        if not self.cola_prioridad.esta_vacia():

            tarea = (
                self.cola_prioridad
                .desencolar()
            )

            # Como otra tarea fue atendida,
            # las regulares acumulan espera.
            self._incrementar_espera_y_escalar(
                actor_id
            )

        elif not self.cola_regular.esta_vacia():

            tarea = (
                self.cola_regular
                .desencolar()
            )

        else:

            raise IndexError(
                "No hay tareas pendientes."
            )

        estado_anterior = (
            tarea.estado
        )

        tarea.estado = (
            "COMPLETADA"
        )

        # Registrar ejecución.
        if self.auditoria is not None:

            self.auditoria.registrar(
                actor_id,
                "EJECUTAR_TAREA",
                tarea.id_tarea
            )

        self._reconstruir_colas()

        # Permitir deshacer la ejecución.
        self.historial.registrar(
            Accion(
                descripcion=(
                    f"Ejecutar tarea "
                    f"{tarea.id_tarea}"
                ),
                id_usuario=actor_id,
                id_tarea=tarea.id_tarea,

                deshacer=lambda:
                self._cambiar_estado_directo(
                    tarea,
                    estado_anterior
                ),

                rehacer=lambda:
                self._cambiar_estado_directo(
                    tarea,
                    "COMPLETADA"
                )
            )
        )

        return tarea

    def _incrementar_espera_y_escalar(
        self,
        actor_id
    ):
        """
        Implementa la regla anti-starvation.

        Cada tarea regular aumenta su contador.

        Si llega a LIMITE_SLA:
        - Su prioridad pasa a ALTA.
        - Se elimina de FIFO.
        - Se inserta en la cola de prioridad.
        - Se registra en auditoría.
        """

        tareas_regulares = (
            self.cola_regular.listar()
        )

        restantes = []

        escaladas = []

        for tarea in tareas_regulares:

            tarea.ciclos_espera += 1

            # Verificar límite.
            if (
                tarea.ciclos_espera
                >=
                self.LIMITE_SLA
            ):

                # Escalamiento automático.
                tarea.prioridad = (
                    "ALTA"
                )

                # Reiniciar contador.
                tarea.ciclos_espera = 0

                escaladas.append(
                    tarea
                )

                # Registrar auditoría.
                if self.auditoria is not None:

                    self.auditoria.registrar(
                        actor_id,
                        "ESCALAMIENTO_SLA",
                        tarea.id_tarea
                    )

            else:

                restantes.append(
                    tarea
                )

        # Reconstruir cola normal solamente
        # con las tareas que no escalaron.
        self.cola_regular.reemplazar(
            restantes
        )

        # Mover tareas escaladas a prioridad.
        for tarea in escaladas:

            self.cola_prioridad.encolar(
                tarea,
                tarea.valor_prioridad
            )

    # ==================================================
    # DESHACER Y REHACER
    # ==================================================

    def deshacer(
        self,
        actor_id
    ):
        """
        Deshace la última modificación realizada.

        Solo ADMIN puede utilizar esta función.
        """

        self._exigir_admin(
            actor_id
        )

        accion = (
            self.historial
            .deshacer()
        )

        # Registrar auditoría.
        if self.auditoria is not None:

            self.auditoria.registrar(
                actor_id,
                (
                    "DESHACER:"
                    f"{accion.descripcion}"
                ),
                accion.id_tarea
            )

        self._reconstruir_colas()

        return accion.descripcion

    def rehacer(
        self,
        actor_id
    ):
        """
        Vuelve a ejecutar la última acción deshecha.

        Solo ADMIN puede usarla.
        """

        self._exigir_admin(
            actor_id
        )

        accion = (
            self.historial
            .rehacer()
        )

        if self.auditoria is not None:

            self.auditoria.registrar(
                actor_id,
                (
                    "REHACER:"
                    f"{accion.descripcion}"
                ),
                accion.id_tarea
            )

        self._reconstruir_colas()

        return accion.descripcion

    # ==================================================
    # BÚSQUEDAS Y REPORTES
    # ==================================================

    def buscar_tarea(
        self,
        id_tarea
    ):
        """
        Busca una tarea por ID.

        Como existen subtareas,
        utiliza la búsqueda recursiva del árbol.
        """

        for tarea_raiz in self.tareas_raiz:

            encontrada = (
                tarea_raiz
                .buscar_recursivo(
                    id_tarea
                )
            )

            if encontrada is not None:

                return encontrada

        return None

    def listar_pendientes(self):
        """
        Devuelve todas las tareas pendientes.
        """

        return [
            tarea
            for tarea in self._todas_tareas()
            if tarea.estado
            ==
            "PENDIENTE"
        ]

    def listar_tareas_usuario(
        self,
        id_usuario
    ):
        """
        Devuelve todas las tareas asignadas
        a un usuario específico.
        """

        return [
            tarea
            for tarea in self._todas_tareas()
            if tarea.id_usuario
            ==
            int(id_usuario)
        ]

    def reporte_tareas(
        self,
        criterio="id",
        algoritmo="merge"
    ):
        """
        Genera un reporte ordenado.

        Criterios:
        - id
        - prioridad
        - descripcion
        - estado
        - responsable

        Algoritmos:
        - burbuja
        - merge
        - quick
        """

        tareas = (
            self._todas_tareas()
        )

        # Funciones utilizadas para definir
        # el criterio de comparación.
        claves = {

            "id":
            lambda tarea:
            tarea.id_tarea,

            "prioridad":
            lambda tarea:
            tarea.valor_prioridad,

            "descripcion":
            lambda tarea:
            tarea.descripcion.lower(),

            "estado":
            lambda tarea:
            tarea.estado,

            "responsable":
            lambda tarea:
            tarea.id_usuario
        }

        # Relación entre texto y algoritmo.
        algoritmos = {

            "burbuja":
            burbuja,

            "merge":
            merge_sort,

            "quick":
            quicksort
        }

        if criterio not in claves:

            raise ValueError(
                "Criterio inválido."
            )

        if algoritmo not in algoritmos:

            raise ValueError(
                "Algoritmo inválido."
            )

        funcion_ordenamiento = (
            algoritmos[algoritmo]
        )

        return funcion_ordenamiento(
            tareas,
            claves[criterio]
        )

    # ==================================================
    # FUNCIONES INTERNAS
    # ==================================================

    def _todas_tareas(self):
        """
        Convierte todos los árboles de tareas
        en una sola lista.

        Incluye:
        - Tareas raíz.
        - Subtareas.
        - Subtareas de subtareas.
        """

        resultado = []

        for tarea in self.tareas_raiz:

            resultado.extend(
                tarea.recorrido_preorden()
            )

        return resultado

    def _aplicar_datos_tarea(
        self,
        tarea,
        datos
    ):
        """
        Función auxiliar utilizada por
        Deshacer/Rehacer de actualizaciones.
        """

        tarea.descripcion = (
            datos[0]
        )

        tarea.prioridad = (
            datos[1]
        )

        tarea.id_usuario = (
            datos[2]
        )

        self._reconstruir_colas()

    def _cambiar_estado_directo(
        self,
        tarea,
        estado
    ):
        """
        Cambia internamente el estado de una tarea.

        No registra una acción nueva porque esta función
        se utiliza desde Deshacer/Rehacer.
        """

        tarea.estado = estado

        self._reconstruir_colas()

    def _eliminar_raiz_sin_historial(
        self,
        id_tarea
    ):
        """
        Elimina una tarea raíz sin generar
        una nueva entrada del historial.
        """

        self.tareas_raiz = [
            tarea
            for tarea in self.tareas_raiz
            if tarea.id_tarea
            !=
            int(id_tarea)
        ]

        self._reconstruir_colas()

    def _restaurar_raiz_sin_historial(
        self,
        tarea
    ):
        """
        Restaura una tarea que fue eliminada
        mediante Deshacer.
        """

        if self.buscar_tarea(
            tarea.id_tarea
        ) is None:

            self.tareas_raiz.append(
                tarea
            )

        self._reconstruir_colas()

    def _insertar_raiz(
        self,
        indice,
        tarea
    ):
        """
        Inserta nuevamente una tarea en la posición
        donde se encontraba originalmente.
        """

        self.tareas_raiz.insert(
            indice,
            tarea
        )

        self._reconstruir_colas()

    def _reconstruir_colas(self):
        """
        Reconstruye las colas a partir del estado
        actual de las tareas principales.

        Reglas:
        - ALTA -> Cola de prioridad.
        - MEDIA/BAJA -> Cola FIFO.
        - Solo tareas PENDIENTES.
        """

        # Crear colas nuevas y vacías.
        self.cola_regular = (
            ColaFIFO()
        )

        self.cola_prioridad = (
            ColaPrioridad()
        )

        for tarea in self.tareas_raiz:

            # Solo tareas pendientes.
            if tarea.estado != "PENDIENTE":
                continue

            # Prioridad alta.
            if tarea.prioridad == "ALTA":

                self.cola_prioridad.encolar(
                    tarea,
                    tarea.valor_prioridad
                )

            # Media o baja.
            else:

                self.cola_regular.encolar(
                    tarea
                )