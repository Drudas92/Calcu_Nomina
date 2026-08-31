from app.database.database import conectar


def guardar_operario(nombre, documento, cargo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO operarios(nombre, documento, cargo)
        VALUES(?,?,?)
    """, (nombre, documento, cargo))

    conn.commit()
    conn.close()


def obtener_operarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, documento, cargo
        FROM operarios
        ORDER BY id
    """)

    operarios = cursor.fetchall()

    conn.close()

    return operarios