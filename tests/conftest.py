# Fixtures compartilhadas entre seus test_*.py — TODO, à sua escolha.
# (A fixture usada por test_00_fornecido.py já vem definida nele mesmo —
# não precisa duplicar aqui.)
import pytest

from celular_robo.fabrica import criar_robo_configurado

@pytest.fixture
def caminho_dados(pytestconfig):
    return pytestconfig.rootpath / "dados"


@pytest.fixture
def pedido_valido():
    return {
        "lote": "Lote de Testes #001",
        "itens": [
            {"codinome": "Projeto Aurora", "quantidade": 2, "posicao": [3, 4],
             "fragil": False, "urgente": False},
            {"codinome": "Projeto Vesper", "quantidade": 1, "posicao": [2, 1],
             "fragil": False, "urgente": False},
        ],
    }


@pytest.fixture
def robo_dupla_conferencia():
    return criar_robo_configurado(
        "RoboColetor", "Coletor-Frágil",
        estrategia_nome="dupla_conferencia", area_nome="centro_padrao",
    )


@pytest.fixture
def robo_coletor_padrao():
    return criar_robo_configurado(
        "RoboColetor", "Coletor-Fluxo",
        estrategia_nome="direta", area_nome="centro_padrao",
    )
