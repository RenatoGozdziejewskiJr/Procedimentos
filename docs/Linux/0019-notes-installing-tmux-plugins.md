# Notes about installing and configuring tmux plugins

[Português (Brasil)](./0019-notas-instalacao-plugins-tmux-pt-br.md)

This guide explains how to turn a standard `tmux` installation into a powerful and visually appealing tool using **TPM (Tmux Plugin Manager)**.

---

## 1. Prerequisite: install tmux
If `tmux` and `git` are not installed on your Linux system, install them with the package manager (Ubuntu/Debian example):

```bash
sudo apt update && sudo apt install tmux git

```

---

## 2. Installing the plugin manager (TPM)
This is the essential step for managing plugins. Run the download in a regular terminal, **outside tmux**.

Run the following command to clone the official TPM repository into the directory where tmux will find it (`~/.tmux/plugins/tpm`):

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

```

---

## 3. Creating the configuration file
All tmux customisation is stored in `~/.tmux.conf`. Still outside tmux, create and edit this file:

```bash
nano ~/.tmux.conf

```
Copy and paste the configuration below:

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
Save the file and exit the editor.

---

## 4. Applying the configuration and installing plugins
1. Start tmux as usual:
   ```bash
      tmux
      
   ```
2. Inside tmux, install the downloaded plugins with this shortcut: press and release `Ctrl + b`, then press `I` (uppercase i).

   Tmux will pause briefly while it downloads and applies the theme. Press `ESC` or `Enter` to close the log screen if it appears.
