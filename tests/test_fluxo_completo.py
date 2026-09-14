# TODO: teste da transição ModoColetando -> ModoAguardandoVerificacao
# disparada pelo Observer quando a bandeja completa — enunciado, Seção 2.7.
import json
import pytest
from celular_robo.excecoes import PedidoInvalido

from celular_robo.fabrica import criar_robo_configurado
from celular_robo.modos import ModoColetando, ModoAguardandoVerificacao
from celular_robo.persistencia import executar_pedido, montar_pedido_de_json, montar_robo_de_config

def test_bandeja_pronta_dispara_transicao_de_modo(robo_coletor_padrao):
    assert isinstance(robo_coletor_padrao.modo, ModoColetando)
    robo_coletor_padrao.notificar("bandeja_pronta", pedido=None)
    assert isinstance(robo_coletor_padrao.modo, ModoAguardandoVerificacao)


def test_rejeitar_bandeja_retorna_a_coletando(robo_coletor_padrao):
    robo_coletor_padrao.notificar("bandeja_pronta", pedido=None)
    assert isinstance(robo_coletor_padrao.modo, ModoAguardandoVerificacao)
    robo_coletor_padrao.rejeitar_bandeja()
    assert isinstance(robo_coletor_padrao.modo, ModoColetando)


def test_processar_pedido_completa_bandeja_e_muda_modo(pedido_valido):
    robo = criar_robo_configurado(
        "RoboColetor", "Coletor-Fluxo",
        estrategia_nome="direta", area_nome="centro_padrao",
    )
    executar_pedido(robo, pedido_valido)
    assert len(robo.bandeja) == 3
    assert isinstance(robo.modo, ModoAguardandoVerificacao)
    assert len(robo.registro_auditoria) > 0
    
    
def test_montar_robo_de_config_a_partir_do_json_de_exemplo(caminho_dados):
    with open(caminho_dados / "config_robo_exemplo.json", encoding="utf-8") as arquivo:
        config = json.load(arquivo)

    robo = montar_robo_de_config(config)

    assert type(robo).__name__ == "RoboColetor"
    assert robo.nome == "Coletor-1"
    assert robo.estrategia_nome == "direta"
    assert robo.area_nome == "centro_padrao"


def test_montar_pedido_de_json_valido(caminho_dados):
    pedido = montar_pedido_de_json(caminho_dados / "pedido_coleta_valido_exemplo.json")

    assert pedido["lote"] == "Lote de Testes #500"
    assert len(pedido["itens"]) == 2


def test_montar_pedido_de_json_do_enunciado_e_invalido(caminho_dados):
    with pytest.raises(PedidoInvalido):
        montar_pedido_de_json(caminho_dados / "pedido_coleta_exemplo.json")


def test_fluxo_completo_a_partir_dos_arquivos_json(caminho_dados):
    with open(caminho_dados / "config_robo_exemplo.json", encoding="utf-8") as arquivo:
        config = json.load(arquivo)
    robo = montar_robo_de_config(config)

    pedido = montar_pedido_de_json(caminho_dados / "pedido_coleta_valido_exemplo.json")
    executar_pedido(robo, pedido)

    assert len(robo.bandeja) == 3
    assert isinstance(robo.modo, ModoAguardandoVerificacao)
    assert len(robo.registro_auditoria) > 0