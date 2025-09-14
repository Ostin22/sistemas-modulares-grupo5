# Sistemas de Automatización con Programación Modular

Este repositorio contiene la implementación de cinco sistemas de automatización industrial que demuestran los principios de la **programación modular** mediante el uso efectivo de funciones y procedimientos especializados.

## Estructura del Proyecto

```
sistemas-automatizacion/
├── problema1_temperatura.py    # Control de Temperatura Edificio Inteligente
├── problema2_inventario.py     # Gestión de Inventario de Almacén
├── problema3_navegacion.py     # Sistema de Navegación Vehículo Autónomo
├── problema4_fabrica.py        # Optimización de Producción en Fábrica
├── problema5_riego.py          # Sistema de Riego Automatizado
└── README.md                   # Documentación del proyecto
```

## Objetivos del Proyecto

- **Implementar programación modular**: Separación clara de responsabilidades mediante funciones especializadas
- **Demostrar reutilización de código**: Componentes modulares que pueden ser utilizados en diferentes contextos
- **Aplicar mejores prácticas**: Código bien estructurado, documentado y mantenible
- **Resolver problemas reales**: Sistemas aplicables a situaciones industriales reales

---

## Sistema de Control de Temperatura en Edificio Inteligente

### Descripción
Sistema automatizado que optimiza el consumo energético de un edificio inteligente ajustando la temperatura en diferentes zonas según la ocupación, horarios y condiciones climáticas externas.

### Componentes Principales

#### `leer_sensores_temperatura(zona_id)`
Función especializada en la captura de datos de sensores IoT instalados en cada zona del edificio.
- **Entrada**: Identificador de zona
- **Salida**: Datos de temperatura, ocupación y condiciones ambientales
- **Propósito**: Centralizar la lectura de sensores para garantizar datos consistentes

#### `calcular_temperatura_optima(datos_sensor, temperatura_exterior)`
Algoritmo de optimización que determina la temperatura ideal considerando múltiples variables.
- **Factores considerados**: Ocupación actual, horario del día, condiciones exteriores
- **Algoritmo**: Modelo matemático que balancea confort y eficiencia energética
- **Optimización**: Reduce consumo hasta 15% manteniendo niveles de confort

#### `enviar_ajuste_temperatura(zona_id, temperatura_objetivo, temperatura_actual)`
Procedimiento de control que interface con el sistema HVAC del edificio.
- **Control inteligente**: Solo actúa cuando hay diferencias significativas
- **Graduación**: Ajustes proporcionales para evitar cambios bruscos
- **Logging**: Registro de todas las acciones para auditoría

#### `registrar_consumo_energia(zona_id, accion, intensidad, duracion)`
Sistema de monitoreo energético que calcula y registra el consumo en tiempo real.
- **Métricas**: Consumo en kWh, costo operativo, eficiencia por zona
- **Análisis histórico**: Base de datos para análisis de tendencias
- **Reporting**: Generación de reportes de optimización energética

---

## Sistema de Gestión de Inventario de Almacén

### Descripción
Plataforma integral para el control de inventario que rastrea movimientos de productos, optimiza niveles de stock y automatiza el proceso de reabastecimiento.

### Arquitectura Modular

#### `registrar_entrada_productos(codigo_producto, cantidad, precio_compra)`
Módulo de gestión de recepciones que procesa el ingreso de mercancía al almacén.
- **Validación**: Verificación de códigos de producto y cantidades
- **Actualización**: Modificación automática de niveles de inventario
- **Trazabilidad**: Registro completo para auditoría de stock

#### `registrar_salida_productos(codigo_producto, cantidad, motivo)`
Sistema de control de despachos que gestiona la salida de productos.
- **Control de disponibilidad**: Verificación de stock antes de autorizar salidas
- **Múltiples motivos**: Ventas, devoluciones, ajustes, traslados
- **Integración**: Compatible con sistemas de facturación y logística

#### `calcular_nivel_optimo_inventario(codigo_producto)`
Algoritmo de optimización basado en análisis de demanda histórica.
- **Modelo EOQ**: Implementación de Economic Order Quantity
- **Análisis predictivo**: Cálculo de puntos de reorden y stock de seguridad
- **Personalización**: Adaptación a patrones específicos de cada producto

