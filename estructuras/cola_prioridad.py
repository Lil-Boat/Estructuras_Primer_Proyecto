class ColaPrioridad:
    """
    Cola de prioridad implementada manualmente
    mediante un heap binario máximo.

    No se utiliza heapq porque el objetivo del curso
    es implementar la estructura desde cero.
    """

    def __init__(self):

        # Lista utilizada internamente para representar
        # el heap binario.
        self._heap = []

        # Permite mantener orden FIFO cuando dos tareas
        # tienen exactamente la misma prioridad.
        self._secuencia = 0

    def _valor(self, elemento):
        """
        Retorna el valor utilizado para comparar
        dos elementos del heap.

        Se considera:
        1. Prioridad.
        2. Orden de llegada.
        """

        prioridad, secuencia, dato = elemento

        return (
            prioridad,
            -secuencia
        )

    def encolar(
        self,
        dato,
        prioridad
    ):
        """
        Inserta un elemento en la cola de prioridad.

        Luego realiza un ajuste hacia arriba para
        mantener la propiedad del heap máximo.
        """

        elemento = (
            int(prioridad),
            self._secuencia,
            dato
        )

        self._secuencia += 1

        # Insertamos inicialmente al final.
        self._heap.append(
            elemento
        )

        indice = (
            len(self._heap) - 1
        )

        # Ajuste hacia arriba.
        while indice > 0:

            padre = (
                indice - 1
            ) // 2

            # Si el padre ya tiene mayor prioridad,
            # la estructura es válida.
            if (
                self._valor(
                    self._heap[padre]
                )
                >=
                self._valor(
                    self._heap[indice]
                )
            ):

                break

            # Intercambiamos padre e hijo.
            self._heap[padre], self._heap[indice] = (
                self._heap[indice],
                self._heap[padre]
            )

            indice = padre

    def desencolar(self):
        """
        Retira y devuelve la tarea con mayor prioridad.

        Después de eliminar la raíz se reorganiza
        el heap para mantener su propiedad.
        """

        if not self._heap:

            raise IndexError(
                "La cola de prioridad está vacía."
            )

        # La raíz siempre es la mayor prioridad.
        raiz = self._heap[0]

        ultimo = self._heap.pop()

        # Si todavía existen elementos...
        if self._heap:

            # Colocamos temporalmente el último elemento
            # en la raíz.
            self._heap[0] = ultimo

            indice = 0

            # Ajuste hacia abajo.
            while True:

                izquierda = (
                    2 * indice + 1
                )

                derecha = (
                    2 * indice + 2
                )

                mayor = indice

                # Comparar hijo izquierdo.
                if (
                    izquierda < len(self._heap)
                    and
                    self._valor(
                        self._heap[izquierda]
                    )
                    >
                    self._valor(
                        self._heap[mayor]
                    )
                ):

                    mayor = izquierda

                # Comparar hijo derecho.
                if (
                    derecha < len(self._heap)
                    and
                    self._valor(
                        self._heap[derecha]
                    )
                    >
                    self._valor(
                        self._heap[mayor]
                    )
                ):

                    mayor = derecha

                # Si el padre ya es mayor,
                # terminamos.
                if mayor == indice:
                    break

                self._heap[indice], self._heap[mayor] = (
                    self._heap[mayor],
                    self._heap[indice]
                )

                indice = mayor

        # El dato está en la posición 2 de la tupla.
        return raiz[2]

    def listar(self):
        """
        Devuelve las tareas ordenadas por prioridad
        sin modificar la cola original.

        Para hacerlo se crea una copia temporal.
        """

        copia = ColaPrioridad()

        copia._heap = (
            self._heap.copy()
        )

        copia._secuencia = (
            self._secuencia
        )

        resultado = []

        while not copia.esta_vacia():

            resultado.append(
                copia.desencolar()
            )

        return resultado

    def esta_vacia(self):
        """
        Indica si la cola de prioridad está vacía.
        """

        return len(self._heap) == 0

    def limpiar(self):
        """
        Vacía completamente la cola de prioridad.
        """

        self._heap = []

        self._secuencia = 0