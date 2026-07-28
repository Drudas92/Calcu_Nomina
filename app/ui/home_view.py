import customtkinter as ctk


def crear_home(app):
    # Título
    titulo = ctk.CTkLabel(
        app,
        text="Calcu_Nomina",
        font=("Arial", 28, "bold")
    )
    titulo.pack(pady=30)

    # Subtítulo
    subtitulo = ctk.CTkLabel(
        app,
        text="Sistema de Gestión y Validación de Nómina",
        font=("Arial", 16)
    )
    subtitulo.pack()