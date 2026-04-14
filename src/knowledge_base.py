


"""
knowledge_base.py
------------------
Base de conocimiento de reglas para el motor de inferencias CRM bancario.

Contiene la función build_rules() que define las 35 reglas de negocio, canal, tipo de acción, ejecución y fallback
usando objetos Rule. Cada regla tiene condiciones y acciones asociadas, y puede ser priorizada por salience.

Las reglas están organizadas en:
 - Canal preferido según arquetipo (1-5)
 - Reglas específicas de negocio (6-9)
 - Clasificación del tipo de acción (10-14)
 - Inferencia RFM (15-18)
 - Transición del customer journey (19-23)
 - Decisión CRM general (24-30)
 - Ejecución (31-34)
 - Fallback (35)

Las reglas usan enums y predicados para máxima robustez y mantenibilidad.
"""

from __future__ import annotations

from typing import List


from actions import set_accion, set_canal, set_metadata, set_tipo_accion
from domain import Arquetipo, Canal, EtapaJourney, NivelAfinidad, TipoAccion, ValorRFM, AccionCRM, TipoEjecucion
from predicates import afinidad_es, arquetipo_es, etapa_es, resultado_sin_accion, resultado_sin_canal, valor_es
from rule_engine import Rule


def _afinidad_nivel(profile, producto: str):
    if hasattr(profile, "afinidad_de"):
        return profile.afinidad_de(producto)
    if getattr(profile, "afinidad_producto", None) == producto:
        return getattr(profile, "nivel_afinidad", None)
    return getattr(profile, "nivel_afinidad", None)


def _accion_actual(profile, result):
    return getattr(result, "accion_crm", getattr(profile, "accion_crm", None))


def _canal_actual(profile, result):
    return getattr(result, "canal_preferido", getattr(profile, "canal_preferido", None))



