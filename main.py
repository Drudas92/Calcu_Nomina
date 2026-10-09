import json
import os
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

CONFIG_PATH = "config_usuario.json"

CONFIG_DEFAULT = {
    "nombre_empleado": "Operador de Monitoreo",
    "cargo": "Operador de Monitoreo",
    "salario_base": 2100000,
    "horas_mes": 210,
    "bono_asistencia": 50000,
    "auxilio_transporte_quincenal": 124548,
    "descuentos_personales": {
        "credito_denario": 172694,
        "otros_descuentos": 0
    },
    "factores_recargo": {
        "recargo_nocturno": 0.35,
        "dom_diurno_nohabitual": 0.90,
        "dom_diurno_habitual": 1.90,
        "dom_nocturno_nohabitual": 1.25,
        "dom_nocturno_habitual": 2.25
    }
}

def cargar_config():
    if not os.path.exists(CONFIG_PATH):
        guardar_config(CONFIG_DEFAULT)
        return CONFIG_DEFAULT
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            datos = json.load(f)
            if "cargo" not in datos:
                datos["cargo"] = "Operador de Monitoreo"
            return datos
    except Exception:
        return CONFIG_DEFAULT

def guardar_config(datos):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

class AppCalculadora(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Nómina y Auditoría - Insight / BUK")
        self.geometry("920x720")

        self.config_data = cargar_config()
        self.valor_hora = self.config_data["salario_base"] / self.config_data["horas_mes"]

        # Encabezado principal
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text=f"¡Hola, {self.config_data['nombre_empleado']}!", 
            font=("Arial", 22, "bold")
        )
        self.lbl_titulo.pack(pady=(12, 2))

        self.lbl_sub = ctk.CTkLabel(
            self, 
            text=f"Cargo: {self.config_data.get('cargo', 'Operador de Monitoreo')} | Sueldo Base: ${self.config_data['salario_base']:,} | Valor Hora: ${self.valor_hora:,.2f}", 
            font=("Arial", 12), 
            text_color="gray"
        )
        self.lbl_sub.pack(pady=(0, 10))

        # Panel de Pestañas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self.tab_calc = self.tabview.add("Mi Cálculo Quincenal")
        self.tab_audit = self.tabview.add("Auditoría vs BUK / Nómina")
        self.tab_perfil = self.tabview.add("Mi Perfil / Configuración")

        self.setup_tab_calculo()
        self.setup_tab_auditoria()
        self.setup_tab_perfil()

    # --- PESTAÑA 1: CÁLCULO QUINCENAL ---
    def setup_tab_calculo(self):
        grid_frame = ctk.CTkFrame(self.tab_calc, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=10, pady=5)

        frame_left = ctk.CTkFrame(grid_frame)
        frame_left.pack(side="left", fill="both", expand=True, padx=(0, 5))

        ctk.CTkLabel(frame_left, text="Horas y Datos de la Quincena", font=("Arial", 14, "bold")).pack(pady=8)

        f_dias = ctk.CTkFrame(frame_left, fg_color="transparent")
        f_dias.pack(fill="x", padx=10, pady=3)
        ctk.CTkLabel(f_dias, text="Días trabajados:").pack(side="left")
        self.txt_dias = ctk.CTkEntry(f_dias, width=70)
        self.txt_dias.insert(0, "15")
        self.txt_dias.pack(side="right")

        self.entries_recargos = {}
        recargos = [
            ("recargo_nocturno", "Recargo Nocturno (0.35)"),
            ("dom_diurno_nohabitual", "Dom/Fest Diurno No Hab. (0.90)"),
            ("dom_diurno_habitual", "Dom/Fest Diurno Hab. (1.90)"),
            ("dom_nocturno_nohabitual", "Dom/Fest Noct. No Hab. (1.25)"),
            ("dom_nocturno_habitual", "Dom/Fest Noct. Hab. (2.25)")
        ]

        for clave, texto in recargos:
            f = ctk.CTkFrame(frame_left, fg_color="transparent")
            f.pack(fill="x", padx=10, pady=3)
            ctk.CTkLabel(f, text=texto, font=("Arial", 11)).pack(side="left")
            ent = ctk.CTkEntry(f, width=70)
            ent.insert(0, "0")
            ent.pack(side="right")
            self.entries_recargos[clave] = ent

        self.var_bono = ctk.BooleanVar(value=True)
        chk_bono = ctk.CTkCheckBox(frame_left, text="Aplica Bono Asistencia ($50,000)", variable=self.var_bono)
        chk_bono.pack(pady=12)

        btn_calc = ctk.CTkButton(frame_left, text="CALCULAR NÓMINA", fg_color="#1F4E79", hover_color="#153654", command=self.calcular_mi_nomina)
        btn_calc.pack(fill="x", padx=10, pady=5)

        frame_right = ctk.CTkFrame(grid_frame)
        frame_right.pack(side="right", fill="both", expand=True, padx=(5, 0))

        ctk.CTkLabel(frame_right, text="Resumen de Liquidación", font=("Arial", 14, "bold")).pack(pady=8)
        self.txt_res = ctk.CTkTextbox(frame_right, font=("Consolas", 11))
        self.txt_res.pack(fill="both", expand=True, padx=8, pady=8)

    def calcular_mi_nomina(self):
        try:
            dias = int(self.txt_dias.get())
            sueldo = (self.config_data["salario_base"] / 30) * dias
            total_recargos = sum(
                float(ent.get().replace(",", ".")) * self.valor_hora * self.config_data["factores_recargo"].get(k, 0)
                for k, ent in self.entries_recargos.items()
            )
            bono = self.config_data["bono_asistencia"] if self.var_bono.get() else 0
            ibc = sueldo + bono + total_recargos
            salud = ibc * 0.04
            pension = ibc * 0.04
            descuentos_personales = sum(self.config_data["descuentos_personales"].values())
            aux_trans = self.config_data["auxilio_transporte_quincenal"] if dias >= 15 else (self.config_data["auxilio_transporte_quincenal"] / 15) * dias
            total_devengado = ibc + aux_trans
            total_descuentos = salud + pension + descuentos_personales
            neto = total_devengado - total_descuentos

            res = "DEVENGOS PRESTACIONALES\n"
            res += f"  Salario ({dias} días):  ${sueldo:>11,.0f}\n"
            res += f"  Bono Asistencia: ${bono:>11,.0f}\n"
            res += f"  Total Recargos:  ${total_recargos:>11,.0f}\n"
            res += f"-----------------------------------------\n"
            res += f"  IBC PILA (Base): ${ibc:>11,.0f}\n\n"
            res += "DEVENGOS NO PRESTACIONALES\n"
            res += f"  Aux. Transporte: ${aux_trans:>11,.0f}\n"
            res += f"  TOTAL DEVENGADO: ${total_devengado:>11,.0f}\n"
            res += f"=========================================\n"
            res += "DESCUENTOS DE LEY Y OTROS\n"
            res += f"  Salud (4%):      ${salud:>11,.0f}\n"
            res += f"  Pensión (4%):    ${pension:>11,.0f}\n"
            for k, v in self.config_data["descuentos_personales"].items():
                if v > 0:
                    nombre_desc = k.replace("_", " ").title()
                    res += f"  {nombre_desc}: ${v:>11,.0f}\n"
            res += f"  TOTAL DESCUENTOS:${total_descuentos:>11,.0f}\n"
            res += f"=========================================\n"
            res += f"  NETO A RECIBIR:  ${neto:>11,.0f}\n"

            self.txt_res.configure(state="normal")
            self.txt_res.delete("1.0", "end")
            self.txt_res.insert("1.0", res)
            self.txt_res.configure(state="disabled")
            return neto, total_devengado, total_recargos
        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos en días y recargos.")
            return 0, 0, 0

    # --- PESTAÑA 2: AUDITORÍA VS BUK ---
    def setup_tab_auditoria(self):
        f = ctk.CTkFrame(self.tab_audit)
        f.pack(fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(f, text="Auditoría: Compara tu Cálculo vs. Desprendible BUK / Pago Real", font=("Arial", 15, "bold")).pack(pady=10)

        f_inputs = ctk.CTkFrame(f, fg_color="transparent")
        f_inputs.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(f_inputs, text="Total Devengado reportado en BUK ($):", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=6)
        self.txt_buk_devengado = ctk.CTkEntry(f_inputs, width=150)
        self.txt_buk_devengado.grid(row=0, column=1, padx=10, pady=6)

        ctk.CTkLabel(f_inputs, text="Neto a Recibir reportado en BUK ($):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=6)
        self.txt_buk_neto = ctk.CTkEntry(f_inputs, width=150)
        self.txt_buk_neto.grid(row=1, column=1, padx=10, pady=6)

        ctk.CTkLabel(f_inputs, text="Valor Consignado en Banco ($):", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=6)
        self.txt_pago_real = ctk.CTkEntry(f_inputs, width=150)
        self.txt_pago_real.grid(row=2, column=1, padx=10, pady=6)

        btn_auditar = ctk.CTkButton(f, text="AUDITAR NÓMINA Y PAGO", fg_color="#D9534F", hover_color="#C9302C", font=("Arial", 12, "bold"), command=self.auditar_nomina)
        btn_auditar.pack(pady=12)

        self.txt_audit_res = ctk.CTkTextbox(f, font=("Consolas", 11))
        self.txt_audit_res.pack(fill="both", expand=True, padx=15, pady=10)

    def auditar_nomina(self):
        try:
            neto_mio, devengado_mio, recargos_mios = self.calcular_mi_nomina()
            if neto_mio == 0:
                return

            str_buk_dev = self.txt_buk_devengado.get().strip().replace(",", "").replace(".", "")
            str_buk_neto = self.txt_buk_neto.get().strip().replace(",", "").replace(".", "")
            str_pago_real = self.txt_pago_real.get().strip().replace(",", "").replace(".", "")

            buk_dev = float(str_buk_dev) if str_buk_dev else 0
            buk_neto = float(str_buk_neto) if str_buk_neto else 0
            pago_real = float(str_pago_real) if str_pago_real else 0

            res = "=== INFORME DE AUDITORÍA Y CONTROL DE PAGO ===\n\n"
            res += f"1. CÁLCULO PROPIO ESTIMADO:\n"
            res += f"   - Total Devengado Esperado: ${devengado_mio:,.0f}\n"
            res += f"   - Neto A Recibir Esperado:  ${neto_mio:,.0f}\n\n"

            if buk_neto > 0:
                dif_buk = buk_neto - neto_mio
                res += f"2. REVISIÓN DESPRENDIBLE BUK (2 Días Antes):\n"
                res += f"   - BUK Devengado: ${buk_dev:,.0f}\n"
                res += f"   - BUK Neto:      ${buk_neto:,.0f}\n"
                if abs(dif_buk) < 1000:
                    res += f"   --> RESULTADO BUK: CORRECTO. Los valores de Nómina coinciden.\n\n"
                elif dif_buk < 0:
                    res += f"   --> RESULTADO BUK: ¡ALERTA DE FALTANTE! BUK reporta ${abs(dif_buk):,.0f} MENOS de lo que calculaste.\n"
                    res += f"       Sugerencia: Revisa en BUK las horas de recargo aprobadas.\n\n"
                else:
                    res += f"   --> RESULTADO BUK: BUK reporta ${abs(dif_buk):,.0f} MÁS de lo esperado.\n\n"
            else:
                res += "2. REVISIÓN DESPRENDIBLE BUK: (No ingresado aún)\n\n"

            if pago_real > 0:
                monto_comparar = buk_neto if buk_neto > 0 else neto_mio
                dif_pago = pago_real - monto_comparar
                res += f"3. VERIFICACIÓN DE PAGO EN BANCO (Días 5 / 20):\n"
                res += f"   - Valor Recibido en Cuenta: ${pago_real:,.0f}\n"
                if abs(dif_pago) < 1000:
                    res += f"   --> RESULTADO BANCO: CORRECTO. El banco te consignó el valor exacto.\n"
                elif dif_pago < 0:
                    res += f"   --> RESULTADO BANCO: ¡ALERTA! La consignación en cuenta fue ${abs(dif_pago):,.0f} MENOR a lo estipulado.\n"
                else:
                    res += f"   --> RESULTADO BANCO: La consignación fue ${abs(dif_pago):,.0f} MAYOR a lo estipulado.\n"

            self.txt_audit_res.configure(state="normal")
            self.txt_audit_res.delete("1.0", "end")
            self.txt_audit_res.insert("1.0", res)
            self.txt_audit_res.configure(state="disabled")

        except ValueError:
            messagebox.showerror("Error", "Ingresa únicamente números en los campos de BUK o Pago.")

    # --- PESTAÑA 3: PERFIL DE USUARIO ---
    def setup_tab_perfil(self):
        f = ctk.CTkFrame(self.tab_perfil)
        f.pack(fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(f, text="Configuración del Perfil y Empleado", font=("Arial", 15, "bold")).pack(pady=10)

        f_form = ctk.CTkFrame(f, fg_color="transparent")
        f_form.pack(pady=10)

        ctk.CTkLabel(f_form, text="Nombre Completo:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=6)
        self.txt_nombre = ctk.CTkEntry(f_form, width=220)
        self.txt_nombre.insert(0, self.config_data["nombre_empleado"])
        self.txt_nombre.grid(row=0, column=1, padx=10, pady=6)

        ctk.CTkLabel(f_form, text="Cargo / Puesto:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=6)
        self.txt_cargo = ctk.CTkEntry(f_form, width=220)
        self.txt_cargo.insert(0, self.config_data.get("cargo", "Operador de Monitoreo"))
        self.txt_cargo.grid(row=1, column=1, padx=10, pady=6)

        ctk.CTkLabel(f_form, text="Sueldo Base ($):", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=6)
        self.txt_sueldo = ctk.CTkEntry(f_form, width=220)
        self.txt_sueldo.insert(0, str(self.config_data["salario_base"]))
        self.txt_sueldo.grid(row=2, column=1, padx=10, pady=6)

        ctk.CTkLabel(f_form, text="Crédito Denario ($):", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=6)
        self.txt_denario = ctk.CTkEntry(f_form, width=220)
        self.txt_denario.insert(0, str(self.config_data["descuentos_personales"].get("credito_denario", 0)))
        self.txt_denario.grid(row=3, column=1, padx=10, pady=6)

        btn_guardar = ctk.CTkButton(f, text="GUARDAR CAMBIOS DE PERFIL", fg_color="#28A745", hover_color="#218838", font=("Arial", 12, "bold"), command=self.guardar_perfil)
        btn_guardar.pack(pady=15)

    def guardar_perfil(self):
        try:
            self.config_data["nombre_empleado"] = self.txt_nombre.get().strip()
            self.config_data["cargo"] = self.txt_cargo.get().strip()
            self.config_data["salario_base"] = int(self.txt_sueldo.get().strip())
            self.config_data["descuentos_personales"]["credito_denario"] = int(self.txt_denario.get().strip())

            guardar_config(self.config_data)
            self.valor_hora = self.config_data["salario_base"] / self.config_data["horas_mes"]

            self.lbl_titulo.configure(text=f"¡Hola, {self.config_data['nombre_empleado']}!")
            self.lbl_sub.configure(
                text=f"Cargo: {self.config_data['cargo']} | Sueldo Base: ${self.config_data['salario_base']:,} | Valor Hora: ${self.valor_hora:,.2f}"
            )

            messagebox.showinfo("Éxito", "Perfil guardado correctamente. Los cambios ya están aplicados.")
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos en Sueldo y Crédito.")

if __name__ == "__main__":
    app = AppCalculadora()
    app.mainloop()