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

def registrar_proyecto():
    """
    Registra un nuevo proyecto y asigna a los empleados usando una transacción
    """
    con, cur = conectar.conectar()
    if con is None:
        return
    
    try:
        con.execute("BEGIN TRANSACTION")
        
        print("\n=== REGISTRAR NUEVO PROYECTO ===")
        
        titulo = input("Título del proyecto: ")
        descripcion = input("Descripción del proyecto: ")
        fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
        fecha_fin = input("Fecha de fin (YYYY-MM-DD): ")
        presupuesto = input("Presupuesto: ")
        
        # Validamos que el presupuesto sea un número
        try:
            float(presupuesto)
        except ValueError:
            raise ValueError("El presupuesto debe ser un número")
        
        print("\nClientes disponibles:")
        cur.execute("SELECT DNI_CIF, NOMBRE FROM CLIENTE")
        clientes = cur.fetchall()
        if not clientes:
            raise ValueError("No hay clientes registrados en la base de datos")
        for dni, nombre in clientes:
            print(f"- {dni}: {nombre}")
        
        id_cliente = input("\nDNI/CIF del cliente: ").strip().upper()
        
        # Verificamos que el cliente existe en la base de datos
        cur.execute("SELECT COUNT(*) FROM CLIENTE WHERE DNI_CIF = ?", (id_cliente,))
        if cur.fetchone()[0] == 0:
            raise ValueError("El cliente no existe")
        
        print("\nEmpleados disponibles para jefe de proyecto:")
        cur.execute("SELECT DNI_CIF, NOMBRE, PUESTO FROM EMPLEADOS")
        empleados = cur.fetchall()
        if not empleados:
            raise ValueError("No hay empleados registrados en la base de datos")
        for dni, nombre, puesto in empleados:
            print(f"- {dni}: {nombre} ({puesto})")
        
        id_jefe_proyecto = input("\nDNI del jefe de proyecto (opcional): ").strip().upper()
        if id_jefe_proyecto:
            cur.execute("SELECT COUNT(*) FROM EMPLEADOS WHERE DNI_CIF = ?", (id_jefe_proyecto,))
            if cur.fetchone()[0] == 0:
                raise ValueError("El jefe de proyecto no existe")
        
        # Insertamos el nuevo proyecto en la tabla PROYECTOS
        cur.execute("""
            INSERT INTO PROYECTOS (TITULO_PROYECTO, DESCRIPCION, FECHA_INICIO, FECHA_FIN, PRESUPUESTO, ID_CLIENTE, ID_JEFE_PROYECTO)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (titulo, descripcion, fecha_inicio, fecha_fin, float(presupuesto), id_cliente, id_jefe_proyecto if id_jefe_proyecto else None))
        
        id_proyecto = cur.lastrowid
        
        # Asignamos los empleados al proyecto 
        print("\n=== ASIGNAR EMPLEADOS AL PROYECTO ===")
        while True:
            dni_empleado = input("\nDNI del empleado a asignar (deja este campo vacío para terminar de insertar empleados al proyecto): ").strip().upper()
            if not dni_empleado:
                break
                
            # Verificamos que el empleado exista en la base de datos
            cur.execute("SELECT COUNT(*) FROM EMPLEADOS WHERE DNI_CIF = ?", (dni_empleado,))
            if cur.fetchone()[0] == 0:
                raise ValueError(f"El empleado con DNI {dni_empleado} no existe en la base de datos")
            
            # Insertamos la relación en la tabla de EMPLEADOS_PROYECTOS
            cur.execute("""
                INSERT INTO EMPLEADOS_PROYECTOS (DNI_CIF_EMPLEADO, ID_PROYECTO)
                VALUES (?, ?)
            """, (dni_empleado, id_proyecto))
            
            print(f"Empleado {dni_empleado} asignado al proyecto")
        
        con.commit()
        print("Proyecto registrado correctamente con sus asignaciones de empleados")
        
    except Exception as e:
        con.rollback()
        print(f"Error: {e}. Se ha revertido la operación.")
    finally:
        con.close()


def eliminar_proyecto():
    """
    Elimina un proyecto y sus asignaciones usando transacción
    """
    con, cur = conectar.conectar()
    if con is None:
        return
    
    try:
        con.execute("BEGIN TRANSACTION")
        
        print("\n=== ELIMINAR PROYECTO ===")
        
        print("Proyectos disponibles:")
        cur.execute("SELECT ID, TITULO_PROYECTO FROM PROYECTOS")
        proyectos = cur.fetchall()
        if not proyectos:
            raise ValueError("No hay proyectos registrados en la base de datos")
        for id_proy, titulo in proyectos:
            print(f"- ID {id_proy}: {titulo}")
        
        id_proyecto = input("\nID del proyecto a eliminar: ")
        
        if not id_proyecto.isdigit():
            raise ValueError("El ID del proyecto debe ser un número")
        
        # Verificar que el proyecto existe
        cur.execute("SELECT COUNT(*) FROM PROYECTOS WHERE ID = ?", (id_proyecto,))
        if cur.fetchone()[0] == 0:
            raise ValueError("El proyecto no existe")
        
        # Eliminamos las asignaciones de empleados primero (por la clave foránea)
        cur.execute("DELETE FROM EMPLEADOS_PROYECTOS WHERE ID_PROYECTO = ?", (id_proyecto,))
        
        # Eliminamos el proyecto
        cur.execute("DELETE FROM PROYECTOS WHERE ID = ?", (id_proyecto,))
        
        con.commit()
        print("Proyecto y sus asignaciones eliminados correctamente")
        
    except Exception as e:
        con.rollback()
        print(f"Error: {e}. Se ha revertido la operación.")
    finally:
        con.close()


def transferir_proyecto():
    """
    Transfiere un proyecto a otro cliente usando transacción
    """
    con, cur = conectar.conectar()
    if con is None:
        return
    
    try:
        con.execute("BEGIN TRANSACTION")
        
        print("\n=== TRANSFERIR PROYECTO A OTRO CLIENTE ===")
        
        print("Proyectos disponibles:")
        cur.execute("SELECT ID, TITULO_PROYECTO, ID_CLIENTE FROM PROYECTOS")
        proyectos = cur.fetchall()
        if not proyectos:
            raise ValueError("No hay proyectos registrados en la base de datos")
        for id_proy, titulo, id_cliente in proyectos:
            print(f"- ID {id_proy}: {titulo} (Cliente actual: {id_cliente})")
        
        id_proyecto = input("\nID del proyecto a transferir: ")
        
        if not id_proyecto.isdigit():
            raise ValueError("El ID del proyecto debe ser un número")
        
        # Verificar que el proyecto existe
        cur.execute("SELECT COUNT(*) FROM PROYECTOS WHERE ID = ?", (id_proyecto,))
        if cur.fetchone()[0] == 0:
            raise ValueError("El proyecto no existe")
        
        print("\nClientes disponibles:")
        cur.execute("SELECT DNI_CIF, NOMBRE FROM CLIENTE")
        clientes = cur.fetchall()
        if not clientes:
            raise ValueError("No hay clientes registrados en la base de datos")
        for dni, nombre in clientes:
            print(f"- {dni}: {nombre}")
        
        nuevo_cliente = input("\nDNI/CIF del nuevo cliente: ").strip().upper()
        
        # Verificamos que el nuevo cliente existe
        cur.execute("SELECT COUNT(*) FROM CLIENTE WHERE DNI_CIF = ?", (nuevo_cliente,))
        if cur.fetchone()[0] == 0:
            raise ValueError("El nuevo cliente no existe")
        
        # Actualizamos el proyecto con el nuevo cliente
        cur.execute("UPDATE PROYECTOS SET ID_CLIENTE = ? WHERE ID = ?", (nuevo_cliente, id_proyecto))
        
        con.commit()
        print("Proyecto transferido correctamente al nuevo cliente")
        
    except Exception as e:
        con.rollback()
        print(f"Error: {e}. Se ha revertido la operación.")
    finally:
        con.close()

def registrar_empleado():
    """
    Registra un nuevo empleado en la base de datos usando una transacción
    """
    con, cur = conectar.conectar()
    if con is None:
        return
    
    try:
        con.execute("BEGIN TRANSACTION")
        
        print("\n=== REGISTRAR NUEVO EMPLEADO ===")
        
        # Solicitamos los datos del empleado
        dni = input("DNI del empleado: ").strip().upper()
        
        # Validamos su DNI
        if not validar_dni(dni):
            raise ValueError("DNI no válido")
        
        # Verificamos si el empleado existía anteriormente
        cur.execute("SELECT COUNT(*) FROM EMPLEADOS WHERE DNI_CIF = ?", (dni,))
        if cur.fetchone()[0] > 0:
            raise ValueError("Ya existe un empleado con este DNI")
        
        nombre = input("Nombre completo del empleado: ").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        
        puesto = input("Puesto del empleado: ").strip()
        if not puesto:
            raise ValueError("El puesto no puede estar vacío")
        
        email = input("Email del empleado: ").strip()
        if email and not validar_email(email):
            raise ValueError("Email no válido")
        
        # Insertamos el empleado nuevo en la tabla EMPLEADOS
        cur.execute("""
            INSERT INTO EMPLEADOS (DNI_CIF, NOMBRE, PUESTO, EMAIL)
            VALUES (?, ?, ?, ?)
        """, (dni, nombre, puesto, email if email else None))
        
        con.commit()
        print("Empleado registrado correctamente")
        
    except Exception as e:
        con.rollback()
        print(f"Error: {e}. No se pudo registrar el empleado.")
    finally:
        con.close()

def menu():
    while True:
        print("\n=== GESTIÓN DE PROYECTOS ===")
        print("1. Actualizar cliente")
        print("2. Actualizar empleado")
        print("3. Registrar nuevo empleado")
        print("4. Actualizar presupuesto de proyecto")
        print("5. Consultar proyectos de un cliente")
        print("6. Consultar empleados de un proyecto")
        print("7. Consultar proyectos de un empleado")
        print("8. Eliminar empleado de un proyecto")
        print("9. Registrar nuevo proyecto con empleados")
        print("10. Eliminar proyecto y asignaciones")
        print("11. Transferir proyecto a otro cliente")
        print("0. Salir")

        opcion = input("\nElige una opción: ")

        if opcion == "1":
            actualizar_cliente()
        elif opcion == "2":
            actualizar_empleado()
        elif opcion == "3":
            registrar_empleado()
        elif opcion == "4":
            actualizar_presupuesto()
        elif opcion == "5":
            consultar_proyectos_cliente()
        elif opcion == "6":
            consultar_empleados_proyecto()
        elif opcion == "7":
            consultar_proyectos_empleado()
        elif opcion == "8":
            eliminar_empleado_proyecto()
        elif opcion == "9":
            registrar_proyecto()
        elif opcion == "10":
            eliminar_proyecto()
        elif opcion == "11":
            transferir_proyecto()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opcion no valida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()