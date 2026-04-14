
# Sistema Basado en Conocimiento CRM Bancario

Definir un sistema modelo RFM para identificar el cliente y permitir el nivel de atención.

 Objetivos Específicos.  
    •	Definir las reglas del sistema Categorizar el valor económico de los clientes mediante la implementación de un modelo RFM (Recency, Frequency, Monetary), permitiendo priorizar el nivel de atención y recursos asignados según la rentabilidad generada

    •	Identificar y clasificar arquetipos comportamentales (como "profesional joven digital" o "familia en expansión") para contextualizar las necesidades financieras y determinar los canales de interacción preferidos de cada cliente

    •	Mapear la etapa del Customer Journey (adquisición, activación, crecimiento, madurez, riesgo de abandono o reactivación) para definir el objetivo estratégico y el momento oportuno de cada intervención del CRM

    •	Estimar la afinidad del cliente con productos específicos mediante el análisis de comportamiento histórico, con el fin de filtrar ofertas irrelevantes y aumentar las tasas de conversión en campañas de cross-selling

    •	Diseñar un motor de inferencia basado en reglas lógicas que integre las dimensiones de rentabilidad, arquetipo, etapa de vida y afinidad para automatizar la recomendación de acciones CRM personalizadas (como asesoría de inversión o incentivos de retención)

    •	Estructurar formalmente la base de conocimiento traduciendo las variables del negocio en hechos y reglas que permitan al sistema recibir el perfil de un cliente y devolver automáticamente la mejor acción posible alineada con la estrategia de marketing
Estructurar la entrevista

Proceso general de decisión

El experto indica que la lógica del CRM sigue cuatro capas principales:
    Valor del cliente (RFM): define la prioridad económica.
    Arquetipo del cliente: define el tipo de comportamiento financiero.
    Etapa del customer journey: define el objetivo de la interacción.
    Afinidad de producto: define qué oferta concreta tiene más sentido.

Ese flujo permite pasar de datos del cliente a una acción específica dentro del CRM

Conocimiento identificado en la entrevista

Experto
•	El banco no trata a todos los clientes igual; la prioridad depende del valor económico.
•	El valor económico se estima con RFM. 
•	Dos clientes con igual valor pueden requerir estrategias distintas según su arquetipo. 
•	La etapa del customer journey define cuándo intervenir. 
•	La afinidad de producto evita ofrecer productos irrelevantes. 
•	El canal de contacto depende principalmente del arquetipo. 
•	El sistema puede modelarse con hechos y reglas de producción.

Definición del cuerpo de atributos del dominio
Entidad principal: Cliente
Atributos del Cliente
valor_rfm
•	Alto
•	Medio
•	Bajo
Recency (Recencia)
Tiempo desde la última interacción relevante.
•	Muy Reciente
•	Reciente 
•	Antiguo
•	Inactivo
fequency
Frecuencia de interacción con el banco
•	alta
•	media
•	baja
monetary
Valor económico que genera el cliente con el banco
•	alto
•	medio
•	bajo
arquetipo
Tipo de comportamiento financiero del cliente
•	profesional_joven_digital: Alta adopción tecnológico, uso de app, y baja interacción en sucursales.
•	familia_en_expansion: Uso de créditos de consumo/hipotecas y necesidad de seguros.
•	cliente_patrimonial: Altos saldos, interés en inversiones y baja sensibilidad al precio.
•	cliente_transaccional: Uso básico de cuentas para depósitos y retiros
•	emprendedor_pequeno_empresario: manejo frecuente de liquidez e interés en créditos comerciales.
etapa_journey
Momento actual del cliente dentro de su relación con el banco
•	adquisición: Apertura reciente de cuenta o producto
•	activación: El cliente tiene el producto, pero requiere incentivos para su uso inicial.
•	Crecimiento: Cliente activo con potencial para aumentar su volumen de negocio o productos
•	Madurez: Relación estable con múltiples productos contratados
•	Riesgo_abandono: Detección de señales como caída en saldos o cancelación de tarjetas
•	Reactivación: Cliente inactivo que se busca recuperar
afinidad_producto
Producto o categoría con mayor probabilidad de adopción.
•	cuenta_corriente 
•	cuenta_ahorro 
•	tarjeta_credito 
•	tarjeta_debito 
•	credito_personal 
•	credito_hipotecario 
•	credito_automotriz 
•	fondos_inversion 
•	deposito_plazo 
•	seguros
nivel_afinidad
Intensidad de la afinidad con el producto.
•	alta
•	media
•	baja
canal_preferido
Acción recomendada por el sistema.
•	activar_producto 
•	ofrecer_tarjeta_credito 
•	ofrecer_seguro 
•	ofrecer_inversion 
•	retener_con_incentivo 
•	reactivar_cliente 
•	cross_selling 
•	asesoria_financiera


