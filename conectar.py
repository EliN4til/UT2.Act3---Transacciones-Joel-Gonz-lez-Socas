import sqlite3

def conectar():
    """
    Establece conexión con la base de datos de SQLite "Empresa.db" y activa las claves foraneas, (me estaba dando error, no se porque, a la hora de crear una nueva db).
    
    Devuelve:
        una tupla: (conexión, cursor) o (None, None) en caso de que haya un error de conexión a la base de datos.
    """
    try:
        con = sqlite3.connect("Empresa.db")
        con.execute("PRAGMA foreign_keys = ON;")
        cur = con.cursor()
        print("Conexión establecida correctamente")
        return con, cur
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None, None

if __name__ == "__main__":
    conectar()