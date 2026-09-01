# getpass permite solicitar una contraseña
# sin mostrarla en pantalla.
from getpass import getpass

from cli.validaciones import (
    leer_entero,
    leer_no_vacio,
    leer_opcion
)


def login(motor):
    """
    Maneja el inicio de sesión.

    Solicita:
    - ID.
    - Contraseña oculta.

    Continúa solicitando los datos hasta
    que las credenciales sean correctas.
    """

    while True:

        print(
            "\n=== INICIO DE SESIÓN ==="
        )

        try:

            id_usuario = leer_entero(
                "ID de usuario: ",
                1
            )

            # La contraseña no se muestra
            # en texto plano.
            contrasena = getpass(
                "Contraseña: "
            )

            usuario = motor.autenticar(
                id_usuario,
                contrasena
            )

            print(
                f"\nBienvenido/a, "
                f"{usuario.nombre}"
            )

            print(
                f"Rol: {usuario.rol}"
            )

            return usuario

        except ValueError as error:

            print(
                f"Error: {error}"
            )


def menu_principal(
    motor,
    persistencia
):
    """
    Después del login revisa el rol.

    ADMIN:
    entra al menú administrativo.

    USUARIO:
    entra al menú restringido.
    """

    usuario = login(
        motor
    )

    if usuario.rol == "ADMIN":

        menu_admin(
            motor,
            persistencia,
            usuario
        )

    else:

        menu_usuario(
            motor,
            persistencia,
            usuario
        )


def menu_admin(
    motor,
    persistencia,
    usuario
):
    """
    Menú principal del administrador.

    Tiene acceso total al sistema.
    """

    while True:

        print(
            "\n=== MENÚ ADMINISTRADOR ==="
        )

        print(
            "1. Gestión de usuarios"
        )

        print(
            "2. Gestión de tareas"
        )

        print(
            "3. Ejecutar siguiente tarea"
        )

        print(
            "4. Deshacer"
        )

        print(
            "5. Rehacer"
        )

        print(
            "6. Reportes"
        )

        print(
            "0. Guardar y salir"
        )

        opcion = leer_opcion(
            "Seleccione una opción: ",
            {
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6"
            }
        )

        try:

            if opcion == "1":

                submenu_usuarios(
                    motor,
                    persistencia,
                    usuario
                )

            elif opcion == "2":

                submenu_tareas(
                    motor,
                    persistencia,
                    usuario
                )

            elif opcion == "3":

                tarea = (
                    motor.ejecutar_siguiente(
                        usuario.id_usuario
                    )
                )

                # Persistencia automática.
                persistencia.guardar_todo(
                    motor
                )

                print(
                    "\nTarea ejecutada:"
                )

                print(
                    f"[{tarea.id_tarea}] "
                    f"{tarea.descripcion}"
                )

            elif opcion == "4":

                descripcion = (
                    motor.deshacer(
                        usuario.id_usuario
                    )
                )

                persistencia.guardar_todo(
                    motor
                )

                print(
                    f"Acción deshecha: "
                    f"{descripcion}"
                )

            elif opcion == "5":

                descripcion = (
                    motor.rehacer(
                        usuario.id_usuario
                    )
                )

                persistencia.guardar_todo(
                    motor
                )

                print(
                    f"Acción rehecha: "
                    f"{descripcion}"
                )

            elif opcion == "6":

                mostrar_reportes(
                    motor
                )

            elif opcion == "0":

                persistencia.guardar_todo(
                    motor
                )

                print(
                    "Datos guardados."
                )

                break

        # Capturar errores conocidos.
        except (
            ValueError,
            IndexError,
            PermissionError
        ) as error:

            print(
                f"Error: {error}"
            )

        # Última protección para evitar
        # que el programa se cierre inesperadamente.
        except Exception as error:

            print(
                f"Error controlado: "
                f"{error}"
            )


