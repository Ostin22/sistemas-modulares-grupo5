"""
Problema 4: Optimización de la Producción en una Fábrica
======================================================

Sistema básico que implementa las 4 funciones requeridas para
demostrar programación modular en optimización de producción.
"""

import random
import datetime

# Variables globales de la fábrica
maquinas = {
    "MAQ001": {"nombre": "Prensa A", "estado": "operativa", "eficiencia": 85, "horas_uso": 120, "ultimo_mantenimiento": "2024-01-15"},
    "MAQ002": {"nombre": "Torno B", "estado": "operativa", "eficiencia": 78, "horas_uso": 200, "ultimo_mantenimiento": "2024-01-10"},
    "MAQ003": {"nombre": "Soldadora C", "estado": "mantenimiento", "eficiencia": 92, "horas_uso": 50, "ultimo_mantenimiento": "2024-01-20"},
    "MAQ004": {"nombre": "Fresadora D", "estado": "operativa", "eficiencia": 88, "horas_uso": 180, "ultimo_mantenimiento": "2024-01-05"}
}

ordenes_produccion = [
    {"id": "ORD001", "producto": "Pieza A", "cantidad": 100, "prioridad": "alta", "estado": "pendiente"},
    {"id": "ORD002", "producto": "Pieza B", "cantidad": 50, "prioridad": "media", "estado": "pendiente"},
    {"id": "ORD003", "producto": "Pieza C", "cantidad": 200, "prioridad": "baja", "estado": "en_proceso"}
]

historial_produccion = []
mantenimientos_programados = []


def monitorear_estado_maquinas():
    """
    Función para monitorear el estado de las máquinas
    
    Returns:
        dict: Estado detallado de todas las máquinas
        
    Rendimiento: O(n) donde n = número de máquinas
    """
    estado_general = {
        "timestamp": datetime.datetime.now(),
        "maquinas_operativas": 0,
        "maquinas_mantenimiento": 0,
        "maquinas_averiadas": 0,
        "eficiencia_promedio": 0,
        "alertas": []
    }
    
    eficiencias = []
    
    print("🏭 MONITOREO DE MÁQUINAS:")
    print("-" * 40)
    
    for id_maquina, maquina in maquinas.items():
        # Simular actualización de datos en tiempo real
        # Variación pequeña en eficiencia
        variacion = random.uniform(-5, 3)
        maquina["eficiencia"] += variacion
        maquina["eficiencia"] = max(0, min(100, maquina["eficiencia"]))  # Mantener entre 0-100
        
        # Incrementar horas de uso si está operativa
        if maquina["estado"] == "operativa":
            maquina["horas_uso"] += random.uniform(0.5, 2.0)
        
        # Determinar estado actual
        estado = maquina["estado"]
        eficiencia = maquina["eficiencia"]
        horas_uso = maquina["horas_uso"]
        
        # Contar estados
        if estado == "operativa":
            estado_general["maquinas_operativas"] += 1
            eficiencias.append(eficiencia)
        elif estado == "mantenimiento":
            estado_general["maquinas_mantenimiento"] += 1
        else:
            estado_general["maquinas_averiadas"] += 1
        
        # Generar alertas
        alertas_maquina = []
        
        if eficiencia < 70:
            alertas_maquina.append("Eficiencia baja")
            estado_general["alertas"].append(f"{id_maquina}: Eficiencia crítica ({eficiencia:.1f}%)")
        
        if horas_uso > 200:
            alertas_maquina.append("Requiere mantenimiento")
            estado_general["alertas"].append(f"{id_maquina}: Muchas horas de uso ({horas_uso:.1f}h)")
        
        if estado == "averiada":
            alertas_maquina.append("AVERIADA")
            estado_general["alertas"].append(f"{id_maquina}: Máquina averiada")
        
        # Mostrar estado de la máquina
        icono = "🟢" if estado == "operativa" else "🟡" if estado == "mantenimiento" else "🔴"
        print(f"{icono} {id_maquina}: {maquina['nombre']}")
        print(f"    Estado: {estado.upper()}")
        print(f"    Eficiencia: {eficiencia:.1f}%")
        print(f"    Horas de uso: {horas_uso:.1f}h")
        
        if alertas_maquina:
            print(f"    ⚠️  Alertas: {', '.join(alertas_maquina)}")
        print()
    
    # Calcular eficiencia promedio
    if eficiencias:
        estado_general["eficiencia_promedio"] = sum(eficiencias) / len(eficiencias)
    
    print(f"📊 RESUMEN GENERAL:")
    print(f"   Operativas: {estado_general['maquinas_operativas']}")
    print(f"   En mantenimiento: {estado_general['maquinas_mantenimiento']}")
    print(f"   Averiadas: {estado_general['maquinas_averiadas']}")
    print(f"   Eficiencia promedio: {estado_general['eficiencia_promedio']:.1f}%")
    print(f"   Total alertas: {len(estado_general['alertas'])}")
    
    return estado_general


