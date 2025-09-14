"""
Problema 1: Control de Temperatura en un Edificio Inteligente
===========================================================

Sistema básico que implementa las 4 funciones requeridas para
demostrar programación modular.
"""

import random
import datetime

# Variables globales para simular el estado del sistema
zonas = {
    "zona_1": {"temperatura": 22.0, "ocupacion": 5, "objetivo": 22.0},
    "zona_2": {"temperatura": 24.0, "ocupacion": 12, "objetivo": 21.0},
    "zona_3": {"temperatura": 20.0, "ocupacion": 0, "objetivo": 23.0}
}

historial_energia = []


def leer_sensores_temperatura(zona_id):
    """
    Función para leer datos de sensores de temperatura
    
    Args:
        zona_id (str): Identificador de la zona
        
    Returns:
        dict: Datos del sensor (temperatura, ocupación, hora)
        
    Rendimiento: O(1) - Acceso directo por clave
    """
    if zona_id not in zonas:
        return None
    
    # Simular lectura de sensores con variación aleatoria
    zona = zonas[zona_id]
    temperatura_actual = zona["temperatura"] + random.uniform(-1, 1)
    ocupacion_actual = zona["ocupacion"] + random.randint(-2, 3)
    ocupacion_actual = max(0, ocupacion_actual)  # No puede ser negativa
    
    datos_sensor = {
        "zona": zona_id,
        "temperatura": round(temperatura_actual, 1),
        "ocupacion": ocupacion_actual,
        "hora": datetime.datetime.now().hour,
        "timestamp": datetime.datetime.now()
    }
    
    print(f"📊 Sensor {zona_id}: {datos_sensor['temperatura']}°C, {datos_sensor['ocupacion']} personas")
    return datos_sensor


def calcular_temperatura_optima(datos_sensor, temperatura_exterior):
    """
    Función para calcular la temperatura óptima en cada zona
    
    Args:
        datos_sensor (dict): Datos del sensor de la zona
        temperatura_exterior (float): Temperatura exterior
        
    Returns:
        float: Temperatura óptima calculada
        
    Rendimiento: O(1) - Cálculos aritméticos simples
    """
    temperatura_base = 22.0  # Temperatura base de confort
    
    # Ajuste por ocupación (más personas = más calor)
    ajuste_ocupacion = datos_sensor["ocupacion"] * 0.2
    
    # Ajuste por horario (reducir temperatura en horas de menor actividad)
    hora = datos_sensor["hora"]
    if 22 <= hora or hora <= 6:  # Noche
        ajuste_horario = -2.0
    elif 9 <= hora <= 17:  # Horas de trabajo
        ajuste_horario = 0.0
    else:  # Transición
        ajuste_horario = -1.0
    
    # Ajuste por temperatura exterior
    diferencia_exterior = abs(temperatura_base - temperatura_exterior)
    if diferencia_exterior > 15:
        ajuste_exterior = 1.0 if temperatura_exterior < temperatura_base else -1.0
    else:
        ajuste_exterior = 0.0
    
    # Calcular temperatura óptima
    temp_optima = temperatura_base - ajuste_ocupacion + ajuste_horario + ajuste_exterior
    temp_optima = max(18.0, min(26.0, temp_optima))  # Limitar rango
    
    print(f"🎯 Temperatura óptima para {datos_sensor['zona']}: {temp_optima}°C")
    return round(temp_optima, 1)


def enviar_ajuste_temperatura(zona_id, temperatura_objetivo, temperatura_actual):
    """
    Procedimiento para enviar señales de ajuste al sistema de calefacción/refrigeración
    
    Args:
        zona_id (str): Zona a ajustar
        temperatura_objetivo (float): Temperatura deseada
        temperatura_actual (float): Temperatura actual
        
    Rendimiento: O(1) - Operación de envío simple
    """
    diferencia = temperatura_objetivo - temperatura_actual
    
    # Solo enviar comando si la diferencia es significativa
    if abs(diferencia) < 0.5:
        print(f"✅ {zona_id}: Temperatura estable ({temperatura_actual}°C)")
        return
    
    if diferencia > 0:
        accion = "CALENTAR"
        intensidad = min(10, int(diferencia * 2))
    else:
        accion = "ENFRIAR"
        intensidad = min(10, int(abs(diferencia) * 2))
    
    # Simular envío de comando al sistema HVAC
    print(f"🔧 COMANDO: {zona_id} - {accion} intensidad {intensidad}")
    print(f"   Objetivo: {temperatura_actual}°C → {temperatura_objetivo}°C")
    
    # Actualizar temperatura de la zona (simulación)
    if zona_id in zonas:
        zonas[zona_id]["temperatura"] = temperatura_objetivo


def registrar_consumo_energia(zona_id, accion, intensidad, duracion_horas):
    """
    Función para registrar y analizar el consumo de energía
    
    Args:
        zona_id (str): Zona donde se aplicó la acción
        accion (str): Tipo de acción (CALENTAR/ENFRIAR)
        intensidad (int): Intensidad aplicada (1-10)
        duracion_horas (float): Duración en horas
        
    Returns:
        dict: Registro del consumo de energía
        
    Rendimiento: O(1) para registro individual
    """
    # Calcular consumo basado en la acción
    consumo_por_intensidad = {
        "CALENTAR": 2.0,  # kW por intensidad
        "ENFRIAR": 2.5    # kW por intensidad
    }
    
    consumo_base = consumo_por_intensidad.get(accion, 1.0)
    consumo_total_kwh = consumo_base * intensidad * duracion_horas
    costo_energia = consumo_total_kwh * 0.15  # $0.15 por kWh
    
    registro = {
        "zona": zona_id,
        "accion": accion,
        "intensidad": intensidad,
        "duracion": duracion_horas,
        "consumo_kwh": round(consumo_total_kwh, 2),
        "costo": round(costo_energia, 2),
        "timestamp": datetime.datetime.now()
    }
    
    # Guardar en historial
    historial_energia.append(registro)
    
    print(f"⚡ Consumo registrado: {registro['consumo_kwh']} kWh - ${registro['costo']}")
    return registro


def main():
    """Función principal para demostrar el sistema"""
    print("=== SISTEMA DE CONTROL DE TEMPERATURA ===\n")
    
    temperatura_exterior = 28.0  # Temperatura exterior simulada
    print(f"🌡️ Temperatura exterior: {temperatura_exterior}°C\n")
    
    # Procesar cada zona
    for zona_id in zonas:
        print(f"--- Procesando {zona_id.upper()} ---")
        
        # 1. Leer sensores
        datos = leer_sensores_temperatura(zona_id)
        
        # 2. Calcular temperatura óptima
        temp_optima = calcular_temperatura_optima(datos, temperatura_exterior)
        
        # 3. Enviar ajuste si es necesario
        enviar_ajuste_temperatura(zona_id, temp_optima, datos["temperatura"])
        
        # 4. Registrar consumo (simulado)
        intensidad = random.randint(3, 8)
        duracion = random.uniform(0.5, 2.0)
        accion = "CALENTAR" if temp_optima > datos["temperatura"] else "ENFRIAR"
        registrar_consumo_energia(zona_id, accion, intensidad, duracion)
        
        print()
    
    # Mostrar resumen de consumo
    print("=== RESUMEN DE CONSUMO ENERGÉTICO ===")
    consumo_total = sum(r["consumo_kwh"] for r in historial_energia)
    costo_total = sum(r["costo"] for r in historial_energia)
    print(f"Consumo total: {consumo_total:.2f} kWh")
    print(f"Costo total: ${costo_total:.2f}")


if __name__ == "__main__":
    main()