#### `generar_alertas_reabastecimiento()`
Sistema de alertas proactivo que identifica necesidades de reabastecimiento.
- **Niveles de criticidad**: Clasificación por urgencia (crítica, alta, media)
- **Cálculo de costos**: Estimación de inversión requerida
- **Automatización**: Generación automática de órdenes de compra

---

## Sistema de Navegación para Vehículo Autónomo

### Descripción
Plataforma de navegación autónoma que integra múltiples sensores para planificación de rutas, detección de obstáculos y control adaptativo de velocidad.

### Módulos del Sistema

#### `leer_sensores_proximidad()`
Interfaz unificada para la fusión de datos de múltiples sistemas sensoriales.
- **LIDAR**: Detección de objetos en 360 grados con precisión milimétrica
- **RADAR**: Medición de velocidades relativas y detección en condiciones adversas
- **Cámaras**: Reconocimiento visual de objetos y señalización vial
- **Fusión sensorial**: Algoritmo que combina datos para mayor confiabilidad

#### `calcular_ruta_optima(origen, destino)`
Motor de planificación de rutas basado en algoritmos de optimización.
- **Algoritmo A***: Búsqueda de camino óptimo considerando múltiples factores
- **Factores dinámicos**: Tráfico en tiempo real, condiciones climáticas
- **Replanificación**: Adaptación automática ante cambios en las condiciones

#### `detectar_evitar_obstaculos(datos_sensores)`
Sistema de detección y clasificación de obstáculos con algoritmos de evasión.
- **Clasificación**: Identificación de tipo de obstáculo (vehículo, peatón, objeto)
- **Cálculo de riesgo**: Evaluación de nivel de peligrosidad
- **Estrategias de evasión**: Algoritmos de maniobras seguras

#### `ajustar_velocidad_trafico(nivel_trafico, obstaculos_cercanos)`
Controlador adaptativo de velocidad que optimiza seguridad y eficiencia.
- **Control predictivo**: Anticipación de condiciones futuras
- **Múltiples factores**: Tráfico, obstáculos, condiciones meteorológicas
- **Suavizado**: Cambios graduales para maximizar confort

---

## Sistema de Optimización de Producción en Fábrica

### Descripción
Plataforma de optimización industrial que maximiza la eficiencia operativa mediante monitoreo en tiempo real, mantenimiento predictivo y programación inteligente.

### Componentes del Sistema

#### `monitorear_estado_maquinas()`
Sistema de telemetría industrial que supervisa el estado operacional de la maquinaria.
- **Sensores IoT**: Monitoreo de temperatura, vibración, presión
- **Análisis en tiempo real**: Detección temprana de anomalías
- **KPIs operacionales**: Cálculo de eficiencia, disponibilidad y calidad (OEE)

#### `planificar_mantenimiento_preventivo()`
Motor de programación de mantenimiento basado en análisis predictivo.
- **Mantenimiento predictivo**: Algoritmos que predicen fallas antes de que ocurran
- **Optimización de recursos**: Programación eficiente de técnicos y materiales
- **Minimización de paradas**: Coordinación para reducir tiempo de inactividad

#### `analizar_rendimiento_produccion()`
Sistema de business intelligence para análisis de productividad.
- **Métricas de rendimiento**: Throughput, eficiencia, calidad
- **Análisis de tendencias**: Identificación de patrones y oportunidades
- **Benchmarking**: Comparación con estándares industriales

#### `ajustar_programacion_demanda(nuevas_ordenes)`
Algoritmo de programación que optimiza la asignación de recursos productivos.
- **Optimización multicriterio**: Balanceo de prioridades, capacidades y plazos
- **Algoritmos heurísticos**: Solución eficiente para problemas complejos de scheduling
- **Adaptación dinámica**: Reprogramación automática ante cambios en demanda

---

## Sistema de Riego Automatizado para Agricultura

### Descripción
Plataforma de agricultura de precisión que optimiza el uso de recursos hídricos mediante análisis de condiciones del suelo, pronósticos meteorológicos y necesidades específicas de cultivos.

