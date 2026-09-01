class auditoria:
    """
    Clase para gestionar una pila (LIFO) con historial de acciones,
    deshacer y rehacer.
    """

    def __init__(self, elementos=None):
        """Inicializa la pila con una lista opcional de elementos."""
        self.pila = [] if elementos is None else list(elementos)
        self.historial = []
        self.pila_deshacer = []
        self.pila_rehacer = []

    def apilar(self, valor):
        """Agrega un elemento al final de la pila."""
        self.pila.append(valor)
        self.pila_deshacer.append({"accion": "apilar", "valor": valor})
        self.pila_rehacer.clear()
        self.historial.append({"accion": "apilar", "valor": valor})
        return valor

    def desapilar(self):
        """Elimina y retorna el elemento del tope de la pila."""
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        valor = self.pila.pop()
        self.pila_deshacer.append({"accion": "desapilar", "valor": valor})
        self.pila_rehacer.clear()
        self.historial.append({"accion": "desapilar", "valor": valor})
        return valor

    def ver_tope(self):
        """Retorna el elemento del tope sin eliminarlo."""
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.pila[-1]

    def esta_vacia(self):
        """Indica si la pila está vacía."""
        return len(self.pila) == 0

    def comprobar_pila_vacia(self):
        """Alias para verificar si la pila está vacía."""
        return self.esta_vacia()

    def tamano(self):
        """Retorna la cantidad de elementos en la pila."""
        return len(self.pila)

    def vaciar(self):
        """Elimina todos los elementos de la pila."""
        self.pila.clear()
        self.pila_deshacer.clear()
        self.pila_rehacer.clear()
        self.historial.append({"accion": "vaciar", "valor": []})

    def historial_acciones(self):
        """Retorna el historial completo de acciones realizadas."""
        return list(self.historial)

    def historial_de_acciones(self):
        """Alias para obtener el historial de acciones."""
        return self.historial_acciones()

    def deshacer(self):
        """Deshace la última acción realizada."""
        if not self.pila_deshacer:
            raise IndexError("No hay acciones para deshacer")

        accion = self.pila_deshacer.pop()
        self.pila_rehacer.append(accion)

        if accion["accion"] == "apilar":
            self.pila.pop()
        elif accion["accion"] == "desapilar":
            self.pila.append(accion["valor"])

        self.historial.append({"accion": "deshacer", "valor": accion})
        return self.ver_tope() if not self.esta_vacia() else None

    def rehacer(self):
        """Rehace la última acción deshecha."""
        if not self.pila_rehacer:
            raise IndexError("No hay acciones para rehacer")

        accion = self.pila_rehacer.pop()
        self.pila_deshacer.append(accion)

        if accion["accion"] == "apilar":
            self.pila.append(accion["valor"])
        elif accion["accion"] == "desapilar":
            self.pila.pop()

        self.historial.append({"accion": "rehacer", "valor": accion})
        return self.ver_tope() if not self.esta_vacia() else None
