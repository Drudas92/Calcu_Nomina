import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "nomina.db")


def conectar():
    return sqlite3.connect(DB_PATH)


def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS operarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        documento TEXT UNIQUE NOT NULL,
        cargo TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()