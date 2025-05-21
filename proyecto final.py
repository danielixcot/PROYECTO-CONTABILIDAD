import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json

MES_ACTUAL = 5
ANIO_ACTUAL = 2025

class SistemaContableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Contable - El Niño")
        self.root.geometry("1050x720")
        self.root.configure(bg="#f0f2f5")

        # Estilos ttk personalizados
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background="#f0f2f5", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"),
                        padding=[12, 8], background="#d9d9d9", foreground="#333")
        style.map("TNotebook.Tab",
                  background=[("selected", "#4a90e2")],
                  foreground=[("selected", "white")])

        style.configure("TLabel", background="#f0f2f5", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background="#f0f2f5")
        style.configure("Bold.TLabel", font=("Segoe UI", 11, "bold"), background="#f0f2f5")

        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.map("TButton",
                  background=[('active', '#357ABD')],
                  foreground=[('active', 'white')])

        # Variables y datos contables
        self.transacciones = []
        self.ultima_fecha_generada = datetime.strptime('01/05/2025', '%d/%m/%Y')
        self.partida_actual = 2

        self.inventario_activos = {
            "Caja": 5000.00,
            "Bancos": 320000.00,
            "Clientes": 40000.00,
            "IVA por Cobrar": 6000.00,
            "Mercaderías": 70000.00,
            "Terrenos": 500000.00,
            "Mobiliario y Equipo": 10000.00,
            "Equipo de Computo": 15000.00,
        }

        self.inventario_pasivos = {
            "Proveedores": 75000.00,
            "Préstamos Bancario": 370000.00,
            "Hipotecas": 310000.00,
            "Préstamos Bancarios a Largo Plazo": 80000.00,
        }

        self.inventario_capital = {
            "Capital": 121000.00  # Patrimonio Neto calculado
        }

        # Configuración de pestañas
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill='both', padx=10, pady=10)

        self.tab_diario = ttk.Frame(self.tab_control)
        self.tab_inventario = ttk.Frame(self.tab_control)
        self.tab_mayor = ttk.Frame(self.tab_control)       # Pestaña de Libro Mayor
        self.tab_balance = ttk.Frame(self.tab_control)     # Pestaña de Balance General

        self.tab_control.add(self.tab_diario, text='Libro Diario')
        self.tab_control.add(self.tab_inventario, text='Resumen Inventario')
        self.tab_control.add(self.tab_mayor, text='Libro Mayor')
        self.tab_control.add(self.tab_balance, text='Balance General')

        # Construcción de cada pestaña
        self.construir_tab_diario()
        self.construir_tab_inventario()
        self.construir_tab_mayor()
        self.construir_tab_balance()

    # --- TAB Libro Diario ---
    def construir_tab_diario(self):
        frame = ttk.Frame(self.tab_diario, padding=15)
        frame.pack(fill='x')

        ttk.Label(frame, text="Tipo de Transacción:", style="Bold.TLabel").grid(row=0, column=0, sticky="w", pady=6)
        self.tipo_var = tk.StringVar()
        self.cbo_tipo = ttk.Combobox(frame, textvariable=self.tipo_var, state="readonly",
                                     values=[
                                         "Venta",
                                         "Compra Mercadería",
                                         "Compra Insumos/Mobiliario",
                                         "Gastos Administrativos",
                                         "Pago de Salarios"
                                     ], width=40)
        self.cbo_tipo.grid(row=0, column=1, sticky="w", pady=6, columnspan=2)
        self.cbo_tipo.bind("<<ComboboxSelected>>", self.activar_campos)

        ttk.Label(frame, text="Cuenta (Debe):", style="Bold.TLabel").grid(row=1, column=0, sticky="w", pady=6)
        self.debe_var = tk.StringVar()
        self.cbo_debe = ttk.Combobox(frame, textvariable=self.debe_var, state="readonly", width=25)
        self.cbo_debe.grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(frame, text="Cuenta (Haber):", style="Bold.TLabel").grid(row=1, column=2, sticky="w", padx=(20,0), pady=6)
        self.haber_var = tk.StringVar()
        self.cbo_haber = ttk.Combobox(frame, textvariable=self.haber_var, state="readonly", width=25)
        self.cbo_haber.grid(row=1, column=3, sticky="w", pady=6)

        ttk.Label(frame, text="Monto:", style="Bold.TLabel").grid(row=2, column=0, sticky="w", pady=6)
        self.txt_monto = ttk.Entry(frame, width=40)
        self.txt_monto.grid(row=2, column=1, sticky="w", pady=6, columnspan=3)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=6, column=0, columnspan=4, pady=15)

        ttk.Button(btn_frame, text="Registrar Transacción", command=self.registrar_transaccion, width=25).grid(row=0, column=0, padx=8)
        ttk.Button(btn_frame, text="Calcular IVA y Depreciaciones", command=self.calcular_iva_y_depreciaciones, width=25).grid(row=0, column=1, padx=8)
        ttk.Button(btn_frame, text="Guardar Reporte JSON", command=self.generar_json, width=25).grid(row=0, column=2, padx=8)

        cols = ("partida", "fecha", "cuenta", "movimiento", "monto")
        self.tbl_diario = ttk.Treeview(self.tab_diario, columns=cols, show="headings", height=15)
        for col in cols:
            self.tbl_diario.heading(col, text=col.capitalize())
            width = 230 if col == "cuenta" else 110
            self.tbl_diario.column(col, width=width, anchor="center")
        self.tbl_diario.pack(padx=15, pady=10, fill='both', expand=True)

        scroll_vert = ttk.Scrollbar(self.tab_diario, orient="vertical", command=self.tbl_diario.yview)
        self.tbl_diario.configure(yscrollcommand=scroll_vert.set)
        scroll_vert.pack(side='right', fill='y')

        scroll_horz = ttk.Scrollbar(self.tab_diario, orient="horizontal", command=self.tbl_diario.xview)
        self.tbl_diario.configure(xscrollcommand=scroll_horz.set)
        scroll_horz.pack(side='bottom', fill='x')

    # --- TAB Resumen Inventario ---
    def construir_tab_inventario(self):
        frame = ttk.Frame(self.tab_inventario, padding=20)
        frame.pack(anchor='nw')

        ttk.Label(frame, text="ACTIVOS", style="Header.TLabel").pack(anchor='w')
        for nombre, monto in self.inventario_activos.items():
            ttk.Label(frame, text=f"{nombre:<30} Q{monto:,.2f}", style="TLabel").pack(anchor='w')

        ttk.Label(frame, text="\nPASIVOS", style="Header.TLabel").pack(anchor='w', pady=(15, 0))
        for nombre, monto in self.inventario_pasivos.items():
            ttk.Label(frame, text=f"{nombre:<30} Q{monto:,.2f}", style="TLabel").pack(anchor='w')

        total_activo = sum(self.inventario_activos.values())
        total_pasivo = sum(self.inventario_pasivos.values())
        patrimonio_neto = total_activo - total_pasivo

        ttk.Label(frame, text="\nPATRIMONIO NETO", style="Header.TLabel").pack(anchor='w', pady=(15, 0))
        ttk.Label(frame, text=f"{'Capital':<30} Q{patrimonio_neto:,.2f}", style="TLabel").pack(anchor='w')

        ttk.Label(frame, text=f"\nTotal Activo:            Q{total_activo:,.2f}", style="Bold.TLabel").pack(anchor='w', pady=6)
        ttk.Label(frame, text=f"Total Pasivo + Capital:  Q{(total_pasivo + patrimonio_neto):,.2f}", style="Bold.TLabel").pack(anchor='w')

    # --- TAB Libro Mayor ---
    def construir_tab_mayor(self):
        frame = ttk.Frame(self.tab_mayor, padding=10)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Libro Mayor ", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.tbl_mayor = ttk.Treeview(frame, columns=("fecha", "partida", "descripcion", "debe", "haber"), show="headings", height=18)
        for col, width in [("fecha", 110), ("partida", 80), ("descripcion", 360), ("debe", 140), ("haber", 140)]:
            self.tbl_mayor.heading(col, text=col.capitalize())
            anchor = 'e' if col in ("debe", "haber") else 'w'
            self.tbl_mayor.column(col, width=width, anchor=anchor)
        self.tbl_mayor.pack(fill='both', expand=True)

        scroll_v = ttk.Scrollbar(frame, orient="vertical", command=self.tbl_mayor.yview)
        scroll_v.pack(side="right", fill="y")
        self.tbl_mayor.configure(yscrollcommand=scroll_v.set)

        ttk.Button(frame, text="Actualizar Libro Mayor", command=self.actualizar_libro_mayor_con_cierres, width=30).pack(pady=10)

    def actualizar_libro_mayor_con_cierres(self):
        for item in self.tbl_mayor.get_children():
            self.tbl_mayor.delete(item)

        cuentas = set(self.inventario_activos) | set(self.inventario_pasivos) | set(self.inventario_capital) | set(t[2] for t in self.transacciones)
        cuentas.add("Ventas")

        cuentas.discard("Depreciación Acumulada Mobiliario y Equipo")
        cuentas.discard("Depreciación Acumulada Equipo de Computo")
        cuentas.discard("Depreciación Mobiliario y Equipo")
        cuentas.discard("Depreciación Equipo de Computo")
        cuentas.add("Depreciación")

        todas_cuentas = sorted(cuentas)

        transacciones_filtradas = [
            t for t in self.transacciones
            if t[2] not in (
                "IVA por Cobrar", "IVA por Pagar",
                "Depreciación Acumulada Mobiliario y Equipo",
                "Depreciación Acumulada Equipo de Computo",
                "Depreciación Mobiliario y Equipo",
                "Depreciación Equipo de Computo"
            )
        ]

        orden = sorted(
            transacciones_filtradas,
            key=lambda x: (x[2], datetime.strptime(x[1], "%d/%m/%Y"), x[0])
        )

        por_cuenta = {}
        for t in orden:
            if t[2] not in ("Depreciación Mobiliario y Equipo", "Depreciación Equipo de Computo"):
                por_cuenta.setdefault(t[2], []).append(t)

        movs_mobiliario = [t for t in self.transacciones if t[2] == "Depreciación Mobiliario y Equipo"]
        movs_computo = [t for t in self.transacciones if t[2] == "Depreciación Equipo de Computo"]

        for t in movs_mobiliario + movs_computo:
            partida, fecha, cuenta, movimiento, monto = t
            movimiento_invertido = "Haber" if movimiento == "Debe" else "Debe"
            por_cuenta.setdefault("Depreciación", []).append((
                partida, fecha, "Depreciación", movimiento_invertido, monto
            ))

        ultimo_dia = 31
        fecha_inicio = f"01/01/{ANIO_ACTUAL}"
        fecha_cierre = f"{ultimo_dia:02d}/{MES_ACTUAL:02d}/{ANIO_ACTUAL}"

        for cuenta in todas_cuentas:
            self.tbl_mayor.insert("", tk.END, values=("", "", f"** {cuenta} **", "", ""))

            saldo_inicial = (
                self.inventario_activos.get(cuenta, 0)
                + self.inventario_pasivos.get(cuenta, 0)
                + self.inventario_capital.get(cuenta, 0)
            )

            debe_ini = f"Q{saldo_inicial:,.2f}" if cuenta in self.inventario_activos or cuenta in self.inventario_capital else ""
            haber_ini = f"Q{saldo_inicial:,.2f}" if cuenta in self.inventario_pasivos or cuenta == "Ventas" or cuenta == "Depreciación" else ""

            if saldo_inicial != 0:
                self.tbl_mayor.insert("", tk.END, values=(
                    fecha_inicio,
                    "P1",
                    f"Partida de inicio según inventario del {fecha_inicio}",
                    debe_ini,
                    haber_ini
                ))

            saldo = saldo_inicial
            total_debe = saldo_inicial if cuenta in self.inventario_activos or cuenta in self.inventario_capital else 0
            total_haber = saldo_inicial if cuenta in self.inventario_pasivos or cuenta == "Ventas" or cuenta == "Depreciación" else 0

            for partida, fecha, c, mov, monto in por_cuenta.get(cuenta, []):
                debe = f"Q{monto:,.2f}" if mov == "Debe" else ""
                haber = f"Q{monto:,.2f}" if mov == "Haber" else ""

                total_debe += monto if mov == "Debe" else 0
                total_haber += monto if mov == "Haber" else 0

                saldo += monto if mov == "Debe" else -monto
                self.tbl_mayor.insert("", tk.END, values=(
                    fecha,
                    f"P{partida}" if partida != "X" else "",
                    f"Partida {partida}" if partida != "X" else "Movimiento unificado",
                    debe,
                    haber
                ))

            if saldo != 0:
                if cuenta in self.inventario_pasivos or cuenta == "Ventas" or cuenta == "Depreciación":
                    debe_cierre = f"Q{abs(saldo):,.2f}"
                    haber_cierre = ""
                else:
                    debe_cierre = ""
                    haber_cierre = f"Q{abs(saldo):,.2f}"
                self.tbl_mayor.insert("", tk.END, values=(
                    fecha_cierre,
                    "P25",
                    f"Partida de cierre de la cuenta {cuenta} al {fecha_cierre}",
                    debe_cierre,
                    haber_cierre
                ))

            total_movimientos = max(total_debe, total_haber)
            total_str = f"Q{total_movimientos:,.2f}" if total_movimientos > 0 else ""
            self.tbl_mayor.insert("", tk.END, values=(
                "", "",
                "Total movimientos",
                total_str,
                total_str
            ))

    # --- TAB Balance General ---
    def construir_tab_balance(self):
        frame = ttk.Frame(self.tab_balance, padding=15)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Balance General", style="Header.TLabel").pack(pady=6)
       
        self.reporte_text = tk.Text(frame, height=40, width=105, font=("Courier New", 10))
        self.reporte_text.pack(fill="both", expand=True)

        ttk.Button(frame, text="Actualizar Datos",
                   command=self.generar_estado_completo, width=40).pack(pady=8)

        self.generar_estado_completo()

    def generar_estado_completo(self):
        self.reporte_text.delete("1.0", tk.END)

        cuentas_fijas = [
            "Caja", "Bancos", "Clientes", "IVA por Cobrar", "Mercaderías",
            "Terrenos", "Mobiliario y Equipo", "Equipo de Computo", "Proveedores",
            "Préstamos Bancario", "Hipotecas"
        ]

        def formatear_q(valor):
            return f"Q{valor:,.2f}" if valor else ""

        texto = ""
        texto += "CUENTA                               SALDO INICIAL     CARGOS DEL MES     ABONOS DEL MES\n"
        texto += "---------------------------------------------------------------------------\n"

        movimientos_por_cuenta = {}
        for t in self.transacciones:
            cuenta = t[2]
            movimiento = t[3]
            monto = t[4]
            movimientos_por_cuenta.setdefault(cuenta, {"Debe": 0, "Haber": 0})
            movimientos_por_cuenta[cuenta][movimiento] += monto

        cargos_total = 0
        abonos_total = 0

        for cuenta in cuentas_fijas:
            cargos_mes = 0
            abonos_mes = 0

            if cuenta in self.inventario_activos:
                cargos_mes = self.inventario_activos.get(cuenta, 0)
            elif cuenta in self.inventario_pasivos:
                abonos_mes = self.inventario_pasivos.get(cuenta, 0)

            cargos_mes += movimientos_por_cuenta.get(cuenta, {}).get("Debe", 0)
            abonos_mes += movimientos_por_cuenta.get(cuenta, {}).get("Haber", 0)

            cargos_total += cargos_mes
            abonos_total += abonos_mes

            texto += f"{cuenta:<35} {'':>15} {formatear_q(cargos_mes):>18} {formatear_q(abonos_mes):>17}\n"

        patrimonio_neto = cargos_total - abonos_total
        texto += f"{'Capital':<35} {'':>15} {'':>18} {formatear_q(patrimonio_neto):>17}\n"

        texto += "---------------------------------------------------------------------------\n"
        texto += f"{'Saldos al 31 de mayo de 2025':<35} {'':>15} {formatear_q(cargos_total):>18} {formatear_q(abonos_total + patrimonio_neto):>17}\n\n"

        # Estado de Pérdidas y Ganancias
        total_ventas = sum(t[4] for t in self.transacciones if t[2] == "Ventas")
        costo_ventas = sum(t[4] for t in self.transacciones if t[2] == "Mercaderías")
        utilidad_bruta = total_ventas - costo_ventas

        dep_mob = round((35825 * 0.20) / 12, 2)
        dep_pc = round((15000 * 0.3333) / 12, 2)
        gastos_admin = sum(t[4] for t in self.transacciones if t[2] == "Gastos Administrativos")
        gastos_venta = sum(t[4] for t in self.transacciones if t[2] in ["Gastos Generales", "Impuestos y Arbitrios"])

        total_gastos_admin = gastos_admin + dep_mob + dep_pc
        total_gastos_venta = gastos_venta
        total_gastos = total_gastos_admin + total_gastos_venta

        utilidad_neta = utilidad_bruta - total_gastos

        def linea(texto, valor=None, indent=0, bold=False):
            esp = ' ' * indent
            if valor is None:
                line = f"{esp}{texto}\n"
            else:
                line = f"{esp}{texto:<40} Q{valor:>10,.2f}\n"
            if bold:
                line = line.upper()
            return line

        texto += linea("ESTADO DE PÉRDIDAS Y GANANCIAS", bold=True)
        texto += linea("VENTAS", bold=True)
        texto += linea("Ventas", total_ventas, indent=2)
        texto += linea("- Costo de ventas", costo_ventas, indent=2)
        texto += linea("UTILIDAD BRUTA", utilidad_bruta, bold=True)
        texto += "\n"
        texto += linea("GASTOS DE OPERACIÓN", bold=True)
        texto += linea("Gastos Administrativos", bold=True)
        texto += linea("Depreciación de M&E", dep_mob, indent=2)
        texto += linea("Depreciación de EC", dep_pc, indent=2)
        texto += linea("Gastos de computación", gastos_admin, indent=2)
        texto += linea("Total Gastos Administrativos", total_gastos_admin, bold=True)
        texto += linea("Gastos de Ventas", bold=True)
        texto += linea("Gastos Generales", gastos_venta, indent=2)
        texto += linea("Impuestos y Arbitrios", 0, indent=2)  # Ajusta si tienes valor real
        texto += linea("Total Gastos de Ventas", total_gastos_venta, bold=True)
        texto += linea("TOTAL GASTOS DE OPERACIÓN", total_gastos, bold=True)
        texto += linea("RESULTADO DEL EJERCICIO (UTILIDAD NETA)", utilidad_neta, bold=True)

        self.reporte_text.insert(tk.END, texto)

    # --- FUNCIONES DE LIBRO DIARIO ---
    def activar_campos(self, event):
        tipo = self.tipo_var.get()
        self.txt_monto.config(state='normal')
        if tipo == "Compra Mercadería":
            self.cbo_debe.config(values=["Mercaderías", "IVA por Cobrar"])
            self.cbo_haber.config(values=["Caja", "Bancos", "Proveedores"])
        elif tipo == "Venta":
            self.cbo_debe.config(values=["Caja", "Bancos", "Clientes"])
            self.cbo_haber.config(values=["Ventas", "IVA por Pagar"])
        elif tipo == "Compra Insumos/Mobiliario":
            self.cbo_debe.config(values=["Insumos", "Mobiliario y Equipo", "IVA por Cobrar"])
            self.cbo_haber.config(values=["Caja", "Bancos", "Proveedores"])
        elif tipo == "Gastos Administrativos":
            self.cbo_debe.config(values=["Gastos Administrativos", "Gastos Públicos", "Publicidad", "Energía"])
            self.cbo_haber.config(values=["Caja", "Bancos"])
        elif tipo == "Pago de Salarios":
            self.cbo_debe.config(values=["Salarios Sala de Ventas", "Salario Administración"])
            self.cbo_haber.config(values=["Caja", "Bancos"])

    def registrar_transaccion(self):
        tipo = self.tipo_var.get()
        fecha = self.generar_fecha_aleatoria()
        partida = self.partida_actual

        try:
            monto = float(self.txt_monto.get())
        except ValueError:
            messagebox.showerror("Error", "Monto no válido.")
            return

        partidas = []
        if tipo == "Compra Mercadería":
            iva = round(monto * 0.12, 2)
            subtotal = round(monto - iva, 2)
            partidas = [
                (fecha, "Mercaderías", "Debe", subtotal),
                (fecha, "IVA por Cobrar", "Debe", iva),
                (fecha, self.haber_var.get(), "Haber", monto)
            ]
        elif tipo == "Venta":
            iva = round(monto * 0.12, 2)
            subtotal = round(monto - iva, 2)
            partidas = [
                (fecha, self.debe_var.get(), "Debe", monto),
                (fecha, "Ventas", "Haber", subtotal),
                (fecha, "IVA por Pagar", "Haber", iva)
            ]
        else:
            partidas = [
                (fecha, self.debe_var.get(), "Debe", monto),
                (fecha, self.haber_var.get(), "Haber", monto)
            ]

        for trans in partidas:
            self.transacciones.append((partida, *trans))
            self.tbl_diario.insert("", tk.END, values=(partida, *trans))

        self.partida_actual += 1
        self.txt_monto.delete(0, tk.END)

    def calcular_iva_y_depreciaciones(self):
        fecha = f"28/{MES_ACTUAL:02d}/{ANIO_ACTUAL}"
        partida = self.partida_actual

        dep_mob = round((35825 * 0.20) / 12, 2)
        dep_pc = round((15000 * 0.3333) / 12, 2)

        movimientos = [
            (fecha, "Depreciación Mobiliario y Equipo", "Debe", dep_mob),
            (fecha, "Depreciación Acumulada Mobiliario y Equipo", "Haber", dep_mob),
            (fecha, "Depreciación Equipo de Computo", "Debe", dep_pc),
            (fecha, "Depreciación Acumulada Equipo de Computo", "Haber", dep_pc),
        ]

        iva_pagar = sum(t[4] for t in self.transacciones if t[2] == "IVA por Pagar" and t[3] == "Haber")
        iva_cobrar = sum(t[4] for t in self.transacciones if t[2] == "IVA por Cobrar" and t[3] == "Debe")
        ajuste = min(iva_pagar, iva_cobrar)
        if ajuste > 0:
            movimientos += [
                (fecha, "IVA por Pagar", "Debe", ajuste),
                (fecha, "IVA por Cobrar", "Haber", ajuste),
            ]

        for mov in movimientos:
            self.transacciones.append((partida, *mov))
            self.tbl_diario.insert("", tk.END, values=(partida, *mov))

        self.partida_actual += 1
        messagebox.showinfo("Cálculo realizado", "Se registraron depreciaciones e IVA ajustado.")

    def generar_json(self):
        data = [
            {"partida": p, "fecha": f, "cuenta": c, "movimiento": m, "monto": v}
            for p, f, c, m, v in self.transacciones
        ]
        with open("libro_diario.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Guardado", "Guardado como 'libro_diario.json'.")

    def generar_fecha_aleatoria(self):
        self.ultima_fecha_generada += timedelta(days=1)
        if self.ultima_fecha_generada.day > 28:
            self.ultima_fecha_generada = self.ultima_fecha_generada.replace(day=28)
        return self.ultima_fecha_generada.strftime("%d/%m/%Y")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaContableApp(root)
    root.mainloop()
