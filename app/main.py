import customtkinter as ctk

from app.ui.home_view import crear_home
from app.database.database import crear_tablas

crear_tablas()

# Crear ventana principal
app = ctk.CTk()
app.title("Calcu_Nomina")
app.geometry("1000x700")

# Crear pantalla principal
crear_home(app)

# Ejecutar aplicación
app.mainloop()