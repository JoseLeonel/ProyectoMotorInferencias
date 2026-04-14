
"""
Tests para el motor de inferencia CRMRecommendationService.

Este módulo contiene pruebas unitarias para validar que el motor de inferencia
recomienda correctamente la acción CRM según el perfil del cliente, siguiendo
las reglas de negocio definidas para el sistema basado en conocimiento bancario.

Casos cubiertos:
- Cliente patrimonial de alto valor en crecimiento con afinidad alta a fondos de inversión.
- Profesional joven digital de valor medio en activación con afinidad alta a tarjeta de crédito.
- Cliente transaccional de bajo valor en riesgo de abandono (ver test_retencion_transaccional).

Cada test crea un perfil de cliente y verifica que la acción recomendada
corresponde a la esperada según las reglas del dominio.
"""
import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from domain import Arquetipo, ClienteProfile, EtapaJourney, NivelAfinidad, ProductoAfinidad, ValorRFM
from service import CRMRecommendationService


class CRMEngineTest(unittest.TestCase):
    def setUp(self):
        self.service = CRMRecommendationService()

    def test_canal_profesional_joven_digital(self):
        """
        Verifica que el canal preferido para profesional joven digital es 'app'.
        """
        cliente = ClienteProfile(
            cliente_id="canal1",
            valor_rfm=ValorRFM.MEDIO,
            arquetipo=Arquetipo.PROFESIONAL_JOVEN_DIGITAL,
            etapa_journey=EtapaJourney.CRECIMIENTO,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        self.assertEqual("app", result.canal_preferido)

    def test_canal_cliente_patrimonial(self):
        """
        Verifica que el canal preferido para cliente patrimonial es 'asesor_personal'.
        """
        cliente = ClienteProfile(
            cliente_id="canal2",
            valor_rfm=ValorRFM.ALTO,
            arquetipo=Arquetipo.CLIENTE_PATRIMONIAL,
            etapa_journey=EtapaJourney.MADUREZ,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        self.assertEqual("asesor_personal", result.canal_preferido)

    def test_canal_familia_en_expansion(self):
        """
        Verifica que el canal preferido para familia en expansión es 'mixto'.
        """
        cliente = ClienteProfile(
            cliente_id="canal3",
            valor_rfm=ValorRFM.MEDIO,
            arquetipo=Arquetipo.FAMILIA_EN_EXPANSION,
            etapa_journey=EtapaJourney.CRECIMIENTO,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        self.assertEqual("mixto", result.canal_preferido)

    def test_canal_cliente_transaccional(self):
        """
        Verifica que el canal preferido para cliente transaccional es 'email'.
        """
        cliente = ClienteProfile(
            cliente_id="canal4",
            valor_rfm=ValorRFM.BAJO,
            arquetipo=Arquetipo.CLIENTE_TRANSACCIONAL,
            etapa_journey=EtapaJourney.MADUREZ,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        self.assertEqual("email", result.canal_preferido)

    def test_canal_emprendedor_pyme(self):
        """
        Verifica que el canal preferido para emprendedor pequeño empresario es 'asesor_personal'.
        """
        cliente = ClienteProfile(
            cliente_id="canal5",
            valor_rfm=ValorRFM.MEDIO,
            arquetipo=Arquetipo.EMPRENDEDOR_PYME,
            etapa_journey=EtapaJourney.CRECIMIENTO,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        self.assertEqual("asesor_personal", result.canal_preferido)

    def test_tipo_accion_activacion(self):
        """
        Verifica que la etapa 'activacion' clasifica la acción como 'activación'.
        """
        cliente = ClienteProfile(
            cliente_id="tipo1",
            valor_rfm=ValorRFM.MEDIO,
            arquetipo=Arquetipo.FAMILIA_EN_EXPANSION,
            etapa_journey=EtapaJourney.ACTIVACION,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        from domain import TipoAccion
        self.assertEqual(TipoAccion.ACTIVACION, result.tipo_accion)

    def test_tipo_accion_crecimiento(self):
        """
        Verifica que la etapa 'crecimiento' clasifica la acción como 'crecimiento'.
        """
        cliente = ClienteProfile(
            cliente_id="tipo2",
            valor_rfm=ValorRFM.ALTO,
            arquetipo=Arquetipo.CLIENTE_PATRIMONIAL,
            etapa_journey=EtapaJourney.CRECIMIENTO,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        self.assertEqual("crecimiento", result.tipo_accion)

    def test_tipo_accion_madurez(self):
        """
        Verifica que la etapa 'madurez' clasifica la acción como 'fidelizacion'.
        """
        cliente = ClienteProfile(
            cliente_id="tipo3",
            valor_rfm=ValorRFM.ALTO,
            arquetipo=Arquetipo.FAMILIA_EN_EXPANSION,
            etapa_journey=EtapaJourney.MADUREZ,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        self.assertEqual("fidelizacion", result.tipo_accion)

    def test_tipo_accion_retencion(self):
        """
        Verifica que la etapa 'riesgo_abandono' clasifica la acción como 'retención'.
        """
        cliente = ClienteProfile(
            cliente_id="tipo4",
            valor_rfm=ValorRFM.BAJO,
            arquetipo=Arquetipo.CLIENTE_TRANSACCIONAL,
            etapa_journey=EtapaJourney.RIESGO_ABANDONO,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        from domain import TipoAccion
        self.assertEqual(TipoAccion.RETENCION, result.tipo_accion)

    def test_tipo_accion_reactivacion(self):
        """
        Verifica que la etapa 'reactivacion' clasifica la acción como 'reactivación'.
        """
        cliente = ClienteProfile(
            cliente_id="tipo5",
            valor_rfm=ValorRFM.BAJO,
            arquetipo=Arquetipo.CLIENTE_TRANSACCIONAL,
            etapa_journey=EtapaJourney.REACTIVACION,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        from domain import TipoAccion
        self.assertEqual(TipoAccion.REACTIVACION, result.tipo_accion)
    def setUp(self):
        self.service = CRMRecommendationService()

    def test_inversion_patrimonial(self):
        """
        Verifica que un cliente patrimonial de alto valor en etapa de crecimiento
        y afinidad alta a fondos de inversión recibe la acción 'ofrecer_inversion'.
        """
        cliente = ClienteProfile(
            cliente_id="1",
            valor_rfm=ValorRFM.ALTO,
            arquetipo=Arquetipo.CLIENTE_PATRIMONIAL,
            etapa_journey=EtapaJourney.CRECIMIENTO,
            afinidades=[ProductoAfinidad("fondos_inversion", NivelAfinidad.ALTA)],
        )
        result = self.service.recomendar(cliente)
        self.assertEqual("ofrecer_inversion", result.accion_crm)

    def test_tarjeta_profesional_joven(self):
        """
        Verifica que un profesional joven digital de valor medio en activación
        y afinidad alta a tarjeta de crédito recibe la acción 'ofrecer_tarjeta_credito'.
        """
        cliente = ClienteProfile(
            cliente_id="2",
            valor_rfm=ValorRFM.MEDIO,
            arquetipo=Arquetipo.PROFESIONAL_JOVEN_DIGITAL,
            etapa_journey=EtapaJourney.ACTIVACION,
            afinidades=[ProductoAfinidad("tarjeta_credito", NivelAfinidad.ALTA)],
        )
        result = self.service.recomendar(cliente)
        self.assertEqual("ofrecer_tarjeta_credito", result.accion_crm)

    def test_retencion_transaccional(self):
        """
        Verifica que un cliente transaccional de bajo valor en riesgo de abandono
        recibe la acción 'retener_con_incentivo'.
        """
        cliente = ClienteProfile(
            cliente_id="3",
            valor_rfm=ValorRFM.BAJO,
            arquetipo=Arquetipo.CLIENTE_TRANSACCIONAL,
            etapa_journey=EtapaJourney.RIESGO_ABANDONO,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        self.assertEqual("retener_con_incentivo", result.accion_crm)

    def test_fallback(self):
        cliente = ClienteProfile(
            cliente_id="4",
            valor_rfm=ValorRFM.BAJO,
            arquetipo=Arquetipo.EMPRENDEDOR_PYME,
            etapa_journey=EtapaJourney.ADQUISICION,
            afinidades=[],
        )
        result = self.service.recomendar(cliente)
        self.assertEqual("asesoria_financiera", result.accion_crm)

    def test_campos_faltantes_no_detienen_inferencia(self):
        cliente = ClienteProfile(
            cliente_id="5",
            valor_rfm=None,
            arquetipo=Arquetipo.CLIENTE_PATRIMONIAL,
            etapa_journey=EtapaJourney.CRECIMIENTO,
            afinidades=None,
        )
        result = self.service.recomendar(cliente)
        self.assertIn("valor_rfm", result.campos_faltantes)
        self.assertEqual("asesoria_financiera", result.accion_crm)
        self.assertEqual("asesor_personal", result.canal_preferido)
        self.assertEqual("crecimiento", result.tipo_accion)


if __name__ == "__main__":
    unittest.main()
