"""
Problema 5: Sistema de Riego Automatizado para Agricultura
========================================================

Sistema básico que implementa las 4 funciones requeridas para
demostrar programación modular en riego automatizado.
"""

import random
import datetime

# Variables globales del sistema
secciones_campo = {
    "SECCION_A": {"cultivo": "Tomate", "area_ha": 2.5, "humedad_actual": 45, "humedad_optima": 70, "valvula": "VALV_A"},
    "SECCION_B": {"cultivo": "Lechuga", "area_ha": 1.8, "humedad_actual": 65, "humedad_optima": 75, "valvula": "VALV_B"},
    "SECCION_C": {"cultivo": "Maíz", "area_ha": 4.0, "humedad_actual": 38, "humedad_optima": 65, "valvula": "VALV_C"},
    "SECCION_D": {"cultivo": "Pepino", "area_ha": 1.2, "humedad_actual": 72, "humedad_optima": 80, "valvula": "VALV_D"}
}

valvulas = {
    "VALV_A": {"estado": "cerrada", "caudal_lh": 1500, "presion": 2.5},
    "VALV_B": {"estado": "cerrada", "caudal_lh": 1200, "presion": 2.3},
    "VALV_C": {"estado": "cerrada", "caudal_lh": 2000, "presion": 2.8},
    "VALV_D": {"estado": "cerrada", "caudal_lh": 1000, "presion": 2.1}
}

historial_riego = []
pronostico_actual = None


def leer_sensores_humedad(seccion_id):
    """
    Función para leer datos de sensores de humedad del suelo
    
    Args:
        seccion_id (str): Identificador de la sección del campo
        
    Returns:
        dict: Datos de humedad y condiciones del suelo
        
    Rendimiento: O(1) - Acceso directo por clave
    """
    if seccion_id not in secciones_campo:
        print(f"❌ Error: Sección {seccion_id} no encontrada")
        return None
    
    seccion = secciones_campo[seccion_id]
    
    # Simular lectura de sensores con variación natural
    variacion = random.uniform(-3, 1)  # La humedad tiende a bajar
    nueva_humedad = seccion["humedad_actual"] + variacion
    nueva_humedad = max(0, min(100, nueva_humedad))  # Mantener entre 0-100%
    
    # Actualizar humedad en el sistema
    secciones_campo[seccion_id]["humedad_actual"] = nueva_humedad
    
    # Simular datos adicionales de sensores
    datos_sensor = {
        "seccion": seccion_id,
        "cultivo": seccion["cultivo"],
        "humedad_promedio": round(nueva_humedad, 1),
        "temperatura_suelo": round(random.uniform(18, 28), 1),
        "ph_suelo": round(random.uniform(6.0, 7.5), 1),
        "conductividad": round(random.uniform(0.8, 2.2), 2),
        "profundidad_sensores": [15, 30, 45],  # cm
        "humedades_profundidad": [
            round(nueva_humedad + random.uniform(-5, 5), 1),
            round(nueva_humedad + random.uniform(-3, 3), 1),
            round(nueva_humedad + random.uniform(-2, 2), 1)
        ],
        "timestamp": datetime.datetime.now()
    }
    
    print(f"💧 Sensores {seccion_id} ({seccion['cultivo']}):")
    print(f"   Humedad promedio: {datos_sensor['humedad_promedio']}%")
    print(f"   Temperatura suelo: {datos_sensor['temperatura_suelo']}°C")
    print(f"   pH: {datos_sensor['ph_suelo']}")
    print(f"   Humedades por profundidad: {datos_sensor['humedades_profundidad']}%")
    
    return datos_sensor