def submenu_usuarios(
    motor,
    persistencia,
    actor
):
    """
    Submenú CRUD para la gestión de usuarios.

    Operaciones:
    - Agregar.
    - Actualizar.
    - Eliminar.
    - Listar.
    - Buscar.
    """

    while True:

        print(
            "\n--- GESTIÓN DE USUARIOS ---"
        )

        print(
            "1. Agregar usuario"
        )

        print(
            "2. Actualizar usuario"
        )

        print(
            "3. Eliminar usuario"
        )

        print(
            "4. Listar usuarios"
        )

        print(
            "5. Buscar usuario por ID"
        )

        print(
            "0. Volver"
        )

        opcion = leer_opcion(
            "Seleccione una opción: ",
            {
                "0",
                "1",
                "2",
                "3",
                "4",
                "5"
            }
        )

        try:

            # --------------------
            # AGREGAR USUARIO
            # --------------------
            if opcion == "1":

                id_usuario = leer_entero(
                    "ID del usuario: ",
                    1
                )

                nombre = leer_no_vacio(
                    "Nombre: "
                )

                # Contraseña oculta.
                contrasena = getpass(
                    "Contraseña: "
                )

                rol = leer_opcion(
                    "Rol (ADMIN/USUARIO): ",
                    {
                        "ADMIN",
                        "USUARIO"
                    }
                )

                motor.agregar_usuario(
                    id_usuario,
                    nombre,
                    contrasena,
                    rol,
                    actor.id_usuario
                )

                persistencia.guardar_todo(
                    motor
                )

                print(
                    "Usuario agregado correctamente."
                )

            # --------------------
            # ACTUALIZAR USUARIO
            # --------------------
            elif opcion == "2":

                id_usuario = leer_entero(
                    "ID a actualizar: ",
                    1
                )

                print(
                    "Presione Enter para "
                    "mantener un dato."
                )

                nombre = input(
                    "Nuevo nombre: "
                ).strip()

                if nombre == "":
                    nombre = None

                cambiar_clave = leer_opcion(
                    "¿Cambiar contraseña? (S/N): ",
                    {
                        "S",
                        "N"
                    }
                )

                if cambiar_clave == "S":

                    contrasena = getpass(
                        "Nueva contraseña: "
                    )

                else:

                    contrasena = None

                rol = input(
                    "Nuevo rol "
                    "ADMIN/USUARIO "
                    "(Enter = mantener): "
                ).strip().upper()

                if rol == "":
                    rol = None

                motor.actualizar_usuario(
                    id_usuario,
                    actor.id_usuario,
                    nombre,
                    contrasena,
                    rol
                )

                persistencia.guardar_todo(
                    motor
                )

                print(
                    "Usuario actualizado."
                )

            # --------------------
            # ELIMINAR USUARIO
            # --------------------
            elif opcion == "3":

                id_usuario = leer_entero(
                    "ID a eliminar: ",
                    1
                )

                motor.eliminar_usuario(
                    id_usuario,
                    actor.id_usuario
                )

                persistencia.guardar_todo(
                    motor
                )

                print(
                    "Usuario eliminado."
                )

            # --------------------
            # LISTAR USUARIOS
            # --------------------
            elif opcion == "4":

                usuarios = (
                    motor.usuarios.listar()
                )

                if not usuarios:

                    print(
                        "No hay usuarios."
                    )

                else:

                    print(
                        "\nID | NOMBRE | ROL"
                    )

                    for usuario in usuarios:

                        print(
                            f"{usuario.id_usuario}"
                            f" | "
                            f"{usuario.nombre}"
                            f" | "
                            f"{usuario.rol}"
                        )

            # --------------------
            # BUSCAR USUARIO
            # --------------------
            elif opcion == "5":

                id_usuario = leer_entero(
                    "ID a buscar: ",
                    1
                )

                usuario = (
                    motor.usuarios.buscar(
                        id_usuario
                    )
                )

                if usuario is None:

                    print(
                        "Usuario no encontrado."
                    )

                else:

                    print(
                        f"ID: "
                        f"{usuario.id_usuario}"
                    )

                    print(
                        f"Nombre: "
                        f"{usuario.nombre}"
                    )

                    print(
                        f"Rol: "
                        f"{usuario.rol}"
                    )

            elif opcion == "0":

                break

        except (
            ValueError,
            PermissionError
        ) as error:

            print(
                f"Error: {error}"
            )


