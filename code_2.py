import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class EnergyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Energética - Soacha")
        self.root.geometry("800x700")
        self.root.configure(bg="#1e1e2e")

        # Base de datos temporal
        self.lista_hogares = []
        self.lista_lecturas = []

        # --- ESTILOS ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#1e1e2e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#313244", foreground="white", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#89b4fa")], foreground=[("selected", "#1e1e2e")])
        style.configure("Treeview", background="#313244", foreground="white", fieldbackground="#313244", rowheight=25)
        style.map("Treeview", background=[("selected", "#585b70")])

        # --- NAVEGACIÓN POR PESTAÑAS ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_registro = tk.Frame(self.notebook, bg="#1e1e2e")
        self.tab_lectura = tk.Frame(self.notebook, bg="#1e1e2e")
        self.tab_consulta = tk.Frame(self.notebook, bg="#1e1e2e")

        self.notebook.add(self.tab_registro, text=" Registro de Hogares ")
        self.notebook.add(self.tab_lectura, text=" Toma de Lecturas ")
        self.notebook.add(self.tab_consulta, text=" Historial de Consumo ")

        self.setup_tab_registro()
        self.setup_tab_lectura()
        self.setup_tab_consulta()

    # --- PESTAÑA 1: REGISTRO DE HOGARES ---
    def setup_tab_registro(self):
        container = tk.Frame(self.tab_registro, bg="#1e1e2e")
        container.pack(pady=20, padx=50, fill="x")

        tk.Label(container, text="REGISTRAR NUEVO CONTADOR", font=("Helvetica", 14, "bold"), fg="#89b4fa", bg="#1e1e2e").pack(pady=10)

        self.reg_id = self.crear_campo(container, "Número de Contador (ID):")
        self.reg_dir = self.crear_campo(container, "Dirección de Residencia:") # Requerimiento de dirección [cite: 97]
        
        tk.Label(container, text="Tipo de Vivienda:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w")
        self.reg_tipo = ttk.Combobox(container, values=["Casa", "Apartamento", "Uso Intensivo"], state="readonly") # Clasificación por tipo [cite: 45, 68]
        self.reg_tipo.pack(fill="x", pady=5)
        self.reg_tipo.set("Casa")

        tk.Label(container, text="Estrato:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w")
        self.reg_estrato = ttk.Combobox(container, values=["1", "2", "3"], state="readonly") # Estratos permitidos [cite: 43]
        self.reg_estrato.pack(fill="x", pady=5)
        self.reg_estrato.set("1")

        tk.Button(container, text="Guardar Hogar", bg="#a6e3a1", command=self.guardar_hogar).pack(pady=20, fill="x")

        # Tabla de contadores agregados
        self.tabla_hogares = ttk.Treeview(self.tab_registro, columns=("ID", "Dirección", "Tipo", "Estrato"), show="headings")
        self.tabla_hogares.heading("ID", text="Contador")
        self.tabla_hogares.heading("Dirección", text="Dirección")
        self.tabla_hogares.heading("Tipo", text="Tipo")
        self.tabla_hogares.heading("Estrato", text="Estrato")
        self.tabla_hogares.pack(fill="both", expand=True, padx=20, pady=10)

    # --- PESTAÑA 2: TOMA DE LECTURAS ---
    def setup_tab_lectura(self):
        container = tk.Frame(self.tab_lectura, bg="#1e1e2e")
        container.pack(pady=20, padx=50, fill="x")

        tk.Label(container, text="INGRESAR CONSUMO MENSUAL", font=("Helvetica", 14, "bold"), fg="#fab387", bg="#1e1e2e").pack(pady=10)

        tk.Label(container, text="Seleccionar Contador:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w")
        self.combo_contadores = ttk.Combobox(container, state="readonly")
        self.combo_contadores.pack(fill="x", pady=5)

        self.lec_kwh = self.crear_campo(container, "Consumo en kWh:")
        
        tk.Button(container, text="Calcular y Generar Alerta", bg="#89b4fa", command=self.registrar_consumo).pack(pady=20, fill="x")

    # --- PESTAÑA 3: HISTORIAL ---
    def setup_tab_consulta(self):
        tk.Label(self.tab_consulta, text="HISTORIAL DE ALERTAS Y FACTURACIÓN", font=("Helvetica", 14, "bold"), fg="#f5e0dc", bg="#1e1e2e").pack(pady=10)
        
        # Tabla de consumos [cite: 74-79]
        self.tabla_consumos = ttk.Treeview(self.tab_consulta, 
            columns=("Fecha", "Contador", "Consumo", "Alerta", "Acción"), show="headings")
        self.tabla_consumos.heading("Fecha", text="Fecha/Hora")
        self.tabla_consumos.heading("Contador", text="ID Contador")
        self.tabla_consumos.heading("Consumo", text="kWh")
        self.tabla_consumos.heading("Alerta", text="Estado")
        self.tabla_consumos.heading("Acción", text="Acción Recomendada")
        self.tabla_consumos.pack(fill="both", expand=True, padx=10, pady=10)

    # --- LÓGICA DE APOYO ---
    def crear_campo(self, parent, texto):
        tk.Label(parent, text=texto, bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w")
        ent = tk.Entry(parent, bg="#313244", fg="white", insertbackground="white", bd=0)
        ent.pack(fill="x", pady=5, ipady=3)
        return ent

    def guardar_hogar(self):
        id_c = self.reg_id.get()
        dir_r = self.reg_dir.get()
        tipo = self.reg_tipo.get()
        est = self.reg_estrato.get()

        if id_c and dir_r:
            hogar = {"id": id_c, "dir": dir_r, "tipo": tipo, "estrato": int(est)}
            self.lista_hogares.append(hogar)
            self.tabla_hogares.insert("", "end", values=(id_c, dir_r, tipo, est))
            
            # Actualizar combo de lecturas
            ids = [h["id"] for h in self.lista_hogares]
            self.combo_contadores["values"] = ids
            
            messagebox.showinfo("Éxito", f"Contador {id_c} registrado correctamente.")
            self.reg_id.delete(0, tk.END)
            self.reg_dir.delete(0, tk.END)
        else:
            messagebox.showwarning("Atención", "Complete todos los campos de registro.")

    def registrar_consumo(self):
        id_c = self.combo_contadores.get()
        try:
            kwh = float(self.lec_kwh.get())
            # Buscar datos del hogar
            hogar = next((h for h in self.lista_hogares if h["id"] == id_c), None)
            
            if not hogar:
                return messagebox.showerror("Error", "Seleccione un contador válido.")

            # Lógica de Alertas [cite: 49, 58, 61, 63, 64]
            estado, accion = "", ""
            if kwh <= 100:
                estado, accion = "BAJO", "Enviar técnico (Posible fraude)"
            elif 101 <= kwh <= 200:
                estado, accion = "NORMAL", "Sin acción"
            elif 201 <= kwh <= 300:
                estado, accion = "ALTO", "Notificación preventiva"
            else:
                estado, accion = "URGENTE", "Revisión técnica inmediata"

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.tabla_consumos.insert("", 0, values=(fecha, id_c, kwh, estado, accion))
            
            messagebox.showinfo("Reporte Generado", f"Estado: {estado}\nAcción: {accion}")
            self.lec_kwh.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "El consumo debe ser un número.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnergyApp(root)
    root.mainloop()