def planificar_mantenimiento_preventivo():
    """
    Procedimiento para planificar el mantenimiento preventivo
    
    Rendimiento: O(n) donde n = número de máquinas
    """
    global mantenimientos_programados
    
    print("\n🔧 PLANIFICACIÓN DE MANTENIMIENTO:")
    print("-" * 40)
    
    mantenimientos_nuevos = []
    fecha_actual = datetime.datetime.now()
    
    for id_maquina, maquina in maquinas.items():
        # Evaluar necesidad de mantenimiento
        horas_uso = maquina["horas_uso"]
        eficiencia = maquina["eficiencia"]
        estado = maquina["estado"]
        
        # Parsear fecha de último mantenimiento
        try:
            ultimo_mant = datetime.datetime.strptime(maquina["ultimo_mantenimiento"], "%Y-%m-%d")
            dias_sin_mantenimiento = (fecha_actual - ultimo_mant).days
        except:
            dias_sin_mantenimiento = 30  # Valor por defecto
        
        # Determinar si necesita mantenimiento
        necesita_mantenimiento = False
        tipo_mantenimiento = ""
        prioridad = ""
        fecha_programada = None
        
        if estado == "averiada":
            necesita_mantenimiento = True
            tipo_mantenimiento = "CORRECTIVO"
            prioridad = "CRITICA"
            fecha_programada = fecha_actual + datetime.timedelta(hours=2)
        
        elif horas_uso > 200:
            necesita_mantenimiento = True
            tipo_mantenimiento = "PREVENTIVO"
            prioridad = "ALTA"
            fecha_programada = fecha_actual + datetime.timedelta(days=1)
        
        elif eficiencia < 75:
            necesita_mantenimiento = True
            tipo_mantenimiento = "PREDICTIVO"
            prioridad = "MEDIA"
            fecha_programada = fecha_actual + datetime.timedelta(days=3)
        
        elif dias_sin_mantenimiento > 30:
            necesita_mantenimiento = True
            tipo_mantenimiento = "PREVENTIVO"
            prioridad = "NORMAL"
            fecha_programada = fecha_actual + datetime.timedelta(days=7)
        
        if necesita_mantenimiento:
            # Estimar duración del mantenimiento
            duraciones = {
                "CORRECTIVO": random.uniform(4, 12),
                "PREVENTIVO": random.uniform(2, 6),
                "PREDICTIVO": random.uniform(3, 8)
            }
            
            duracion_estimada = duraciones[tipo_mantenimiento]
            
            # Crear registro de mantenimiento
            mantenimiento = {
                "id_maquina": id_maquina,
                "nombre_maquina": maquina["nombre"],
                "tipo": tipo_mantenimiento,
                "prioridad": prioridad,
                "fecha_programada": fecha_programada,
                "duracion_estimada_horas": duracion_estimada,
                "costo_estimado": duracion_estimada * 80,  # $80 por hora
                "estado": "PROGRAMADO"
            }
            
            mantenimientos_nuevos.append(mantenimiento)
            
            print(f"📅 {id_maquina}: {maquina['nombre']}")
            print(f"    Tipo: {tipo_mantenimiento} (Prioridad: {prioridad})")
            print(f"    Programado: {fecha_programada.strftime('%Y-%m-%d %H:%M')}")
            print(f"    Duración estimada: {duracion_estimada:.1f} horas")
            print(f"    Costo estimado: ${mantenimiento['costo_estimado']:.2f}")
            print()
    
    # Agregar a la lista de mantenimientos programados
    mantenimientos_programados.extend(mantenimientos_nuevos)
    
    # Ordenar por prioridad y fecha
    orden_prioridad = {"CRITICA": 1, "ALTA": 2, "MEDIA": 3, "NORMAL": 4}
    mantenimientos_programados.sort(key=lambda x: (orden_prioridad[x["prioridad"]], x["fecha_programada"]))
    
    if not mantenimientos_nuevos:
        print("✅ No se requiere mantenimiento inmediato")
    else:
        print(f"📋 {len(mantenimientos_nuevos)} mantenimientos programados")
        costo_total = sum(m["costo_estimado"] for m in mantenimientos_nuevos)
        print(f"💰 Costo total estimado: ${costo_total:.2f}")


