# creartablas.py
import sqlite3
import conectar as conectar

def crear_tablas():
    con, cur = conectar.conectar()
    if con is None: 
        return 

    try:
        # Tabla CLIENTE
        cur.execute("""
            CREATE TABLE IF NOT EXISTS CLIENTE (
                DNI_CIF TEXT PRIMARY KEY,
                NOMBRE TEXT NOT NULL,
                TELEFONO TEXT,
                EMAIL TEXT
            )
        """)

        # Tabla EMPLEADOS
        cur.execute("""
            CREATE TABLE IF NOT EXISTS EMPLEADOS (
                DNI_CIF TEXT PRIMARY KEY,
                NOMBRE TEXT NOT NULL,
                PUESTO TEXT,
                EMAIL TEXT
            )
        """)

        # Tabla PROYECTOS
        cur.execute("""
            CREATE TABLE IF NOT EXISTS PROYECTOS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TITULO_PROYECTO TEXT NOT NULL,
                DESCRIPCION TEXT,
                FECHA_INICIO DATE,
                FECHA_FIN DATE,
                PRESUPUESTO REAL,
                ID_CLIENTE TEXT,
                ID_JEFE_PROYECTO TEXT,
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(DNI_CIF),
                FOREIGN KEY (ID_JEFE_PROYECTO) REFERENCES EMPLEADOS(DNI_CIF)
            )
        """)
        
        # Tabla EMPLEADOS_PROYECTOS
        cur.execute("""
            CREATE TABLE IF NOT EXISTS EMPLEADOS_PROYECTOS (
                DNI_CIF_EMPLEADO TEXT,
                ID_PROYECTO INTEGER,
                PRIMARY KEY (DNI_CIF_EMPLEADO, ID_PROYECTO),
                FOREIGN KEY (DNI_CIF_EMPLEADO) REFERENCES EMPLEADOS(DNI_CIF),
                FOREIGN KEY (ID_PROYECTO) REFERENCES PROYECTOS(ID)
            )
        """)
        
        con.commit()
        print("Todas las tablas han sido creadas correctamente")
    except sqlite3.Error as e:
        print(f" Error al crear las tablas: {e}")
    finally:
        if con: con.close()

