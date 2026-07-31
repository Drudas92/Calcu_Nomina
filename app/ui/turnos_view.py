import customtkinter as ctk


def crear_turnos(contenido):
    for widget in contenido.winfo_children():
        widget.destroy()

    titulo = ctk.CTkLabel(
        contenido,
        text="Gestión de Turnos",
        font=("Arial", 28, "bold")
    )
    titulo.pack(pady=30)

    subtitulo = ctk.CTkLabel(
        contenido,
        text="Aquí se administrarán los turnos de los operarios.",
        font=("Arial", 16)
    )
    subtitulo.pack()