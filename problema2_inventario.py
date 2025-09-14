"""
Problema 2: Gestión de Inventario en un Almacén
==============================================

Sistema básico que implementa las 4 funciones requeridas para
demostrar programación modular en gestión de inventario.
"""

import datetime

# Variables globales para simular la base de datos del almacén
inventario = {
    "PROD001": {"nombre": "Laptop", "stock": 25, "min": 10, "max": 50, "precio": 800},
    "PROD002": {"Mouse", "stock", "min", "max", "precio"},
    "PROD003": {"nombre": "Teclado", "stock": 45, "min": 15, "max": 80, "precio": 60},
    "PROD004": {"nombre": "Monitor", "stock": 8, "min": 5, "max": 30, "precio": 300}
}

movimientos = []  # Historial de movimientos


def registrar_entrada_productos(codigo_producto, cantidad, precio_compra):
    """
    Función para registrar la entrada de productos
    
    Args:
        codigo_producto (str): Código del producto
        cantidad (int): Cantidad que ingresa
        precio_compra (float): Precio de compra unitario
        
    Returns:
        bool: True si se registró exitosamente
        
    Rendimiento: O(1) - Acceso directo por clave
    """
    # Verificar que el producto existe
    if codigo_producto not in inventario:
        print(f"❌ Error: Producto {codigo_producto} no encontrado")
        return False
    
    # Verificar cantidad válida
    if cantidad <= 0:
        print(f"❌ Error: Cantidad debe ser mayor a 0")
        return False
    
    # Actualizar stock
    inventario[codigo_producto]["stock"] += cantidad
    inventario[codigo_producto]["precio"] = precio_compra
    
    # Registrar movimiento
    movimiento = {
        "tipo": "ENTRADA",
        "codigo": codigo_producto,
        "cantidad": cantidad,
        "precio": precio_compra,
        "fecha": datetime.datetime.now(),
        "stock_resultante": inventario[codigo_producto]["stock"]
    }
    movimientos.append(movimiento)
    
    producto = inventario[codigo_producto]
    print(f"✅ Entrada registrada: {cantidad} x {producto['nombre']}")
    print(f"   Stock actual: {producto['stock']} unidades")
    
    return True


def registrar_salida_productos(codigo_producto, cantidad, motivo="Venta"):
    """
    Función para registrar la salida de productos
    
    Args:
        codigo_producto (str): Código del producto
        cantidad (int): Cantidad que sale
        motivo (str): Motivo de la salida
        
    Returns:
        bool: True si se registró exitosamente
        
    Rendimiento: O(1) - Acceso directo por clave
    """
    # Verificar que el producto existe
    if codigo_producto not in inventario:
        print(f"❌ Error: Producto {codigo_producto} no encontrado")
        return False
    
    # Verificar cantidad válida
    if cantidad <= 0:
        print(f"❌ Error: Cantidad debe ser mayor a 0")
        return False
    
    producto = inventario[codigo_producto]
    
    # Verificar stock suficiente
    if producto["stock"] < cantidad:
        print(f"❌ Error: Stock insuficiente. Disponible: {producto['stock']}, Solicitado: {cantidad}")
        return False
    
    # Actualizar stock
    inventario[codigo_producto]["stock"] -= cantidad
    
    # Registrar movimiento
    movimiento = {
        "tipo": "SALIDA",
        "codigo": codigo_producto,
        "cantidad": cantidad,
        "motivo": motivo,
        "fecha": datetime.datetime.now(),
        "stock_resultante": inventario[codigo_producto]["stock"]
    }
    movimientos.append(movimiento)
    
    print(f"✅ Salida registrada: {cantidad} x {producto['nombre']}")
    print(f"   Stock actual: {producto['stock']} unidades")
    print(f"   Motivo: {motivo}")
    
    return True


def calcular_nivel_optimo_inventario(codigo_producto):
    """
    Procedimiento para calcular el nivel óptimo de inventario
    
    Args:
        codigo_producto (str): Código del producto a analizar
        
    Rendimiento: O(n) donde n = movimientos del producto
    """
    if codigo_producto not in inventario:
        print(f"❌ Error: Producto {codigo_producto} no encontrado")
        return
    
    producto = inventario[codigo_producto]
    
    # Analizar movimientos de salida para calcular demanda
    salidas = [m for m in movimientos if m["codigo"] == codigo_producto and m["tipo"] == "SALIDA"]
    
    if len(salidas) < 2:
        print(f"📊 {producto['nombre']}: Datos insuficientes para análisis")
        print(f"   Stock actual: {producto['stock']}")
        print(f"   Rango configurado: {producto['min']} - {producto['max']}")
        return
    
    # Calcular demanda promedio
    total_vendido = sum(s["cantidad"] for s in salidas)
    dias_con_ventas = len(salidas)
    demanda_promedio = total_vendido / dias_con_ventas
    
    # Calcular niveles recomendados
    # Stock de seguridad = demanda promedio * 3 días
    stock_seguridad = int(demanda_promedio * 3)
    
    # Punto de reorden = stock de seguridad + demanda durante tiempo de entrega (7 días)
    punto_reorden = int(stock_seguridad + (demanda_promedio * 7))
    
    # Stock máximo = punto de reorden + lote económico (estimado)
    lote_economico = int(demanda_promedio * 15)  # 15 días de demanda
    stock_maximo = punto_reorden + lote_economico
    
    print(f"📊 Análisis de {producto['nombre']}:")
    print(f"   Stock actual: {producto['stock']} unidades")
    print(f"   Demanda promedio: {demanda_promedio:.1f} unidades/día")
    print(f"   Stock de seguridad recomendado: {stock_seguridad}")
    print(f"   Punto de reorden recomendado: {punto_reorden}")
    print(f"   Stock máximo recomendado: {stock_maximo}")
    
    # Actualizar niveles en el sistema (opcional)
    respuesta = input(f"¿Actualizar niveles para {producto['nombre']}? (s/n): ")
    if respuesta.lower() == 's':
        inventario[codigo_producto]["min"] = punto_reorden
        inventario[codigo_producto]["max"] = stock_maximo
        print("✅ Niveles actualizados en el sistema")


