import datetime

# --- CONFIGURACIÓN GLOBAL ---
COSTO_KWH = 850  
LIMITE_SUBSIDIO = 130  

# --- BASE DE DATOS EN MEMORIA ---
hogares = {}  
historial_lecturas = []

def calcular_factura(consumo, estrato):
    """Calcula el cobro real diferenciando lo subsidiado de lo pleno."""
    porcentajes = {1: 0.60, 2: 0.50, 3: 0.15}
    desc_pct = porcentajes.get(estrato, 0)
    kwh_subsidiados = min(consumo, LIMITE_SUBSIDIO)
    valor_subsidiado = kwh_subsidiados * COSTO_KWH * (1 - desc_pct)
    kwh_plenos = max(0, consumo - LIMITE_SUBSIDIO) # Corrección interna: consumo
    kwh_plenos = max(0, consumo - LIMITE_SUBSIDIO)
    valor_pleno = kwh_plenos * COSTO_KWH
    return valor_subsidiado + valor_pleno, desc_pct * 100

def analizar_alerta_personalizada(consumo, tamaño):
    """Detecta anomalías comparando consumo vs tamaño del hogar."""
    rangos = {"1": (30, 160), "2": (60, 220), "3": (90, 300)}
    bajo, alto = rangos.get(tamaño)
    if consumo < bajo:
        return "⚠️ SOSPECHA DE FRAUDE", "Consumo muy bajo. Revisar medidor. ENVIAR TÉCNICO."
    elif consumo > alto:
        return "🚨 CONSUMO EXCESIVO", "Consumo fuera de rango. Revisar fugas."
    else:
        return "✅ CONSUMO NORMAL", "El consumo es coherente."

def registrar_hogar():
    print("\n" + "╔" + "═"*38 + "╗")
    print("║      REGISTRO DE NUEVO CLIENTE       ║")
    print("╚" + "═"*38 + "╝")
    
    # VALIDACIÓN ID NUMÉRICO
    while True:
        id_c = input("ID del Contador (Solo números): ").strip()
        if id_c.isdigit(): break
        print("❌ Error: El ID debe contener solo números.")

    if id_c in hogares:
        print("❌ Error: Este contador ya existe."); return

    # VALIDACIÓN NOMBRE (SOLO LETRAS Y ESPACIOS)
    while True:
        nombre_input = input("Nombre del Titular (Solo letras): ").strip()
        # Verificamos que al quitar espacios, todo sean letras
        if nombre_input.replace(" ", "").isalpha() and len(nombre_input) > 2:
            nombre = nombre_input.upper()
            break
        print("❌ Error: El nombre no puede contener números, símbolos o estar vacío.")

    direccion = input("Dirección completa: ")
    
    while True: # VALIDACIÓN TAMAÑO
        print("\nCarga del Hogar: 1.Pequeño | 2.Mediano | 3.Grande")
        tam = input("Seleccione (1, 2 o 3): ")
        if tam in ["1", "2", "3"]: break
        print("❌ Selección inválida.")

    while True: # VALIDACIÓN ESTRATO
        try:
            est = int(input("Estrato (1, 2 o 3): "))
            if est in [1, 2, 3]: break
            print("❌ Solo estratos 1, 2 o 3.")
        except ValueError: print("❌ Ingrese solo el número.")

    hogares[id_c] = {"nombre": nombre, "direccion": direccion, "tamaño": tam, "estrato": est}
    print(f"✅ ¡Cliente {nombre} registrado con éxito!")

def ingresar_lectura():
    print("\n" + "╔" + "═"*38 + "╗")
    print("║     CAPTURA DE LECTURA MENSUAL       ║")
    print("╚" + "═"*38 + "╝")
    
    while True: # VALIDACIÓN ID AL BUSCAR
        id_c = input("ID del contador a buscar (Números): ").strip()
        if id_c.isdigit(): break
        print("❌ Ingrese un ID válido (Solo números).")

    if id_c not in hogares:
        print("❌ El contador no existe."); return

    while True: # VALIDACIÓN CONSUMO
        try:
            entrada = input("Lectura actual (kWh): ")
            consumo = float(entrada)
            if consumo >= 0: break
            print("❌ El consumo no puede ser negativo.")
        except ValueError: print(f"❌ '{entrada}' no es un número válido.")

    h = hogares[id_c]
    total, pct = calcular_factura(consumo, h['estrato'])
    estado, accion = analizar_alerta_personalizada(consumo, h['tamaño'])
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    historial_lecturas.append({
        "fecha": fecha, "id": id_c, "nombre": h['nombre'], 
        "consumo": consumo, "total": total, "alerta": estado, "accion": accion
    })
    
    print("\n" + "!"*45)
    print(f" FACTURA GENERADA PARA: {h['nombre']}")
    print(f" TOTAL A PAGAR: ${total:,.0f} COP (Subsidio: {pct}%)")
    print(f" ESTADO TÉCNICO: {estado}")
    print(f" RECOMENDACIÓN: {accion}")
    print("!"*45)

def ver_historial():
    print("\n" + "="*110)
    print(f"{'Fecha':<16} | {'Titular':<15} | {'kWh':<5} | {'Total ($)':<12} | {'Estado':<10} | {'Acción'}")
    print("-" * 110)
    if not historial_lecturas: print("Sin registros.")
    else:
        for r in historial_lecturas:
            print(f"{r['fecha']:<16} | {r['nombre']:<15} | {r['consumo']:<5} | ${r['total']:<11,.0f} | {r['alerta']:<10} | {r['accion'][:20]}...")

def generar_reporte_auditoria():
    print("\n" + "█"*45)
    print("   REPORTE GERENCIAL DE AUDITORÍA")
    print("█"*45)
    if not historial_lecturas: print("Sin datos."); return
    
    total_recaudo = sum(r['total'] for r in historial_lecturas)
    total_energia = sum(r['consumo'] for r in historial_lecturas)
    casos_criticos = sum(1 for r in historial_lecturas if "⚠️" in r['alerta'] or "🚨" in r['alerta'])

    print(f"💰 Dinero Total Facturado: ${total_recaudo:,.0f} COP")
    print(f"⚡ Energía Total Consumida: {total_energia:.1f} kWh")
    print(f"🔍 Visitas Técnicas Pendientes: {casos_criticos}")
    print(f"📊 Total Registros: {len(historial_lecturas)}")
    print("█"*45)

def menu():
    while True:
        print("\n" + "═"*45)
        print("   GESTOR ENERGÉTICO CODENSA - SOACHA")
        print("═"*45)
        print("1. Registrar Nuevo Cliente")
        print("2. Ver Directorio de Clientes")
        print("3. Ingresar Lectura y Facturar")
        print("4. Ver Historial de Facturación")
        print("5. Reporte Gerencial (Auditoría)")
        print("6. Salir")
        op = input("\nSeleccione una opción: ")

        if op == "1": registrar_hogar()
        elif op == "2": 
            print(f"\n{'ID':<10} | {'Titular':<20} | {'Dirección'}")
            for id_c, d in hogares.items(): print(f"{id_c:<10} | {d['nombre']:<20} | {d['direccion']}")
        elif op == "3": ingresar_lectura()
        elif op == "4": ver_historial()
        elif op == "5": generar_reporte_auditoria()
        elif op == "6": print("¡Éxitos mañana!"); break
        else: print("❌ Opción inválida.")

if __name__ == "__main__":
    menu()