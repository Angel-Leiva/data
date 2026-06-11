from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent
from src.schemas.contexto import ContextoMAS
from src.schemas.mensajes import MensajeAgente
from src.services.eda_service import EDAService


class AgenteEDA(BaseAgent):
    nombre = "Agente EDA"

    def __init__(self, service: EDAService | None = None) -> None:
        self.service = service or EDAService()

    def ejecutar(self, contexto: ContextoMAS) -> dict[str, Any]:
        payload = self.service.analizar(contexto.df_modelo, contexto.target)
        resultado = payload["resultado"]
        alertas = payload["alertas"]
        recomendaciones = payload["recomendaciones"]
        contexto.resultados["eda"] = resultado
        contexto.agregar_alertas(alertas)
        contexto.agregar_recomendaciones(recomendaciones)
        contexto.registrar(
            MensajeAgente(
                agente=self.nombre,
                tipo="REPORTE_EDA",
                estado="completado",
                contenido={"resumen": resultado, "alertas": alertas, "recomendaciones": recomendaciones},
            )
        )
        return resultado
