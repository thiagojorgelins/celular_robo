# Modelo de features / LPS — enunciado, Seção 2.4.
#
# TODO: implemente aqui. TIPOS_VALIDOS, ESTRATEGIAS_VALIDAS (derivados dos
# registros de Seção 2.2, não digitados à mão), REQUER/EXCLUI (4 dimensões: tipo,
# estratégia, área, urgência) e validar_configuracao levantando
# ConfiguracaoInvalida antes de qualquer robô ser instanciado.

from celular_robo.robo_base import Robo
from celular_robo.estrategias import RotaColeta
from celular_robo.excecoes import ConfiguracaoInvalida
import celular_robo.robo

TIPOS_VALIDOS = set(Robo._registro)
ESTRATEGIAS_VALIDAS = set(RotaColeta._registro_rotas)

AREAS_VALIDAS = {"centro_padrao", "area_quarentena"}
OBSTACULOS_POR_AREA = {
    "centro_padrao": set(),
    "area_quarentena": {(5, 5), (5, 6), (5, 7)},
}

EXCLUI = {
    "area_quarentena": {"direta"},
}

REQUER = {
    "fragil": "dupla_conferencia",
    "urgente": "direta",
}

def validar_configuracao(tipo_nome, estrategia_nome, area_nome):
    if tipo_nome not in TIPOS_VALIDOS:
        raise ConfiguracaoInvalida(f"tipo de robô desconhecido: {tipo_nome!r}. Válidos: {sorted(TIPOS_VALIDOS)}")
    if estrategia_nome not in ESTRATEGIAS_VALIDAS:
         raise ConfiguracaoInvalida(f"estratégia de rota desconhecida: {estrategia_nome!r}. Válidas: {sorted(ESTRATEGIAS_VALIDAS)}")
    if area_nome not in AREAS_VALIDAS:
        raise ConfiguracaoInvalida(f"área desconhecida: {area_nome!r}. Válidas: {sorted(AREAS_VALIDAS)}")
    proibidas = EXCLUI.get(area_nome, set())
    if estrategia_nome in proibidas:
        raise ConfiguracaoInvalida(f"área {area_nome!r} exclui a estratégia {estrategia_nome!r}")
    return True


def validar_requisitos_item(item, estrategia_nome):
    codinome = item.get("codinome", "<sem codinome>")
    if item.get("fragil") and estrategia_nome != REQUER["fragil"]:
        raise ConfiguracaoInvalida(
            f"item frágil {codinome!r} exige a estratégia {REQUER['fragil']!r}"
            f"robô está configurado com {estrategia_nome!r}"
        )
    if item.get("urgente") and estrategia_nome != REQUER["urgente"]:
        raise ConfiguracaoInvalida(
            f"item urgente {codinome!r} exige a estratégia {REQUER['urgente']!r}"
            f"robô está configurado com {estrategia_nome!r}"
        )
    