def consultar_pronostico_meteorologico():
    """
    Función para consultar las previsiones meteorológicas
    
    Returns:
        dict: Pronóstico meteorológico de los próximos días
        
    Rendimiento: O(1) - Consulta directa a API meteorológica
    """
    global pronostico_actual
    
    # Simular consulta a servicio meteorológico
    pronostico = {
        "ubicacion": "Campo Agrícola",
        "fecha_consulta": datetime.datetime.now(),
        "condiciones_actuales": {
            "temperatura": round(random.uniform(18, 32), 1),
            "humedad_relativa": round(random.uniform(45, 85), 1),
            "viento_kmh": round(random.uniform(5, 20), 1),
            "presion_atmosferica": round(random.uniform(1010, 1025), 1),
            "radiacion_solar": round(random.uniform(200, 900), 0),
            "precipitacion_hoy": round(random.uniform(0, 15), 1)
        },
        "pronostico_7_dias": []
    }
    
    # Generar pronóstico para 7 días
    for dia in range(1, 8):
        dia_pronostico = {
            "dia": dia,
            "fecha": (datetime.datetime.now() + datetime.timedelta(days=dia)).strftime("%Y-%m-%d"),
            "temperatura_max": round(random.uniform(22, 35), 1),
            "temperatura_min": round(random.uniform(12, 22), 1),
            "probabilidad_lluvia": round(random.uniform(0, 80), 0),
            "precipitacion_esperada": round(random.uniform(0, 25), 1),
            "humedad_relativa": round(random.uniform(50, 90), 1),
            "viento_kmh": round(random.uniform(8, 25), 1)
        }
        pronostico["pronostico_7_dias"].append(dia_pronostico)
    
    pronostico_actual = pronostico
    
    # Mostrar información relevante
    actual = pronostico["condiciones_actuales"]
    print(f"🌤️  PRONÓSTICO METEOROLÓGICO:")
    print(f"   Temperatura actual: {actual['temperatura']}°C")
    print(f"   Humedad relativa: {actual['humedad_relativa']}%")
    print(f"   Precipitación hoy: {actual['precipitacion_hoy']} mm")
    print(f"   Viento: {actual['viento_kmh']} km/h")
    
    # Resumen próximos 3 días
    lluvia_3_dias = sum(d["precipitacion_esperada"] for d in pronostico["pronostico_7_dias"][:3])
    print(f"   Lluvia próximos 3 días: {lluvia_3_dias:.1f} mm")
    
    dias_con_lluvia = sum(1 for d in pronostico["pronostico_7_dias"][:3] if d["probabilidad_lluvia"] > 60)
    print(f"   Días con alta probabilidad de lluvia: {dias_con_lluvia}/3")
    
    return pronostico


def calcular_cantidad_riego_optima(seccion_id, datos_sensor):
    """
    Procedimiento para calcular la cantidad óptima de riego
    
    Args:
        seccion_id (str): Identificador de la sección
        datos_sensor (dict): Datos del sensor de humedad
        
    Rendimiento: O(1) - Cálculos aritméticos directos
    """
    if seccion_id not in secciones_campo:
        print(f"❌ Error: Sección {seccion_id} no encontrada")
        return None
    
    seccion = secciones_campo[seccion_id]
    humedad_actual = datos_sensor["humedad_promedio"]
    humedad_optima = seccion["humedad_optima"]
    area_ha = seccion["area_ha"]
    
    print(f"\n🧮 CÁLCULO DE RIEGO - {seccion_id}:")
    print(f"   Cultivo: {seccion['cultivo']}")
    print(f"   Área: {area_ha} hectáreas")
    print(f"   Humedad actual: {humedad_actual}%")
    print(f"   Humedad óptima: {humedad_optima}%")
    
    # Verificar si necesita riego
    deficit_humedad = humedad_optima - humedad_actual
    
    if deficit_humedad <= 5:  # Tolerancia de 5%
        print(f"   ✅ No requiere riego (déficit: {deficit_humedad:.1f}%)")
        return {
            "necesita_riego": False,
            "deficit_humedad": deficit_humedad,
            "cantidad_litros": 0,
            "duracion_minutos": 0,
            "motivo": "Humedad suficiente"
        }
    
    # Calcular cantidad de agua necesaria
    # Fórmula simplificada: 1% de déficit = 100L por hectárea
    litros_por_ha_por_deficit = 100
    cantidad_base = deficit_humedad * litros_por_ha_por_deficit * area_ha
    
    # Ajustes según condiciones
    factor_temperatura = 1.0
    factor_viento = 1.0
    factor_lluvia = 1.0
    
    if pronostico_actual:
        temp_actual = pronostico_actual["condiciones_actuales"]["temperatura"]
        viento = pronostico_actual["condiciones_actuales"]["viento_kmh"]
        lluvia_pronosticada = sum(d["precipitacion_esperada"] for d in pronostico_actual["pronostico_7_dias"][:2])
        
        # Ajuste por temperatura (más calor = más agua)
        if temp_actual > 28:
            factor_temperatura = 1.3
        elif temp_actual > 25:
            factor_temperatura = 1.1
        elif temp_actual < 20:
            factor_temperatura = 0.9
        
        # Ajuste por viento (más viento = más evaporación)
        if viento > 15:
            factor_viento = 1.2
        elif viento > 10:
            factor_viento = 1.1
        
        # Ajuste por lluvia pronosticada
        if lluvia_pronosticada > 20:
            factor_lluvia = 0.5  # Reducir significativamente
        elif lluvia_pronosticada > 10:
            factor_lluvia = 0.7
        elif lluvia_pronosticada > 5:
            factor_lluvia = 0.9
    
    # Calcular cantidad final
    cantidad_final = cantidad_base * factor_temperatura * factor_viento * factor_lluvia
    
    # Calcular duración del riego
    valvula_id = seccion["valvula"]
    caudal_lh = valvulas[valvula_id]["caudal_lh"]
    duracion_horas = cantidad_final / caudal_lh
    duracion_minutos = duracion_horas * 60
    
    # Limitar duración máxima (2 horas)
    if duracion_minutos > 120:
        duracion_minutos = 120
        cantidad_final = caudal_lh * 2  # Recalcular cantidad
    
    resultado = {
        "necesita_riego": True,
        "deficit_humedad": round(deficit_humedad, 1),
        "cantidad_litros": round(cantidad_final, 0),
        "duracion_minutos": round(duracion_minutos, 0),
        "caudal_lh": caudal_lh,
        "factores_aplicados": {
            "temperatura": factor_temperatura,
            "viento": factor_viento,
            "lluvia": factor_lluvia
        },
        "costo_estimado": round(cantidad_final * 0.001, 2),  # $0.001 por litro
        "humedad_esperada": min(100, humedad_actual + (deficit_humedad * 0.8))
    }
    
    print(f"   💧 Cantidad recomendada: {resultado['cantidad_litros']} litros")
    print(f"   ⏱️  Duración: {resultado['duracion_minutos']} minutos")
    print(f"   💰 Costo estimado: ${resultado['costo_estimado']}")
    print(f"   📈 Humedad esperada: {resultado['humedad_esperada']:.1f}%")
    print(f"   🔧 Factores: Temp {factor_temperatura}x, Viento {factor_viento}x, Lluvia {factor_lluvia}x")
    
    return resultado


