from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent
from src.schemas.contexto import ContextoMAS
from src.schemas.mensajes import MensajeAgente
from src.services.classification_service import ClassificationService


class AgenteClasificacion(BaseAgent):
    nombre = "Agente Clasificación"

    def __init__(self, service: ClassificationService | None = None) -> None:
        self.service = service or ClassificationService()

    def ejecutar(self, contexto: ContextoMAS) -> dict[str, Any]:
        if not contexto.target:
            raise ValueError("El Agente Clasificación requiere variable objetivo.")

        resultado = self.service.ejecutar(contexto.df_modelo, contexto.target, contexto.modo_ejecucion)
        recomendaciones = resultado["recomendaciones"]
        contexto.resultados["clasificacion"] = resultado
        contexto.agregar_recomendaciones(recomendaciones)
        contexto.registrar(
            MensajeAgente(
                agente=self.nombre,
                tipo="REPORTE_CLASIFICACION",
                estado="completado",
                contenido={"mejor": resultado["mejor"], "recomendaciones": recomendaciones},
            )
        )
        return resultado
