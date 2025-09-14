"""
Problema 3: Sistema de Navegación para un Vehículo Autónomo
=========================================================

Sistema básico que implementa las 4 funciones requeridas para
demostrar programación modular en navegación autónoma.
"""

import random
import math
import datetime

# Variables globales del vehículo
posicion_actual = {"x": 0, "y": 0}
destino = {"x": 100, "y": 100}
velocidad_actual = 50  # km/h
obstaculos_detectados = []
ruta_actual = []


def leer_sensores_proximidad():
    """
    Función para leer datos de sensores de proximidad y cámaras
    
    Returns:
        dict: Datos de todos los sensores
        
    Rendimiento: O(n) donde n = número de sensores
    """
    sensores = {
        "lidar": [],
        "radar": [],
        "camaras": [],
        "timestamp": datetime.datetime.now()
    }
    
    # Simular lecturas de LIDAR (8 direcciones)
    direcciones = ["Norte", "NorEste", "Este", "SurEste", "Sur", "SurOeste", "Oeste", "NorOeste"]
    
    for direccion in direcciones:
        # Simular detección de objetos
        if random.random() < 0.3:  # 30% probabilidad de detectar algo
            distancia = random.uniform(5, 100)  # metros
            objeto = {
                "direccion": direccion,
                "distancia": distancia,
                "tipo": random.choice(["vehiculo", "peaton", "objeto_estatico"]),
                "velocidad": random.uniform(-20, 20) if direccion in ["Norte", "Sur"] else 0
            }
            sensores["lidar"].append(objeto)
    
    # Simular sensores RADAR (frente y atrás)
    for posicion in ["frontal", "trasero"]:
        if random.random() < 0.4:  # 40% probabilidad
            radar_data = {
                "posicion": posicion,
                "distancia": random.uniform(10, 200),
                "velocidad_relativa": random.uniform(-30, 30),
                "intensidad_señal": random.uniform(0.5, 1.0)
            }
            sensores["radar"].append(radar_data)
    
    # Simular datos de cámaras
    for camara in ["frontal", "trasera", "lateral_izq", "lateral_der"]:
        objetos_visibles = []
        num_objetos = random.randint(0, 3)
        
        for _ in range(num_objetos):
            objeto_visual = {
                "tipo": random.choice(["auto", "camion", "moto", "peaton", "señal"]),
                "distancia_estimada": random.uniform(5, 50),
                "confianza": random.uniform(0.6, 1.0)
            }
            objetos_visibles.append(objeto_visual)
        
        sensores["camaras"].append({
            "camara": camara,
            "objetos": objetos_visibles,
            "calidad_imagen": random.uniform(0.7, 1.0)
        })
    
    print(f"📡 Sensores leídos:")
    print(f"   LIDAR: {len(sensores['lidar'])} objetos detectados")
    print(f"   RADAR: {len(sensores['radar'])} señales")
    print(f"   Cámaras: {sum(len(c['objetos']) for c in sensores['camaras'])} objetos visuales")
    
    return sensores


