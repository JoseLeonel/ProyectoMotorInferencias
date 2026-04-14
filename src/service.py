

"""
service.py
----------
Servicio de recomendación CRM: fachada para el motor de inferencias.

Provee una interfaz sencilla para obtener recomendaciones CRM a partir del perfil de cliente,
ocultando la complejidad del motor de reglas y la base de conocimiento.
"""

from __future__ import annotations

from domain import ClienteProfile
from knowledge_base import build_rules
from rule_engine import RuleEngine



class CRMRecommendationService:
    """
    Servicio de recomendación CRM: expone el método recomendar para obtener recomendaciones.
    """
    def __init__(self) -> None:
        """
        Inicializa el servicio con el motor de reglas y la base de conocimiento.
        """
        self.engine = RuleEngine(build_rules())

    def recomendar(self, profile: ClienteProfile):
        """
        Ejecuta el motor de inferencias sobre el perfil de cliente y retorna el resultado.
        Args:
            profile: ClienteProfile con los datos del cliente.
        Returns:
            InferenceResult con la recomendación CRM.
        """
        return self.engine.run(profile)