def controlar_valvulas_riego(plan_riego):
    """
    Función para controlar las válvulas de riego en diferentes secciones del campo
    
    Args:
        plan_riego (dict): Diccionario con secciones y sus planes de riego
        
    Returns:
        dict: Resultado del control de válvulas
        
    Rendimiento: O(n) donde n = número de secciones a regar
    """
    print(f"\n🔧 CONTROL DE VÁLVULAS:")
    print("-" * 30)
    
    resultado_control = {
        "timestamp": datetime.datetime.now(),
        "secciones_programadas": len(plan_riego),
        "valvulas_activadas": 0,
        "valvulas_error": 0,
        "volumen_total": 0,
        "duracion_total": 0,
        "costo_total": 0,
        "activaciones_exitosas": [],
        "errores": []
    }
    
    for seccion_id, plan in plan_riego.items():
        if seccion_id not in secciones_campo:
            error = f"Sección {seccion_id} no existe"
            resultado_control["errores"].append(error)
            print(f"❌ {error}")
            continue
        
        if not plan["necesita_riego"]:
            print(f"⏭️  {seccion_id}: No requiere riego")
            continue
        
        seccion = secciones_campo[seccion_id]
        valvula_id = seccion["valvula"]
        
        if valvula_id not in valvulas:
            error = f"Válvula {valvula_id} no encontrada para {seccion_id}"
            resultado_control["errores"].append(error)
            print(f"❌ {error}")
            continue
        
        valvula = valvulas[valvula_id]
        
        # Verificar condiciones para activar válvula
        if valvula["presion"] < 2.0:
            error = f"Presión insuficiente en {valvula_id} ({valvula['presion']} bar)"
            resultado_control["errores"].append(error)
            print(f"⚠️  {error}")
            resultado_control["valvulas_error"] += 1
            continue
        
        if valvula["estado"] == "averiada":
            error = f"Válvula {valvula_id} averiada"
            resultado_control["errores"].append(error)
            print(f"❌ {error}")
            resultado_control["valvulas_error"] += 1
            continue
        
        # Activar válvula
        try:
            # Simular activación (95% de éxito)
            if random.random() > 0.05:
                valvulas[valvula_id]["estado"] = "abierta"
                
                activacion = {
                    "seccion": seccion_id,
                    "valvula": valvula_id,
                    "cultivo": seccion["cultivo"],
                    "cantidad_litros": plan["cantidad_litros"],
                    "duracion_minutos": plan["duracion_minutos"],
                    "caudal_lh": plan["caudal_lh"],
                    "hora_inicio": datetime.datetime.now(),
                    "hora_fin_estimada": datetime.datetime.now() + datetime.timedelta(minutes=plan["duracion_minutos"]),
                    "costo": plan["costo_estimado"]
                }
                
                resultado_control["activaciones_exitosas"].append(activacion)
                resultado_control["valvulas_activadas"] += 1
                resultado_control["volumen_total"] += plan["cantidad_litros"]
                resultado_control["duracion_total"] += plan["duracion_minutos"]
                resultado_control["costo_total"] += plan["costo_estimado"]
                
                # Registrar en historial
                historial_riego.append({
                    "fecha": datetime.datetime.now(),
                    "seccion": seccion_id,
                    "cantidad": plan["cantidad_litros"],
                    "duracion": plan["duracion_minutos"],
                    "motivo": "Riego automático programado"
                })
                
                print(f"✅ {seccion_id} ({seccion['cultivo']}):")
                print(f"    Válvula {valvula_id} ACTIVADA")
                print(f"    {plan['cantidad_litros']} L en {plan['duracion_minutos']} min")
                print(f"    Fin estimado: {activacion['hora_fin_estimada'].strftime('%H:%M')}")
                
            else:
                # Simular fallo
                error = f"Fallo en activación de {valvula_id}"
                resultado_control["errores"].append(error)
                resultado_control["valvulas_error"] += 1
                print(f"❌ {error}")
                
        except Exception as e:
            error = f"Error inesperado en {valvula_id}: {str(e)}"
            resultado_control["errores"].append(error)
            resultado_control["valvulas_error"] += 1
            print(f"❌ {error}")
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DE ACTIVACIÓN:")
    print(f"   Válvulas activadas: {resultado_control['valvulas_activadas']}")
    print(f"   Válvulas con error: {resultado_control['valvulas_error']}")
    print(f"   Volumen total: {resultado_control['volumen_total']} litros")
    print(f"   Tiempo total de riego: {resultado_control['duracion_total']} minutos")
    print(f"   Costo total: ${resultado_control['costo_total']:.2f}")
    
    return resultado_control


