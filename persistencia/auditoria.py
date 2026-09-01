from datetime import datetime

from pathlib import Path


class Auditoria:
    """
    Maneja la bitácora de auditoría.

    Este archivo es append-only:
    únicamente se agregan nuevas líneas.

    Nunca se modifica ni se elimina
    información anterior.
    """

    def __init__(self, ruta):

        self.ruta = Path(ruta)

        # Crear carpeta si no existe.
        self.ruta.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Crear archivo inicialmente.
        if not self.ruta.exists():

            self.ruta.write_text(
                (
                    "fecha_hora|"
                    "id_usuario|"
                    "accion|"
                    "id_tarea\n"
                ),
                encoding="utf-8"
            )

    def registrar(
        self,
        id_usuario,
        accion,
        id_tarea="-"
    ):
        """
        Agrega una nueva entrada de auditoría.

        Formato:
        Fecha | Usuario | Acción | Tarea
        """

        fecha = (
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        linea = (
            f"{fecha}|"
            f"{id_usuario}|"
            f"{accion}|"
            f"{id_tarea}\n"
        )

        # El modo "a" significa append.
        # Solamente agrega información al final.
        with open(
            self.ruta,
            "a",
            encoding="utf-8"
        ) as archivo:

            archivo.write(
                linea
            )