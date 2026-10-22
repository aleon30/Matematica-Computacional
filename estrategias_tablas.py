"""
Módulo de Contratos, DTOs y Estrategias de Formateo.
Aplica el formato numérico '#00', '#01', etc., bajo el patrón Strategy.
"""
from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass(frozen=True)
class EventoPasoDTO:
    """Objeto de transferencia de datos emitido por el algoritmo."""
    paso_indice: int
    tipo: str
    nodo_actual: int
    nodo_vecino: Optional[int] = None
    costo: int = 0
    peso_arista: Optional[int] = None
    costo_conocido: Optional[int] = None
    decision: str = ""
    mensaje: str = ""


@dataclass(frozen=True)
class ModeloFilaPaso:
    """Modelo con las 5 columnas originales y el paso formateado con '#'."""
    paso_id: str
    nodo: str
    vecino: str
    calculo: str
    decision_badge: str
    etiqueta_estilo: str


def crear_evento_desde_diccionario(indice: int, datos: dict) -> EventoPasoDTO:
    """Convierte el diccionario de Grafo.py a un DTO inmutable."""
    nodo = datos.get('nodo_actual', datos.get('nodo', 0))
    vecino = datos.get('vecino')
    costo = datos.get('nuevo_costo', datos.get('costo', 0))
    peso_arista = datos.get('peso_arista')
    costo_conocido = datos.get('costo_conocido')
    decision = datos.get('decision', '')
    mensaje = datos.get('mensaje', '')

    return EventoPasoDTO(
        paso_indice=indice,
        tipo=datos.get('tipo', ''),
        nodo_actual=nodo,
        nodo_vecino=vecino,
        costo=costo,
        peso_arista=peso_arista,
        costo_conocido=costo_conocido,
        decision=decision,
        mensaje=mensaje
    )


class IEstrategiaFilaPaso(Protocol):
    """Contrato del patrón Strategy para formatear filas."""
    def formatear(self, evento: EventoPasoDTO) -> ModeloFilaPaso:
        ...


class EstrategiaFilaVisitado(IEstrategiaFilaPaso):
    """Formatea el paso cuando se visita un nodo."""
    def formatear(self, evento: EventoPasoDTO) -> ModeloFilaPaso:
        return ModeloFilaPaso(
            paso_id=f"#{evento.paso_indice:02d}",
            nodo=str(evento.nodo_actual),
            vecino="-",
            calculo=f"Acumulado: {evento.costo}",
            decision_badge="● Visitando",
            etiqueta_estilo="estado_visita"
        )


class EstrategiaFilaEncolada(IEstrategiaFilaPaso):
    """Formatea la evaluación de arista con acumulado por debajo."""
    def formatear(self, evento: EventoPasoDTO) -> ModeloFilaPaso:
        arista = evento.peso_arista if evento.peso_arista is not None else "-"
        return ModeloFilaPaso(
            paso_id=f"#{evento.paso_indice:02d}",
            nodo=str(evento.nodo_actual),
            vecino=str(evento.nodo_vecino if evento.nodo_vecino is not None else "-"),
            calculo=f"Arista: {arista}\nAcumulado: {evento.costo}",
            decision_badge="↗ Encolada",
            etiqueta_estilo="estado_encolada"
        )


class EstrategiaFilaDescarte(IEstrategiaFilaPaso):
    """Formatea el descarte de ruta ya superada."""
    def formatear(self, evento: EventoPasoDTO) -> ModeloFilaPaso:
        costo_previo = evento.costo_conocido if evento.costo_conocido is not None else "-"
        return ModeloFilaPaso(
            paso_id=f"#{evento.paso_indice:02d}",
            nodo=str(evento.nodo_actual),
            vecino="-",
            calculo=f"Costo: {evento.costo}\nVisitado: {costo_previo}",
            decision_badge="✕ Descartado",
            etiqueta_estilo="estado_descarte"
        )


class EstrategiaFilaDestino(IEstrategiaFilaPaso):
    """Formatea la llegada al nodo destino."""
    def formatear(self, evento: EventoPasoDTO) -> ModeloFilaPaso:
        return ModeloFilaPaso(
            paso_id=f"#{evento.paso_indice:02d}",
            nodo=str(evento.nodo_actual),
            vecino="-",
            calculo=f"Acumulado: {evento.costo}",
            decision_badge="✓ Destino!",
            etiqueta_estilo="estado_destino"
        )


class EstrategiaFilaSinCamino(IEstrategiaFilaPaso):
    """Formatea cuando no existe camino."""
    def formatear(self, evento: EventoPasoDTO) -> ModeloFilaPaso:
        return ModeloFilaPaso(
            paso_id=f"#{evento.paso_indice:02d}",
            nodo=str(evento.nodo_actual),
            vecino="-",
            calculo="-",
            decision_badge="✕ Sin camino",
            etiqueta_estilo="estado_descarte"
        )


class RegistroEstrategiasPaso:
    """Registro que resuelve la estrategia en O(1)."""
    def __init__(self) -> None:
        self._estrategias: dict[str, IEstrategiaFilaPaso] = {
            'Visitado': EstrategiaFilaVisitado(),
            'Agregar a cola': EstrategiaFilaEncolada(),
            'Descartado': EstrategiaFilaDescarte(),
            'destino_alcanzado': EstrategiaFilaDestino(),
            'sin_camino': EstrategiaFilaSinCamino()
        }
        self._defecto = EstrategiaFilaVisitado()

    def resolver(self, tipo_evento: str) -> IEstrategiaFilaPaso:
        return self._estrategias.get(tipo_evento, self._defecto)