
import os
import sys

from getpass import getpass


def leer_entero(mensaje, minimo=None):
    """Solicita un número entero y repite la entrada hasta que sea válida."""
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if minimo is not None and valor < minimo:
                print(f"Error: el valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Error: debe ingresar un número entero válido.")


def leer_no_vacio(mensaje):
    """Solicita texto y evita que el usuario deje el campo vacío."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Error: este campo no puede quedar vacío.")


def leer_opcion(mensaje, opciones):
    """Valida que la opción ingresada pertenezca al conjunto permitido."""
    opciones = {str(o).upper() for o in opciones}
    while True:
        valor = input(mensaje).strip().upper()
        if valor in opciones:
            return valor
        print("Error: opción inválida. Intente nuevamente.")


def leer_contrasena(mensaje):
    """
    Solicita una contraseña sin mostrarla en pantalla.

    getpass funciona correctamente únicamente cuando la entrada
    proviene de una consola interactiva real.

    En Windows, getpass siempre lee del teclado físico mediante
    msvcrt, ignorando el stdin redirigido. Si el programa se
    ejecuta desde un entorno sin consola real (IDE, tubería,
    CI, etc.), getpass puede quedarse bloqueado esperando teclas.

    Por lo tanto:
    - Si el stdin no es una terminal interactiva,
      se lee con input() normal para no bloquearse.
    - Si getpass falla por cualquier motivo,
      se reintenta con input().

    Para forzar que la contraseña siempre se muestre en pantalla,
    se puede definir la variable de entorno:

        FLUJOS_MOSTRAR_CLAVE=1
    """

    # Permitir forzar el modo con eco en entornos problemáticos.
    if os.environ.get("FLUJOS_MOSTRAR_CLAVE", "").upper() == "1":
        return input(mensaje)

    # Sin terminal interactiva real: no usar getpass.
    if sys.stdin is None or not sys.stdin.isatty():
        return input(mensaje)

    try:
        return getpass(mensaje)
    except Exception:
        # Última red de seguridad: si getpass falla,
        # se lee normalmente sin ocultar caracteres.
        return input(mensaje)
