import datetime

# --- BASE DE DATOS EN MEMORIA ---
hogares = {}  # Diccionario para almacenar datos de la vivienda
historial_lecturas = []  # Lista para los registros de consumo

def calcular_subsidio(consumo, estrato):
    """Calcula el beneficio según el estrato sobre los primeros 130 kWh"""
    limite_subsidiado = min(consumo, 130) # Límite de subsistencia
    # Porcentajes: Estrato 1 (60%), 2 (50%), 3 (15%)
    porcentajes = {1: 0.60, 2: 0.50, 3: 0.15} 
    descuento = porcentajes.get(estrato, 0)
    return limite_subsidiado, descuento

def obtener_alerta(consumo):
    """Clasifica el consumo y determina la acción técnica"""
    if consumo <= 100:
        return "BAJO", "Generar alerta para enviar técnico a revisar el hogar"
    elif 101 <= consumo <= 200:
        return "NORMAL", "No se genera ninguna alerta"
    elif 201 <= consumo <= 300:
        return "ALTO", "Generar alerta preventiva para notificar al hogar"
    else: # > 300
        return "URGENTE", "Generar alerta urgente y programar revisión técnica inmediata"

def registrar_hogar():
    print("\n--- REGISTRO DE NUEVO HOGAR ---")
    id_c = input("ID del Contador: ") # Identificador único
    if id_c in hogares:
        print("⚠️ Este contador ya está registrado.")
        return
    
    direccion = input("Dirección de Residencia: ")
    print("Clasificación: 1. Pequeño | 2. Mediano | 3. Uso Intensivo")
    op_tipo = input("Seleccione tipo (1/2/3): ")
    tipos = {"1": "Pequeño", "2": "Mediano", "3": "Uso Intensivo"}
    tipo = tipos.get(op_tipo, "Mediano")
    
    try:
        estrato = int(input("Estrato (1, 2 o 3): ")) # Nivel socioeconómico
        if estrato not in [1, 2, 3]:
            print("❌ Error: Solo se aplican subsidios para estratos 1, 2 y 3")
            return

        hogares[id_c] = {"direccion": direccion, "tipo": tipo, "estrato": estrato}
        print(f"✅ Hogar registrado con éxito.")
    except ValueError:
        print("❌ Error: Entrada inválida.")

def ingresar_lectura():
    print("\n--- TOMA DE LECTURA MENSUAL ---")
    id_c = input("ID del contador: ")
    if id_c not in hogares:
        print("❌ Error: El contador no existe.")
        return

    try:
        # Consumo mensual registrado
        consumo = float(input(f"Consumo en kWh: ")) 
        datos = hogares[id_c]
        
        limite_sub, pct = calcular_subsidio(consumo, datos['estrato'])
        tipo_alerta, accion = obtener_alerta(consumo)
        
        # Registro con fecha y hora
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        registro = {
            "fecha": fecha, 
            "id": id_c, 
            "consumo": consumo,
            "alerta": tipo_alerta, 
            "accion": accion
        }
        historial_lecturas.append(registro)
        print(f"\n✅ Análisis completado. Clasificación: {tipo_alerta}")
    except ValueError:
        print("❌ Error: Ingrese un número válido para el consumo.")

def eliminar_datos():
    print("\n--- MENÚ DE ELIMINACIÓN ---")
    print("1. Eliminar un Contador")
    print("2. Eliminar registro del Historial")
    print("3. Volver")
    op = input("Seleccione: ")

    if op == "1":
        id_c = input("ID del contador a borrar: ")
        if id_c in hogares:
            del hogares[id_c]
            global historial_lecturas
            historial_lecturas = [r for r in historial_lecturas if r['id'] != id_c]
            print(f"✅ Datos del contador {id_c} eliminados.")
        else:
            print("❌ No se encontró el contador.")

    elif op == "2":
        ver_historial()
        if not historial_lecturas: return
        try:
            idx = int(input("Índice a eliminar: "))
            if 0 <= idx < len(historial_lecturas):
                historial_lecturas.pop(idx)
                print("✅ Registro eliminado.")
            else:
                print("❌ Índice inválido.")
        except ValueError:
            print("❌ Entrada no válida.")

def ver_historial():
    print("\n--- HISTORIAL DE CONSUMOS Y ALERTAS ---")
    if not historial_lecturas:
        print("No hay registros almacenados.")
        return
    
    print(f"{'Idx':<4} | {'Fecha':<16} | {'Contador':<10} | {'kWh':<6} | {'Estado'}")
    print("-" * 60)
    for i, r in enumerate(historial_lecturas):
        print(f"{i:<4} | {r['fecha']:<16} | {r['id']:<10} | {r['consumo']:<6} | {r['alerta']}")

def menu():
    while True:
        print("\n================================")
        print("SOFTWARE CONSUMO ENERGÍA SOACHA")
        print("================================")
        print("1. Registrar Hogar")
        print("2. Ingresar Lectura")
        print("3. Ver Historial")
        print("4. Eliminar Datos")
        print("5. Salir")
        opcion = input("Opción: ")

        if opcion == "1": registrar_hogar()
        elif opcion == "2": ingresar_lectura()
        elif opcion == "3": ver_historial()
        elif opcion == "4": eliminar_datos()
        elif opcion == "5": break
        else: print("Opción no válida.")

if __name__ == "__main__":
    menu()