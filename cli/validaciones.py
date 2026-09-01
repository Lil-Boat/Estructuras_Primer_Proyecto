
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