Definición de hechos del dominio
Los hechos son afirmaciones concretas que el sistema conoce sobre cada tipo de cliente.
       Ejemplo de hechos
•	valor_cliente = alto 
•	arquetipo = cliente_patrimonial 
•	etapa_journey = crecimiento 
•	afinidad_producto = fondos_inversion 
•	nivel_afinidad = alta 
•	canal_preferido = asesor_personal
  Otro ejemplo:
•	valor_cliente = medio 
•	arquetipo = profesional_joven_digital 
•	etapa_journey = activacion 
•	afinidad_producto = tarjeta_credito 
•	nivel_afinidad = alta 
•	canal_preferido = app
Son ejemplos extraídos de los casos concretos de la entrevista con el experto.

Reglas del negocio y producción

Reglas sobre canal preferido (relación entre arquetipo y canal)

Reglas de canal preferido
Regla 1
Si arquetipo = profesional_joven_digital
Entonces canal_preferido = app
Regla 2
Si arquetipo = cliente_patrimonial
Entonces canal_preferido = asesor_personal
Regla 3
Si arquetipo = familia_en_expansion
Entonces canal_preferido = mixto
Regla 4
Si arquetipo = cliente_transaccional
Entonces canal_preferido = email
Regla 5
Si arquetipo = emprendedor_pequeno_empresario
Entonces canal_preferido = asesor_personal
 Reglas específicas del negocio 
Regla 6
Si valor_rfm = alto
y arquetipo = cliente_patrimonial
y etapa_journey = crecimiento
y afinidad_producto = fondos_inversion
y nivel_afinidad = alta
Entonces accion_crm = ofrecer_inversion
Regla 7
Si valor_rfm = medio
y arquetipo = profesional_joven_digital
y etapa_journey = activacion
y afinidad_producto = tarjeta_credito
y nivel_afinidad = alta
Entonces accion_crm = ofrecer_tarjeta_credito
Regla 8
Si valor_rfm = alto
y arquetipo = familia_en_expansion
y etapa_journey = madurez
y afinidad_producto = seguros
y nivel_afinidad = alta
Entonces accion_crm = ofrecer_seguro
Regla 9
Si valor_rfm = bajo
y arquetipo = cliente_transaccional
y etapa_journey = riesgo_abandono
Entonces accion_crm = retener_con_incentivo
 Reglas de clasificación de acción
Regla 10
Si etapa_journey = activacion
Entonces tipo_accion = activacion
Regla 11
Si etapa_journey = crecimiento
Entonces tipo_accion = crecimiento
Regla 12
Si etapa_journey = madurez
Entonces tipo_accion = fidelizacion
Regla 13
Si etapa_journey = riesgo_abandono
Entonces tipo_accion = retencion
Regla 14
Si etapa_journey = reactivacion
Entonces tipo_accion = reactivacion
Reglas de inferencia (RFM)
Regla 15
Si monetary = alto y frequency = alta
Entonces valor_rfm = alto
Regla 16
Si monetary = medio y frequency = media
Entonces valor_rfm = medio
Regla 17
Si monetary = bajo y frequency = baja
Entonces valor_rfm = bajo
Regla 18
Si recency = inactivo
Entonces valor_rfm = bajo