def analizar_rendimiento_produccion():
    """
    Función para analizar el rendimiento de la producción
    
    Returns:
        dict: Análisis completo del rendimiento
        
    Rendimiento: O(n + m) donde n = máquinas, m = órdenes
    """
    print("\n📈 ANÁLISIS DE RENDIMIENTO:")
    print("-" * 40)
    
    # Calcular capacidad de producción actual
    capacidad_total = 0
    maquinas_disponibles = 0
    
    for maquina in maquinas.values():
        if maquina["estado"] == "operativa":
            # Capacidad = eficiencia * factor base (100 unidades/hora por máquina al 100%)
            capacidad_maquina = (maquina["eficiencia"] / 100) * 100
            capacidad_total += capacidad_maquina
            maquinas_disponibles += 1
    
    # Analizar órdenes de producción
    ordenes_pendientes = [o for o in ordenes_produccion if o["estado"] == "pendiente"]
    ordenes_en_proceso = [o for o in ordenes_produccion if o["estado"] == "en_proceso"]
    ordenes_completadas = [o for o in ordenes_produccion if o["estado"] == "completada"]
    
    # Calcular demanda total pendiente
    demanda_total = sum(o["cantidad"] for o in ordenes_pendientes)
    
    # Calcular tiempo estimado para completar órdenes pendientes
    if capacidad_total > 0:
        tiempo_estimado_horas = demanda_total / capacidad_total
    else:
        tiempo_estimado_horas = float('inf')
    
    # Simular datos históricos de producción
    produccion_ultima_semana = random.randint(800, 1200)
    objetivo_produccion = 1000
    
    # Calcular métricas
    eficiencia_global = (produccion_ultima_semana / objetivo_produccion) * 100
    utilizacion_maquinas = (maquinas_disponibles / len(maquinas)) * 100
    
    rendimiento = {
        "timestamp": datetime.datetime.now(),
        "capacidad_actual_unidades_hora": round(capacidad_total, 1),
        "maquinas_disponibles": maquinas_disponibles,
        "utilizacion_maquinas_porcentaje": round(utilizacion_maquinas, 1),
        "ordenes_pendientes": len(ordenes_pendientes),
        "ordenes_en_proceso": len(ordenes_en_proceso),
        "ordenes_completadas": len(ordenes_completadas),
        "demanda_pendiente": demanda_total,
        "tiempo_estimado_completion_horas": round(tiempo_estimado_horas, 2),
        "produccion_ultima_semana": produccion_ultima_semana,
        "objetivo_semanal": objetivo_produccion,
        "eficiencia_global_porcentaje": round(eficiencia_global, 1),
        "recomendaciones": []
    }
    
    # Generar recomendaciones
    if eficiencia_global < 80:
        rendimiento["recomendaciones"].append("Eficiencia por debajo del objetivo - revisar procesos")
    
    if utilizacion_maquinas < 75:
        rendimiento["recomendaciones"].append("Baja utilización de máquinas - optimizar programación")
    
    if tiempo_estimado_horas > 40:  # Más de una semana de trabajo
        rendimiento["recomendaciones"].append("Backlog alto - considerar horas extra o nuevas máquinas")
    
    if len(ordenes_pendientes) > 5:
        rendimiento["recomendaciones"].append("Muchas órdenes pendientes - priorizar programación")
    
    # Mostrar resultados
    print(f"⚡ Capacidad actual: {rendimiento['capacidad_actual_unidades_hora']} unidades/hora")
    print(f"🏭 Utilización de máquinas: {rendimiento['utilizacion_maquinas_porcentaje']}%")
    print(f"📦 Órdenes pendientes: {rendimiento['ordenes_pendientes']}")
    print(f"⏱️  Tiempo para completar backlog: {rendimiento['tiempo_estimado_completion_horas']:.1f} horas")
    print(f"📊 Producción última semana: {rendimiento['produccion_ultima_semana']} / {rendimiento['objetivo_semanal']} (objetivo)")
    print(f"✅ Eficiencia global: {rendimiento['eficiencia_global_porcentaje']}%")
    
    if rendimiento["recomendaciones"]:
        print(f"\n💡 RECOMENDACIONES:")
        for i, rec in enumerate(rendimiento["recomendaciones"], 1):
            print(f"   {i}. {rec}")
    
    return rendimiento


