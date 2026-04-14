

"""
predicates.py
-------------
Predicados reutilizables para reglas del motor de inferencias CRM.

Cada función retorna un predicado (función booleana) que evalúa condiciones sobre el perfil del cliente o el resultado de inferencia.
Se usan en la definición de reglas para hacer el sistema flexible y expresivo.
"""

from __future__ import annotations

from typing import Iterable

from domain import Arquetipo, Canal, ClienteProfile, EtapaJourney, NivelAfinidad, ValorRFM
from domain import InferenceResult


def valor_es(*valores: ValorRFM):
    """
    Predicado: verifica si el valor RFM del cliente está en los valores dados.
    Args:
        *valores: Uno o más valores de ValorRFM.
    Returns:
        Callable que recibe (perfil, resultado) y retorna True/False.
    """
    return lambda p, r: p.valor_rfm in valores


def arquetipo_es(*arquetipos: Arquetipo):
    """
    Predicado: verifica si el arquetipo del cliente está en los arquetipos dados.
    Args:
        *arquetipos: Uno o más valores de Arquetipo.
    Returns:
        Callable que recibe (perfil, resultado) y retorna True/False.
    """
    return lambda p, r: p.arquetipo in arquetipos


def etapa_es(*etapas: EtapaJourney):
    """
    Predicado: verifica si la etapa del journey del cliente está en las etapas dadas.
    Args:
        *etapas: Uno o más valores de EtapaJourney.
    Returns:
        Callable que recibe (perfil, resultado) y retorna True/False.
    """
    return lambda p, r: p.etapa_journey in etapas


def afinidad_es(producto: str, *niveles: NivelAfinidad):
    """
    Predicado: verifica si el cliente tiene el nivel de afinidad indicado para un producto.
    Args:
        producto: Nombre del producto.
        *niveles: Uno o más niveles de NivelAfinidad.
    Returns:
        Callable que recibe (perfil, resultado) y retorna True/False.
    """
    return lambda p, r: p.afinidad_de(producto) in niveles


def resultado_sin_accion():
    """
    Predicado: verifica si aún no se ha asignado una acción CRM al resultado.
    Returns:
        Callable que recibe (perfil, resultado) y retorna True/False.
    """
    return lambda p, r: r.accion_crm is None


def resultado_sin_canal():
    """
    Predicado: verifica si aún no se ha asignado un canal preferido al resultado.
    Returns:
        Callable que recibe (perfil, resultado) y retorna True/False.
    """
    return lambda p, r: r.canal_preferido is None