def mostrar_estado_sistema():
    """Función auxiliar para mostrar el estado general del sistema"""
    print("\n🌾 ESTADO GENERAL DEL SISTEMA:")
    print("-" * 40)
    
    for seccion_id, seccion in secciones_campo.items():
        humedad = seccion["humedad_actual"]
        optima = seccion["humedad_optima"]
        
        if humedad >= optima - 5:
            estado = "🟢 ÓPTIMO"
        elif humedad >= optima - 15:
            estado = "🟡 NECESITA RIEGO"
        else:
            estado = "🔴 CRÍTICO"
        
        print(f"{estado} {seccion_id}: {seccion['cultivo']}")
        print(f"    Humedad: {humedad:.1f}% (óptimo: {optima}%)")
        print(f"    Área: {seccion['area_ha']} ha")
        print(f"    Válvula: {seccion['valvula']} ({valvulas[seccion['valvula']]['estado']})")


def main():
    """Función principal para demostrar el sistema"""
    print("=== SISTEMA DE RIEGO AUTOMATIZADO ===\n")
    
    # Mostrar estado inicial
    mostrar_estado_sistema()
    
    # Consultar pronóstico meteorológico
    print()
    pronostico = consultar_pronostico_meteorologico()
    
    # Leer sensores y calcular necesidades de riego
    plan_riego = {}
    
    print(f"\n🔍 ANÁLISIS DE NECESIDADES DE RIEGO:")
    print("=" * 45)
    
    for seccion_id in secciones_campo:
        print(f"\n--- {seccion_id} ---")
        
        # Leer sensores
        datos_sensor = leer_sensores_humedad(seccion_id)
        
        # Calcular cantidad óptima de riego
        calculo_riego = calcular_cantidad_riego_optima(seccion_id, datos_sensor)
        
        if calculo_riego:
            plan_riego[seccion_id] = calculo_riego
    
    # Ejecutar plan de riego
    if any(plan["necesita_riego"] for plan in plan_riego.values()):
        resultado = controlar_valvulas_riego(plan_riego)
    else:
        print(f"\n✅ Todas las secciones tienen humedad suficiente - No se requiere riego")
        resultado = {"mensaje": "No se requiere riego"}
    
    # Estado final del sistema
    print()
    mostrar_estado_sistema()
    
    # Resumen del ciclo
    print(f"\n{'='*40}")
    print("RESUMEN DEL CICLO DE RIEGO")
    print("=" * 40)
    
    secciones_evaluadas = len(secciones_campo)
    secciones_regadas = resultado.get("valvulas_activadas", 0)
    
    print(f"🌾 Secciones evaluadas: {secciones_evaluadas}")
    print(f"💧 Secciones regadas: {secciones_regadas}")
    
    if "volumen_total" in resultado:
        print(f"🚰 Volumen total aplicado: {resultado['volumen_total']} litros")
        print(f"💰 Costo total: ${resultado['costo_total']:.2f}")
        print(f"⏱️  Tiempo total de riego: {resultado['duracion_total']} minutos")
    
    print(f"📊 Registros en historial: {len(historial_riego)}")
    
    # Próximo análisis recomendado
    proxima_revision = datetime.datetime.now() + datetime.timedelta(hours=6)
    print(f"⏰ Próxima revisión recomendada: {proxima_revision.strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()