# RoboColetor + QuantidadeValida — enunciado, Seção 2.1.
#
# `Robo` (posição, __init_subclass__/_registro, avancar/girar, estrategia/modo,
# Observer) já vem pronto em robo_base.py — não precisa reescrever, só importar:
#
#   from celular_robo.robo_base import Robo, Coordenada
#
# TODO: implemente aqui.
# - RoboColetor(Robo): reaproveita Coordenada (x, y) por herança — não precisa
#   redeclarar. Adicione o que for específico da coleta (ex.: bandeja).
# - QuantidadeValida: descriptor novo (mesmo protocolo de Coordenada/Percentual
#   em robo_base.py), validando que a quantidade coletada de um item nunca é
#   negativa nem passa do pedido.
# - __str__/__repr__ (robô) e __len__ (bandeja — quantos itens já coletados).
from celular_robo.robo_base import Robo
from celular_robo.comandos import ComandoColeta
from celular_robo.modos import ModoColetando, ModoAguardandoVerificacao
from celular_robo.excecoes import PedidoInvalido

class QuantidadeValida:
    def __set__name__(self, owner, name):
        self.nome = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.nome]

    def __set__(self, instance, valor):
        if valor < 0:
            raise ValueError(f"quantidade coletada não poder ser negativa: {valor}")
        maximo = getattr(instance, "quantidade_pedida", None)
        if maximo is not None and valor > maximo:
            raise ValueError(f"quantidade coletada ({valor}) excede a quantidade pedida ({maximo})")
        instance.__dict__[self.nome] = valor

class ItemBandeja:
    quantidade_coletada = QuantidadeValida()
    
    def __init__(self, codinome, quantidade_pedida):
        self.codinome = codinome
        self.quantidade_pedida = quantidade_pedida
        self.quantidade_coletada = 0
    
    @property
    def completa(self):
        return self.quantidade_coletada >= self.quantidade_pedida
    
    def __repr__(self):
        return (
            f"ItemBandeja({self.codinome!r}, "
            f"{self.quantidade_coletada}/{self.quantidade_pedida})"
        )
        

class Bandeja:
    def __init__(self):
        self._itens = []
        
    def registrar_pedido(self, itens_pedido):
        self.itens = {
            item["codinome"]: ItemBandeja(item["codinome"], item["quantidade"])
            for item in itens_pedido
        }
        
    def coletar(self, codinome, quantidade):
        item = self.itens.setdefault(codinome, ItemBandeja(codinome, quantidade))
        item.quantidade_coletada += quantidade
        
    def devolver(self, codinome, quantidade):
        item = self._itens.get(codinome)
        if item is not None:
            item.quantidade_coletada -= quantidade
        
    def esta_completa(self):
        return bool(self._itens) and all(item.completa for item in self._itens.values())
    
    def limpar(self):
        self._itens = {}
        
    def __len__(self):
        return sum(item.quantidade_coletada for item in self._itens.values())
    
    def __repr__(self):
        return f"Bandeja({dict(self._itens)})"
    
    
class RoboColetor(Robo, categoria="coleta"):
    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.bandeja = Bandeja()
        self.pedido_atual = None
        self.estrategia_nome = None
        self.area_nome = None
        self._comandos_pedentes = []

    def __str__(self):
        return (
            f"{self.nome} [coletor] em ({self.x}, {self.y})"
            f"bandeja: {len(self.bandeja)} itens coletados, modo={type(self.modo).__name__}"
        )

    def __repr__(self):
        return f"RoboColetor(nome={self.nome!r}, x={self.x}, y={self.y}, bandeja={len(self.bandeja)})"

    def processar_pedido(self, pedido):
        if isinstance(self.modo, ModoAguardandoVerificacao):
            self.notificar(
                "pedido_rejeitado", motivo="bandeja aguardando aprovação da equipe de testes"
            )
            raise PedidoInvalido(
                "robô aguardando aprovação da bandeja; não pode iniciar novo pedido"
            )
        self.pedido_atual = pedido
        self.bandeja.registrar_pedido(pedido["itens"])
        self._comandos_pedentes = [
            ComandoColeta(item["codinome"], tuple(item["posicao"]), item["quantidade"])
            for item in pedido["itens"]
        ]
        while self._comandos_pedentes and isinstance(self.modo, ModoColetando):
            self.modo.mover(self)
            
    def aprovar_bandeja(self):
        self.notificar("bandeja_aprovada", pedido=self.pedido_atual)
        self.bandeja.limpar()
        self.pedido_atual = None
        self.modo =  ModoColetando()
        
    def rejeitar_bandeja(self, motivo="rejeitada pela equipe de testes"):
        self.notificar("pedido_rejeitado", motivo=motivo)
        self.modo = ModoColetando()