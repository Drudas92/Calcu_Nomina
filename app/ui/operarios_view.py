import customtkinter as ctk


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
        text="Registra un nuevo operario a continuación.",
        font=("Arial", 16)
    )
    subtitulo.pack(pady=(0, 20))

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
        entry = ctk.CTkEntry(
            form_frame,
            width=380
        )
        label.pack(anchor="w", pady=(10, 5))
        entry.pack(fill="x")
        return entry

    entry_nombre = crear_campo("Nombre")
    entry_documento = crear_campo("Documento")
    entry_cargo = crear_campo("Cargo")

    mensaje_guardado = ctk.CTkLabel(
        contenido,
        text="",
        font=("Arial", 13),
        text_color="#28a745"
    )
    mensaje_guardado.pack(pady=(10, 0))

    def guardar_operario():
        nombre = entry_nombre.get().strip()
        documento = entry_documento.get().strip()
        cargo = entry_cargo.get().strip()

        if not nombre or not documento or not cargo:
            mensaje_guardado.configure(
                text="Por favor completa todos los campos.",
                text_color="#d9534f"
            )
            return

        mensaje_guardado.configure(
            text=f"Operario guardado: {nombre} ({cargo})",
            text_color="#28a745"
        )
        entry_nombre.delete(0, "end")
        entry_documento.delete(0, "end")
        entry_cargo.delete(0, "end")

    boton_guardar = ctk.CTkButton(
        contenido,
        text="Guardar",
        width=120,
        command=guardar_operario
    )
    boton_guardar.pack(pady=20)
