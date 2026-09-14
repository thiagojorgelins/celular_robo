# Robô Coletor de Celulares

## Setup

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Como rodar

Testes (a partir da raiz do projeto):

```bash
pytest -v
```

## Decisões de projeto

- **Bandeja**: implementada como classe própria (`Bandeja`, em `robo.py`),
  não como `dict` solto em `RoboColetor`. Internamente guarda um
  `ItemBandeja` por codinome, cada um com `quantidade_coletada` validada
  pelo descriptor `QuantidadeValida`. `len(bandeja)` retorna o total de
  unidades já coletadas.
- **`QuantidadeValida`**: como a quantidade máxima válida varia por item
  (depende de `quantidade_pedida`, não é fixa por classe como
  `Coordenada(0, LADO_GRADE)`), o descriptor lê o limite do próprio
  `ItemBandeja` (`getattr(instance, "quantidade_pedida")`) em vez de
  receber `minimo`/`maximo` no `__init__`.
- **Navegação em `ComandoColeta`**: para "navegar até cada posição" o
  comando reaproveita `girar_ate`/`avancar_n` já prontos em `Robo`
  (respeitando `sensor`/`obstaculos` de verdade, não um teleporte). Se o
  robô ficar bloqueado por um obstáculo no caminho, ele para antes do
  alvo (mesmo comportamento de `avancar()`); a coleta em si não é abortada
  nesse caso.
- **Conflito `fragil`+`urgente` no mesmo item** (Seção 2.4): recusado com
  `PedidoInvalido`, é um problema no **conteúdo** do item em si (pedir as
  duas rotas ao mesmo tempo), não na configuração do robô.
- **Conflito entre itens do mesmo pedido** (um `urgente`, outro `fragil`):
  também `PedidoInvalido`, verificado em `validar_pedido`
  (`persistencia.py`) antes de processar qualquer item, `robo.estrategia`
  é única por robô e não pode satisfazer as duas exigências.
- **Item `fragil`/`urgente` vs. estratégia do robô** (dimensão 4 do LPS):
  como esse cruzamento depende do robô específico (não só do JSON de
  config), a checagem mora em `validar_requisitos_item`
  (`modelo_features.py`) e é chamada por `executar_pedido`
  (`persistencia.py`), não em `validar_configuracao`, que não tem acesso
  aos itens do pedido. Mismatch levanta `ConfiguracaoInvalida`.
- **Pedido com item inválido**: rejeita o pedido inteiro (`PedidoInvalido`
  em `validar_pedido`) em vez de pular o item, mantém o "tudo ou nada" já
  usado no conflito acima, e é mais simples de auditar.
- **Par baixo-nível / validado**: seguindo o mesmo padrão de
  `criar_robo_coletor`/`criar_robo_configurado`, `robo.processar_pedido`
  (baixo nível, sem validar) tem um par validado,
  `persistencia.executar_pedido`, que roda `validar_pedido` +
  `validar_requisitos_item` antes de delegar.
- **Observers padrão**: `criar_robo_coletor` já registra `MonitorBandeja`
  (conector Observer→State), `EquipeDeTestes` e `RegistroAuditoria` em todo
  robô criado.
- **Testes com os arquivos .json de `dados/`**: além dos testes com fixtures em
  memória, `test_fluxo_completo.py` também exercita `montar_robo_de_config`
  e `montar_pedido_de_json` direto sobre `config_robo_exemplo.json`,
  `pedido_coleta_valido_exemplo.json` e `pedido_coleta_exemplo.json` (esse
  último, o exemplo literal do enunciado, confirmando que ele levanta
  `PedidoInvalido` de propósito). O caminho da pasta `dados/` é
  resolvido pela fixture `caminho_dados` (`conftest.py`), via
  `pytestconfig.rootpath`, não depende do diretório de onde `pytest` é
  chamado.

| Mecanismo | Arquivo / classe |
|---|---|
| Descriptors (posição) | `robo_base.Coordenada` (herdado por `RoboColetor`) |
| Descriptor novo (quantidade) | `robo.QuantidadeValida` |
| Métodos especiais (`__str__`/`__repr__`/`__len__`) | `robo.RoboColetor`, `robo.Bandeja` |
| `__init_subclass__` / registro automático (robôs) | `robo_base.Robo._registro` (usado por `RoboColetor`) |
| `__init_subclass__` / registro automático (rotas) | `estrategias.RotaColeta._registro_rotas` |
| Strategy | `estrategias.RotaDireta`, `estrategias.RotaComDuplaConferencia` |
| Command (+ undo) | `comandos.ComandoColeta` (`.executar`/`.desfazer`) |
| Factory | `fabrica.criar_robo_coletor`, `fabrica.criar_robo_configurado` |
| Observer | `observadores.EquipeDeTestes`, `observadores.RegistroAuditoria` |
| State | `modos.ModoColetando`, `modos.ModoAguardandoVerificacao` |
| Observer → State (conector) | `modos.MonitorBandeja` |
| Modelo de features / LPS | `modelo_features.py` (`TIPOS_VALIDOS`, `ESTRATEGIAS_VALIDAS`, `REQUER`, `EXCLUI`, `validar_configuracao`, `validar_requisitos_item`) |
| Hierarquia de exceções | `excecoes.py` (`ErroColeta`, `ConfiguracaoInvalida`, `PedidoInvalido`) |
| Configuração/persistência | `persistencia.py` (`montar_robo_de_config`, `montar_pedido_de_json`, `executar_pedido`) |
| Testes | `tests/test_configuracao.py`, `tests/test_pedido.py`, `tests/test_fluxo_completo.py` (inclui testes com os JSONs de `dados/`) (+ `tests/test_00_fornecido.py`, fornecido) |
