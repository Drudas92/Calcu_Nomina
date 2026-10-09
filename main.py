import json
import os
import customtkinter as ctk

# Configuración del tema de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

CONFIG_PATH = "config_usuario.json"

CONFIG_DEFAULT = {
    "nombre_empleado": "Diego Alejandro Rudas",
    "salario_base": 2100000,
    "horas_mes": 210,
    "bono_asistencia": 50000,
    "auxilio_transporte_quincenal": 124548,
    "descuentos_personales": {
        "credito_denario": 172694,
        "otros_descuentos": 0,
    },
    "factores_recargo": {
        "recargo_nocturno": 0.35,
        "dom_diurno_nohabitual": 0.90,
        "dom_diurno_habitual": 1.90,
        "dom_nocturno_nohabitual": 1.25,
        "dom_nocturno_habitual": 2.25,
    },
}


def cargar_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(CONFIG_DEFAULT, f, indent=4, ensure_ascii=False)
        return CONFIG_DEFAULT
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class AppCalculadora(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Calculadora de Nómina - Insight / BUK")
        self.geometry("850x600")

        self.config_data = cargar_config()
        self.valor_hora = (
            self.config_data["salario_base"] / self.config_data["horas_mes"]
        )

        self.crear_interfaz()

    def crear_interfaz(self):
        # Header
        lbl_titulo = ctk.CTkLabel(
            self,
            text=f"¡Hola, {self.config_data['nombre_empleado']}!",
            font=("Arial", 22, "bold"),
        )
        lbl_titulo.pack(pady=(15, 2))

        lbl_sub = ctk.CTkLabel(
            self,
            text=f"Sueldo Base: ${self.config_data['salario_base']:,} | Valor Hora Ordinaria: ${self.valor_hora:,.2f}",
            font=("Arial", 12),
            text_color="gray",
        )
        lbl_sub.pack(pady=(0, 15))

        # Contenedor Principal
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # --- PANEL IZQUIERDO: FORMULARIO ---
        frame_left = ctk.CTkFrame(grid_frame)
        frame_left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(
            frame_left, text="Horas y Datos de la Quincena", font=("Arial", 15, "bold")
        ).pack(pady=10)

        # Días trabajados
        f_dias = ctk.CTkFrame(frame_left, fg_color="transparent")
        f_dias.pack(fill="x", padx=15, pady=4)
        ctk.CTkLabel(f_dias, text="Días trabajados:").pack(side="left")
        self.txt_dias = ctk.CTkEntry(f_dias, width=70)
        self.txt_dias.insert(0, "15")
        self.txt_dias.pack(side="right")

        # Entradas de recargos
        self.entries_recargos = {}
        recargos_labels = [
            ("recargo_nocturno", "Recargo Nocturno (0.35)"),
            ("dom_diurno_nohabitual", "Dom/Fest Diurno No Hab. (0.90)"),
            ("dom_diurno_habitual", "Dom/Fest Diurno Hab. (1.90)"),
            ("dom_nocturno_nohabitual", "Dom/Fest Noct. No Hab. (1.25)"),
            ("dom_nocturno_habitual", "Dom/Fest Noct. Hab. (2.25)"),
        ]

        for clave, texto in recargos_labels:
            f_row = ctk.CTkFrame(frame_left, fg_color="transparent")
            f_row.pack(fill="x", padx=15, pady=3)
            ctk.CTkLabel(f_row, text=texto, font=("Arial", 12)).pack(
                side="left"
            )
            ent = ctk.CTkEntry(f_row, width=70)
            ent.insert(0, "0")
            ent.pack(side="right")
            self.entries_recargos[clave] = ent

        # Checkbox Bono
        self.var_bono = ctk.BooleanVar(value=True)
        chk_bono = ctk.CTkCheckBox(
            frame_left,
            text=f"Aplica Bono Asistencia (${self.config_data['bono_asistencia']:,})",
            variable=self.var_bono,
        )
        chk_bono.pack(pady=12)

        # Botón Calcular
        btn_calc = ctk.CTkButton(
            frame_left,
            text="CALCULAR NÓMINA",
            font=("Arial", 13, "bold"),
            fg_color="#1F4E79",
            hover_color="#153654",
            command=self.calcular_nomina,
        )
        btn_calc.pack(fill="x", padx=15, pady=10)

        # --- PANEL DERECHO: RESULTADOS ---
        frame_right = ctk.CTkFrame(grid_frame)
        frame_right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(
            frame_right, text="Resumen de Liquidación", font=("Arial", 15, "bold")
        ).pack(pady=10)

        self.txt_res = ctk.CTkTextbox(
            frame_right, font=("Consolas", 12), activate_scrollbars=True
        )
        self.txt_res.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.calcular_nomina()

    def calcular_nomina(self):
        try:
            dias = int(self.txt_dias.get())

            sueldo_quincena = (
                self.config_data["salario_base"] / 30
            ) * dias

            total_recargos = 0
            for clave, ent in self.entries_recargos.items():
                horas = float(ent.get().replace(",", "."))
                factor = self.config_data["factores_recargo"].get(clave, 0)
                total_recargos += horas * self.valor_hora * factor

            bono = (
                self.config_data["bono_asistencia"] if self.var_bono.get() else 0
            )

            ibc = sueldo_quincena + bono + total_recargos

            salud = ibc * 0.04
            pension = ibc * 0.04
            descuentos_ley = salud + pension

            descuentos_personales = sum(
                self.config_data["descuentos_personales"].values()
            )

            aux_trans = (
                self.config_data["auxilio_transporte_quincenal"]
                if dias >= 15
                else (self.config_data["auxilio_transporte_quincenal"] / 15)
                * dias
            )

            total_devengado = ibc + aux_trans
            total_descuentos = descuentos_ley + descuentos_personales
            neto_pagar = total_devengado - total_descuentos

            res_text = f"DEVENGOS PRESTACIONALES\n"
            res_text += f" Salario ({dias} días):  ${sueldo_quincena:>10,.0f}\n"
            res_text += f" Bono Asistencia:   ${bono:>10,.0f}\n"
            res_text += f" Total Recargos:    ${total_recargos:>10,.0f}\n"
            res_text += f"---------------------------------\n"
            res_text += f" IBC PILA (Base):   ${ibc:>10,.0f}\n\n"
            res_text += f"DEVENGOS NO PRESTACIONALES\n"
            res_text += f" Aux. Transporte:   ${aux_trans:>10,.0f}\n"
            res_text += f" TOTAL DEVENGADO:   ${total_devengado:>10,.0f}\n"
            res_text += f"=================================\n"
            res_text += f"DESCUENTOS DE LEY Y OTROS\n"
            res_text += f" Salud (4%):        ${salud:>10,.0f}\n"
            res_text += f" Pensión (4%):      ${pension:>10,.0f}\n"
            res_text += f" Crédito Denario:   ${descuentos_personales:>10,.0f}\n"
            res_text += f" TOTAL DESCUENTOS:  ${total_descuentos:>10,.0f}\n"
            res_text += f"=================================\n"
            res_text += f" NETO A RECIBIR:    ${neto_pagar:>10,.0f}\n"

            self.txt_res.configure(state="normal")
            self.txt_res.delete("1.0", "end")
            self.txt_res.insert("1.0", res_text)
            self.txt_res.configure(state="disabled")

        except ValueError:
            self.txt_res.configure(state="normal")
            self.txt_res.delete("1.0", "end")
            self.txt_res.insert("1.0", "Error: Ingrese números válidos.")
            self.txt_res.configure(state="disabled")


if __name__ == "__main__":
    app = AppCalculadora()
    app.mainloop()