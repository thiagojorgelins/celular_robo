# TODO: seus testes de pedido — enunciado, Seção 2.7 (pytest.raises(PedidoInvalido),
# conflito fragil+urgente de Seção 2.4).

import pytest

from celular_robo.persistencia import validar_pedido, buscar_item
from celular_robo.excecoes import PedidoInvalido


def test_codinome_inexistente_no_lote(pedido_valido):
    with pytest.raises(PedidoInvalido):
        buscar_item(pedido_valido, "Codinome Que Não Existe")


def test_pedido_vazio_invalido():
    with pytest.raises(PedidoInvalido):
        validar_pedido({"lote": "Vazio", "itens": []})


def test_item_fragil_e_urgente_ao_mesmo_tempo_invalido(pedido_valido):
    pedido_valido["itens"][0]["fragil"] = True
    pedido_valido["itens"][0]["urgente"] = True
    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido_valido)


def test_conflito_urgente_e_fragil_em_itens_diferentes_invalido(pedido_valido):
    pedido_valido["itens"][0]["urgente"] = True
    pedido_valido["itens"][1]["fragil"] = True
    with pytest.raises(PedidoInvalido):
        validar_pedido(pedido_valido)