Reglas de transición del customer journey
Regla 19
Si recency = muy_reciente
Entonces etapa_journey = activacion
Regla 20
Si recency = reciente y frequency = alta
Entonces etapa_journey = crecimiento
Regla 21
Si recency = reciente y frequency = media
Entonces etapa_journey = madurez
Regla 22
Si recency = antiguo y frequency = baja
Entonces etapa_journey = riesgo_abandono
Regla 23
Si recency = inactivo
Entonces etapa_journey = reactivacion

Reglas generales de decisión CRM (sin ambigüedad)
Regla 24
Si etapa_journey = activacion
y no se cumple ninguna regla específica
Entonces accion_crm = activar_producto
Regla 25
Si etapa_journey = crecimiento
y nivel_afinidad = alta
y no se cumple ninguna regla específica
Entonces accion_crm = cross_selling
Regla 26
Si etapa_journey = crecimiento
y nivel_afinidad <> alta
y no se cumple ninguna regla específica
Entonces accion_crm = asesoria_financiera
Regla 27
Si etapa_journey = madurez
y nivel_afinidad = alta
y no se cumple ninguna regla específica
Entonces accion_crm = up_selling
Regla 28
Si etapa_journey = madurez
y nivel_afinidad <> alta
y no se cumple ninguna regla específica
Entonces accion_crm = fidelizacion
Regla 29
Si etapa_journey = riesgo_abandono
y no se cumple ninguna regla específica
Entonces accion_crm = retener_con_incentivo
Regla 30
Si etapa_journey = reactivacion
y no se cumple ninguna regla específica
Entonces accion_crm = reactivar_cliente
Reglas de ejecución
Regla 31
Si canal_preferido = app
Entonces tipo_ejecucion = campaña_digital
Regla 32
Si canal_preferido = asesor_personal
Entonces tipo_ejecucion = contacto_personal
Regla 33
Si canal_preferido = email
Entonces tipo_ejecucion = campaña_email
Regla 34
Si canal_preferido = mixto
Entonces tipo_ejecucion = estrategia_multicanal
Regla fallback
Regla 35
Si ninguna regla anterior se cumple
Entonces accion_crm = asesoria_financiera


El documento agrupa las acciones precisamente en esos cuatro grandes tipos.

## Ejemplo de regla aplicada y test

### Regla 2: Canal preferido para cliente patrimonial

**Regla:**
Si el arquetipo del cliente es `cliente_patrimonial`, entonces el canal preferido será `asesor_personal`.

**Implementación en el motor de inferencia:**
```python
if cliente.arquetipo == Arquetipo.CLIENTE_PATRIMONIAL:
  cliente.canal_preferido = Canal.ASESOR_PERSONAL
```

**Test unitario asociado:**
```python
def test_regla_2(self):
  c = DummyCliente()
  c.arquetipo = Arquetipo.CLIENTE_PATRIMONIAL
  result = self.DummyResult()
  for r in self.rules:
    for cond in r.conditions:
      try:
        if cond(c, result):
          for action in r.actions:
            action(c, result)
      except Exception:
        continue
  self.assertEqual(c.canal_preferido, Canal.ASESOR_PERSONAL)
```

Motor de inferencia
Pasos  
•	Leer hechos del cliente
•	Determinar canal preferido según el arquetipo
•	Evaluar reglas de acción CRM
•	Retornar la mejor recomendación.
Entrada del sistema
•	valor_rfm 
•	arquetipo 
•	etapa_journey 
•	afinidad_producto 
•	nivel_afinidad
Proceso
•	aplicación de reglas
•	asignación de canal
•	selección de acción
Salida
•	accion_crm
•	canal_preferido
•	justificación

Este flujo  respeta la cadena decisión  : priorización económica , interpretación  del perfil , identificación del momento y selección de oferta.


## Ejecutar
```bash
python src/main.py
```

## Ejecutar pruebas
```bash
python -m unittest discover -s tests -p "test_*.py"
```
