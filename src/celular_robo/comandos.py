# Command — ComandoColeta — enunciado, Seção 2.3.
#
# Herde de `Comando` (comandos_base.py — ABC com registro automático):
#
#   from celular_robo.comandos_base import Comando
#
# TODO: implemente aqui. ComandoColeta(Comando): __init__(codinome, posicao,
# quantidade), com .executar(robo) e .desfazer(robo) (remove o item da
# bandeja, decrementa a contagem coletada).
from celular_robo.comandos_base import Comando
from celular_robo.robo_base import Direcao
from celular_robo.excecoes import PedidoInvalido

class ComandoColeta(Comando):
    def __init__(self, codinome, posicao, quantidade):
        self.codinome = codinome
        self.posicao = posicao
        self.quantidade = quantidade

    def executar(self, robo):
        self._navegar_ate(robo, self.posicao)
        robo.bandeja.coletar(self.codinome, self.quantidade)
        robo.notificar(
            "coleta", codinome=self.codinome, quantidade=self.quantidade, posicao=self.posicao
        )

    def desfazer(self, robo):
        robo.bandeja.devolver(self.codinome, self.quantidade)
        robo.notificar("coleta_desfeita", codinome=self.codinome, quantidade=self.quantidade)
        
    def _navegar_ate(self, robo, posicao):
        alvo_x, alvo_y = posicao
        try:
            if robo.x < alvo_x:
                robo.girar_ate(Direcao.LESTE)
                robo.avancar_n(alvo_x - robo.x)
            elif robo.x > alvo_x:
                robo.girar_ate(Direcao.OESTE)
                robo.avancar_n(robo.x - alvo_x)
            if robo.y < alvo_y:
                robo.girar_ate(Direcao.NORTE)
                robo.avancar_n(alvo_y - robo.y)
            elif robo.y > alvo_y:
                robo.girar_ate(Direcao.SUL)
                robo.avancar_n(robo.y - alvo_y)
        except ValueError as erro:
            raise PedidoInvalido(
                f"posição {posicao} inválida para {self.codinome!r}: {erro}"
            )
    
    def __repr__(self):
        return f"ComandoColeta({self.codinome!r}, {self.posicao}, {self.quantidade})"