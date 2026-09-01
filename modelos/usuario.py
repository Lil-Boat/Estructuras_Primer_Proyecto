ROLES_VALIDOS = {"ADMIN","USUARIO"}

class Usuario:
    """
    Representa a un usuario del sistema.

    Cada usuario tiene:
    - ID único.
    - Nombre.
    - Contraseña.
    - Rol: ADMIN o USUARIO.
    """

    def __init__(self, id_usuario, nombre, contrasena, rol):

        # Convertimos el rol a mayúsculas para evitar problemas
        # si el usuario escribe "admin", "Admin", etc.
        rol = rol.upper()

        # Validamos que el rol ingresado sea uno permitido.
        if rol not in ROLES_VALIDOS:
            raise ValueError(
                "Rol inválido. Use ADMIN o USUARIO."
            )

        # Guardamos los datos del usuario.
        self.id_usuario = int(id_usuario)
        self.nombre = nombre.strip()
        self.contrasena = contrasena
        self.rol = rol

    def __repr__(self):
        """
        Devuelve una representación sencilla del usuario.

        Es útil principalmente para depuración y pruebas.
        """
        return (
            f"Usuario("
            f"{self.id_usuario}, "
            f"{self.nombre!r}, "
            f"{self.rol})"
        )


class NodoUsuario:
    """
    Nodo utilizado dentro de la lista doblemente enlazada.

    Cada nodo guarda:
    - Un usuario.
    - Una referencia al nodo anterior.
    - Una referencia al nodo siguiente.
    """

    def __init__(self, usuario):

        self.usuario = usuario

        # En una lista doble cada nodo conoce
        # tanto al anterior como al siguiente.
        self.anterior = None
        self.siguiente = None


class ListaDobleUsuarios:
    """
    Implementación manual de una lista doblemente enlazada.

    Se utiliza específicamente para almacenar los usuarios
    registrados en el sistema.
    """

    def __init__(self):

        # Primer nodo de la lista.
        self.cabeza = None

        # Último nodo de la lista.
        self.cola = None

        # Cantidad de usuarios almacenados.
        self._tamano = 0

    def agregar(self, usuario):
        """
        Agrega un nuevo usuario al final de la lista.

        Antes de insertarlo se valida que no exista
        otro usuario con el mismo ID.
        """

        # Validamos que el ID no esté repetido.
        if self.buscar(usuario.id_usuario) is not None:
            raise ValueError(
                f"Ya existe un usuario con ID "
                f"{usuario.id_usuario}"
            )

        # Creamos el nodo que almacenará el usuario.
        nuevo_nodo = NodoUsuario(usuario)

        # Si la lista está vacía, el nuevo nodo
        # será simultáneamente cabeza y cola.
        if self.cabeza is None:

            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo

        else:

            # El nodo nuevo apunta hacia la cola actual.
            nuevo_nodo.anterior = self.cola

            # La cola actual apunta hacia el nuevo nodo.
            self.cola.siguiente = nuevo_nodo

            # Actualizamos la cola.
            self.cola = nuevo_nodo

        self._tamano += 1

    def buscar(self, id_usuario):
        """
        Busca un usuario por su ID.

        Recorre la lista desde la cabeza hasta encontrar
        el usuario solicitado.

        Si no existe, retorna None.
        """

        actual = self.cabeza

        while actual is not None:

            if actual.usuario.id_usuario == int(id_usuario):
                return actual.usuario

            actual = actual.siguiente

        return None

    def actualizar(
        self,
        id_usuario,
        nombre=None,
        contrasena=None,
        rol=None
    ):
        """
        Actualiza los datos de un usuario existente.

        Los campos que lleguen como None se mantienen
        con su valor anterior.
        """

        usuario = self.buscar(id_usuario)

        # No se puede actualizar un usuario inexistente.
        if usuario is None:
            raise ValueError(
                "Usuario no encontrado."
            )

        # Cambiar nombre únicamente si se recibió uno.
        if nombre is not None and nombre.strip():
            usuario.nombre = nombre.strip()

        # Cambiar contraseña únicamente si se recibió una.
        if contrasena is not None and contrasena:
            usuario.contrasena = contrasena

        # Cambiar rol únicamente si fue solicitado.
        if rol is not None:

            rol = rol.upper()

            if rol not in ROLES_VALIDOS:
                raise ValueError(
                    "Rol inválido."
                )

            usuario.rol = rol

        return usuario

    def eliminar(self, id_usuario):
        """
        Elimina un usuario de la lista doblemente enlazada.

        Se actualizan correctamente las conexiones de los
        nodos anterior y siguiente.
        """

        actual = self.cabeza

        while actual is not None:

            if actual.usuario.id_usuario == int(id_usuario):

                # Si tiene nodo anterior,
                # conectamos ese nodo con el siguiente.
                if actual.anterior is not None:

                    actual.anterior.siguiente = (
                        actual.siguiente
                    )

                else:

                    # Si no tiene anterior significa
                    # que estamos eliminando la cabeza.
                    self.cabeza = actual.siguiente

                # Si tiene nodo siguiente,
                # conectamos ese nodo con el anterior.
                if actual.siguiente is not None:

                    actual.siguiente.anterior = (
                        actual.anterior
                    )

                else:

                    # Si no tiene siguiente significa
                    # que estamos eliminando la cola.
                    self.cola = actual.anterior

                self._tamano -= 1

                return actual.usuario

            actual = actual.siguiente

        raise ValueError(
            "Usuario no encontrado."
        )

    def listar(self):
        """
        Devuelve una lista normal de Python con todos
        los usuarios almacenados.

        La estructura principal sigue siendo la lista
        doblemente enlazada.
        """

        resultado = []

        actual = self.cabeza

        while actual is not None:

            resultado.append(
                actual.usuario
            )

            actual = actual.siguiente

        return resultado

    def __len__(self):
        """
        Devuelve la cantidad de usuarios registrados.
        """

        return self._tamano