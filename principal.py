import sqlite3
import re
import conectar as conectar

def validar_dni(dni):
    """
    Valida un DNI español (8 números y una letra de control correcta).
    """
    dni = dni.strip().upper()
    if not re.match(r'^\d{8}[A-Z]$', dni):
        return False
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    numero = int(dni[:-1])
    letra_correcta = letras[numero % 23]
    return dni[-1] == letra_correcta


def validar_cif(cif):
    """
    Valida un CIF español básico (letra inicial + 7 números + carácter final).
    """
    cif = cif.strip().upper()
    if not re.match(r'^[ABCDEFGHJKLMNPQRSUVW]\d{7}[0-9A-J]$', cif):
        return False
    return True


def validar_email(email):
    """
    Valida un correo electrónico básico.
    """
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def actualizar_cliente():
    con, cur = conectar.conectar()
    if con is None:
        return
    try:
        print("\nClientes disponibles:")
        cur.execute("SELECT DNI_CIF, NOMBRE FROM CLIENTE")
        for dni, nombre in cur.fetchall():
            print(f"- {dni}: {nombre}")

        dni = input("\nIntroduce el DNI/CIF del cliente: ").strip().upper()

        if not (validar_dni(dni) or validar_cif(dni)):
            print("DNI/CIF no válido. Operación cancelada.")
            return

        nuevo_nombre = input("Nuevo nombre (dejar vacío si no cambia): ")
        nuevo_telefono = input("Nuevo teléfono (dejar vacío si no cambia): ")
        nuevo_email = input("Nuevo email (dejar vacío si no cambia): ")

        if nuevo_email and not validar_email(nuevo_email):
            print("Correo electrónico no válido.")
            return

        campos = []
        valores = []

        if nuevo_nombre:
            campos.append("NOMBRE = ?")
            valores.append(nuevo_nombre)
        if nuevo_telefono:
            campos.append("TELEFONO = ?")
            valores.append(nuevo_telefono)
        if nuevo_email:
            campos.append("EMAIL = ?")
            valores.append(nuevo_email)

        if not campos:
            print("No se proporcionaron campos a actualizar.")
            return

        consulta = f"UPDATE CLIENTE SET {', '.join(campos)} WHERE DNI_CIF = ?"
        valores.append(dni)
        cur.execute(consulta, valores)
        con.commit()

        if cur.rowcount > 0:
            print("Cliente actualizado correctamente.")
        else:
            print("No se encontró el cliente.")
    except sqlite3.Error as e:
        print(f"Error al actualizar cliente: {e}")
        con.rollback()
    finally:
        con.close()


def actualizar_empleado():
    con, cur = conectar.conectar()
    if con is None:
        return
    try:
        print("\nEmpleados disponibles:")
        cur.execute("SELECT DNI_CIF, NOMBRE, PUESTO FROM EMPLEADOS")
        for dni, nombre, puesto in cur.fetchall():
            print(f"- {dni}: {nombre} ({puesto})")

        dni = input("\nIntroduce el DNI del empleado: ").strip().upper()
        if not validar_dni(dni):
            print("DNI no válido. Operación cancelada.")
            return

        nuevo_puesto = input("Nuevo puesto del empleado: ")
        cur.execute("UPDATE EMPLEADOS SET PUESTO = ? WHERE DNI_CIF = ?", (nuevo_puesto, dni))
        con.commit()
        if cur.rowcount > 0:
            print("Puesto actualizado correctamente.")
        else:
            print("No se encontró el empleado.")
    except sqlite3.Error as e:
        print(f"Error al actualizar empleado: {e}")
        con.rollback()
    finally:
        con.close()


def actualizar_presupuesto():
    con, cur = conectar.conectar()
    if con is None:
        return
    try:
        print("\nProyectos disponibles:")
        cur.execute("SELECT ID, TITULO_PROYECTO, PRESUPUESTO FROM PROYECTOS")
        for idp, titulo, pres in cur.fetchall():
            print(f"- ID {idp}: {titulo} (Presupuesto actual: {pres})")

        id_proyecto = input("\nIntroduce el ID del proyecto: ")
        if not id_proyecto.isdigit():
            print("El ID debe ser un número entero.")
            return

        nuevo_presupuesto = input("Nuevo presupuesto: ")
        if not nuevo_presupuesto.replace('.', '', 1).isdigit():
            print("Presupuesto no válido (debe ser numérico).")
            return

        cur.execute("UPDATE PROYECTOS SET PRESUPUESTO = ? WHERE ID = ?", (nuevo_presupuesto, id_proyecto))
        con.commit()
        if cur.rowcount > 0:
            print("Presupuesto actualizado correctamente.")
        else:
            print("No se encontró el proyecto.")
    except sqlite3.Error as e:
        print(f"Error al actualizar presupuesto: {e}")
        con.rollback()
    finally:
        con.close()

def consultar_proyectos_cliente():
    con, cur = conectar.conectar()
    if con is None:
        return
    try:
        print("\nClientes disponibles:")
        cur.execute("SELECT DNI_CIF, NOMBRE FROM CLIENTE")
        for dni, nombre in cur.fetchall():
            print(f"- {dni}: {nombre}")

        dni = input("\nIntroduce el DNI/CIF del cliente: ").strip().upper()

        cur.execute("""
            SELECT ID, TITULO_PROYECTO, FECHA_INICIO, FECHA_FIN, PRESUPUESTO
            FROM PROYECTOS WHERE ID_CLIENTE = ?
        """, (dni,))
        resultados = cur.fetchall()
        if resultados:
            print("\nProyectos del cliente:")
            for r in resultados:
                print(f"ID: {r[0]} | {r[1]} | Inicio: {r[2]} | Fin: {r[3]} | Presupuesto: {r[4]}")
        else:
            print("No hay proyectos para este cliente.")
    except sqlite3.Error as e:
        print(f"Error al consultar proyectos del cliente: {e}")
    finally:
        con.close()


