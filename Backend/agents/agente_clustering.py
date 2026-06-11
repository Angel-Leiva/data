from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent
from src.schemas.contexto import ContextoMAS
from src.schemas.mensajes import MensajeAgente
from src.services.clustering_service import ClusteringService


class AgenteClustering(BaseAgent):
    nombre = "Agente Clustering"

    def __init__(self, service: ClusteringService | None = None) -> None:
        self.service = service or ClusteringService()

    def ejecutar(self, contexto: ContextoMAS) -> dict[str, Any]:
        resultado = self.service.ejecutar(contexto.df_modelo)
        recomendaciones = resultado["recomendaciones"]
        contexto.resultados["clustering"] = resultado
        contexto.agregar_recomendaciones(recomendaciones)
        contexto.registrar(
            MensajeAgente(
                agente=self.nombre,
                tipo="REPORTE_CLUSTERING",
                estado="completado",
                contenido={"mejor": resultado["mejor"], "recomendaciones": recomendaciones},
            )
        )
        return resultado