def calcular_ruta_optima(origen, destino):
    """
    Procedimiento para calcular la ruta óptima
    
    Args:
        origen (dict): Posición de inicio {x, y}
        destino (dict): Posición de destino {x, y}
        
    Rendimiento: O(n) donde n = número de puntos intermedios
    """
    global ruta_actual
    
    # Calcular distancia total
    dx = destino["x"] - origen["x"]
    dy = destino["y"] - origen["y"]
    distancia_total = math.sqrt(dx*dx + dy*dy)
    
    # Generar puntos intermedios (ruta simple en línea recta con desviaciones)
    num_puntos = max(5, int(distancia_total / 20))  # Un punto cada 20 unidades
    ruta_actual = []
    
    for i in range(num_puntos + 1):
        factor = i / num_puntos
        
        # Posición base en línea recta
        x = origen["x"] + dx * factor
        y = origen["y"] + dy * factor
        
        # Agregar pequeñas desviaciones para simular calles reales
        if 0 < i < num_puntos:  # No desviar origen y destino
            desviacion = random.uniform(-5, 5)
            x += desviacion
            y += desviacion
        
        punto = {"x": round(x, 1), "y": round(y, 1)}
        ruta_actual.append(punto)
    
    # Calcular distancia final de la ruta
    distancia_ruta = 0
    for i in range(len(ruta_actual) - 1):
        p1 = ruta_actual[i]
        p2 = ruta_actual[i + 1]
        segmento = math.sqrt((p2["x"] - p1["x"])**2 + (p2["y"] - p1["y"])**2)
        distancia_ruta += segmento
    
    tiempo_estimado = distancia_ruta / (velocidad_actual * 1000/3600)  # Convertir km/h a m/s
    
    print(f"🗺️  Ruta calculada:")
    print(f"   Origen: ({origen['x']}, {origen['y']})")
    print(f"   Destino: ({destino['x']}, {destino['y']})")
    print(f"   Puntos intermedios: {len(ruta_actual) - 2}")
    print(f"   Distancia: {distancia_ruta:.1f} metros")
    print(f"   Tiempo estimado: {tiempo_estimado:.1f} segundos")


def detectar_evitar_obstaculos(datos_sensores):
    """
    Función para detectar y evitar obstáculos
    
    Args:
        datos_sensores (dict): Datos de todos los sensores
        
    Returns:
        list: Lista de obstáculos con recomendaciones de evasión
        
    Rendimiento: O(m) donde m = obstáculos detectados
    """
    global obstaculos_detectados
    obstaculos_detectados = []
    
    # Procesar datos de LIDAR
    for deteccion in datos_sensores["lidar"]:
        if deteccion["distancia"] < 50:  # Solo obstáculos cercanos (50m)
            obstaculo = {
                "fuente": "LIDAR",
                "direccion": deteccion["direccion"],
                "distancia": deteccion["distancia"],
                "tipo": deteccion["tipo"],
                "peligrosidad": calcular_peligrosidad(deteccion["distancia"], deteccion.get("velocidad", 0)),
                "accion_recomendada": calcular_accion_evasion(deteccion["direccion"], deteccion["distancia"])
            }
            obstaculos_detectados.append(obstaculo)
    
    # Procesar datos de RADAR
    for radar in datos_sensores["radar"]:
        if radar["distancia"] < 100:  # Radar tiene mayor alcance
            obstaculo = {
                "fuente": "RADAR",
                "direccion": radar["posicion"],
                "distancia": radar["distancia"],
                "velocidad_relativa": radar["velocidad_relativa"],
                "peligrosidad": calcular_peligrosidad(radar["distancia"], radar["velocidad_relativa"]),
                "accion_recomendada": "MANTENER_DISTANCIA" if radar["velocidad_relativa"] > -5 else "PUEDE_ADELANTAR"
            }
            obstaculos_detectados.append(obstaculo)
    
    # Procesar datos de cámaras (confirmación visual)
    for camara_data in datos_sensores["camaras"]:
        for objeto in camara_data["objetos"]:
            if objeto["distancia_estimada"] < 30 and objeto["confianza"] > 0.8:
                obstaculo = {
                    "fuente": "CAMARA",
                    "direccion": camara_data["camara"],
                    "distancia": objeto["distancia_estimada"],
                    "tipo": objeto["tipo"],
                    "confianza": objeto["confianza"],
                    "peligrosidad": calcular_peligrosidad(objeto["distancia_estimada"], 0),
                    "accion_recomendada": "CONFIRMAR_VISUAL"
                }
                obstaculos_detectados.append(obstaculo)
    
    # Filtrar obstáculos por peligrosidad
    obstaculos_criticos = [o for o in obstaculos_detectados if o["peligrosidad"] > 0.7]
    
    print(f"⚠️  Obstáculos detectados: {len(obstaculos_detectados)}")
    print(f"   Críticos: {len(obstaculos_criticos)}")
    
    for obs in obstaculos_criticos:
        print(f"   🚨 {obs['tipo']} a {obs['distancia']:.1f}m ({obs['direccion']}) - {obs['accion_recomendada']}")
    
    return obstaculos_detectados