def generar_alertas_reabastecimiento():
    """
    Función para generar alertas de reabastecimiento
    
    Returns:
        list: Lista de alertas generadas
        
    Rendimiento: O(n) donde n = número de productos
    """
    alertas = []
    
    print("🚨 ANÁLISIS DE REABASTECIMIENTO:")
    print("-" * 40)
    
    for codigo, producto in inventario.items():
        stock_actual = producto["stock"]
        stock_minimo = producto["min"]
        stock_maximo = producto["max"]
        
        # Determinar estado del stock
        if stock_actual <= 0:
            nivel = "CRÍTICO"
            urgencia = "INMEDIATA"
            cantidad_sugerida = stock_maximo
        elif stock_actual <= stock_minimo:
            nivel = "BAJO"
            urgencia = "ALTA"
            cantidad_sugerida = stock_maximo - stock_actual
        elif stock_actual <= stock_minimo * 1.5:
            nivel = "ADVERTENCIA"
            urgencia = "MEDIA"
            cantidad_sugerida = stock_maximo - stock_actual
        else:
            continue  # Stock suficiente, no generar alerta
        
        # Crear alerta
        alerta = {
            "codigo": codigo,
            "producto": producto["nombre"],
            "stock_actual": stock_actual,
            "stock_minimo": stock_minimo,
            "nivel": nivel,
            "urgencia": urgencia,
            "cantidad_sugerida": cantidad_sugerida,
            "costo_estimado": cantidad_sugerida * producto["precio"]
        }
        
        alertas.append(alerta)
        
        # Mostrar alerta
        print(f"⚠️  {nivel}: {producto['nombre']}")
        print(f"    Stock: {stock_actual}/{stock_minimo} (mínimo)")
        print(f"    Sugerencia: Pedir {cantidad_sugerida} unidades")
        print(f"    Costo estimado: ${alerta['costo_estimado']:.2f}")
        print()
    
    if not alertas:
        print("✅ Todos los productos tienen stock suficiente")
    else:
        print(f"📋 Total de alertas: {len(alertas)}")
    
    return alertas


def mostrar_estado_inventario():
    """Función auxiliar para mostrar el estado actual del inventario"""
    print("\n📦 ESTADO ACTUAL DEL INVENTARIO:")
    print("-" * 50)
    
    for codigo, producto in inventario.items():
        stock = producto["stock"]
        minimo = producto["min"]
        maximo = producto["max"]
        
        # Indicador visual del nivel de stock
        if stock <= 0:
            indicador = "🔴"
        elif stock <= minimo:
            indicador = "🟡"
        elif stock > maximo:
            indicador = "🔵"
        else:
            indicador = "🟢"
        
        print(f"{indicador} {codigo}: {producto['nombre']}")
        print(f"    Stock: {stock} | Rango: {minimo}-{maximo} | Precio: ${producto['precio']}")


def main():
    """Función principal para demostrar el sistema"""
    print("=== SISTEMA DE GESTIÓN DE INVENTARIO ===\n")
    
    # Mostrar estado inicial
    mostrar_estado_inventario()
    
    print("\n=== SIMULACIÓN DE MOVIMIENTOS ===")
    
    # Simular algunas entradas
    print("\n--- REGISTRANDO ENTRADAS ---")
    registrar_entrada_productos("PROD001", 10, 750)
    registrar_entrada_productos("PROD002", 50, 23)
    
    # Simular algunas salidas
    print("\n--- REGISTRANDO SALIDAS ---")
    registrar_salida_productos("PROD001", 15, "Venta corporativa")
    registrar_salida_productos("PROD002", 30, "Venta retail")
    registrar_salida_productos("PROD004", 5, "Venta online")
    
    # Calcular niveles óptimos
    print("\n--- CALCULANDO NIVELES ÓPTIMOS ---")
    calcular_nivel_optimo_inventario("PROD001")
    print()
    calcular_nivel_optimo_inventario("PROD002")
    
    # Generar alertas
    print("\n--- GENERANDO ALERTAS ---")
    alertas = generar_alertas_reabastecimiento()
    
    # Estado final
    mostrar_estado_inventario()
    
    # Resumen
    print(f"\n=== RESUMEN ===")
    print(f"Total de movimientos: {len(movimientos)}")
    print(f"Alertas generadas: {len(alertas)}")
    
    entradas = [m for m in movimientos if m["tipo"] == "ENTRADA"]
    salidas = [m for m in movimientos if m["tipo"] == "SALIDA"]
    print(f"Entradas: {len(entradas)} | Salidas: {len(salidas)}")


if __name__ == "__main__":
    main()