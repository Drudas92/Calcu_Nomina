import customtkinter as ctk

def crear_inicio(contenido):

    titulo = ctk.CTkLabel(
        contenido,
        text="Calcu_Nomina",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=30)

    subtitulo = ctk.CTkLabel(
        contenido,
        text="Sistema de Gestión y Validación de Nómina",
        font=("Arial", 16)
    )

    subtitulo.pack()

    mensaje = ctk.CTkLabel(
        contenido,
        text="Seleccione una opcion del menú",
        font=("Arial", 15)
    )

    mensaje.pack(pady=30)
