import tkinter as tk
from tkinter import messagebox, ttk

class EnergyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Consumo Energético - Soacha")
        self.root.geometry("500x700")
        self.root.configure(bg="#1e1e2e")  # Fondo oscuro moderno

        # Estilo para los widgets
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # --- ENCABEZADO ---
        header = tk.Frame(root, bg="#313244", height=80)
        header.pack(fill="x")
        tk.Label(header, text="MONITOR DE ENERGÍA", font=("Helvetica", 18, "bold"), 
                 fg="#cdd6f4", bg="#313244").pady=20
        tk.Label(header, text="Soacha, Cundinamarca", font=("Helvetica", 10), 
                 fg="#a6adc8", bg="#313244").pack()
        header.pack_propagate(False)
        header.pack(pady=(0, 20))

        # --- FORMULARIO ---
        container = tk.Frame(root, bg="#1e1e2e")
        container.pack(padx=30, fill="both")

        # Entrada: ID Contador
        self.create_label(container, "ID Contador / Medidor:")
        self.ent_id = self.create_entry(container)

        # Entrada: Estrato
        self.create_label(container, "Estrato Socioeconómico (1, 2 o 3):")
        self.combo_estrato = ttk.Combobox(container, values=["1", "2", "3"], state="readonly")
        self.combo_estrato.pack(fill="x", pady=(0, 15))
        self.combo_estrato.set("1")

        # Entrada: Consumo kWh
        self.create_label(container, "Consumo Mensual (kWh):")
        self.ent_consumo = self.create_entry(container)

        # --- BOTÓN DE PROCESAMIENTO ---
        self.btn_calc = tk.Button(container, text="ANALIZAR CONSUMO", command=self.procesar_datos,
                                  bg="#89b4fa", fg="#1e1e2e", font=("Helvetica", 12, "bold"),
                                  activebackground="#74c7ec", cursor="hand2", bd=0, pady=10)
        self.btn_calc.pack(fill="x", pady=20)

        # --- RESULTADOS Y ALERTAS ---
        self.res_frame = tk.LabelFrame(container, text=" Resultados del Análisis ", bg="#1e1e2e", 
                                       fg="#f5e0dc", font=("Helvetica", 10, "bold"))
        self.res_frame.pack(fill="both", expand=True, pady=10)

        self.lbl_subsidio = tk.Label(self.res_frame, text="Subsidio Aplicado: $0", bg="#1e1e2e", fg="#cdd6f4")
        self.lbl_subsidio.pack(anchor="w", padx=10, pady=5)

        self.lbl_alerta = tk.Label(self.res_frame, text="ALERTA: Pendiente", font=("Helvetica", 11, "bold"),
                                   bg="#1e1e2e", fg="#f9e2af")
        self.lbl_alerta.pack(fill="x", padx=10, pady=10)

        self.txt_accion = tk.Label(self.res_frame, text="Acción: Ingrese datos", bg="#1e1e2e", 
                                   fg="#a6adc8", wraplength=400)
        self.txt_accion.pack(padx=10, pady=5)

    def create_label(self, parent, text):
        lbl = tk.Label(parent, text=text, bg="#1e1e2e", fg="#cdd6f4", font=("Helvetica", 10))
        lbl.pack(anchor="w", pady=(5, 2))
        return lbl

    def create_entry(self, parent):
        ent = tk.Entry(parent, bg="#313244", fg="white", insertbackground="white", bd=0, font=("Helvetica", 11))
        ent.pack(fill="x", pady=(0, 15), ipady=5)
        return ent

    def procesar_datos(self):
        try:
            consumo = float(self.ent_consumo.get())
            estrato = int(self.combo_estrato.get())
            
            # 1. Lógica de Subsidio [cite: 52-55]
            limite = 130
            porcentajes = {1: 0.60, 2: 0.50, 3: 0.15}
            p_sub = porcentajes[estrato]
            
            consumo_subsidiado = min(consumo, limite)
            ahorro_texto = f"{int(p_sub * 100)}% sobre los primeros {consumo_subsidiado} kWh"
            self.lbl_subsidio.config(text=f"Beneficio: {ahorro_texto}")

            # 2. Lógica de Alertas [cite: 49-50, 58-65]
            if consumo <= 100:
                self.mostrar_alerta("BAJO - POSIBLE FRAUDE", "#f38ba8", 
                                   "Enviar técnico urgente: Posible manipulación del contador.")
            elif 101 <= consumo <= 200:
                self.mostrar_alerta("NORMAL", "#a6e3a1", 
                                   "Consumo dentro del rango esperado. No se requiere acción.")
            elif 201 <= consumo <= 300:
                self.mostrar_alerta("ALTO - PREVENTIVA", "#fab387", 
                                   "Notificar al hogar: Verificar posibles fallas o uso elevado.")
            else: # > 300
                self.mostrar_alerta("ALARMANTE - URGENTE", "#eba0ac", 
                                   "Programar revisión técnica inmediata por consumo inusual.")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un valor numérico válido en el consumo.")

    def mostrar_alerta(self, titulo, color, accion):
        self.lbl_alerta.config(text=f"ESTADO: {titulo}", fg=color)
        self.txt_accion.config(text=f"ACCIÓN: {accion}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnergyApp(root)
    root.mainloop()