def insertar_datos():
    con, cur = conectar.conectar()
    if con is None:
        return

    try:
        cur.execute("SELECT COUNT(*) FROM CLIENTE")
        if cur.fetchone()[0] == 0:
            clientes = [
                ('E19329838', 'TechNova Servicios S.L.', '912345678', 'contacto@technova.es'),
                ('H65740417', 'InnovaSoft S.A.', '934567890', 'info@innovasoft.com'),
                ('H10703833', 'ElectroCanarias S.L.', '928765432', 'ventas@electrocanarias.es'),
                ('E17889122', 'DataLink Consulting S.L.', '911234567', 'contacto@datalink.es'),
                ('B79670238', 'Redes Globales S.A.', '932456789', 'soporte@redesglobales.com'),
                ('B74987306', 'LogiTech Systems S.L.', '915678234', 'info@logitechsystems.es'),
                ('B57556367', 'Soluciones Verdes S.L.', '918765321', 'info@solucionesverdes.es'),
                ('H49210420', 'BlueCode Software S.L.', '922345678', 'contact@bluecode.es'),
                ('B35290931', 'MundoDigital S.A.', '935678901', 'ventas@mundodigital.es'),
                ('A24642928', 'CanaryTech Solutions S.L.', '928912345', 'info@canarytech.es')
            ]
            cur.executemany("INSERT INTO CLIENTE VALUES (?, ?, ?, ?)", clientes)
            print("Datos insertados correctamente en la tabla CLIENTE")

        cur.execute("SELECT COUNT(*) FROM EMPLEADOS")
        if cur.fetchone()[0] == 0:
            empleados = [
                ('17520760G', 'Laura Sánchez', 'Jefa de Proyecto', 'laura.sanchez@empresa.local'),
                ('87744401E', 'Carlos Pérez', 'Desarrollador', 'carlos.perez@empresa.local'),
                ('60657870Q', 'Marta Gómez', 'Analista', 'marta.gomez@empresa.local'),
                ('35108908Y', 'Jorge Ruiz', 'Diseñador UX', 'jorge.ruiz@empresa.local'),
                ('58527949X', 'Ana Torres', 'Desarrolladora', 'ana.torres@empresa.local'),
                ('31388313Y', 'David Martín', 'Administrador de Sistemas', 'david.martin@empresa.local'),
                ('13769630J', 'Lucía Hernández', 'Jefa de Proyecto', 'lucia.hernandez@empresa.local'),
                ('26477401P', 'Pablo Díaz', 'Tester QA', 'pablo.diaz@empresa.local'),
                ('74604140Y', 'Sergio Morales', 'Consultor Técnico', 'sergio.morales@empresa.local'),
                ('91121204B', 'Beatriz Navarro', 'Desarrolladora', 'beatriz.navarro@empresa.local')
            ]
            cur.executemany("INSERT INTO EMPLEADOS VALUES (?, ?, ?, ?)", empleados)
            print("Datos insertados correctamente en la tabla EMPLEADOS")

        cur.execute("SELECT COUNT(*) FROM PROYECTOS")
        if cur.fetchone()[0] == 0:
            proyectos = [
                ('Rediseño Web TechNova', 'Actualización completa del portal corporativo.', '2024-01-15', '2024-06-30', 25000.0, 'E19329838', '17520760G'),
                ('Sistema ERP InnovaSoft', 'Implementación de un ERP personalizado.', '2024-03-01', '2024-10-01', 60000.0, 'H65740417', '13769630J'),
                ('Infraestructura Cloud ElectroCanarias', 'Migración de servidores a la nube.', '2024-02-10', '2024-08-15', 45000.0, 'H10703833', '17520760G'),
                ('App Móvil DataLink', 'Desarrollo de app Android/iOS para gestión de clientes.', '2024-04-05', '2024-09-20', 30000.0, 'E17889122', '13769630J'),
                ('Redes Globales IoT', 'Integración de dispositivos IoT para control remoto.', '2024-05-01', '2024-12-10', 52000.0, 'B79670238', '17520760G'),
                ('Sistema Logístico LogiTech', 'Software de gestión de almacenes y rutas.', '2024-07-01', '2025-01-30', 70000.0, 'B74987306', '13769630J'),
                ('Plataforma Verde', 'Portal de sostenibilidad y control energético.', '2024-06-15', '2024-12-31', 38000.0, 'B57556367', '17520760G'),
                ('BlueCode Cloud Service', 'Servicios cloud para clientes europeos.', '2024-08-01', '2025-02-15', 65000.0, 'H49210420', '13769630J'),
                ('MundoDigital CRM', 'CRM corporativo con panel analítico.', '2024-09-01', '2025-03-31', 42000.0, 'B35290931', '17520760G'),
                ('CanaryTech Integraciones', 'Proyectos de integración y soporte 24/7.', '2024-10-01', '2025-04-30', 48000.0, 'A24642928', '13769630J')
            ]
            cur.executemany("""
                INSERT INTO PROYECTOS 
                (TITULO_PROYECTO, DESCRIPCION, FECHA_INICIO, FECHA_FIN, PRESUPUESTO, ID_CLIENTE, ID_JEFE_PROYECTO)
                VALUES (?, ?, ?, ?, ?, ?, ?)""", proyectos)
            print("Datos insertados correctamente en la tabla PROYECTOS")

        cur.execute("SELECT COUNT(*) FROM EMPLEADOS_PROYECTOS")
        if cur.fetchone()[0] == 0:
            relaciones = [
                ('17520760G', 1), ('87744401E', 1), ('35108908Y', 1),
                ('13769630J', 2), ('60657870Q', 2), ('58527949X', 2), ('26477401P', 2),
                ('17520760G', 3), ('31388313Y', 3), ('74604140Y', 3),
                ('13769630J', 4), ('58527949X', 4), ('91121204B', 4),
                ('17520760G', 5), ('87744401E', 5), ('74604140Y', 5),
                ('13769630J', 6), ('31388313Y', 6), ('26477401P', 6),
                ('17520760G', 7), ('60657870Q', 7), ('91121204B', 7),
                ('13769630J', 8), ('58527949X', 8), ('31388313Y', 8),
                ('17520760G', 9), ('87744401E', 9), ('91121204B', 9),
                ('13769630J', 10), ('74604140Y', 10), ('26477401P', 10)
            ]
            cur.executemany("INSERT INTO EMPLEADOS_PROYECTOS VALUES (?, ?)", relaciones)
            print("Datos insertados correctamente en la tabla EMPLEADOS_PROYECTOS")

        con.commit()
        print("Todos los datos han sido insertados correctamente")

    except sqlite3.Error as e:
        print(f"Error al insertar los datos: {e}")
        con.rollback()
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    crear_tablas()
    insertar_datos()