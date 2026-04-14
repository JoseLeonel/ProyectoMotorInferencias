
from __future__ import annotations

from typing import Optional

from domain import Canal, ClienteProfile, InferenceResult, TipoAccion


def _append_reason(result: InferenceResult, reason: str) -> None:
    if not reason:
        return
    if hasattr(result, "add_reason"):
        result.add_reason(reason)
        return
    razones = getattr(result, "razones", None)
    if isinstance(razones, list):
        razones.append(reason)


def set_canal(canal: Canal, reason: str):
    def _action(profile: ClienteProfile, result: InferenceResult) -> None:
        result.canal_preferido = canal
        setattr(profile, "canal_preferido", canal)
        _append_reason(result, reason)
    return _action


def set_tipo_accion(tipo: TipoAccion, reason: str):
    def _action(profile: ClienteProfile, result: InferenceResult) -> None:
        result.tipo_accion = tipo
        setattr(profile, "tipo_accion", tipo)
        _append_reason(result, reason)
    return _action


def set_accion(accion: str, producto_objetivo: Optional[str], reason: str):
    def _action(profile: ClienteProfile, result: InferenceResult) -> None:
        result.accion_crm = accion
        result.producto_objetivo = producto_objetivo
        setattr(profile, "accion_crm", accion)
        setattr(profile, "producto_objetivo", producto_objetivo)
        _append_reason(result, reason)
    return _action


def set_metadata(key: str, value):
    def _action(profile: ClienteProfile, result: InferenceResult) -> None:
        metadata = getattr(result, "metadata", None)
        if isinstance(metadata, dict):
            metadata[key] = value
        setattr(profile, key, value)
    return _action