def ajustar_programacion_demanda(nuevas_ordenes):
    """
    Procedimiento para ajustar la programación de la producción en función de la demanda
    
    Args:
        nuevas_ordenes (list): Lista de nuevas órdenes de producción
        
    Rendimiento: O(n log n) donde n = total de órdenes
    """
    global ordenes_produccion
    
    print(f"\n📋 AJUSTE DE PROGRAMACIÓN:")
    print("-" * 40)
    
    # Agregar nuevas órdenes
    for nueva_orden in nuevas_ordenes:
        orden = {
            "id": f"ORD{len(ordenes_produccion) + 1:03d}",
            "producto": nueva_orden.get("producto", "Producto X"),
            "cantidad": nueva_orden.get("cantidad", 100),
            "prioridad": nueva_orden.get("prioridad", "media"),
            "estado": "pendiente",
            "fecha_solicitud": datetime.datetime.now()
        }
        ordenes_produccion.append(orden)
        print(f"➕ Nueva orden: {orden['id']} - {orden['producto']} ({orden['cantidad']} unidades, prioridad {orden['prioridad']})")
    
    # Ordenar órdenes por prioridad
    orden_prioridad = {"critica": 1, "alta": 2, "media": 3, "baja": 4}
    ordenes_pendientes = [o for o in ordenes_produccion if o["estado"] == "pendiente"]
    ordenes_pendientes.sort(key=lambda x: orden_prioridad.get(x["prioridad"], 5))
    
    # Calcular capacidad disponible
    capacidad_disponible = 0
    maquinas_asignables = []
    
    for id_maquina, maquina in maquinas.items():
        if maquina["estado"] == "operativa":
            capacidad_maquina = (maquina["eficiencia"] / 100) * 100  # unidades/hora
            capacidad_disponible += capacidad_maquina
            maquinas_asignables.append({
                "id": id_maquina,
                "nombre": maquina["nombre"],
                "capacidad": capacidad_maquina
            })
    
    print(f"\n🏭 Capacidad disponible: {capacidad_disponible:.1f} unidades/hora")
    print(f"⚙️  Máquinas disponibles: {len(maquinas_asignables)}")
    
    # Asignar órdenes a máquinas
    asignaciones = []
    capacidad_restante = capacidad_disponible
    
    print(f"\n📅 PROGRAMACIÓN OPTIMIZADA:")
    
    for orden in ordenes_pendientes[:5]:  # Programar máximo 5 órdenes
        if capacidad_restante <= 0:
            print(f"⚠️  Capacidad agotada - {orden['id']} queda pendiente")
            break
        
        # Calcular tiempo necesario
        tiempo_necesario = orden["cantidad"] / capacidad_restante if capacidad_restante > 0 else float('inf')
        
        if tiempo_necesario <= 8:  # Máximo 8 horas por orden
            # Asignar la mejor máquina disponible
            if maquinas_asignables:
                mejor_maquina = max(maquinas_asignables, key=lambda x: x["capacidad"])
                
                asignacion = {
                    "orden_id": orden["id"],
                    "producto": orden["producto"],
                    "cantidad": orden["cantidad"],
                    "maquina_asignada": mejor_maquina["id"],
                    "tiempo_estimado_horas": round(tiempo_necesario, 2),
                    "fecha_inicio": datetime.datetime.now() + datetime.timedelta(hours=len(asignaciones) * 2),
                    "prioridad": orden["prioridad"]
                }
                
                asignaciones.append(asignacion)
                orden["estado"] = "programado"
                
                print(f"✅ {orden['id']}: {orden['producto']}")
                print(f"    Máquina: {mejor_maquina['nombre']}")
                print(f"    Tiempo estimado: {asignacion['tiempo_estimado_horas']} horas")
                print(f"    Inicio programado: {asignacion['fecha_inicio'].strftime('%Y-%m-%d %H:%M')}")
                
                # Reducir capacidad disponible
                capacidad_restante -= mejor_maquina["capacidad"]
        else:
            print(f"⏰ {orden['id']}: Requiere demasiado tiempo ({tiempo_necesario:.1f}h) - reprogramar")
    
    # Resumen de la programación
    print(f"\n📊 RESUMEN DE PROGRAMACIÓN:")
    print(f"   Órdenes programadas: {len(asignaciones)}")
    print(f"   Órdenes pendientes: {len([o for o in ordenes_produccion if o['estado'] == 'pendiente'])}")
    
    tiempo_total = sum(a["tiempo_estimado_horas"] for a in asignaciones)
    print(f"   Tiempo total programado: {tiempo_total:.1f} horas")
    
    if asignaciones:
        fecha_completion = max(a["fecha_inicio"] for a in asignaciones) + datetime.timedelta(hours=max(a["tiempo_estimado_horas"] for a in asignaciones))
        print(f"   Completion estimado: {fecha_completion.strftime('%Y-%m-%d %H:%M')}")
    
    return asignaciones


