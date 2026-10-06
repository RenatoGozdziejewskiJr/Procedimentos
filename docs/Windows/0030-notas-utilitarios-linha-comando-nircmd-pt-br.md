# Notas sobre utilitários de linha de comando do NirCmd

[English (UK)](0030-notes-nircmd-command-line-utilities.md)

[NirCmd](https://www.nirsoft.net/utils/nircmd.html) é um pequeno utilitário de linha de comando para Windows que permite executar diversas tarefas do sistema sem exibir uma interface gráfica.

## 1. Comandos úteis

### 1.1 Manter uma janela sempre no topo

Force um aplicativo a permanecer acima das outras janelas.
O exemplo abaixo mantém o Wireshark no topo:
```cmd
nircmd win settopmost process Wireshark.exe 1
```
*(Para desativar, mude `1` para `0`.)*

### 1.2 Ativar ou focar uma janela específica

Traga uma janela para o primeiro plano com base no título:
```cmd
nircmd win activate title "TeamViewer"
```

### 1.3 Reproduzir um bipe

Reproduza um bipe pelo alto-falante do sistema. Sintaxe: `nircmd beep [Frequência] [Duração_em_ms]`
```cmd
nircmd beep 800 2000 
```
