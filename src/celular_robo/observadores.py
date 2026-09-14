# Observer — EquipeDeTestes, RegistroAuditoria — enunciado, Seção 2.3.
#
# Herde de `Observador` (observadores_base.py — ABC com registro automático):
#
#   from celular_robo.observadores_base import Observador
#
# TODO: implemente aqui. EquipeDeTestes(Observador) reage a "bandeja_pronta";
# RegistroAuditoria(Observador) loga todo evento (coleta, bandeja pronta,
# pedido rejeitado), pensando em trilha de auditoria, não só depuração.
from celular_robo.observadores_base import Observador

class EquipeDeTestes(Observador):
    def __init__(self):
        self.notificacoes = []
        
    def atualizar(self, evento, **dados):
        if evento == "bandeja_pronta":
            mensagem = f"[EquipeDeTestes] bandeja de {dados['robo'].nome} pronta para retirada"
            self.notificacoes.append(mensagem)
            print(mensagem)
        
    
class RegistroAuditoria(Observador):
    def __init__(self):
        self.trilha = []
        
    def atualizar(self, evento, **dados):
        detalhes = {chave: valor for chave, valor in dados.items() if chave != "robo"}
        self.trilha.append({"evento": evento, **detalhes})
        
    def __len__(self):
        return len(self.trilha)