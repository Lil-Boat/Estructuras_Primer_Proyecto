
from getpass import getpass
from cli.validaciones import leer_entero, leer_no_vacio, leer_opcion


def login(motor):
    """Solicita ID y contraseña oculta hasta autenticar correctamente al usuario."""
    while True:
        print("\n=== INICIO DE SESIÓN ===")
        try:
            id_usuario = leer_entero("ID de usuario: ", 1)
            contrasena = getpass("Contraseña: ")
            usuario = motor.autenticar(id_usuario, contrasena)
            print(f"Bienvenido/a, {usuario.nombre} ({usuario.rol})")
            return usuario
        except ValueError as e:
            print(f"Error: {e}")


def menu_principal(motor, persistencia):
    """Redirige al menú correspondiente según el rol del usuario autenticado."""
    usuario = login(motor)

    if usuario.rol == "ADMIN":
        menu_admin(motor, persistencia, usuario)
    else:
        menu_usuario(motor, persistencia, usuario)


def menu_admin(motor, persistencia, usuario):
    """Muestra las opciones exclusivas del administrador y controla sus errores."""
    while True:
        print("\n=== MENÚ ADMINISTRADOR ===")
        print("1. Gestión de usuarios")
        print("2. Gestión de tareas")
        print("3. Ejecutar siguiente tarea")
        print("4. Deshacer")
        print("5. Rehacer")
        print("6. Reportes")
        print("0. Guardar y salir")

        op = leer_opcion("Opción: ", {"0","1","2","3","4","5","6"})

        try:
            if op == "1":
                submenu_usuarios(motor, persistencia, usuario)
            elif op == "2":
                submenu_tareas(motor, persistencia, usuario)
            elif op == "3":
                t = motor.ejecutar_siguiente(usuario.id_usuario)
                persistencia.guardar_todo(motor)
                print(f"Ejecutada: [{t.id_tarea}] {t.descripcion}")
            elif op == "4":
                print("Deshecho:", motor.deshacer(usuario.id_usuario))
                persistencia.guardar_todo(motor)
            elif op == "5":
                print("Rehecho:", motor.rehacer(usuario.id_usuario))
                persistencia.guardar_todo(motor)
            elif op == "6":
                mostrar_reportes(motor)
            elif op == "0":
                persistencia.guardar_todo(motor)
                print("Datos guardados.")
                break
        except (ValueError, IndexError, PermissionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error controlado: {e}")


def submenu_usuarios(motor, persistencia, actor):
    """Permite al administrador agregar, actualizar, eliminar, listar y buscar usuarios."""
    while True:
        print("\n--- GESTIÓN DE USUARIOS ---")
        print("1. Agregar")
        print("2. Actualizar")
        print("3. Eliminar")
        print("4. Listar")
        print("5. Buscar por ID")
        print("0. Volver")

        op = leer_opcion("Opción: ", {"0","1","2","3","4","5"})
        try:
            if op == "1":
                uid = leer_entero("ID: ", 1)
                nombre = leer_no_vacio("Nombre: ")
                clave = getpass("Contraseña: ")
                rol = leer_opcion("Rol (ADMIN/USUARIO): ", {"ADMIN","USUARIO"})
                motor.agregar_usuario(uid, nombre, clave, rol, actor.id_usuario)
                persistencia.guardar_todo(motor)
                print("Usuario agregado.")
            elif op == "2":
                uid = leer_entero("ID a actualizar: ", 1)
                nombre = input("Nuevo nombre (Enter = mantener): ").strip() or None
                cambiar_clave = leer_opcion("¿Cambiar contraseña? (S/N): ", {"S","N"})
                clave = getpass("Nueva contraseña: ") if cambiar_clave == "S" else None
                rol_txt = input("Nuevo rol ADMIN/USUARIO (Enter = mantener): ").strip().upper()
                rol = rol_txt or None
                motor.actualizar_usuario(uid, actor.id_usuario, nombre, clave, rol)
                persistencia.guardar_todo(motor)
                print("Usuario actualizado.")
            elif op == "3":
                uid = leer_entero("ID a eliminar: ", 1)
                motor.eliminar_usuario(uid, actor.id_usuario)
                persistencia.guardar_todo(motor)
                print("Usuario eliminado.")
            elif op == "4":
                for u in motor.usuarios.listar():
                    print(f"{u.id_usuario} | {u.nombre} | {u.rol}")
            elif op == "5":
                uid = leer_entero("ID: ", 1)
                u = motor.usuarios.buscar(uid)
                print(f"{u.id_usuario} | {u.nombre} | {u.rol}" if u else "Usuario no encontrado.")
            elif op == "0":
                break
        except (ValueError, PermissionError) as e:
            print(f"Error: {e}")


def submenu_tareas(motor, persistencia, actor):
    """Permite al administrador gestionar tareas y subtareas desde consola."""
    while True:
        print("\n--- GESTIÓN DE TAREAS ---")
        print("1. Agregar tarea")
        print("2. Actualizar tarea")
        print("3. Cancelar tarea")
        print("4. Eliminar tarea raíz")
        print("5. Listar pendientes")
        print("6. Buscar por ID")
        print("7. Agregar subtarea")
        print("0. Volver")

        op = leer_opcion("Opción: ", {"0","1","2","3","4","5","6","7"})
        try:
            if op == "1":
                tid = leer_entero("ID tarea: ", 1)
                prioridad = leer_opcion("Prioridad (BAJA/MEDIA/ALTA): ", {"BAJA","MEDIA","ALTA"})
                responsable = leer_entero("ID responsable: ", 1)
                desc = leer_no_vacio("Descripción: ")
                motor.crear_tarea(tid, prioridad, responsable, desc, actor.id_usuario)
                persistencia.guardar_todo(motor)
                print("Tarea creada.")
            elif op == "2":
                tid = leer_entero("ID tarea: ", 1)
                desc = input("Nueva descripción (Enter = mantener): ").strip() or None
                prioridad_txt = input("Nueva prioridad BAJA/MEDIA/ALTA (Enter = mantener): ").strip().upper()
                prioridad = prioridad_txt or None
                resp_txt = input("Nuevo responsable ID (Enter = mantener): ").strip()
                responsable = int(resp_txt) if resp_txt else None
                motor.actualizar_tarea(tid, actor.id_usuario, desc, prioridad, responsable)
                persistencia.guardar_todo(motor)
                print("Tarea actualizada.")
            elif op == "3":
                tid = leer_entero("ID tarea: ", 1)
                motor.cancelar_tarea(tid, actor.id_usuario)
                persistencia.guardar_todo(motor)
                print("Tarea cancelada.")
            elif op == "4":
                tid = leer_entero("ID tarea raíz: ", 1)
                motor.eliminar_tarea(tid, actor.id_usuario)
                persistencia.guardar_todo(motor)
                print("Tarea eliminada.")
            elif op == "5":
                for t in motor.listar_pendientes():
                    print(f"{t.id_tarea} | {t.prioridad} | Responsable {t.id_usuario} | {t.descripcion}")
            elif op == "6":
                tid = leer_entero("ID tarea: ", 1)
                t = motor.buscar_tarea(tid)
                if t:
                    print(f"{t.id_tarea} | {t.prioridad} | {t.estado} | Resp: {t.id_usuario} | {t.descripcion}")
                else:
                    print("Tarea no encontrada.")
            elif op == "7":
                sid = leer_entero("ID subtarea: ", 1)
                pid = leer_entero("ID tarea padre: ", 1)
                desc = leer_no_vacio("Descripción: ")
                prioridad = leer_opcion("Prioridad (BAJA/MEDIA/ALTA): ", {"BAJA","MEDIA","ALTA"})
                responsable = leer_entero("ID responsable: ", 1)
                motor.agregar_subtarea(sid, pid, desc, actor.id_usuario, prioridad, responsable)
                persistencia.guardar_todo(motor)
                print("Subtarea agregada.")
            elif op == "0":
                break
        except ValueError as e:
            print(f"Error: {e}")
        except PermissionError as e:
            print(f"Permiso denegado: {e}")


def menu_usuario(motor, persistencia, usuario):
    """Ofrece al usuario normal solo las acciones permitidas por su rol."""
    while True:
        print("\n=== MENÚ USUARIO ===")
        print("1. Ver lista general de tareas")
        print("2. Ver mis tareas")
        print("3. Cambiar estado de una tarea asignada")
        print("0. Salir")

        op = leer_opcion("Opción: ", {"0","1","2","3"})
        try:
            if op == "1":
                for t in motor.reporte_tareas("id", "merge"):
                    print(f"{t.id_tarea} | {t.prioridad} | {t.estado} | Resp: {t.id_usuario} | {t.descripcion}")
            elif op == "2":
                for t in motor.listar_tareas_usuario(usuario.id_usuario):
                    print(f"{t.id_tarea} | {t.prioridad} | {t.estado} | {t.descripcion}")
            elif op == "3":
                tid = leer_entero("ID tarea: ", 1)
                estado = leer_opcion("Estado (PENDIENTE/COMPLETADA): ", {"PENDIENTE","COMPLETADA"})
                motor.cambiar_estado_tarea(tid, estado, usuario.id_usuario)
                persistencia.guardar_todo(motor)
                print("Estado actualizado.")
            elif op == "0":
                break
        except (ValueError, PermissionError) as e:
            print(f"Error: {e}")


def mostrar_reportes(motor):
    """Solicita criterio y algoritmo para mostrar un reporte ordenado de tareas."""
    criterio = leer_opcion(
        "Criterio (ID/PRIORIDAD/DESCRIPCION/ESTADO/RESPONSABLE): ",
        {"ID","PRIORIDAD","DESCRIPCION","ESTADO","RESPONSABLE"}
    ).lower()
    algoritmo = leer_opcion(
        "Algoritmo (BURBUJA/MERGE/QUICK): ",
        {"BURBUJA","MERGE","QUICK"}
    ).lower()
    for t in motor.reporte_tareas(criterio, algoritmo):
        print(f"{t.id_tarea} | {t.prioridad} | {t.estado} | Resp: {t.id_usuario} | {t.descripcion}")