def consultar_empleados_proyecto():
    con, cur = conectar.conectar()
    if con is None:
        return
    try:
        print("\nProyectos disponibles:")
        cur.execute("SELECT ID, TITULO_PROYECTO FROM PROYECTOS")
        for idp, titulo in cur.fetchall():
            print(f"- ID {idp}: {titulo}")

        id_proyecto = input("\nIntroduce el ID del proyecto: ")
        cur.execute("""
            SELECT E.NOMBRE, E.PUESTO, E.EMAIL
            FROM EMPLEADOS E
            JOIN EMPLEADOS_PROYECTOS EP ON E.DNI_CIF = EP.DNI_CIF_EMPLEADO
            WHERE EP.ID_PROYECTO = ?
        """, (id_proyecto,))
        empleados = cur.fetchall()
        if empleados:
            print("\nEmpleados asignados al proyecto:")
            for e in empleados:
                print(f"- {e[0]} ({e[1]}) | {e[2]}")
        else:
            print("No hay empleados asignados a este proyecto.")
    except sqlite3.Error as e:
        print(f"Error al consultar empleados del proyecto: {e}")
    finally:
        con.close()


def consultar_proyectos_empleado():
    con, cur = conectar.conectar()
    if con is None:
        return
    try:
        print("\nEmpleados disponibles:")
        cur.execute("SELECT DNI_CIF, NOMBRE, PUESTO FROM EMPLEADOS")
        for dni, nombre, puesto in cur.fetchall():
            print(f"- {dni}: {nombre} ({puesto})")

        dni = input("\nIntroduce el DNI del empleado: ").strip().upper()
        if not validar_dni(dni):
            print("DNI no válido.")
            return

        cur.execute("""
            SELECT P.ID, P.TITULO_PROYECTO, P.FECHA_INICIO, P.FECHA_FIN
            FROM PROYECTOS P
            JOIN EMPLEADOS_PROYECTOS EP ON P.ID = EP.ID_PROYECTO
            WHERE EP.DNI_CIF_EMPLEADO = ?
        """, (dni,))
        proyectos = cur.fetchall()
        if proyectos:
            print("\nProyectos en los que ha trabajado el empleado:")
            for p in proyectos:
                print(f"- {p[1]} (Inicio: {p[2]} - Fin: {p[3]})")
        else:
            print("Este empleado no ha trabajado en ningún proyecto.")
    except sqlite3.Error as e:
        print(f"Error al consultar proyectos del empleado: {e}")
    finally:
        con.close()

def eliminar_empleado_proyecto():
    con, cur = conectar.conectar()
    if con is None:
        return
    try:
        print("\nEmpleados disponibles:")
        cur.execute("SELECT DNI_CIF, NOMBRE FROM EMPLEADOS")
        for dni, nombre in cur.fetchall():
            print(f"- {dni}: {nombre}")

        dni = input("\nIntroduce el DNI del empleado: ").strip().upper()
        if not validar_dni(dni):
            print("DNI no válido.")
            return

        print("\nProyectos disponibles:")
        cur.execute("SELECT ID, TITULO_PROYECTO FROM PROYECTOS")
        for idp, titulo in cur.fetchall():
            print(f"- ID {idp}: {titulo}")

        id_proyecto = input("\nIntroduce el ID del proyecto: ")
        cur.execute("""
            DELETE FROM EMPLEADOS_PROYECTOS
            WHERE DNI_CIF_EMPLEADO = ? AND ID_PROYECTO = ?
        """, (dni, id_proyecto))
        con.commit()
        if cur.rowcount > 0:
            print("Relación empleado-proyecto eliminada correctamente.")
        else:
            print("No existe esa relación.")
    except sqlite3.Error as e:
        print(f"Error al eliminar relación: {e}")
        con.rollback()
    finally:
        con.close()

def registrar_empleado():
    # Registramos a un nuevo empleado en la base de datos mediante una transacción START TRANSACTION
    con, cur = conectar.conectar()
    if con is None:
        return
    try:
        dni = input("Introduce el DNI del empleado: ").strip().upper()
        if not validar_dni(dni):
            print("DNI no válido. Operación cancelada.")
            return

        nombre = input("Nombre del empleado: ")
        puesto = input("Puesto del empleado: ")
        email = input("Email del empleado: ")
        if not validar_email(email):
            print("Correo electrónico no válido.")
            return
    except Exception as e:
        print(f"Error al leer dat {e}")
        cur.execute(""" START TRANSACTION
        INSERT INTO EMPLEADOS (DNI_CIF, NOMBRE, PUESTO, EMAIL)
                    VALUES (?, ?, ?, ?)""", (dni, nombre, puesto, email))
def menu():
    while True:
        print("\n=== GESTIÓN DE PROYECTOS ===")
        print("1. Actualizar cliente")
        print("2. Actualizar empleado")
        print("3. Actualizar presupuesto de proyecto")
        print("4. Consultar proyectos de un cliente")
        print("5. Consultar empleados de un proyecto")
        print("6. Consultar proyectos de un empleado")
        print("7. Eliminar empleado de un proyecto")
        print("0. Salir")

        opcion = input("\nElige una opción: ")

        if opcion == "1":
            actualizar_cliente()
        elif opcion == "2":
            actualizar_empleado()
        elif opcion == "3":
            actualizar_presupuesto()
        elif opcion == "4":
            consultar_proyectos_cliente()
        elif opcion == "5":
            consultar_empleados_proyecto()
        elif opcion == "6":
            consultar_proyectos_empleado()
        elif opcion == "7":
            eliminar_empleado_proyecto()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()