def calcular_peligrosidad(distancia, velocidad_relativa):
    """Función auxiliar para calcular el nivel de peligro de un obstáculo"""
    peligro = 0.0
    
    # Factor distancia (más cerca = más peligroso)
    if distancia < 10:
        peligro += 0.8
    elif distancia < 25:
        peligro += 0.5
    elif distancia < 50:
        peligro += 0.2
    
    # Factor velocidad (acercándose = más peligroso)
    if velocidad_relativa > 10:  # Se acerca rápido
        peligro += 0.6
    elif velocidad_relativa > 0:  # Se acerca lento
        peligro += 0.3
    
    return min(1.0, peligro)


def calcular_accion_evasion(direccion, distancia):
    """Función auxiliar para determinar la acción de evasión"""
    if distancia < 15:
        return "FRENAR_INMEDIATAMENTE"
    elif direccion in ["Norte", "NorEste", "NorOeste"]:
        return "REDUCIR_VELOCIDAD"
    elif direccion in ["Este", "Oeste"]:
        return "CAMBIAR_CARRIL"
    else:
        return "MANTENER_CURSO"


def ajustar_velocidad_trafico(nivel_trafico, obstaculos_cercanos):
    """
    Procedimiento para ajustar la velocidad del vehículo según las condiciones del tráfico
    
    Args:
        nivel_trafico (str): Nivel de tráfico ("LIBRE", "MODERADO", "PESADO", "CONGESTION")
        obstaculos_cercanos (list): Lista de obstáculos cercanos
        
    Rendimiento: O(n) donde n = obstáculos cercanos
    """
    global velocidad_actual
    
    velocidad_anterior = velocidad_actual
    
    # Velocidad base según tráfico
    velocidades_trafico = {
        "LIBRE": 80,      # km/h
        "MODERADO": 60,
        "PESADO": 40,
        "CONGESTION": 20
    }
    
    velocidad_objetivo = velocidades_trafico.get(nivel_trafico, 50)
    
    # Ajustar por obstáculos cercanos
    obstaculos_criticos = [o for o in obstaculos_cercanos if o["peligrosidad"] > 0.7]
    
    if obstaculos_criticos:
        # Encontrar el obstáculo más cercano y peligroso
        obstaculo_mas_critico = min(obstaculos_criticos, key=lambda x: x["distancia"])
        distancia_critica = obstaculo_mas_critico["distancia"]
        
        if distancia_critica < 10:
            velocidad_objetivo = 0  # Parar
        elif distancia_critica < 20:
            velocidad_objetivo = min(velocidad_objetivo, 15)  # Muy lento
        elif distancia_critica < 50:
            velocidad_objetivo = min(velocidad_objetivo, 30)  # Lento
    
    # Aplicar cambio gradual (no cambios bruscos)
    diferencia = velocidad_objetivo - velocidad_actual
    if abs(diferencia) > 20:  # Cambio muy grande
        if diferencia > 0:
            velocidad_actual += 15  # Acelerar gradual
        else:
            velocidad_actual -= 20  # Frenar más rápido por seguridad
    else:
        velocidad_actual = velocidad_objetivo
    
    # Limitar velocidad mínima
    velocidad_actual = max(0, velocidad_actual)
    
    # Mostrar cambio si es significativo
    if abs(velocidad_actual - velocidad_anterior) > 5:
        if velocidad_actual > velocidad_anterior:
            accion = "🟢 ACELERANDO"
        elif velocidad_actual < velocidad_anterior:
            accion = "🔴 FRENANDO"
        else:
            accion = "🟡 MANTENIENDO"
        
        print(f"{accion}: {velocidad_anterior:.0f} → {velocidad_actual:.0f} km/h")
        print(f"   Motivo: Tráfico {nivel_trafico}, {len(obstaculos_criticos)} obstáculos críticos")
        
        if obstaculos_criticos:
            print(f"   Obstáculo más cercano: {obstaculo_mas_critico['distancia']:.1f}m")


