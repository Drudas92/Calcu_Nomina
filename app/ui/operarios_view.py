import customtkinter as ctk
from tkinter import ttk
from app.services.operarios_service import guardar_operario, obtener_operarios


def crear_operarios(contenido):

    for widget in contenido.winfo_children():
        widget.destroy()

    titulo = ctk.CTkLabel(
        contenido,
        text="Gestión de Operarios",
        font=("Arial", 28, "bold")
    )
    titulo.pack(pady=(20, 10))

    subtitulo = ctk.CTkLabel(
        contenido,
        text="Registra y consulta los operarios.",
        font=("Arial", 16)
    )
    subtitulo.pack(pady=(0, 20))

    # ==========================
    # FORMULARIO
    # ==========================

    form_frame = ctk.CTkFrame(
        contenido,
        fg_color="transparent"
    )
    form_frame.pack(padx=40, pady=10, fill="x")

    def crear_campo(label_text):
        label = ctk.CTkLabel(
            form_frame,
            text=label_text,
            font=("Arial", 14)
        )
        label.pack(anchor="w", pady=(10, 5))

        entry = ctk.CTkEntry(
            form_frame,
            width=380
        )
        entry.pack(fill="x")

        return entry

    entry_nombre = crear_campo("Nombre")
    entry_documento = crear_campo("Documento")
    entry_cargo = crear_campo("Cargo")

    mensaje_guardado = ctk.CTkLabel(
        contenido,
        text="",
        font=("Arial", 13)
    )
    mensaje_guardado.pack(pady=(10, 0))

    # ==========================
    # TABLA
    # ==========================

    tabla_frame = ctk.CTkFrame(contenido)
    tabla_frame.pack(
        padx=40,
        pady=20,
        fill="both",
        expand=True
    )

    columnas = (
        "id",
        "nombre",
        "documento",
        "cargo"
    )

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings"
    )

    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("documento", text="Documento")
    tabla.heading("cargo", text="Cargo")

    tabla.column("id", width=50)
    tabla.column("nombre", width=200)
    tabla.column("documento", width=150)
    tabla.column("cargo", width=150)

    tabla.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ==========================
    # CARGAR OPERARIOS
    # ==========================

    def cargar_operarios():
        for fila in tabla.get_children():
            tabla.delete(fila)

        operarios = obtener_operarios()

        for operario in operarios:
            tabla.insert(
                "",
                "end",
                values=operario
            )

    # ==========================
    # GUARDAR OPERARIO
    # ==========================

    def guardar_operario_click():
        nombre = entry_nombre.get().strip()
        documento = entry_documento.get().strip()
        cargo = entry_cargo.get().strip()

        if not nombre or not documento or not cargo:
            mensaje_guardado.configure(
                text="Por favor completa todos los campos.",
                text_color="#d9534f"
            )
            return

        try:
            guardado, mensaje = guardar_operario(
                nombre,
                documento,
                cargo
            )

            if guardado:
                mensaje_guardado.configure(
                    text=f"Operario guardado: {nombre} ({cargo})",
                    text_color="#28a745"
                )

                entry_nombre.delete(0, "end")
                entry_documento.delete(0, "end")
                entry_cargo.delete(0, "end")

                cargar_operarios()

            else:
                mensaje_guardado.configure(
                    text=mensaje,
                    text_color="#d9534f"
                )

        except Exception as e:
            mensaje_guardado.configure(
                text=f"Error al guardar: {e}",
                text_color="#d9534f"
            )

    boton_guardar = ctk.CTkButton(
        contenido,
        text="Guardar",
        width=120,
        command=guardar_operario_click
    )
    boton_guardar.pack(pady=10)

    # Carga la lista inicial de registros al abrir la pantalla
    cargar_operarios()