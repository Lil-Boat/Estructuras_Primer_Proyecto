class NodoPila:
    """
    Nodo utilizado dentro de la pila.
    """

    def __init__(
        self,
        dato,
        siguiente=None
    ):

        self.dato = dato

        self.siguiente = siguiente


class Pila:
    """
    Implementación manual de una pila LIFO.

    LIFO:
    Last In, First Out.

    El último elemento que entra es el primero
    que sale.
    """

    def __init__(self):

        # Nodo ubicado en la parte superior.
        self.tope = None

        self._tamano = 0

    def apilar(self, dato):
        """
        Inserta un elemento en el tope de la pila.
        """

        nuevo_nodo = NodoPila(
            dato,
            self.tope
        )

        self.tope = nuevo_nodo

        self._tamano += 1

    def desapilar(self):
        """
        Elimina y retorna el elemento del tope.
        """

        if self.tope is None:

            raise IndexError(
                "La pila está vacía."
            )

        dato = self.tope.dato

        self.tope = (
            self.tope.siguiente
        )

        self._tamano -= 1

        return dato

    def esta_vacia(self):
        """
        Indica si la pila está vacía.
        """

        return self.tope is None

    def limpiar(self):
        """
        Elimina todos los elementos de la pila.
        """

        self.tope = None

        self._tamano = 0


class Accion:
    """
    Representa una acción que puede ser
    deshecha y rehecha.

    Guarda las funciones necesarias para realizar
    ambas operaciones.
    """

    def __init__(
        self,
        descripcion,
        id_usuario,
        id_tarea,
        deshacer,
        rehacer
    ):

        self.descripcion = descripcion

        # Usuario que realizó originalmente la acción.
        self.id_usuario = id_usuario

        # Tarea relacionada, si aplica.
        self.id_tarea = id_tarea

        # Función que revierte la operación.
        self.deshacer = deshacer

        # Función que vuelve a aplicarla.
        self.rehacer = rehacer


class Historial:
    """
    Administra el sistema de Deshacer/Rehacer.

    Utiliza dos pilas:
    - Una pila para deshacer.
    - Otra pila para rehacer.
    """

    def __init__(self):

        self.pila_deshacer = Pila()

        self.pila_rehacer = Pila()

    def registrar(
        self,
        accion
    ):
        """
        Registra una nueva acción.

        Cuando ocurre una acción nueva,
        se limpia la pila de rehacer porque
        esas acciones anteriores ya no deberían
        volver a aplicarse.
        """

        self.pila_deshacer.apilar(
            accion
        )

        self.pila_rehacer.limpiar()

    def deshacer(self):
        """
        Deshace la última acción realizada.
        """

        if self.pila_deshacer.esta_vacia():

            raise IndexError(
                "No hay acciones para deshacer."
            )

        accion = (
            self.pila_deshacer
            .desapilar()
        )

        # Ejecutamos la función inversa.
        accion.deshacer()

        # Ahora esta acción puede rehacerse.
        self.pila_rehacer.apilar(
            accion
        )

        return accion

    def rehacer(self):
        """
        Vuelve a realizar la última acción
        que había sido deshecha.
        """

        if self.pila_rehacer.esta_vacia():

            raise IndexError(
                "No hay acciones para rehacer."
            )

        accion = (
            self.pila_rehacer
            .desapilar()
        )

        accion.rehacer()

        # La acción vuelve a formar parte
        # del historial normal.
        self.pila_deshacer.apilar(
            accion
        )

        return accion