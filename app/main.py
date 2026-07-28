import customtkinter as ctk

# Configuración inicial
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Crear ventana principal
app = ctk.CTk()
app.title("Calcu_Nomina")
app.geometry("1000x700")

# Título
titulo = ctk.CTkLabel(
    app,
    text="Calcu_Nomina",
    font=("Arial", 28, "bold")
)
titulo.pack(pady=30)

subtitulo = ctk.CTkLabel(
    app,
    text="Sistema de Gestión y Validación de Nómina",
    font=("Arial", 16)
)
subtitulo.pack()

# Ejecutar aplicación
app.mainloop()