import customtkinter as ctk

from ui.inicio_view import crear_inicio
from ui.operarios_view import crear_operarios
from ui.turnos_view import crear_turnos


def crear_home(app):

    def limpiar_contenido():
        for widget in contenido.winfo_children():
            widget.destroy()

    def cambiar_mensaje(texto):
        mensaje.configure(text=texto)

    def mostrar_inicio():
        limpiar_contenido()
        crear_inicio(contenido)

    def mostrar_operarios():
        limpiar_contenido()
        crear_operarios(contenido)

    def mostrar_turnos():
        limpiar_contenido()
        crear_turnos(contenido)

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
    text="CALCU_NÓMINA",
    font=("Arial", 22, "bold"),
    text_color="white"
)

    menu.pack(pady=30)
    boton_inicio = ctk.CTkButton(
    sidebar,
    text="🏠  Inicio",
    width=180,
    command=mostrar_inicio
    )
    boton_inicio.pack(pady=10)

    boton_operarios = ctk.CTkButton(
    sidebar,
    text="👤  Operarios",
    width=180,
    command=mostrar_operarios
)

    boton_operarios.pack(pady=10)

    boton_turnos = ctk.CTkButton(
    sidebar,
    text="📅  Turnos",
    width=180,
    command=mostrar_turnos
)

    boton_turnos.pack(pady=10)

    boton_nomina = ctk.CTkButton(
    sidebar,
    text="💰  Nómina",
    width=180,
    command=lambda: cambiar_mensaje("módulo de nómina")
)

    boton_nomina.pack(pady=10)
    
    # ==========================
    # Área principal
    # ==========================
    contenido = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)

    contenido.pack(side="right", fill="both", expand=True)

    mensaje = crear_inicio(contenido)