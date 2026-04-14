
"""
Test unitario para cada regla del sistema CRM.
"""
import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from domain import Arquetipo, ValorRFM, EtapaJourney, NivelAfinidad, Canal, AccionCRM, TipoEjecucion
from knowledge_base import build_rules

class DummyCliente:
    pass

class DummyResult:
    def add_rule(self, rule_id):
        pass

class TestReglasCRM(unittest.TestCase):
    def init_cliente(self, **kwargs):
        # Inicializa todos los atributos posibles con None y luego sobreescribe con los valores dados
        c = DummyCliente()
        # Atributos posibles según reglas y enums
        c.arquetipo = None
        c.valor_rfm = None
        c.etapa_journey = None
        c.nivel_afinidad = None
        c.canal_preferido = None
        c.afinidad_producto = None
        c.accion_crm = None
        c.tipo_accion = None
        c.tipo_ejecucion = None
        c.monetary = None
        c.frequency = None
        c.recency = None
        # Sobrescribir con valores específicos
        for k, v in kwargs.items():
            setattr(c, k, v)
        return c

    def setUp(self):
        self.rules = build_rules()

    def test_regla_1(self):
        """
        Regla 1: Si arquetipo = profesional_joven_digital, entonces canal_preferido = app.
        """
        c = self.init_cliente(arquetipo=Arquetipo.PROFESIONAL_JOVEN_DIGITAL)
        result = DummyResult()
        regla = self.rules[0]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.canal_preferido, Canal.APP)

    def test_regla_2(self):
        """
        Regla 2: Canal preferido para cliente patrimonial
        Si el arquetipo del cliente es 'cliente_patrimonial', entonces el canal preferido será 'asesor_personal'.
        """
        c = self.init_cliente(arquetipo=Arquetipo.CLIENTE_PATRIMONIAL)
        result = DummyResult()
        regla = self.rules[1]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.canal_preferido, Canal.ASESOR_PERSONAL)

   

    def test_regla_3(self):
        """
        Regla 3: Si arquetipo = familia_en_expansion, entonces canal_preferido = mixto.
        """
        c = self.init_cliente(arquetipo=Arquetipo.FAMILIA_EN_EXPANSION)
        result = DummyResult()
        regla = self.rules[2]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.canal_preferido, Canal.MIXTO)

    def test_regla_4(self):
        """
        Regla 4: Si arquetipo = cliente_transaccional, entonces canal_preferido = email.
        """
        c = self.init_cliente(arquetipo=Arquetipo.CLIENTE_TRANSACCIONAL)
        result = DummyResult()
        regla = self.rules[3]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.canal_preferido, Canal.EMAIL)

    def test_regla_5(self):
        """
        Regla 5: Si arquetipo = emprendedor_pequeno_empresario, entonces canal_preferido = asesor_personal.
        """
        c = DummyCliente()
        c.arquetipo = Arquetipo.EMPRENDEDOR_PYME
        result = DummyResult()
        regla = self.rules[4]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.canal_preferido, Canal.ASESOR_PERSONAL)

    def test_regla_6(self):
        """
        Regla 6: Si valor_rfm = alto, arquetipo = cliente_patrimonial, etapa_journey = crecimiento, afinidad_producto = fondos_inversion, nivel_afinidad = alta, entonces accion_crm = ofrecer_inversion.
        """
        c = self.init_cliente(valor_rfm=ValorRFM.ALTO, arquetipo=Arquetipo.CLIENTE_PATRIMONIAL, etapa_journey=EtapaJourney.CRECIMIENTO, afinidad_producto="fondos_inversion", nivel_afinidad=NivelAfinidad.ALTA)
        result = DummyResult()
        regla = self.rules[5]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.OFRECER_INVERSION)

    def test_regla_7(self):
        """
        Regla 7: Si valor_rfm = medio, arquetipo = profesional_joven_digital, etapa_journey = activacion, afinidad_producto = tarjeta_credito, nivel_afinidad = alta, entonces accion_crm = ofrecer_tarjeta_credito.
        """
        c = self.init_cliente(valor_rfm=ValorRFM.MEDIO, arquetipo=Arquetipo.PROFESIONAL_JOVEN_DIGITAL, etapa_journey=EtapaJourney.ACTIVACION, afinidad_producto="tarjeta_credito", nivel_afinidad=NivelAfinidad.ALTA)
        result = DummyResult()
        regla = self.rules[6]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.OFRECER_TARJETA_CREDITO)

    def test_regla_8(self):
        """
        Regla 8: Si valor_rfm = alto, arquetipo = familia_en_expansion, etapa_journey = madurez, afinidad_producto = seguros, nivel_afinidad = alta, entonces accion_crm = ofrecer_seguro.
        """
        c = self.init_cliente(valor_rfm=ValorRFM.ALTO, arquetipo=Arquetipo.FAMILIA_EN_EXPANSION, etapa_journey=EtapaJourney.MADUREZ, afinidad_producto="seguros", nivel_afinidad=NivelAfinidad.ALTA)
        result = DummyResult()
        regla = self.rules[7]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.OFRECER_SEGURO)

    def test_regla_9(self):
        """
        Regla 9: Si valor_rfm = bajo, arquetipo = cliente_transaccional, etapa_journey = riesgo_abandono, entonces accion_crm = retener_con_incentivo.
        """
        c = self.init_cliente(valor_rfm=ValorRFM.BAJO, arquetipo=Arquetipo.CLIENTE_TRANSACCIONAL, etapa_journey=EtapaJourney.RIESGO_ABANDONO)
        result = DummyResult()
        regla = self.rules[8]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.RETENER_CON_INCENTIVO)

    def test_regla_10(self):
        """
        Regla 10: Si etapa_journey = activacion, entonces tipo_accion = activacion.
        """
        c = self.init_cliente(etapa_journey=EtapaJourney.ACTIVACION)
        result = DummyResult()
        regla = self.rules[9]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.tipo_accion, "activacion")   

    def test_regla_11(self):
        """
        Regla 11: Si etapa_journey = crecimiento, entonces tipo_accion = crecimiento.
        """
        c = self.init_cliente(etapa_journey=EtapaJourney.CRECIMIENTO)
        result = DummyResult()
        regla = self.rules[10]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.tipo_accion, "crecimiento")

    def test_regla_12(self):
        """
        Regla 12: Si etapa_journey = madurez, entonces tipo_accion = fidelizacion.
        """
        c = self.init_cliente(etapa_journey=EtapaJourney.MADUREZ)
        result = DummyResult()
        regla = self.rules[11]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.tipo_accion, "fidelizacion")

    def test_regla_13(self):
        """
        Regla 13: Si etapa_journey = riesgo_abandono, entonces tipo_accion = retencion.
        """
        c = self.init_cliente(etapa_journey=EtapaJourney.RIESGO_ABANDONO)
        result = DummyResult()
        regla = self.rules[12]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.tipo_accion, "retencion")

    def test_regla_14(self):
        """
        Regla 14: Si etapa_journey = reactivacion, entonces tipo_accion = reactivacion.
        """
        c = self.init_cliente(etapa_journey=EtapaJourney.REACTIVACION)
        result = DummyResult()
        regla = self.rules[13]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.tipo_accion, "reactivacion")

    def test_regla_15(self):
        """
        Regla 15: Si monetary = alto y frequency = alta, entonces valor_rfm = alto.
        """
        c = self.init_cliente(monetary="alto", frequency="alta")
        result = DummyResult()
        regla = self.rules[14]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.valor_rfm, ValorRFM.ALTO)

    def test_regla_16(self):
        """
        Regla 16: Si monetary = medio y frequency = media, entonces valor_rfm = medio.
        """
        c = self.init_cliente(monetary="medio", frequency="media")
        result = DummyResult()
        regla = self.rules[15]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.valor_rfm, ValorRFM.MEDIO)

    def test_regla_17(self):
        """
        Regla 17: Si monetary = bajo y frequency = baja, entonces valor_rfm = bajo.
        """
        c = self.init_cliente(monetary="bajo", frequency="baja")
        result = DummyResult()
        regla = self.rules[16]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.valor_rfm, ValorRFM.BAJO)

    def test_regla_18(self):
        """
        Regla 18: Si recency = inactivo, entonces valor_rfm = bajo.
        """
        c = self.init_cliente(recency="inactivo")
        result = DummyResult()
        regla = self.rules[17]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.valor_rfm, ValorRFM.BAJO)

    def test_regla_19(self):
        """
        Regla 19: Si recency = muy_reciente, entonces etapa_journey = activacion.
        """
        c = self.init_cliente(recency="muy_reciente")
        result = DummyResult()
        regla = self.rules[18]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.etapa_journey, EtapaJourney.ACTIVACION)

    def test_regla_20(self):
        """
        Regla 20: Si recency = reciente y frequency = alta, entonces etapa_journey = crecimiento.
        """
        c = self.init_cliente(recency="reciente", frequency="alta")
        result = DummyResult()
        regla = self.rules[19]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.etapa_journey, EtapaJourney.CRECIMIENTO)

    def test_regla_21(self):
        """
        Regla 21: Si recency = reciente y frequency = media, entonces etapa_journey = madurez.
        """
        c = self.init_cliente(recency="reciente", frequency="media")
        result = DummyResult()
        regla = self.rules[20]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.etapa_journey, EtapaJourney.MADUREZ)

    def test_regla_22(self):
        """
        Regla 22: Si recency = antiguo y frequency = baja, entonces etapa_journey = riesgo_abandono.
        """
        c = self.init_cliente(recency="antiguo", frequency="baja")
        result = DummyResult()
        regla = self.rules[21]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.etapa_journey, EtapaJourney.RIESGO_ABANDONO)

    def test_regla_23(self):
        """
        Regla 23: Si recency = inactivo, entonces etapa_journey = reactivacion.
        """
        c = self.init_cliente(recency="inactivo")
        result = DummyResult()
        regla = self.rules[22]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.etapa_journey, EtapaJourney.REACTIVACION)

    def test_regla_24(self):
        """
        Regla 24: Si etapa_journey = activacion y no se cumple ninguna regla específica, entonces accion_crm = activar_producto.
        """
        # Para que no se dispare ninguna regla específica, afinidad_producto y nivel_afinidad deben ser None
        c = self.init_cliente(etapa_journey=EtapaJourney.ACTIVACION, accion_crm=None, afinidad_producto=None, nivel_afinidad=None, arquetipo=None, valor_rfm=None)
        result = DummyResult()
        regla = self.rules[23]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.ACTIVAR_PRODUCTO)

    def test_regla_25(self):
        """
        Regla 25: Si etapa_journey = crecimiento y nivel_afinidad = alta y no se cumple ninguna regla específica, entonces accion_crm = cross_selling.
        """
        c = self.init_cliente(etapa_journey=EtapaJourney.CRECIMIENTO, nivel_afinidad=NivelAfinidad.ALTA, accion_crm=None, afinidad_producto=None, arquetipo=None, valor_rfm=None)
        result = DummyResult()
        regla = self.rules[24]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.CROSS_SELLING)

    def test_regla_26(self):
        """
        Regla 26: Si etapa_journey = crecimiento y nivel_afinidad <> alta y no se cumple ninguna regla específica, entonces accion_crm = asesoria_financiera.
        """
        c = self.init_cliente(etapa_journey=EtapaJourney.CRECIMIENTO, nivel_afinidad=NivelAfinidad.MEDIA, accion_crm=None, afinidad_producto=None, arquetipo=None, valor_rfm=None)
        result = DummyResult()
        regla = self.rules[25]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.ASESORIA_FINANCIERA)

    def test_regla_27(self):
        """
        Regla 27: Si etapa_journey = madurez y nivel_afinidad = alta y no se cumple ninguna regla específica, entonces accion_crm = up_selling.
        """
        c = self.init_cliente(etapa_journey=EtapaJourney.MADUREZ, nivel_afinidad=NivelAfinidad.ALTA, accion_crm=None, afinidad_producto=None, arquetipo=None, valor_rfm=None)
        result = DummyResult()
        regla = self.rules[26]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.UP_SELLING)

    def test_regla_28(self):
        """
        Regla 28: Si etapa_journey = madurez y nivel_afinidad <> alta y no se cumple ninguna regla específica, entonces accion_crm = fidelizacion.
        """
        c = self.init_cliente(etapa_journey=EtapaJourney.MADUREZ, nivel_afinidad=NivelAfinidad.BAJA, accion_crm=None, afinidad_producto=None, arquetipo=None, valor_rfm=None)
        result = DummyResult()
        regla = self.rules[27]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.FIDELIZACION)

    def test_regla_29(self):
        """
        Regla 29: Si etapa_journey = riesgo_abandono y no se cumple ninguna regla específica, entonces accion_crm = retener_con_incentivo.
        """
        c = self.init_cliente(etapa_journey=EtapaJourney.RIESGO_ABANDONO, accion_crm=None, afinidad_producto=None, arquetipo=None, valor_rfm=None)
        result = DummyResult()
        regla = self.rules[28]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.RETENER_CON_INCENTIVO)

    def test_regla_30(self):
        """
        Regla 30: Si etapa_journey = reactivacion y no se cumple ninguna regla específica, entonces accion_crm = reactivar_cliente.
        """
        c = self.init_cliente(etapa_journey=EtapaJourney.REACTIVACION, accion_crm=None, afinidad_producto=None, arquetipo=None, valor_rfm=None)
        result = DummyResult()
        regla = self.rules[29]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.REACTIVAR_CLIENTE)

    def test_regla_31(self):
        """
        Regla 31: Si canal_preferido = app, entonces tipo_ejecucion = campaña_digital.
        """
        c = self.init_cliente(canal_preferido=Canal.APP)
        result = DummyResult()
        regla = self.rules[30]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.tipo_ejecucion, TipoEjecucion.CAMPANA_DIGITAL)

    def test_regla_32(self):
        """
        Regla 32: Si canal_preferido = asesor_personal, entonces tipo_ejecucion = contacto_personal.
        """
        c = self.init_cliente(canal_preferido=Canal.ASESOR_PERSONAL)
        result = DummyResult()
        regla = self.rules[31]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.tipo_ejecucion, TipoEjecucion.CONTACTO_PERSONAL)

    def test_regla_33(self):
        """
        Regla 33: Si canal_preferido = email, entonces tipo_ejecucion = campaña_email.
        """
        c = self.init_cliente(canal_preferido=Canal.EMAIL)
        result = DummyResult()
        regla = self.rules[32]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.tipo_ejecucion, TipoEjecucion.CAMPANA_EMAIL)

    def test_regla_34(self):
        """
        Regla 34: Si canal_preferido = mixto, entonces tipo_ejecucion = estrategia_multicanal.
        """
        c = self.init_cliente(canal_preferido=Canal.MIXTO)
        result = DummyResult()
        regla = self.rules[33]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.tipo_ejecucion, TipoEjecucion.ESTRATEGIA_MULTICANAL)

    def test_regla_35(self):
        """
        Regla 35: Si ninguna regla anterior se cumple, entonces accion_crm = asesoria_financiera.
        """
        c = self.init_cliente()
        result = DummyResult()
        regla = self.rules[34]
        if all(cond(c, result) for cond in regla.conditions):
            for action in regla.actions:
                action(c, result)
        self.assertEqual(c.accion_crm, AccionCRM.ASESORIA_FINANCIERA)

  

if __name__ == "__main__":
    unittest.main()
