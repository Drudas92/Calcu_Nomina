import customtkinter as ctk


def crear_home(app):

    # Frame principal
    frame_principal = ctk.CTkFrame(app)
    frame_principal.pack(fill="both", expand=True)

    # ==========================
    # Barra lateral
    # ==========================
    sidebar = ctk.CTkFrame(
    frame_principal,
    width=220,
    corner_radius=0,
    fg_color="#1f6aa5"
)

    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    menu = ctk.CTkLabel(
    sidebar,
    text="MENÚ",
    font=("Arial", 22, "bold"),
    text_color="white"
)

    menu.pack(pady=30)

    # ==========================
    # Área principal
    # ==========================
    contenido = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)

    contenido.pack(side="right", fill="both", expand=True)

    # ==========================
    # Título
    # ==========================

    titulo = ctk.CTkLabel(
        contenido,
        text="Calcu_Nomina",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=30)

    subtitulo = ctk.CTkLabel(
        contenido,
        text="Sistema Inteligente de Gestión y Validación de Nómina",
        font=("Arial", 16)
    )

    subtitulo.pack()