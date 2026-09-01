class Tarea:
    """
    Representa una tarea dentro del sistema.

    Cada tarea funciona como un nodo de un árbol general:

    - Puede tener múltiples subtareas.
    - Cada subtarea puede tener, a su vez,
      otras subtareas.

    Atributos:
    - ID único.
    - Prioridad: ALTA, MEDIA o BAJA.
    - Responsable (id_usuario).
    - Descripción.
    - Estado: PENDIENTE, COMPLETADA o CANCELADA.
    - Ciclos de espera utilizados por el SLA.
    - Lista de subtareas.
    """

    # Valor numérico que se utiliza para comparar
    # prioridades dentro de la cola de prioridad.
    VALORES_PRIORIDAD = {
        "BAJA": 1,
        "MEDIA": 2,
        "ALTA": 3,
    }

    def __init__(
        self,
        id_tarea,
        prioridad,
        id_usuario,
        descripcion,
        estado="PENDIENTE",
        ciclos_espera=0
    ):

        self.id_tarea = int(id_tarea)

        self.prioridad = (
            prioridad.upper()
        )

        self.id_usuario = int(id_usuario)

        self.descripcion = (
            descripcion.strip()
        )

        self.estado = (
            estado.upper()
        )

        self.ciclos_espera = int(
            ciclos_espera
        )

        # Hojas del árbol general.
        self.subtareas = []

    @property
    def valor_prioridad(self):
        """
        Devuelve el valor numérico de la prioridad.

        Se utiliza en:
        - Cola de prioridad.
        - Reportes ordenados por prioridad.
        """

        return (
            self.VALORES_PRIORIDAD
            .get(
                self.prioridad,
                self.VALORES_PRIORIDAD["MEDIA"]
            )
        )

    def agregar_subtarea(
        self,
        subtarea
    ):
        """
        Agrega una nueva subtarea al final
        de la lista de hijos.
        """

        self.subtareas.append(
            subtarea
        )

    def buscar_recursivo(
        self,
        id_tarea
    ):
        """
        Busca una tarea o subtarea por su ID.

        Caso base:
        Si el ID coincide con esta tarea,
        se devuelve esta tarea.

        Caso recursivo:
        Se busca primero en esta tarea y luego
        en cada una de sus subtareas.
        """

        if (
            self.id_tarea
            ==
            int(id_tarea)
        ):

            return self

        for subtarea in self.subtareas:

            encontrada = (
                subtarea.buscar_recursivo(
                    id_tarea
                )
            )

            if encontrada is not None:

                return encontrada

        return None

    def recorrido_preorden(self):
        """
        Recorre el árbol comenzando por esta tarea
        y luego todas sus subtareas.

        El resultado incluye todos los niveles:
        - Tarea.
        - Subtareas.
        - Subtareas de subtareas.
        """

        resultado = [
            self
        ]

        for subtarea in self.subtareas:

            resultado.extend(
                subtarea.recorrido_preorden()
            )

        return resultado

    def mostrar_jerarquia(
        self,
        sangria=0
    ):
        """
        Devuelve una representación con sangría
        de la tarea y sus subtareas.

        Es útil para visualizar el árbol
        cuando se muestran reportes.
        """

        texto = (
            " " * sangria
            +
            f"- [{self.id_tarea}] "
            f"{self.descripcion} "
            f"({self.prioridad}) "
            f"[{self.estado}]\n"
        )

        for subtarea in self.subtareas:

            texto += (
                subtarea.mostrar_jerarquia(
                    sangria + 2
                )
            )

        return texto

    def __repr__(self):
        """
        Representación sencilla para depuración y pruebas.
        """

        return (
            f"Tarea("
            f"{self.id_tarea}, "
            f"{self.prioridad!r}, "
            f"{self.id_usuario}, "
            f"{self.descripcion!r}, "
            f"{self.estado})"
        )