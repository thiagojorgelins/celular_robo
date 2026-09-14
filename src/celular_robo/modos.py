# State — ModoColetando, ModoAguardandoVerificacao — enunciado, Seção 2.3.
#
# Herde de `ModoOperacao` (modos_base.py — ABC com registro automático):
#
#   from celular_robo.modos_base import ModoOperacao
#
# TODO: implemente aqui. A transição ModoColetando -> ModoAguardandoVerificacao
# acontece via Observer (não é o próprio modo que decide sozinho), quando a
# bandeja completa.

from celular_robo.modos_base import ModoOperacao
from celular_robo.observadores_base import Observador

class ModoColetando(ModoOperacao):
    def mover(self, robo):
        if not robo._comandos_pendentes:
            return False
        comando = robo._comandos_pendentes.pop(0)
        robo.estrategia.coletar(robo, comando)
        robo._historico_comandos.append(comando)
        if robo.bandeja.esta_completa():
            robo.notificar("bandeja_pronta", pedido=robo.pedido_atual)
        return True
    

class ModoAguardandoVerificacao(ModoOperacao):
    def mover(self, robo):
        print(f"{robo.nome} está aguardando verificação da bandeja; coleta pausada.")
        return False


class MonitorBandeja(Observador):
    def atualizar(self, evento, **dados):
        if evento == "bandeja_pronta":
            dados["robo"].modo = ModoAguardandoVerificacao()