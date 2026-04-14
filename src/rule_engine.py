

"""
rule_engine.py
--------------
Motor de reglas para el sistema de inferencias CRM.

Define la clase Rule y RuleEngine para modelar reglas de negocio, su evaluación y ejecución.
Permite construir sistemas expertos basados en reglas con prioridad (salience) y condiciones/acciones flexibles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

from domain import ClienteProfile, InferenceResult


Condition = Callable[[ClienteProfile, InferenceResult], bool]
Action = Callable[[ClienteProfile, InferenceResult], None]



@dataclass(order=True)
class Rule:
    """
    Representa una regla de negocio con condiciones, acciones y prioridad (salience).
    """
    salience: int
    rule_id: str = field(compare=False)
    name: str = field(compare=False)
    description: str = field(compare=False)
    conditions: List[Condition] = field(compare=False, default_factory=list)
    actions: List[Action] = field(compare=False, default_factory=list)
    stop_on_fire: bool = field(compare=False, default=False)

    def matches(self, profile: ClienteProfile, result: InferenceResult) -> bool:
        """
        Evalúa si todas las condiciones de la regla se cumplen para el perfil y resultado dados.
        """
        return all(condition(profile, result) for condition in self.conditions)

    def fire(self, profile: ClienteProfile, result: InferenceResult) -> None:
        """
        Ejecuta todas las acciones de la regla y registra la regla disparada en el resultado.
        """
        for action in self.actions:
            action(profile, result)
        result.add_rule(self.rule_id)



class RuleEngine:
    """
    Motor de reglas: evalúa y ejecuta reglas sobre un perfil de cliente.
    """
    def __init__(self, rules: List[Rule]) -> None:
        """
        Inicializa el motor con una lista de reglas, ordenadas por prioridad (salience).
        """
        self.rules = sorted(rules, reverse=True)

    def run(self, profile: ClienteProfile) -> InferenceResult:
        """
        Ejecuta el motor de reglas sobre un perfil de cliente y retorna el resultado de inferencia.
        """
        result = InferenceResult()
        for field_name in profile.campos_faltantes():
            result.add_missing_field(field_name)

        if result.campos_faltantes:
            result.metadata["campos_faltantes"] = list(result.campos_faltantes)
            result.add_reason(
                "Campos faltantes en el perfil: " + ", ".join(result.campos_faltantes)
            )

        for rule in self.rules:
            if rule.matches(profile, result):
                rule.fire(profile, result)
                if rule.stop_on_fire:
                    break
        return result
