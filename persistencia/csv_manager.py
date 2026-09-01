import csv
from pathlib import Path


class CSVManager:
    """
    Se encarga de guardar y cargar la información del sistema
    utilizando archivos CSV.

    Maneja:
    - usuarios.csv
    - tareas.csv
    - subtareas.csv
    """

    def __init__(self, carpeta):
        """
        Recibe la carpeta donde se almacenarán los archivos CSV.

        Si la carpeta no existe, se crea automáticamente.
        """

        self.carpeta = Path(carpeta)

        self.carpeta.mkdir(
            parents=True,
            exist_ok=True
        )

        # Definimos la ubicación de cada archivo CSV.
        self.usuarios_csv = (
            self.carpeta / "usuarios.csv"
        )

        self.tareas_csv = (
            self.carpeta / "tareas.csv"
        )

        self.subtareas_csv = (
            self.carpeta / "subtareas.csv"
        )

    def guardar_todo(self, motor):
        """
        Guarda todo el estado actual del sistema.

        Cada vez que se modifica un usuario o tarea,
        esta función permite actualizar los archivos CSV.
        """

        self._guardar_usuarios(
            motor
        )

        self._guardar_tareas(
            motor
        )

    def _guardar_usuarios(self, motor):
        """
        Guarda todos los usuarios registrados.

        La información proviene de la lista doblemente enlazada.
        """

        with open(
            self.usuarios_csv,
            "w",
            newline="",
            encoding="utf-8"
        ) as archivo:

            escritor = csv.writer(
                archivo
            )

            # Encabezados del archivo.
            escritor.writerow([
                "id_usuario",
                "nombre",
                "contrasena",
                "rol"
            ])

            # Recorremos todos los usuarios.
            for usuario in motor.usuarios.listar():

                escritor.writerow([
                    usuario.id_usuario,
                    usuario.nombre,
                    usuario.contrasena,
                    usuario.rol
                ])

    def _guardar_tareas(self, motor):
        """
        Guarda las tareas raíz y las subtareas.

        Las tareas raíz se almacenan en tareas.csv.
        Las subtareas se almacenan en subtareas.csv.
        """

        # ----------------------------
        # Guardar tareas principales.
        # ----------------------------
        with open(
            self.tareas_csv,
            "w",
            newline="",
            encoding="utf-8"
        ) as archivo:

            escritor = csv.writer(
                archivo
            )

            escritor.writerow([
                "id_tarea",
                "prioridad",
                "id_usuario",
                "descripcion",
                "estado",
                "ciclos_espera"
            ])

            # Solo las tareas raíz van en este archivo.
            for tarea in motor.tareas_raiz:

                escritor.writerow([
                    tarea.id_tarea,
                    tarea.prioridad,
                    tarea.id_usuario,
                    tarea.descripcion,
                    tarea.estado,
                    tarea.ciclos_espera
                ])

        # ----------------------------
        # Guardar subtareas.
        # ----------------------------
        with open(
            self.subtareas_csv,
            "w",
            newline="",
            encoding="utf-8"
        ) as archivo:

            escritor = csv.writer(
                archivo
            )

            escritor.writerow([
                "id_subtarea",
                "id_padre",
                "prioridad",
                "id_usuario",
                "descripcion",
                "estado",
                "ciclos_espera"
            ])

            # Las subtareas deben guardarse recursivamente.
            for tarea in motor.tareas_raiz:

                self._guardar_subtareas_rec(
                    escritor,
                    tarea
                )

    def _guardar_subtareas_rec(
        self,
        escritor,
        padre
    ):
        """
        Guarda recursivamente todas las subtareas.

        Se utiliza recursividad porque una subtarea puede
        tener otras subtareas dentro de ella.
        """

        for subtarea in padre.subtareas:

            escritor.writerow([
                subtarea.id_tarea,
                padre.id_tarea,
                subtarea.prioridad,
                subtarea.id_usuario,
                subtarea.descripcion,
                subtarea.estado,
                subtarea.ciclos_espera
            ])

            # Llamada recursiva para revisar si
            # esta subtarea también tiene hijos.
            self._guardar_subtareas_rec(
                escritor,
                subtarea
            )

    def cargar_todo(self, motor):
        """
        Reconstruye el estado anterior del sistema.

        Al iniciar el programa:
        1. Carga usuarios.
        2. Carga tareas.
        3. Carga subtareas.
        4. Reconstruye las colas.
        """

        self._cargar_usuarios(
            motor
        )

        self._cargar_tareas(
            motor
        )

        # Después de cargar las tareas,
        # reconstruimos las colas correspondientes.
        motor._reconstruir_colas()

    def _cargar_usuarios(self, motor):
        """
        Lee usuarios.csv y vuelve a crear los usuarios
        dentro de la lista doblemente enlazada.
        """

        # Si el archivo todavía no existe,
        # simplemente no hay usuarios que cargar.
        if not self.usuarios_csv.exists():
            return

        with open(
            self.usuarios_csv,
            newline="",
            encoding="utf-8"
        ) as archivo:

            lector = csv.DictReader(
                archivo
            )

            for fila in lector:

                try:

                    # actor_id = 0 significa carga interna.
                    # No se aplican permisos ni historial.
                    motor.agregar_usuario(
                        id_usuario=int(
                            fila["id_usuario"]
                        ),
                        nombre=fila["nombre"],
                        contrasena=fila["contrasena"],
                        rol=fila["rol"],
                        actor_id=0,
                        registrar=False
                    )

                except Exception:

                    # Si una fila está dañada,
                    # no dejamos que todo el programa falle.
                    continue

    def _cargar_tareas(self, motor):
        """
        Lee tareas.csv y subtareas.csv.

        Después reconstruye las relaciones del árbol.
        """

        # -----------------------------
        # Cargar tareas principales.
        # -----------------------------
        if self.tareas_csv.exists():

            with open(
                self.tareas_csv,
                newline="",
                encoding="utf-8"
            ) as archivo:

                lector = csv.DictReader(
                    archivo
                )

                for fila in lector:

                    try:

                        motor.crear_tarea(
                            id_tarea=int(
                                fila["id_tarea"]
                            ),
                            prioridad=fila[
                                "prioridad"
                            ],
                            id_usuario=int(
                                fila["id_usuario"]
                            ),
                            descripcion=fila[
                                "descripcion"
                            ],
                            estado=fila[
                                "estado"
                            ],
                            ciclos_espera=int(
                                fila.get(
                                    "ciclos_espera",
                                    0
                                )
                            ),
                            actor_id=0,
                            registrar=False
                        )

                    except Exception:

                        continue

        # -----------------------------
        # Cargar subtareas.
        # -----------------------------
        if self.subtareas_csv.exists():

            with open(
                self.subtareas_csv,
                newline="",
                encoding="utf-8"
            ) as archivo:

                pendientes = list(
                    csv.DictReader(
                        archivo
                    )
                )

            """
            Se realizan varias pasadas porque podría ocurrir esto:

            Tarea 1
               └── Subtarea 2
                     └── Subtarea 3

            Para agregar la subtarea 3 primero debe existir la 2.
            """

            for _ in range(
                len(pendientes) + 1
            ):

                restantes = []

                hubo_cambio = False

                for fila in pendientes:

                    try:

                        motor.agregar_subtarea(
                            id_subtarea=int(
                                fila[
                                    "id_subtarea"
                                ]
                            ),
                            id_padre=int(
                                fila[
                                    "id_padre"
                                ]
                            ),
                            descripcion=fila[
                                "descripcion"
                            ],
                            prioridad=fila[
                                "prioridad"
                            ],
                            id_usuario=int(
                                fila[
                                    "id_usuario"
                                ]
                            ),
                            estado=fila[
                                "estado"
                            ],
                            ciclos_espera=int(
                                fila.get(
                                    "ciclos_espera",
                                    0
                                )
                            ),
                            actor_id=0,
                            registrar=False
                        )

                        hubo_cambio = True

                    except Exception:

                        # Si el padre todavía no existe,
                        # dejamos la subtarea para la próxima pasada.
                        restantes.append(
                            fila
                        )

                pendientes = restantes

                # Si no logramos insertar ninguna nueva,
                # no tiene sentido seguir intentando.
                if not hubo_cambio:
                    break