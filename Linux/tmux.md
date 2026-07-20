# Guia Básico do Tmux

O **tmux** (Terminal Multiplexer) permite criar "janelas" virtuais que continuam rodando em segundo plano mesmo se a sua conexão SSH cair.

## Instalação

Para instalar o tmux em sistemas baseados em Debian/Ubuntu (como o Raspberry Pi OS):

```bash
sudo apt install tmux -y
```

## Comandos Úteis (No Terminal)

| Comando | Descrição |
|---------|-----------|
| `tmux new -s meuserver` | Inicia uma nova sessão nomeada como "meuserver" |
| `tmux ls` | Mostra os processos/sessões rodando no tmux no momento |
| `tmux attach -t meuserver` | Retorna (conecta-se) à sessão ativa "meuserver" |
| `tmux kill-session -t meuserver` | Encerra (mata) a sessão "meuserver" |
| `tmux kill-server` | Encerra (mata) todas as sessões do tmux |
| `exit` (ou `Ctrl+D`) | Encerra a sessão ativa de dentro dela |

## Atalhos de Teclado (Dentro do Tmux)

Todos os atalhos do tmux exigem que você pressione um **prefixo** antes do comando. O prefixo padrão é `Ctrl + B`.

Após pressionar e soltar `Ctrl + B`, pressione uma das teclas abaixo:

| Atalho | O que faz |
|--------|-----------|
| `%` | Divide a sua tela ao meio na vertical (lado a lado) |
| `"` | Divide a sua tela ao meio na horizontal (cima e baixo) |
| `Setas` | Pula de uma tela dividida para a outra (navegação) |
| `x` | Fecha o painel/tela dividida onde o seu cursor está no momento |
| `c` | Cria uma nova aba/janela limpa (janela inteira) |
| `n` | Pula para a próxima aba (Next) |
| `p` | Volta para a aba anterior (Prev) |
| `d` | Sai da sessão deixando tudo rodando em segundo plano (Detach) |