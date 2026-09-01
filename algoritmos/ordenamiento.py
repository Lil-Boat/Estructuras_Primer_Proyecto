def burbuja(
    datos,
    clave=lambda x: x
):
    """
    Ordenamiento Burbuja optimizado.

    Complejidad:
    - Mejor caso: O(n)
    - Promedio: O(n²)
    - Peor caso: O(n²)
    - Espacio: O(1) adicional
    """

    arreglo = list(datos)

    n = len(arreglo)

    # En cada pasada el elemento mayor restante
    # termina colocado al final.
    for i in range(n):

        intercambio = False

        for j in range(
            0,
            n - i - 1
        ):

            if (
                clave(arreglo[j])
                >
                clave(arreglo[j + 1])
            ):

                arreglo[j], arreglo[j + 1] = (
                    arreglo[j + 1],
                    arreglo[j]
                )

                intercambio = True

        # Si no hubo intercambios significa
        # que el arreglo ya estaba ordenado.
        if not intercambio:
            break

    return arreglo


def merge_sort(
    datos,
    clave=lambda x: x
):
    """
    Implementación recursiva de Merge Sort.

    Divide el arreglo repetidamente en mitades
    y luego combina las partes ordenadas.

    Complejidad temporal:
    O(n log n)

    Complejidad espacial:
    O(n)
    """

    arreglo = list(datos)

    # Caso base de la recursividad.
    if len(arreglo) <= 1:
        return arreglo

    medio = (
        len(arreglo) // 2
    )

    izquierda = merge_sort(
        arreglo[:medio],
        clave
    )

    derecha = merge_sort(
        arreglo[medio:],
        clave
    )

    return _merge(
        izquierda,
        derecha,
        clave
    )


def _merge(
    izquierda,
    derecha,
    clave
):
    """
    Combina dos listas previamente ordenadas
    en una única lista ordenada.
    """

    resultado = []

    i = 0
    j = 0

    while (
        i < len(izquierda)
        and
        j < len(derecha)
    ):

        if (
            clave(izquierda[i])
            <=
            clave(derecha[j])
        ):

            resultado.append(
                izquierda[i]
            )

            i += 1

        else:

            resultado.append(
                derecha[j]
            )

            j += 1

    # Agregar los elementos restantes.
    resultado.extend(
        izquierda[i:]
    )

    resultado.extend(
        derecha[j:]
    )

    return resultado


def quicksort(
    datos,
    clave=lambda x: x
):
    """
    Implementación recursiva de Quicksort.

    Se selecciona un pivote y los elementos
    se dividen en menores, iguales y mayores.

    Complejidad:
    - Promedio: O(n log n)
    - Peor caso: O(n²)
    """

    arreglo = list(datos)

    # Caso base.
    if len(arreglo) <= 1:
        return arreglo

    # Seleccionamos el elemento central como pivote.
    pivote = arreglo[
        len(arreglo) // 2
    ]

    menores = [
        elemento
        for elemento in arreglo
        if clave(elemento)
        <
        clave(pivote)
    ]

    iguales = [
        elemento
        for elemento in arreglo
        if clave(elemento)
        ==
        clave(pivote)
    ]

    mayores = [
        elemento
        for elemento in arreglo
        if clave(elemento)
        >
        clave(pivote)
    ]

    return (
        quicksort(
            menores,
            clave
        )
        +
        iguales
        +
        quicksort(
            mayores,
            clave
        )
    )