def build_rules() -> List[Rule]:
    """
    Construye y retorna la lista de 35 reglas de negocio para el motor de inferencias CRM.
    """
    rules: List[Rule] = []

    # 1. Canal preferido (1-5)
    rules.extend([
        Rule(0, "R1", "Regla 1", "Canal preferido para profesional joven digital", [lambda f, r: f.arquetipo == Arquetipo.PROFESIONAL_JOVEN_DIGITAL], [set_canal(Canal.APP, "Arquetipo profesional joven digital")]),
        Rule(0, "R2", "Regla 2", "Canal preferido para cliente patrimonial", [lambda f, r: f.arquetipo == Arquetipo.CLIENTE_PATRIMONIAL], [set_canal(Canal.ASESOR_PERSONAL, "Arquetipo cliente patrimonial")]),
        Rule(0, "R3", "Regla 3", "Canal preferido para familia en expansión", [lambda f, r: f.arquetipo == Arquetipo.FAMILIA_EN_EXPANSION], [set_canal(Canal.MIXTO, "Arquetipo familia en expansión")]),
        Rule(0, "R4", "Regla 4", "Canal preferido para cliente transaccional", [lambda f, r: f.arquetipo == Arquetipo.CLIENTE_TRANSACCIONAL], [set_canal(Canal.EMAIL, "Arquetipo cliente transaccional")]),
        Rule(0, "R5", "Regla 5", "Canal preferido para emprendedor pyme", [lambda f, r: f.arquetipo == Arquetipo.EMPRENDEDOR_PYME], [set_canal(Canal.ASESOR_PERSONAL, "Arquetipo emprendedor pyme")]),
    ])

    # 2. Específicas de negocio (6-9)
    rules.extend([
        Rule(0, "R6", "Regla 6", "Ofrecer inversión a cliente patrimonial con alto valor y afinidad a fondos de inversión", [lambda f, r: f.valor_rfm == ValorRFM.ALTO and f.arquetipo == Arquetipo.CLIENTE_PATRIMONIAL and f.etapa_journey == EtapaJourney.CRECIMIENTO and _afinidad_nivel(f, "fondos_inversion") == NivelAfinidad.ALTA and _accion_actual(f, r) is None], [set_accion(AccionCRM.OFRECER_INVERSION, "fondos_inversion", "Oferta de inversión para cliente patrimonial con afinidad alta")]),
        Rule(0, "R7", "Regla 7", "Ofrecer tarjeta de crédito a profesional joven digital con valor medio y afinidad alta", [lambda f, r: f.valor_rfm == ValorRFM.MEDIO and f.arquetipo == Arquetipo.PROFESIONAL_JOVEN_DIGITAL and f.etapa_journey == EtapaJourney.ACTIVACION and _afinidad_nivel(f, "tarjeta_credito") == NivelAfinidad.ALTA and _accion_actual(f, r) is None], [set_accion(AccionCRM.OFRECER_TARJETA_CREDITO, "tarjeta_credito", "Oferta de tarjeta de crédito para profesional joven digital")]),
        Rule(0, "R8", "Regla 8", "Ofrecer seguro a familia en expansión con alto valor y afinidad alta", [lambda f, r: f.valor_rfm == ValorRFM.ALTO and f.arquetipo == Arquetipo.FAMILIA_EN_EXPANSION and f.etapa_journey == EtapaJourney.MADUREZ and _afinidad_nivel(f, "seguros") == NivelAfinidad.ALTA and _accion_actual(f, r) is None], [set_accion(AccionCRM.OFRECER_SEGURO, "seguros", "Oferta de seguro para familia en expansión con afinidad alta")]),
        Rule(0, "R9", "Regla 9", "Retener con incentivo a cliente transaccional de bajo valor en riesgo de abandono", [lambda f, r: f.valor_rfm == ValorRFM.BAJO and f.arquetipo == Arquetipo.CLIENTE_TRANSACCIONAL and f.etapa_journey == EtapaJourney.RIESGO_ABANDONO and _accion_actual(f, r) is None], [set_accion(AccionCRM.RETENER_CON_INCENTIVO, None, "Retener con incentivo a cliente en riesgo de abandono")]),
    ])

    # 3. Clasificación de acción (10-14)
    rules.extend([
        Rule(0, "R10", "Regla 10", "Tipo de acción: activación", [lambda f, r: f.etapa_journey == EtapaJourney.ACTIVACION], [set_tipo_accion("activacion", "Etapa journey activación")]),
        Rule(0, "R11", "Regla 11", "Tipo de acción: crecimiento", [lambda f, r: f.etapa_journey == EtapaJourney.CRECIMIENTO], [set_tipo_accion("crecimiento", "Etapa journey crecimiento")]),
        Rule(0, "R12", "Regla 12", "Tipo de acción: fidelización", [lambda f, r: f.etapa_journey == EtapaJourney.MADUREZ], [set_tipo_accion("fidelizacion", "Etapa journey madurez")]),
        Rule(0, "R13", "Regla 13", "Tipo de acción: retención", [lambda f, r: f.etapa_journey == EtapaJourney.RIESGO_ABANDONO], [set_tipo_accion("retencion", "Etapa journey riesgo abandono")]),
        Rule(0, "R14", "Regla 14", "Tipo de acción: reactivación", [lambda f, r: f.etapa_journey == EtapaJourney.REACTIVACION], [set_tipo_accion("reactivacion", "Etapa journey reactivación")]),
    ])

    # 4. Inferencia RFM (15-18)
    rules.extend([
        Rule(0, "R15", "Regla 15", "Valor RFM alto por monetary y frequency", [lambda f, r: getattr(f, "monetary", None) == "alto" and getattr(f, "frequency", None) == "alta"], [lambda f, r: setattr(f, "valor_rfm", ValorRFM.ALTO)]),
        Rule(0, "R16", "Regla 16", "Valor RFM medio por monetary y frequency", [lambda f, r: getattr(f, "monetary", None) == "medio" and getattr(f, "frequency", None) == "media"], [lambda f, r: setattr(f, "valor_rfm", ValorRFM.MEDIO)]),
        Rule(0, "R17", "Regla 17", "Valor RFM bajo por monetary y frequency", [lambda f, r: getattr(f, "monetary", None) == "bajo" and getattr(f, "frequency", None) == "baja"], [lambda f, r: setattr(f, "valor_rfm", ValorRFM.BAJO)]),
        Rule(0, "R18", "Regla 18", "Valor RFM bajo por recency inactivo", [lambda f, r: getattr(f, "recency", None) == "inactivo"], [lambda f, r: setattr(f, "valor_rfm", ValorRFM.BAJO)]),
    ])

    # 5. Transición del customer journey (19-23)
    rules.extend([
        Rule(0, "R19", "Regla 19", "Transición a activación por recency muy reciente", [lambda f, r: getattr(f, "recency", None) == "muy_reciente"], [lambda f, r: setattr(f, "etapa_journey", EtapaJourney.ACTIVACION)]),
        Rule(0, "R20", "Regla 20", "Transición a crecimiento por recency reciente y frequency alta", [lambda f, r: getattr(f, "recency", None) == "reciente" and getattr(f, "frequency", None) == "alta"], [lambda f, r: setattr(f, "etapa_journey", EtapaJourney.CRECIMIENTO)]),
        Rule(0, "R21", "Regla 21", "Transición a madurez por recency reciente y frequency media", [lambda f, r: getattr(f, "recency", None) == "reciente" and getattr(f, "frequency", None) == "media"], [lambda f, r: setattr(f, "etapa_journey", EtapaJourney.MADUREZ)]),
        Rule(0, "R22", "Regla 22", "Transición a riesgo abandono por recency antiguo y frequency baja", [lambda f, r: getattr(f, "recency", None) == "antiguo" and getattr(f, "frequency", None) == "baja"], [lambda f, r: setattr(f, "etapa_journey", EtapaJourney.RIESGO_ABANDONO)]),
        Rule(0, "R23", "Regla 23", "Transición a reactivación por recency inactivo", [lambda f, r: getattr(f, "recency", None) == "inactivo"], [lambda f, r: setattr(f, "etapa_journey", EtapaJourney.REACTIVACION)]),
    ])

    # 6. Decisión CRM general (24-30)
    rules.extend([
        Rule(0, "R24", "Regla 24", "Activar producto si etapa es activación y no hay acción previa", [lambda f, r: f.etapa_journey == EtapaJourney.ACTIVACION and _accion_actual(f, r) is None], [set_accion(AccionCRM.ACTIVAR_PRODUCTO, None, "Activar producto en etapa activación")]),
        Rule(0, "R25", "Regla 25", "Cross selling si etapa es crecimiento, afinidad alta a fondos_inversion y no hay acción previa", [lambda f, r: f.etapa_journey == EtapaJourney.CRECIMIENTO and _afinidad_nivel(f, "fondos_inversion") == NivelAfinidad.ALTA and _accion_actual(f, r) is None], [set_accion(AccionCRM.CROSS_SELLING, None, "Cross selling en etapa crecimiento y afinidad alta a fondos_inversion")]),
        Rule(0, "R26", "Regla 26", "Asesoría financiera si etapa es crecimiento, afinidad no alta a fondos_inversion y no hay acción previa", [lambda f, r: f.etapa_journey == EtapaJourney.CRECIMIENTO and _afinidad_nivel(f, "fondos_inversion") != NivelAfinidad.ALTA and _accion_actual(f, r) is None], [set_accion(AccionCRM.ASESORIA_FINANCIERA, None, "Asesoría financiera en etapa crecimiento y afinidad no alta a fondos_inversion")]),
        Rule(0, "R27", "Regla 27", "Up selling si etapa es madurez, afinidad alta a seguros y no hay acción previa", [lambda f, r: f.etapa_journey == EtapaJourney.MADUREZ and _afinidad_nivel(f, "seguros") == NivelAfinidad.ALTA and _accion_actual(f, r) is None], [set_accion(AccionCRM.UP_SELLING, None, "Up selling en etapa madurez y afinidad alta a seguros")]),
        Rule(0, "R28", "Regla 28", "Fidelización si etapa es madurez, afinidad no alta a seguros y no hay acción previa", [lambda f, r: f.etapa_journey == EtapaJourney.MADUREZ and _afinidad_nivel(f, "seguros") != NivelAfinidad.ALTA and _accion_actual(f, r) is None], [set_accion(AccionCRM.FIDELIZACION, None, "Fidelización en etapa madurez y afinidad no alta a seguros")]),
        Rule(0, "R29", "Regla 29", "Retener con incentivo si etapa es riesgo abandono y no hay acción previa", [lambda f, r: f.etapa_journey == EtapaJourney.RIESGO_ABANDONO and _accion_actual(f, r) is None], [set_accion(AccionCRM.RETENER_CON_INCENTIVO, None, "Retener con incentivo en etapa riesgo abandono")]),
        Rule(0, "R30", "Regla 30", "Reactivar cliente si etapa es reactivación y no hay acción previa", [lambda f, r: f.etapa_journey == EtapaJourney.REACTIVACION and _accion_actual(f, r) is None], [set_accion(AccionCRM.REACTIVAR_CLIENTE, None, "Reactivar cliente en etapa reactivación")]),
    ])

    # 7. Ejecución (31-34)
    rules.extend([
        Rule(0, "R31", "Regla 31", "Ejecución: campaña digital si canal preferido es app", [lambda f, r: _canal_actual(f, r) == Canal.APP], [set_metadata("tipo_ejecucion", TipoEjecucion.CAMPANA_DIGITAL)]),
        Rule(0, "R32", "Regla 32", "Ejecución: contacto personal si canal preferido es asesor personal", [lambda f, r: _canal_actual(f, r) == Canal.ASESOR_PERSONAL], [set_metadata("tipo_ejecucion", TipoEjecucion.CONTACTO_PERSONAL)]),
        Rule(0, "R33", "Regla 33", "Ejecución: campaña email si canal preferido es email", [lambda f, r: _canal_actual(f, r) == Canal.EMAIL], [set_metadata("tipo_ejecucion", TipoEjecucion.CAMPANA_EMAIL)]),
        Rule(0, "R34", "Regla 34", "Ejecución: estrategia multicanal si canal preferido es mixto", [lambda f, r: _canal_actual(f, r) == Canal.MIXTO], [set_metadata("tipo_ejecucion", TipoEjecucion.ESTRATEGIA_MULTICANAL)]),
    ])

    # 8. Fallback (35)
    rules.append(
        Rule(0, "R35", "Regla 35", "Fallback: asesoría financiera por defecto", [lambda f, r: _accion_actual(f, r) is None], [set_accion(AccionCRM.ASESORIA_FINANCIERA, None, "No se encontró una regla más específica; se aplica fallback")])
    )

    return rules
    # Regla 4: Si arquetipo = cliente_transaccional, canal_preferido = email