def simular_avance():
    """Función auxiliar para simular el avance del vehículo"""
    global posicion_actual
    
    if not ruta_actual or velocidad_actual == 0:
        return
    
    # Calcular distancia recorrida en esta iteración (simulando 1 segundo)
    distancia_recorrida = velocidad_actual * 1000 / 3600  # km/h a m/s
    
    # Encontrar el siguiente punto en la ruta
    if len(ruta_actual) > 1:
        siguiente_punto = ruta_actual[1]
        
        # Calcular dirección hacia el siguiente punto
        dx = siguiente_punto["x"] - posicion_actual["x"]
        dy = siguiente_punto["y"] - posicion_actual["y"]
        distancia_al_punto = math.sqrt(dx*dx + dy*dy)
        
        if distancia_al_punto > 0:
            # Normalizar dirección
            dx_norm = dx / distancia_al_punto
            dy_norm = dy / distancia_al_punto
            
            # Mover hacia el siguiente punto
            posicion_actual["x"] += dx_norm * distancia_recorrida
            posicion_actual["y"] += dy_norm * distancia_recorrida
            
            # Si llegamos cerca del punto, avanzar al siguiente
            if distancia_al_punto < distancia_recorrida:
                ruta_actual.pop(0)  # Remover punto alcanzado


def main():
    """Función principal para demostrar el sistema"""
    print("=== SISTEMA DE NAVEGACIÓN AUTÓNOMA ===\n")
    
    # Posición inicial y destino
    origen = {"x": 0, "y": 0}
    destino_final = {"x": 100, "y": 100}
    
    print(f"🚗 Vehículo en posición: ({origen['x']}, {origen['y']})")
    print(f"🎯 Destino: ({destino_final['x']}, {destino_final['y']})")
    print(f"⚡ Velocidad inicial: {velocidad_actual} km/h\n")
    
    # Calcular ruta inicial
    calcular_ruta_optima(origen, destino_final)
    
    # Simular varios ciclos de navegación
    for ciclo in range(5):
        print(f"\n--- CICLO {ciclo + 1} ---")
        
        # Leer sensores
        datos = leer_sensores_proximidad()
        
        # Detectar obstáculos
        obstaculos = detectar_evitar_obstaculos(datos)
        
        # Determinar nivel de tráfico (simulado)
        nivel_trafico = random.choice(["LIBRE", "MODERADO", "PESADO", "CONGESTION"])
        
        # Ajustar velocidad
        ajustar_velocidad_trafico(nivel_trafico, obstaculos)
        
        # Simular avance
        simular_avance()
        
        # Mostrar estado actual
        distancia_restante = math.sqrt(
            (destino_final["x"] - posicion_actual["x"])**2 + 
            (destino_final["y"] - posicion_actual["y"])**2
        )
        
        print(f"📍 Posición: ({posicion_actual['x']:.1f}, {posicion_actual['y']:.1f})")
        print(f"📏 Distancia al destino: {distancia_restante:.1f}m")
        print(f"🚦 Tráfico: {nivel_trafico}")
        
        # Verificar si llegamos al destino
        if distancia_restante < 5:
            print("\n🎉 ¡DESTINO ALCANZADO!")
            break
    
    print(f"\n=== RESUMEN DEL VIAJE ===")
    print(f"Posición final: ({posicion_actual['x']:.1f}, {posicion_actual['y']:.1f})")
    print(f"Velocidad final: {velocidad_actual} km/h")
    print(f"Obstáculos detectados en total: {len(obstaculos_detectados)}")
    print(f"Puntos de ruta restantes: {len(ruta_actual)}")


if __name__ == "__main__":
    main()