def submenu_tareas(
    motor,
    persistencia,
    actor
):
    """
    Submenú administrativo de tareas.

    Permite:
    - Crear.
    - Actualizar.
    - Cancelar.
    - Eliminar.
    - Listar pendientes.
    - Buscar.
    - Agregar subtareas.
    """

    while True:

        print(
            "\n--- GESTIÓN DE TAREAS ---"
        )

        print(
            "1. Agregar tarea"
        )

        print(
            "2. Actualizar tarea"
        )

        print(
            "3. Cancelar tarea"
        )

        print(
            "4. Eliminar tarea raíz"
        )

        print(
            "5. Listar tareas pendientes"
        )

        print(
            "6. Buscar tarea por ID"
        )

        print(
            "7. Agregar subtarea"
        )

        print(
            "0. Volver"
        )

        opcion = leer_opcion(
            "Seleccione una opción: ",
            {
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7"
            }
        )

        try:

            # --------------------
            # CREAR TAREA
            # --------------------
            if opcion == "1":

                id_tarea = leer_entero(
                    "ID de tarea: ",
                    1
                )

                prioridad = leer_opcion(
                    "Prioridad "
                    "(BAJA/MEDIA/ALTA): ",
                    {
                        "BAJA",
                        "MEDIA",
                        "ALTA"
                    }
                )

                responsable = leer_entero(
                    "ID del responsable: ",
                    1
                )

                descripcion = leer_no_vacio(
                    "Descripción: "
                )

                motor.crear_tarea(
                    id_tarea,
                    prioridad,
                    responsable,
                    descripcion,
                    actor.id_usuario
                )

                persistencia.guardar_todo(
                    motor
                )

                print(
                    "Tarea creada."
                )

            # --------------------
            # ACTUALIZAR TAREA
            # --------------------
            elif opcion == "2":

                id_tarea = leer_entero(
                    "ID de tarea: ",
                    1
                )

                print(
                    "Presione Enter para mantener "
                    "el valor actual."
                )

                descripcion = input(
                    "Nueva descripción: "
                ).strip()

                if descripcion == "":
                    descripcion = None

                prioridad = input(
                    "Nueva prioridad "
                    "BAJA/MEDIA/ALTA: "
                ).strip().upper()

                if prioridad == "":
                    prioridad = None

                responsable_texto = input(
                    "Nuevo responsable ID: "
                ).strip()

                if responsable_texto == "":

                    responsable = None

                else:

                    try:

                        responsable = int(
                            responsable_texto
                        )

                    except ValueError:

                        raise ValueError(
                            "El responsable "
                            "debe ser un número entero."
                        )

                motor.actualizar_tarea(
                    id_tarea,
                    actor.id_usuario,
                    descripcion,
                    prioridad,
                    responsable
                )

                persistencia.guardar_todo(
                    motor
                )

                print(
                    "Tarea actualizada."
                )

            # --------------------
            # CANCELAR TAREA
            # --------------------
            elif opcion == "3":

                id_tarea = leer_entero(
                    "ID de tarea: ",
                    1
                )

                motor.cancelar_tarea(
                    id_tarea,
                    actor.id_usuario
                )

                persistencia.guardar_todo(
                    motor
                )

                print(
                    "Tarea cancelada."
                )

            # --------------------
            # ELIMINAR TAREA
            # --------------------
            elif opcion == "4":

                id_tarea = leer_entero(
                    "ID de tarea raíz: ",
                    1
                )

                motor.eliminar_tarea(
                    id_tarea,
                    actor.id_usuario
                )

                persistencia.guardar_todo(
                    motor
                )

                print(
                    "Tarea eliminada."
                )

            # --------------------
            # LISTAR PENDIENTES
            # --------------------
            elif opcion == "5":

                pendientes = (
                    motor.listar_pendientes()
                )

                if not pendientes:

                    print(
                        "No existen tareas pendientes."
                    )

                else:

                    print(
                        "\nID | PRIORIDAD | "
                        "RESPONSABLE | DESCRIPCIÓN"
                    )

                    for tarea in pendientes:

                        print(
                            f"{tarea.id_tarea}"
                            f" | "
                            f"{tarea.prioridad}"
                            f" | "
                            f"{tarea.id_usuario}"
                            f" | "
                            f"{tarea.descripcion}"
                        )

            # --------------------
            # BUSCAR TAREA
            # --------------------
            elif opcion == "6":

                id_tarea = leer_entero(
                    "ID de tarea: ",
                    1
                )

                tarea = motor.buscar_tarea(
                    id_tarea
                )

                if tarea is None:

                    print(
                        "Tarea no encontrada."
                    )

                else:

                    print(
                        f"ID: "
                        f"{tarea.id_tarea}"
                    )

                    print(
                        f"Descripción: "
                        f"{tarea.descripcion}"
                    )

                    print(
                        f"Prioridad: "
                        f"{tarea.prioridad}"
                    )

                    print(
                        f"Estado: "
                        f"{tarea.estado}"
                    )

                    print(
                        f"Responsable: "
                        f"{tarea.id_usuario}"
                    )

                    print(
                        f"Ciclos de espera: "
                        f"{tarea.ciclos_espera}"
                    )

            # --------------------
            # AGREGAR SUBTAREA
            # --------------------
            elif opcion == "7":

                id_subtarea = leer_entero(
                    "ID de subtarea: ",
                    1
                )

                id_padre = leer_entero(
                    "ID de tarea padre: ",
                    1
                )

                descripcion = leer_no_vacio(
                    "Descripción: "
                )

                prioridad = leer_opcion(
                    "Prioridad "
                    "(BAJA/MEDIA/ALTA): ",
                    {
                        "BAJA",
                        "MEDIA",
                        "ALTA"
                    }
                )

                responsable = leer_entero(
                    "ID responsable: ",
                    1
                )

                motor.agregar_subtarea(
                    id_subtarea,
                    id_padre,
                    descripcion,
                    actor.id_usuario,
                    prioridad,
                    responsable
                )

                persistencia.guardar_todo(
                    motor
                )

                print(
                    "Subtarea agregada."
                )

            elif opcion == "0":

                break

        except (
            ValueError,
            PermissionError
        ) as error:

            print(
                f"Error: {error}"
            )


