class NodoCola:
    """
    Nodo utilizado por la cola FIFO.

    Cada nodo almacena un dato y una referencia
    al siguiente nodo.
    """

    def __init__(self, dato):

        self.dato = dato

        self.siguiente = None


class ColaFIFO:
    """
    Implementación manual de una cola FIFO.

    FIFO significa:
    First In, First Out.

    El primer elemento que entra será el primero
    que salga.
    """

    def __init__(self):

        # Primer elemento de la cola.
        self.frente = None

        # Último elemento.
        self.final = None

        self._tamano = 0

    def encolar(self, dato):
        """
        Inserta un nuevo elemento al final de la cola.
        """

        nuevo_nodo = NodoCola(
            dato
        )

        # Si no hay elementos,
        # frente y final serán el mismo nodo.
        if self.final is None:

            self.frente = nuevo_nodo
            self.final = nuevo_nodo

        else:

            # El antiguo último elemento apunta
            # hacia el nuevo nodo.
            self.final.siguiente = (
                nuevo_nodo
            )

            # Actualizamos el final.
            self.final = nuevo_nodo

        self._tamano += 1

    def desencolar(self):
        """
        Retira y retorna el primer elemento de la cola.
        """

        # No se puede desencolar una cola vacía.
        if self.frente is None:

            raise IndexError(
                "La cola está vacía."
            )

        dato = self.frente.dato

        # El segundo elemento pasa a ser el frente.
        self.frente = (
            self.frente.siguiente
        )

        # Si ya no quedan elementos,
        # también eliminamos la referencia al final.
        if self.frente is None:
            self.final = None

        self._tamano -= 1

        return dato

    def listar(self):
        """
        Devuelve los elementos respetando el orden FIFO.
        """

        resultado = []

        actual = self.frente

        while actual is not None:

            resultado.append(
                actual.dato
            )

            actual = actual.siguiente

        return resultado

    def reemplazar(
        self,
        elementos
    ):
        """
        Reconstruye completamente la cola.

        Esta función se utiliza principalmente durante
        el escalamiento SLA.
        """

        self.frente = None
        self.final = None
        self._tamano = 0

        for elemento in elementos:

            self.encolar(
                elemento
            )

    def esta_vacia(self):
        """
        Retorna True si la cola no contiene elementos.
        """

        return self.frente is None