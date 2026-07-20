# NirCmd - Utilitários de Linha de Comando

O [NirCmd](https://www.nirsoft.net/utils/nircmd.html) é um pequeno utilitário de linha de comando para Windows que permite realizar diversas tarefas do sistema sem exibir interface gráfica.

## Comandos Úteis

### Manter uma Janela Sempre no Topo (Always on Top)
Para forçar um aplicativo a ficar sempre por cima das outras janelas.
No exemplo abaixo, travamos o Wireshark no topo:
```cmd
nircmd win settopmost process Wireshark.exe 1
```
*(Para desativar, mude o `1` para `0`)*

### Ativar / Focar uma Janela Específica
Traz uma janela para o primeiro plano baseando-se no seu título:
```cmd
nircmd win activate title "TeamViewer"
```

### Tocar um Bip (Som)
Reproduz um som de bipe através do alto-falante do sistema. Sintaxe: `nircmd beep [Frequência] [Duração_em_ms]`
```cmd
nircmd beep 800 2000 
```