def main():
    """Función principal para demostrar el sistema"""
    print("=== SISTEMA DE OPTIMIZACIÓN DE PRODUCCIÓN ===\n")
    
    # 1. Monitorear estado de máquinas
    estado = monitorear_estado_maquinas()
    
    # 2. Planificar mantenimiento
    planificar_mantenimiento_preventivo()
    
    # 3. Analizar rendimiento
    rendimiento = analizar_rendimiento_produccion()
    
    # 4. Simular nuevas órdenes y ajustar programación
    nuevas_ordenes = [
        {"producto": "Pieza D", "cantidad": 75, "prioridad": "alta"},
        {"producto": "Pieza E", "cantidad": 120, "prioridad": "media"},
        {"producto": "Pieza F", "cantidad": 50, "prioridad": "critica"}
    ]
    
    asignaciones = ajustar_programacion_demanda(nuevas_ordenes)
    
    # Resumen ejecutivo
    print(f"\n{'='*50}")
    print("RESUMEN EJECUTIVO")
    print("=" * 50)
    print(f"🏭 Máquinas operativas: {estado['maquinas_operativas']}/{len(maquinas)}")
    print(f"⚡ Eficiencia promedio: {estado['eficiencia_promedio']:.1f}%")
    print(f"🔧 Mantenimientos programados: {len(mantenimientos_programados)}")
    print(f"📦 Órdenes en programación: {len(asignaciones)}")
    print(f"⚠️  Alertas activas: {len(estado['alertas'])}")
    
    if estado['alertas']:
        print(f"\n🚨 ALERTAS PRINCIPALES:")
        for alerta in estado['alertas'][:3]:
            print(f"   - {alerta}")


if __name__ == "__main__":
    main()