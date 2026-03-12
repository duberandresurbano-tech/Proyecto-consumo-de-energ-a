import datetime

# --- BASE DE DATOS EN MEMORIA ---
hogares = {}  
historial_lecturas = []

def calcular_subsidio(consumo, estrato):
    """Lógica de subsidios según el documento oficial de tu proyecto."""
    limite_subsidiado = min(consumo, 130)
    # Estrato 1: 60%, Estrato 2: 50%, Estrato 3: 15%
    porcentajes = {1: 0.60, 2: 0.50, 3: 0.15}
    descuento = porcentajes.get(estrato, 0)
    return limite_subsidiado, descuento

def analizar_alerta_personalizada(consumo, tamaño):
    """Lógica de alertas basada en la cantidad de personas."""
    # 1 o 2 personas
    if tamaño == "1": 
        if 80 <= consumo <= 120: return "BAJO", "Consumo eficiente."
        if 121 <= consumo <= 200: return "NORMAL", "Consumo promedio."
        if consumo > 200: return "ALTO", "Alerta: Consumo elevado para 1-2 personas."
        return "MUY BAJO", "Revisar posible falla de medidor."

    # 3 o 4 personas
    elif tamaño == "2":
        if 150 <= consumo <= 200: return "BAJO", "Consumo controlado."
        if 201 <= consumo <= 300: return "NORMAL", "Consumo estándar para familia mediana."
        if consumo > 300: return "ALTO", "Alerta: Supera el rango normal de 300 kWh."
        return "MUY BAJO", "Consumo por debajo del mínimo esperado."

    # 5 o más personas
    elif tamaño == "3":
        if 250 <= consumo <= 300: return "BAJO", "Uso de energía muy ahorrativo."
        if 301 <= consumo <= 450: return "NORMAL", "Consumo esperado para familia grande."
        if consumo > 450: return "ALTO", "Alerta Crítica: Revisar instalaciones por alto consumo."
        return "MUY BAJO", "Revisar si hay manipulación de contador."
    
    return "DESCONOCIDO", "Sin datos suficientes."

def registrar_hogar():
    print("\n" + "="*30)
    print(" REGISTRAR NUEVO HOGAR ")
    print("="*30)
    id_c = input("ID del Contador: ")
    if id_c in hogares:
        print("⚠️ Este contador ya existe.")
        return
    
    direccion = input("Dirección de Residencia: ")
    print("\nTamaño del hogar:")
    print("1. Pequeño (1-2 personas)")
    print("2. Mediano (3-4 personas)")
    print("3. Grande (5+ personas)")
    tamaño = input("Seleccione opción (1, 2 o 3): ")
    
    if tamaño not in ["1", "2", "3"]:
        print("❌ Opción inválida.")
        return

    try:
        estrato = int(input("Estrato (1, 2 o 3): "))
        if estrato not in [1, 2, 3]:
            print("❌ Solo se permiten estratos 1, 2 y 3.")
            return

        hogares[id_c] = {
            "direccion": direccion, 
            "tamaño": tamaño, 
            "estrato": estrato
        }
        print(f"✅ Hogar registrado en {direccion}.")
    except ValueError:
        print("❌ El estrato debe ser un número.")

def ingresar_lectura():
    print("\n" + "="*30)
    print(" INGRESAR CONSUMO ")
    print("="*30)
    id_c = input("ID del contador: ")
    if id_c not in hogares:
        print("❌ El contador no existe. Primero regístrelo.")
        return

    try:
        consumo = float(input("Consumo mensual en kWh: "))
        datos = hogares[id_c]
        
        estado, accion = analizar_alerta_personalizada(consumo, datos['tamaño'])
        limite, pct = calcular_subsidio(consumo, datos['estrato'])
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        registro = {
            "fecha": fecha, "id": id_c, "consumo": consumo,
            "alerta": estado, "accion": accion
        }
        historial_lecturas.append(registro)
        
        print(f"\nANÁLISIS PARA {id_c}:")
        print(f"-> Clasificación: {estado}")
        print(f"-> Acción: {accion}")
        print(f"-> Subsidio: {int(pct*100)}% aplicado a {limite} kWh.")
    except ValueError:
        print("❌ Ingrese un número válido para el consumo.")

def ver_historial():
    print("\n" + "="*60)
    print(f"{'Idx':<4} | {'Fecha':<16} | {'ID':<8} | {'kWh':<6} | {'Estado'}")
    print("-" * 60)
    if not historial_lecturas:
        print("No hay registros en el historial.")
    else:
        for i, r in enumerate(historial_lecturas):
            print(f"{i:<4} | {r['fecha']:<16} | {r['id']:<8} | {r['consumo']:<6} | {r['alerta']}")

def eliminar_datos():
    print("\n--- ELIMINAR ---")
    print("1. Eliminar un Contador")
    print("2. Eliminar un registro del historial")
    op = input("Seleccione (1 o 2): ")

    if op == "1":
        id_c = input("ID del contador a borrar: ")
        if id_c in hogares:
            del hogares[id_c]
            # Borrar también sus lecturas
            global historial_lecturas
            historial_lecturas = [r for r in historial_lecturas if r['id'] != id_c]
            print(f"✅ Contador {id_c} eliminado.")
        else:
            print("❌ No encontrado.")
    elif op == "2":
        ver_historial()
        try:
            idx = int(input("Índice a borrar: "))
            historial_lecturas.pop(idx)
            print("✅ Registro borrado.")
        except:
            print("❌ Índice inválido.")

def menu():
    while True:
        print("\n" + "*"*35)
        print("  SISTEMA ENERGÉTICO SOACHA - SENA ")
        print("*"*35)
        print("1. Registrar Hogar")
        print("2. Ingresar Lectura")
        print("3. Ver Historial")
        print("4. Eliminar Contador o Registro")
        print("5. Salir")
        opcion = input("Elija una opción: ")

        if opcion == "1": registrar_hogar()
        elif opcion == "2": ingresar_lectura()
        elif opcion == "3": ver_historial()
        elif opcion == "4": eliminar_datos()
        elif opcion == "5": 
            print("Cerrando programa...")
            break
        else:
            print("Opción no válida.")

# ESTO ES LO QUE HACE QUE EL PROGRAMA ARRANQUE
if __name__ == "__main__":
    menu()