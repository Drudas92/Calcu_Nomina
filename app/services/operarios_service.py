import sqlite3
from app.database.database import conectar


def guardar_operario(nombre, documento, cargo):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO operarios(nombre, documento, cargo)
            VALUES(?,?,?)
        """, (nombre, documento, cargo))

        conn.commit()
        return True, "Operario guardado correctamente."

    except sqlite3.IntegrityError:
        conn.rollback()
        return False, "Ya existe un operario con ese número de documento."

    except Exception as e:
        conn.rollback()
        return False, f"Error en la base de datos: {e}"

    finally:
        conn.close()


def obtener_operarios():
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, nombre, documento, cargo
            FROM operarios
            ORDER BY id
        """)
        operarios = cursor.fetchall()
        return operarios
    except Exception as e:
        print(f"Error al obtener operarios: {e}")
        return []
    finally:
        conn.close()