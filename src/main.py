

"""
main.py
-------
Script principal de ejemplo para ejecutar el motor de inferencias CRM bancario.

Define un cliente de prueba, ejecuta la recomendación y muestra el resultado en consola.
"""

from __future__ import annotations

from domain import Arquetipo, ClienteProfile, EtapaJourney, NivelAfinidad, ProductoAfinidad, ValorRFM
from service import CRMRecommendationService



def imprimir_resultado(result) -> None:
    """
    Imprime en consola el resultado de la recomendación CRM de forma legible.

    Args:
        result: Objeto InferenceResult con los datos de la recomendación.
    """
    print("=== RESULTADO DEL MOTOR DE INFERENCIA ===")
    print(f"Canal preferido : {result.canal_preferido}")
    print(f"Tipo de acción  : {result.tipo_accion}")
    print(f"Acción CRM      : {result.accion_crm}")
    print(f"Producto objetivo: {result.producto_objetivo}")
    print(f"Reglas disparadas: {result.reglas_disparadas}")
    if result.campos_faltantes:
        print(f"Campos faltantes: {result.campos_faltantes}")
    print("Razones:")
    for razon in result.razones:
        print(f" - {razon}")
    print(f"Metadata: {result.metadata}")



def main() -> None:
    """
    Función principal de ejemplo: crea un cliente de prueba, ejecuta la recomendación y muestra el resultado.
    """
    service = CRMRecommendationService()

    print("\n--- Ejemplo 1: Cliente patrimonial, inversión alta ---")
    cliente1 = ClienteProfile(
        cliente_id="EJ1",
        valor_rfm=ValorRFM.ALTO,
        arquetipo=Arquetipo.CLIENTE_PATRIMONIAL,
        etapa_journey=EtapaJourney.CRECIMIENTO,
        afinidades=[
            ProductoAfinidad("fondos_inversion", NivelAfinidad.ALTA),
        ],
    )
    resultado1 = service.recomendar(cliente1)
    imprimir_resultado(resultado1)

    print("\n--- Ejemplo 2: Profesional joven digital, tarjeta crédito alta ---")
    cliente2 = ClienteProfile(
        cliente_id="EJ2",
        valor_rfm=ValorRFM.MEDIO,
        arquetipo=Arquetipo.PROFESIONAL_JOVEN_DIGITAL,
        etapa_journey=EtapaJourney.ACTIVACION,
        afinidades=[
            ProductoAfinidad("tarjeta_credito", NivelAfinidad.ALTA),
        ],
    )
    resultado2 = service.recomendar(cliente2)
    imprimir_resultado(resultado2)

    print("\n--- Ejemplo 3: Familia en expansión, seguros ---")
    cliente3 = ClienteProfile(
        cliente_id="EJ3",
        valor_rfm=ValorRFM.ALTO,
        arquetipo=Arquetipo.FAMILIA_EN_EXPANSION,
        etapa_journey=EtapaJourney.MADUREZ,
        afinidades=[
            ProductoAfinidad("seguros", NivelAfinidad.ALTA),
        ],
    )
    resultado3 = service.recomendar(cliente3)
    imprimir_resultado(resultado3)

    print("\n--- Ejemplo 4: Cliente transaccional, bajo valor, riesgo de abandono ---")
    cliente4 = ClienteProfile(
        cliente_id="EJ4",
        valor_rfm=ValorRFM.BAJO,
        arquetipo=Arquetipo.CLIENTE_TRANSACCIONAL,
        etapa_journey=EtapaJourney.RIESGO_ABANDONO,
        afinidades=[],
    )
    resultado4 = service.recomendar(cliente4)
    imprimir_resultado(resultado4)

    print("\n--- Ejemplo 5: Cliente con atributos faltantes ---")
    cliente5 = ClienteProfile(
        cliente_id="EJ5",
        valor_rfm=None,
        arquetipo=Arquetipo.CLIENTE_PATRIMONIAL,
        etapa_journey=EtapaJourney.CRECIMIENTO,
        afinidades=None,
    )
    resultado5 = service.recomendar(cliente5)
    imprimir_resultado(resultado5)


if __name__ == "__main__":
    main()