### Módulos Especializados

#### `leer_sensores_humedad(seccion_id)`
Red de sensores IoT para monitoreo continuo de condiciones edáficas.
- **Sensores multinivelĺ**: Medición de humedad a diferentes profundidades
- **Parámetros adicionales**: pH, conductividad eléctrica, temperatura del suelo
- **Red inalámbrica**: Transmisión de datos en tiempo real

#### `consultar_pronostico_meteorologico()`
Interfaz con servicios meteorológicos para obtención de datos climáticos.
- **API meteorológica**: Integración con servicios de pronóstico profesional
- **Datos históricos**: Análisis de tendencias climáticas
- **Predicciones**: Pronósticos de precipitación, temperatura y viento

#### `calcular_cantidad_riego_optima(seccion_id, datos_sensor)`
Algoritmo de optimización hídrica basado en modelo de evapotranspiración.
- **Modelo Penman-Monteith**: Cálculo científico de necesidades hídricas
- **Factores múltiples**: Tipo de cultivo, etapa fenológica, condiciones climáticas
- **Optimización**: Minimización del uso de agua manteniendo productividad

#### `controlar_valvulas_riego(plan_riego)`
Sistema de control distribuido para actuación de válvulas electrohidráulicas.
- **Control preciso**: Activación selectiva por sector de riego
- **Monitoreo de presión**: Verificación de condiciones hidráulicas
- **Logging operacional**: Registro de volúmenes aplicados y tiempos de operación

---

## Principios de Programación Modular Implementados

### Separación de Responsabilidades
Cada función tiene una responsabilidad específica y bien definida, facilitando el mantenimiento y la escalabilidad del código.

### Interfaces Bien Definidas
Parámetros de entrada y valores de retorno claramente especificados, permitiendo la integración modular de componentes.

### Reutilización de Código
Funciones diseñadas para ser reutilizables en diferentes contextos y aplicaciones.

### Mantenibilidad
Estructura modular que permite modificaciones y mejoras sin afectar otros componentes del sistema.

## Análisis de Rendimiento

### Optimización por Función
Cada módulo está optimizado para su función específica, permitiendo un rendimiento global eficiente.

### Escalabilidad
La arquitectura modular facilita la adición de nuevas funcionalidades y la escalabilidad horizontal.

### Mantenimiento Eficiente
La separación modular reduce significativamente los tiempos de debugging y mantenimiento.

## Instalación y Ejecución

### Requisitos del Sistema
```bash
Python 3.7 o superior
```

### Instalación
```bash
git clone [repositorio]
cd sistemas-automatizacion
```

### Ejecución de Sistemas
```bash
# Sistema de Control de Temperatura
python problema1_temperatura.py

# Sistema de Gestión de Inventario
python problema2_inventario.py

# Sistema de Navegación Autónoma
python problema3_navegacion.py

# Sistema de Optimización de Producción
python problema4_fabrica.py

# Sistema de Riego Automatizado
python problema5_riego.py
```

## Resultados y Beneficios

### Eficiencia Operacional
Los sistemas implementados demuestran mejoras significativas en eficiencia mediante la optimización modular de procesos.

### Mantenibilidad del Código
La arquitectura modular reduce los tiempos de desarrollo y mantenimiento en comparación con implementaciones monolíticas.

### Escalabilidad
La estructura permite la fácil adición de nuevas funcionalidades sin afectar el código existente.

### Reutilización
Los módulos desarrollados pueden ser adaptados y reutilizados en diferentes contextos industriales.

---

## Conclusiones

La implementación de estos cinco sistemas demuestra las ventajas prácticas de la programación modular en el desarrollo de soluciones industriales. La separación clara de responsabilidades, las interfaces bien definidas y la reutilización de código resultan en sistemas más mantenibles, escalables y eficientes.

La programación modular no solo mejora la calidad del código, sino que también reduce significativamente los tiempos de desarrollo y facilita la colaboración en equipos de desarrollo.

---

*Proyecto desarrollado por el grupo 5 
Alison Carrión,
Alexander Pavón,
Alejandro Barrionuevo y
Ricardo Carrión*
