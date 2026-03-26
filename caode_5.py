import datetime

# --- BASE DE DATOS EN MEMORIA ---
hogares = {}  
historial_lecturas = []

def calcular_subsidio(consumo, estrato):
    """Calcula subsidios sobre los primeros 130 kWh."""
    limite_subsidiado = min(consumo, 130)
    # Solo estratos 1, 2 y 3 tienen subsidio según tu proyecto
    porcentajes = {1: 0.60, 2: 0.50, 3: 0.15}
    descuento = porcentajes.get(estrato, 0)
    return limite_subsidiado, descuento

def analizar_alerta_personalizada(consumo, tamaño):
    """Lógica de alertas con mensajes directos para el técnico."""
    MSG_FRAUDE = "Consumo muy bajo. ENVIAR TÉCNICO POR POSIBLE FRAUDE."
    MSG_NORMAL = "Consumo Normal."
    MSG_FALLA = "Consumo demasiado elevado. ENVIAR TÉCNICO POR POSIBLE FALLA ELÉCTRICA."

    if tamaño == "1": # 1-2 personas
        if consumo < 80: return "BAJO", MSG_FRAUDE
        if 80 <= consumo <= 200: return "ESTABLE", MSG_NORMAL
        return "ALTO", MSG_FALLA
    elif tamaño == "2": # 3-4 personas
        if consumo < 150: return "BAJO", MSG_FRAUDE
        if 150 <= consumo <= 300: return "ESTABLE", MSG_NORMAL
        return "ALTO", MSG_FALLA
    elif tamaño == "3": # 5+ personas
        if consumo < 250: return "BAJO", MSG_FRAUDE
        if 250 <= consumo <= 450: return "ESTABLE", MSG_NORMAL
        return "ALTO", MSG_FALLA
    
    return "ERROR", "Datos de tamaño inválidos."

def registrar_hogar():
    print("\n" + "="*40)
    print("      REGISTRO DE PROPIEDAD - CODENSA")
    print("="*40)
    
    id_c = input("ID del Contador/Medidor: ")
    if id_c in hogares:
        print("⚠️ Este contador ya está registrado.")
        return
    
    direccion = input("Dirección y Casa/Apto: ")

    # VALIDACIÓN DEL TAMAÑO (No sale de aquí hasta que sea 1, 2 o 3)
    while True:
        print("\nConfiguración de carga:")
        print("1. Hogar Pequeño (1-2 personas)")
        print("2. Hogar Mediano (3-4 personas)")
        print("3. Hogar Grande (5+ personas)")
        tamaño = input("Seleccione (1, 2 o 3): ")
        if tamaño in ["1", "2", "3"]:
            break
        else:
            print("❌ Error: Selección inválida. Intente de nuevo.")

    # VALIDACIÓN DEL ESTRATO (No sale de aquí hasta que sea 1, 2 o 3 y sea NÚMERO)
    while True:
        try:
            estrato = int(input("Estrato Socioeconómico (1, 2 o 3): "))
            if estrato in [1, 2, 3]:
                break # Dato correcto, salimos del bucle
            else:
                print("❌ Error: El estrato debe ser 1, 2 o 3. El estrato 4 no existe en este sistema.")
        except ValueError:
            print("❌ Error: Entrada inválida. Por favor ingrese solo el NÚMERO del estrato.")

    hogares[id_c] = {
        "direccion": direccion, 
        "tamaño": tamaño, 
        "estrato": estrato
    }
    print(f"\n✅ Registro completado exitosamente para el contador {id_c}.")

def ingresar_lectura():
    print("\n" + "="*40)
    print("      NUEVA LECTURA DE CONSUMO")
    print("="*40)
    id_c = input("Ingrese ID del contador: ")
    if id_c not in hogares:
        print("❌ El contador no existe.")
        return

    # VALIDACIÓN DEL CONSUMO (Evita que letras rompan el programa)
    while True:
        try:
            consumo = float(input("Consumo registrado (kWh): "))
            if consumo < 0:
                print("❌ El consumo no puede ser negativo.")
                continue
            break
        except ValueError:
            print("❌ Error: Ingrese un valor numérico (ejemplo: 150.5).")

    datos = hogares[id_c]
    estado, accion = analizar_alerta_personalizada(consumo, datos['tamaño'])
    limite, pct = calcular_subsidio(consumo, datos['estrato'])
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    historial_lecturas.append({
        "fecha": fecha, "id": id_c, "consumo": consumo,
        "alerta": estado, "accion": accion
    })
    
    print(f"\n--- REPORTE GENERADO ---")
    print(f"Estado: {estado}")
    print(f"Acción: {accion}")

def ver_historial():
    print("\n" + "="*85)
    print(f"{'Índice':<6} | {'Fecha':<16} | {'Contador':<10} | {'kWh':<6} | {'Acción del Técnico'}")
    print("-" * 85)
    if not historial_lecturas:
        print("No hay registros.")
    else:
        for i, r in enumerate(historial_lecturas):
            print(f"{i:<6} | {r['fecha']:<16} | {r['id']:<10} | {r['consumo']:<6} | {r['accion']}")

def eliminar_datos():
    print("\n1. Borrar Contador | 2. Borrar Registro Histórico")
    op = input("Opción: ")
    if op == "1":
        id_c = input("ID a borrar: ")
        if id_c in hogares:
            del hogares[id_c]
            global historial_lecturas
            historial_lecturas = [r for r in historial_lecturas if r['id'] != id_c]
            print("✅ Datos eliminados.")
    elif op == "2":
        ver_historial()
        try:
            idx = int(input("Índice a eliminar: "))
            historial_lecturas.pop(idx)
            print("✅ Registro eliminado.")
        except:
            print("❌ Error al eliminar.")

def menu():
    while True:
        print("\n" + "*"*40)
        print("  SISTEMA DE GESTIÓN ENERGÉTICA SOACHA")
        print("*"*40)
        print("1. Registrar Hogar")
        print("2. Ingresar Lectura")
        print("3. Ver Historial")
        print("4. Eliminar Información")
        print("5. Salir")
        opcion = input("Seleccione: ")

        if opcion == "1": registrar_hogar()
        elif opcion == "2": ingresar_lectura()
        elif opcion == "3": ver_historial()
        elif opcion == "4": eliminar_datos()
        elif opcion == "5": break
        else: print("Opción no válida.")

if __name__ == "__main__":
    menu()