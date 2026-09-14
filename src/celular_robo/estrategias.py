# Strategy — RotaDireta, RotaComDuplaConferencia — enunciado, Seção 2.3.
# (Não confundir com estrategias_base.py — genérico do curso, não editar. Ao
# contrário de Command/Observer/State, aqui você NÃO herda de `Estrategia`:
# escreva sua própria base, ver TODO abaixo — motivo em estrategias_base.py.)
#
# TODO: implemente aqui. Considere uma base comum (RotaColeta) com
# __init_subclass__ registrando cada rota, ver Seção 2.2 (metaprogramação
# aplicada a uma segunda hierarquia).
from abc import ABC, abstractmethod

from celular_robo.excecoes import PedidoInvalido


class RotaColeta(ABC):
    _registro_rotas = {}
    
    def __init_subclass__(cls,nome_registro=None, **kwargs):
        super().__init_subclass__(**kwargs)
        RotaColeta._registro_rotas[nome_registro or cls.__name__] = cls
    
    @abstractmethod
    def coletar(self, robo, comando):
        pass
    

class RotaDireta(RotaColeta, nome_registro="direta"):
    def coletar(self, robo, comando):
        comando.executar(robo)
        

class RotaComDuplaConferencia(RotaColeta, nome_registro="dupla_conferencia"):
    def coletar(self, robo, comando):
        self._conferir(comando)
        comando.executar(robo)
        self._conferir(comando)
        
    def _conferir(self, comando):
        if not comando.codinome or comando.quantidade <= 0:
            raise PedidoInvalido(
                f"item {comando.codinome!r} não passou na dupla conferência"
                f"(quantidade={comando.quantidade})"
            )