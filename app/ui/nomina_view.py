import customtkinter as ctk


def crear_nomina(contenido):
    for widget in contenido.winfo_children():
        widget.destroy()

    titulo = ctk.CTkLabel(
        contenido,
        text="Gestión de Nómina",
        font=("Arial", 28, "bold")
    )
    titulo.pack(pady=30)

    subtitulo = ctk.CTkLabel(
        contenido,
        text="Aquí se calculará y administrará la nómina.",
        font=("Arial", 16)
    )
    subtitulo.pack()
