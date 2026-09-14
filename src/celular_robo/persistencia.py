# Configuração e persistência — enunciado, Seção 2.6.
#
# TODO: implemente aqui. montar_robo_de_config(config) e
# montar_pedido_de_json(caminho) — mesmo par de funções do capstone do curso
# (montar_robo_de_config/montar_frota_de_json), adaptado: um arquivo
# configura o robô (tipo, estratégia, área), outro traz o pedido de coleta.
import json

from celular_robo.fabrica import criar_robo_configurado
from celular_robo.excecoes import PedidoInvalido
from celular_robo.modelo_features import validar_requisitos_item

def montar_robo_de_config(config):
    dados = dict(config)
    tipo_nome = dados.pop("tipo_nome")
    nome = dados.pop("nome")
    estrategia_nome = dados.pop("estrategia_nome")
    area_nome = dados.pop("area_nome")
    return criar_robo_configurado(
        tipo_nome, nome, estrategia_nome=estrategia_nome, area_nome=area_nome, **dados
    )


def montar_pedido_de_json(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        pedido = json.load(arquivo)
    validar_pedido(pedido)
    return pedido


def validar_pedido(pedido):
    itens = pedido.get("itens", [])
    if not itens:
        raise PedidoInvalido("pedido vazio: nenhum item para coletar")

    tem_urgente = False
    tem_fragil = False
    for item in itens:
        codinome = item.get("codinome")
        quantidade = item.get("quantidade", 0)
        fragil = bool(item.get("fragil", False))
        urgente = bool(item.get("urgente", False))

        if not codinome:
            raise PedidoInvalido("item sem codinome válido no pedido")
        if quantidade <= 0:
            raise PedidoInvalido(f"quantidade inválida para {codinome!r}: {quantidade}")
        if fragil and urgente:
            raise PedidoInvalido(
                f"item {codinome!r} não pode ser frágil e urgente ao mesmo tempo"
            )
        tem_urgente = tem_urgente or urgente
        tem_fragil = tem_fragil or fragil

    if tem_urgente and tem_fragil:
        raise PedidoInvalido(
            "pedido com itens urgentes e frágeis ao mesmo tempo — a estratégia "
            "do robô é única e não atende as duas exigências simultaneamente"
        )
    return True


def buscar_item(pedido, codinome):
    for item in pedido.get("itens", []):
        if item["codinome"] == codinome:
            return item
    raise PedidoInvalido(f"codinome {codinome!r} não encontrado no lote")


def executar_pedido(robo, pedido):
    validar_pedido(pedido)
    for item in pedido["itens"]:
        validar_requisitos_item(item, robo.estrategia_nome)
    robo.processar_pedido(pedido)
