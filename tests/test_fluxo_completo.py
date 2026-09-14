# TODO: teste da transição ModoColetando -> ModoAguardandoVerificacao
# disparada pelo Observer quando a bandeja completa — enunciado, Seção 2.7.

from celular_robo.fabrica import criar_robo_configurado
from celular_robo.modos import ModoColetando, ModoAguardandoVerificacao
from celular_robo.persistencia import executar_pedido


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