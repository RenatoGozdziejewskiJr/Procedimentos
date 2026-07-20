# Guia de Gerenciamento do WSL e Apps Linux

Dicas para gerenciar distros no **Windows Subsystem for Linux (WSL)** e instalar ferramentas gráficas.

## Comandos Básicos (Executar no PowerShell/CMD)

```powershell
# Listar todas as distros instaladas e verificar a imagem ativa
wsl -l -v
# ou
wsl --list --verbose

# Ver distros disponíveis para download
wsl --list --online

# Instalar uma nova distro (ex: Ubuntu)
wsl --install -d <NomeDaDistro>

# Alterar a distro padrão (aquela que abre quando você apenas digita 'wsl')
wsl --set-default ubuntu

# Remover/Desinstalar uma distro do WSL
wsl --unregister <NomeDaDistro>
```

## Dentro do Linux (Executar no Terminal do WSL)

### Verificar Versão do Linux
```bash
lsb_release -a
```

### Atualização Básica
```bash
sudo apt update && sudo apt upgrade -y
```

## Instalação de Ferramentas e Apps Gráficos (GUI)
O WSL (especialmente a versão 2 com WSLg) permite rodar aplicações gráficas nativas do Linux dentro do Windows.

### Ferramentas de Sistema e Produtividade
```bash
# Editor de Texto Gedit
sudo apt install gedit -y

# Gerenciador de Arquivos Nautilus (útil para navegar nos arquivos do Linux visualmente)
sudo apt install nautilus -y

# Editor de Imagens GIMP
sudo apt install gimp -y

# Reprodutor Multimídia VLC
sudo apt install vlc -y

# Apps básicos do X11 (para testes de GUI, ex: xeyes)
sudo apt install x11-apps -y
```

### Instalação de Navegadores e Apps Proprietários (pacotes `.deb`)

**Google Chrome:**
```bash
cd /tmp
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb 
# Caso falte alguma dependência, o comando abaixo corrige e finaliza a instalação:
sudo apt install --fix-broken -y
```

**Microsoft Edge (Dev Version):**
```bash
curl -O https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-dev/microsoft-edge-dev_118.0.2060.1-1_amd64.deb
sudo dpkg -i microsoft-edge-dev_118.0.2060.1-1_amd64.deb
sudo apt install --fix-broken -y
```

**Microsoft Teams:**
```bash
cd /tmp
curl -L -o "./teams.deb" "https://teams.microsoft.com/downloads/desktopurl?env=production&plat=linux&arch=x64&download=true&linuxArchiveType=deb"
sudo apt install ./teams.deb -y
```
