# Factory — criar_robo_coletor, criar_robo_configurado — enunciado, Seção 2.3.
# (Ver fabrica_base.py — genérico do curso, não editar: criar_robo("RoboColetor",
# ...) já funciona, pode chamar direto ou usar como modelo.)
#
# TODO: implemente aqui. criar_robo_coletor(tipo_nome, ...) a partir do
# _registro (Seção 2.2); criar_robo_configurado combina isso com a validação do
# modelo de features (Seção 2.4).
#
# Contrato mínimo exigido por tests/test_00_fornecido.py (não altere a
# assinatura abaixo sem também atualizar aquele arquivo):
#
#   criar_robo_configurado(tipo_nome, nome, estrategia_nome=..., area_nome=...)
from celular_robo.fabrica_base import criar_robo
from celular_robo.estrategias import RotaColeta
from celular_robo.modos import ModoColetando, MonitorBandeja
from celular_robo.observadores import EquipeDeTestes, RegistroAuditoria
from celular_robo.modelo_features import validar_configuracao, OBSTACULOS_POR_AREA


def criar_robo_coletor(tipo_nome, nome, estrategia_nome, area_nome, **kwargs):
    rota_classe = RotaColeta._registro_rotas[estrategia_nome]
    obstaculos = set(OBSTACULOS_POR_AREA.get(area_nome, set()))
    robo = criar_robo(
        tipo_nome, nome,
        estrategia=rota_classe(),
        modo=ModoColetando(),
        obstaculos=obstaculos,
        **kwargs,
    )
    robo.estrategia_nome = estrategia_nome
    robo.area_nome = area_nome

    robo.adicionar_observador(MonitorBandeja())
    robo.equipe_de_testes = EquipeDeTestes()
    robo.adicionar_observador(robo.equipe_de_testes)
    robo.registro_auditoria = RegistroAuditoria()
    robo.adicionar_observador(robo.registro_auditoria)
    return robo


def criar_robo_configurado(tipo_nome, nome, estrategia_nome, area_nome, **kwargs):
    validar_configuracao(tipo_nome, estrategia_nome, area_nome)
    return criar_robo_coletor(tipo_nome, nome, estrategia_nome, area_nome, **kwargs)
