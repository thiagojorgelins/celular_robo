# TODO: seus testes de configuração/LPS — enunciado, Seção 2.7 (pytest.raises,
# @pytest.mark.parametrize cobrindo estratégia×área).
import pytest

from celular_robo.fabrica import criar_robo_configurado
from celular_robo.excecoes import ConfiguracaoInvalida
from celular_robo.estrategias import RotaDireta, RotaComDuplaConferencia


@pytest.mark.parametrize(
    "estrategia_nome, area_nome, deve_funcionar, classe_esperada",
    [
        ("direta", "centro_padrao", True, RotaDireta),
        ("dupla_conferencia", "centro_padrao", True, RotaComDuplaConferencia),
        ("dupla_conferencia", "area_quarentena", True, RotaComDuplaConferencia),
        ("direta", "area_quarentena", False, None),
    ],
)
def test_contrato_criar_ou_recusar(estrategia_nome, area_nome, deve_funcionar, classe_esperada):
    if deve_funcionar:
        robo = criar_robo_configurado(
            "RoboColetor", "Coletor-Teste",
            estrategia_nome=estrategia_nome, area_nome=area_nome,
        )
        assert type(robo).__name__ == "RoboColetor"
        assert isinstance(robo.estrategia, classe_esperada)
        assert robo.estrategia_nome == estrategia_nome
        assert robo.area_nome == area_nome
    else:
        with pytest.raises(ConfiguracaoInvalida):
            criar_robo_configurado(
                "RoboColetor", "Coletor-Teste",
                estrategia_nome=estrategia_nome, area_nome=area_nome,
            )


def test_area_quarentena_tem_obstaculo():
    robo = criar_robo_configurado(
        "RoboColetor", "Coletor-Quarentena",
        estrategia_nome="dupla_conferencia", area_nome="area_quarentena",
    )
    assert len(robo.obstaculos) >= 1


def test_tipo_invalido_recusado():
    with pytest.raises(ConfiguracaoInvalida):
        criar_robo_configurado(
            "RoboFantasma", "X", estrategia_nome="direta", area_nome="centro_padrao"
        )
