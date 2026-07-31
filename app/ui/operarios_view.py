import customtkinter as ctk


def crear_operarios(contenido):

    titulo = ctk.CTkLabel(
        contenido,
        text="Gestión de Operarios",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=30)

    subtitulo = ctk.CTkLabel(
        contenido,
        text="Aquí administraremos los operarios.",
        font=("Arial", 16)
    )

    subtitulo.pack()