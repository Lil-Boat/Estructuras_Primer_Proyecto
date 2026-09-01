from pathlib import Path

from nucleo.motor import MotorFlujos

from persistencia.csv_manager import (
    CSVManager
)

from persistencia.auditoria import (
    Auditoria
)

from cli.menu import (
    menu_principal
)


def crear_admin_inicial(
    motor
):
    """
    Crea un administrador inicial únicamente
    cuando el sistema todavía no tiene usuarios.

    Esto permite entrar al programa por primera vez.
    """

    if len(motor.usuarios) == 0:

        motor.agregar_usuario(
            id_usuario=1,
            nombre="Administrador",
            contrasena="admin123",
            rol="ADMIN",
            actor_id=0,
            registrar=False
        )


def main():
    """
    Función principal del programa.

    Se encarga de:
    1. Definir las rutas de archivos.
    2. Crear el administrador de persistencia.
    3. Crear el sistema de auditoría.
    4. Crear el motor.
    5. Recuperar los datos anteriores.
    6. Abrir el menú de consola.
    """

    # Ruta donde se encuentra el proyecto.
    base = Path(
        __file__
    ).parent

    # Administrador de archivos CSV.
    persistencia = CSVManager(
        base / "data"
    )

    # Archivo de auditoría.
    auditoria = Auditoria(
        base
        /
        "data"
        /
        "auditoria_log.csv"
    )

    # Crear motor principal.
    motor = MotorFlujos(
        auditoria
    )

    # Recuperar usuarios y tareas
    # almacenados anteriormente.
    persistencia.cargar_todo(
        motor
    )

    # Crear administrador inicial si
    # todavía no existe ningún usuario.
    crear_admin_inicial(
        motor
    )

    # Guardar el estado inicial.
    persistencia.guardar_todo(
        motor
    )

    # Iniciar interfaz de consola.
    menu_principal(
        motor,
        persistencia
    )


# Esta condición hace que main() solamente
# se ejecute cuando abrimos directamente main.py.
if __name__ == "__main__":

    main()