def menu_usuario(
    motor,
    persistencia,
    usuario
):
    """
    Menú del usuario normal.

    Tiene acceso restringido según el enunciado.
    """

    while True:

        print(
            "\n=== MENÚ USUARIO ==="
        )

        print(
            "1. Ver lista general de tareas"
        )

        print(
            "2. Ver mis tareas"
        )

        print(
            "3. Cambiar estado de una tarea asignada"
        )

        print(
            "0. Salir"
        )

        opcion = leer_opcion(
            "Seleccione una opción: ",
            {
                "0",
                "1",
                "2",
                "3"
            }
        )

        try:

            # --------------------
            # LISTA GENERAL
            # --------------------
            if opcion == "1":

                tareas = (
                    motor.reporte_tareas(
                        "id",
                        "merge"
                    )
                )

                if not tareas:

                    print(
                        "No existen tareas."
                    )

                else:

                    for tarea in tareas:

                        print(
                            f"{tarea.id_tarea}"
                            f" | "
                            f"{tarea.prioridad}"
                            f" | "
                            f"{tarea.estado}"
                            f" | Responsable: "
                            f"{tarea.id_usuario}"
                            f" | "
                            f"{tarea.descripcion}"
                        )

            # --------------------
            # MIS TAREAS
            # --------------------
            elif opcion == "2":

                tareas = (
                    motor.listar_tareas_usuario(
                        usuario.id_usuario
                    )
                )

                if not tareas:

                    print(
                        "No tiene tareas asignadas."
                    )

                else:

                    for tarea in tareas:

                        print(
                            f"{tarea.id_tarea}"
                            f" | "
                            f"{tarea.prioridad}"
                            f" | "
                            f"{tarea.estado}"
                            f" | "
                            f"{tarea.descripcion}"
                        )

            # --------------------
            # CAMBIAR ESTADO
            # --------------------
            elif opcion == "3":

                id_tarea = leer_entero(
                    "ID de tarea: ",
                    1
                )

                # Usuario normal solamente puede
                # alternar entre pendiente y completada.
                estado = leer_opcion(
                    "Nuevo estado "
                    "(PENDIENTE/COMPLETADA): ",
                    {
                        "PENDIENTE",
                        "COMPLETADA"
                    }
                )

                motor.cambiar_estado_tarea(
                    id_tarea,
                    estado,
                    usuario.id_usuario
                )

                persistencia.guardar_todo(
                    motor
                )

                print(
                    "Estado actualizado."
                )

            elif opcion == "0":

                break

        except (
            ValueError,
            PermissionError
        ) as error:

            print(
                f"Error: {error}"
            )


def mostrar_reportes(
    motor
):
    """
    Permite elegir:
    - El criterio de ordenamiento.
    - El algoritmo.

    Así se demuestra el uso real de los
    tres algoritmos requeridos.
    """

    criterio = leer_opcion(
        (
            "Criterio "
            "(ID/PRIORIDAD/DESCRIPCION/"
            "ESTADO/RESPONSABLE): "
        ),
        {
            "ID",
            "PRIORIDAD",
            "DESCRIPCION",
            "ESTADO",
            "RESPONSABLE"
        }
    ).lower()

    algoritmo = leer_opcion(
        (
            "Algoritmo "
            "(BURBUJA/MERGE/QUICK): "
        ),
        {
            "BURBUJA",
            "MERGE",
            "QUICK"
        }
    ).lower()

    tareas = motor.reporte_tareas(
        criterio,
        algoritmo
    )

    print(
        "\n=== REPORTE DE TAREAS ==="
    )

    for tarea in tareas:

        print(
            f"{tarea.id_tarea}"
            f" | "
            f"{tarea.prioridad}"
            f" | "
            f"{tarea.estado}"
            f" | Responsable: "
            f"{tarea.id_usuario}"
            f" | "
            f"{tarea.descripcion}"
        )