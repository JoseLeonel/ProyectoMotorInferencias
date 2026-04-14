
from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# Enum para los tipos de ejecución CRM recomendados
class TipoEjecucion(str, Enum):
    CAMPANA_DIGITAL = "campana_digital"
    CONTACTO_PERSONAL = "contacto_personal"
    CAMPANA_EMAIL = "campana_email"
    ESTRATEGIA_MULTICANAL = "estrategia_multicanal"

# Enum para las acciones CRM específicas sugeridas por el motor de inferencias
class AccionCRM(str, Enum):
    OFRECER_INVERSION = "ofrecer_inversion"
    OFRECER_TARJETA_CREDITO = "ofrecer_tarjeta_credito"
    OFRECER_SEGURO = "ofrecer_seguro"
    RETENER_CON_INCENTIVO = "retener_con_incentivo"
    ACTIVAR_PRODUCTO = "activar_producto"
    CROSS_SELLING = "cross_selling"
    ASESORIA_FINANCIERA = "asesoria_financiera"
    UP_SELLING = "up_selling"
    FIDELIZACION = "fidelizacion"
    REACTIVAR_CLIENTE = "reactivar_cliente"


class ValorRFM(str, Enum):
    """
    Enum para los valores RFM (Recencia, Frecuencia, Monto) de un cliente.
    ALTO: Cliente de alto valor.
    MEDIO: Cliente de valor medio.
    BAJO: Cliente de bajo valor.
    """
    ALTO = "alto"
    MEDIO = "medio"
    BAJO = "bajo"
    


class Arquetipo(str, Enum):
    """
    Enum para los arquetipos de clientes bancarios.
    """
    PROFESIONAL_JOVEN_DIGITAL = "profesional_joven_digital"
    FAMILIA_EN_EXPANSION = "familia_en_expansion"
    CLIENTE_TRANSACCIONAL = "cliente_transaccional"
    CLIENTE_PATRIMONIAL = "cliente_patrimonial"
    EMPRENDEDOR_PYME = "emprendedor_pequeno_empresario"
    


class EtapaJourney(str, Enum):
    """
    Enum para las etapas del ciclo de vida del cliente (Customer Journey).
    """
    ADQUISICION = "adquisicion"
    ACTIVACION = "activacion"
    CRECIMIENTO = "crecimiento"
    MADUREZ = "madurez"
    RIESGO_ABANDONO = "riesgo_abandono"
    REACTIVACION = "reactivacion"


class NivelAfinidad(str, Enum):
    """
    Enum para el nivel de afinidad del cliente con un producto.
    """
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


class Canal(str, Enum):
    """
    Enum para los canales preferidos de comunicación o atención.
    """
    APP = "app"
    EMAIL = "email"
    ASESOR_PERSONAL = "asesor_personal"
    MIXTO = "mixto"


class TipoAccion(str, Enum):
    """
    Enum para los tipos de acción CRM recomendadas.
    """
    ACTIVACION = "activacion"
    CRECIMIENTO = "crecimiento"
    RETENCION = "retencion"
    REACTIVACION = "reactivacion"


@dataclass(frozen=True)
class ProductoAfinidad:
    """
    Representa la afinidad de un cliente con un producto específico.
    producto: Nombre del producto.
    nivel: Nivel de afinidad (ALTA, MEDIA, BAJA).
    """
    producto: str
    nivel: NivelAfinidad


@dataclass
class ClienteProfile:
    """
    Perfil de cliente bancario para el motor de inferencias.
    cliente_id: Identificador único del cliente.
    valor_rfm: Valor RFM del cliente.
    arquetipo: Arquetipo del cliente.
    etapa_journey: Etapa actual en el ciclo de vida.
    afinidades: Lista de afinidades a productos.
    """
    cliente_id: Optional[str] = None
    valor_rfm: Optional[ValorRFM] = None
    arquetipo: Optional[Arquetipo] = None
    etapa_journey: Optional[EtapaJourney] = None
    afinidades: Optional[List[ProductoAfinidad]] = field(default_factory=list)
    recency: Optional[str] = None
    frequency: Optional[str] = None
    monetary: Optional[str] = None
    afinidad_producto: Optional[str] = None
    nivel_afinidad: Optional[NivelAfinidad] = None

    def __post_init__(self) -> None:
        if self.afinidades is None:
            self.afinidades = []

    def campos_faltantes(self) -> List[str]:
        """
        Retorna los campos principales que no fueron informados en el perfil.
        """
        faltantes: List[str] = []
        campos_principales = {
            "cliente_id": self.cliente_id,
            "valor_rfm": self.valor_rfm,
            "arquetipo": self.arquetipo,
            "etapa_journey": self.etapa_journey,
        }
        for nombre, valor in campos_principales.items():
            if valor is None:
                faltantes.append(nombre)
        return faltantes

    def afinidad_de(self, producto: str) -> Optional[NivelAfinidad]:
        """
        Devuelve el nivel de afinidad del cliente para un producto dado.
        """
        if self.afinidad_producto == producto and self.nivel_afinidad is not None:
            return self.nivel_afinidad
        for item in self.afinidades or []:
            if item.producto == producto:
                return item.nivel
        return None


@dataclass
class InferenceResult:
    """
    Resultado de la inferencia CRM.
    canal_preferido: Canal sugerido para el cliente.
    tipo_accion: Tipo de acción recomendada.
    accion_crm: Acción CRM específica sugerida.
    producto_objetivo: Producto objetivo de la recomendación.
    razones: Lista de justificaciones para la recomendación.
    reglas_disparadas: Reglas que se activaron durante la inferencia.
    metadata: Información adicional relevante.
    """
    canal_preferido: Optional[Canal] = None
    tipo_accion: Optional[TipoAccion] = None
    accion_crm: Optional[str] = None
    producto_objetivo: Optional[str] = None
    razones: List[str] = field(default_factory=list)
    reglas_disparadas: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    campos_faltantes: List[str] = field(default_factory=list)

    def add_reason(self, message: str) -> None:
        """
        Agrega una justificación al resultado de inferencia.
        """
        self.razones.append(message)

    def add_rule(self, rule_id: str) -> None:
        """
        Agrega el identificador de una regla disparada.
        """
        self.reglas_disparadas.append(rule_id)

    def add_missing_field(self, field_name: str) -> None:
        """
        Registra un campo faltante sin duplicados.
        """
        if field_name not in self.campos_faltantes:
            self.campos_faltantes.append(field_name)
