# Guia Completo: Instalação e Configuração de Plugins no Tmux
Este guia detalha o processo para transformar seu `tmux` padrão em uma ferramenta poderosa e visualmente agradável, utilizando o **TPM (Tmux Plugin Manager)**.

---

## 0. Pré-requisito: Instalar o Tmux
Caso o `tmux` e o `git` não estejam instalados no seu Linux, instale-os via gerenciador de pacotes (exemplo para Ubuntu/Debian):

```bash
sudo apt update && sudo apt install tmux git

```

---

## 1. Instalando o Gerenciador de Plugins (TPM)
Este é o passo fundamental para gerenciar os plugins. O download deve ser feito no seu terminal normal, **fora do tmux**.

Execute o comando abaixo para clonar o repositório oficial do TPM diretamente para a pasta onde o tmux o reconhecerá (`~/.tmux/plugins/tpm`):

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

```

---

## 2. Criando o Arquivo de Configuração
Toda a personalização do tmux fica no arquivo `~/.tmux.conf`. Ainda fora do tmux, crie e edite este arquivo:

```bash
nano ~/.tmux.conf

```
Copie e cole a configuração abaixo:

```tmux
# ==========================================
# Configurações Base e Usabilidade
# ==========================================
set -g mouse on                           # Habilita suporte ao mouse
set -g default-terminal "screen-256color" # Habilita suporte a 256 cores reais

# ==========================================
# Lista de Plugins
# ==========================================
# 1. O próprio Gerenciador de Plugins (Obrigatório estar aqui)
set -g @plugin 'tmux-plugins/tpm'

# 2. Configurações sensatas e úteis
set -g @plugin 'tmux-plugins/tmux-sensible'

# 3. Tema Dracula
set -g @plugin 'dracula/tmux'
set -g @dracula-show-powerline true
set -g @dracula-plugins "cpu-usage ram-usage ssh-session time"
set -g @dracula-show-flags true
set -g @dracula-show-left-icon session

# ==========================================
# Inicialização do TPM
# ==========================================
# ATENÇÃO: Esta linha deve ser SEMPRE a última do arquivo ~/.tmux.conf
run '~/.tmux/plugins/tpm/tpm'

```
Salve o arquivo e saia do editor.

---

## 3. Aplicando e Instalando de Fato
1. Inicie o tmux normalmente:
   ```bash
      tmux
      
   ```
2. Dentro do tmux, instale os plugins baixados usando o atalho:*Pressione e solte: *`Ctrl + b`Em seguida, pressione: `I` (i maiúsculo)
*O tmux vai congelar por alguns instantes para baixar e aplicar o tema. Pressione *`ESC`* ou *`Enter`* para fechar a tela de log se ela aparecer.*