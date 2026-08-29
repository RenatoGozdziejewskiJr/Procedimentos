# Guia de Instalação e Configuração do TigerVNC no Radxa A7s
Este documento descreve o procedimento passo a passo para instalar, configurar e automatizar a inicialização do TigerVNC em uma placa Radxa A7s acessada de forma *headless* (sem monitor), utilizando um túnel SSH para garantir a segurança da conexão.

## Pré-requisitos
- Placa Radxa A7s rodando Linux com interface gráfica já instalada.
- Acesso via terminal (SSH) à placa.
- Cliente TigerVNC Viewer instalado no computador host (ex: Windows).

---

## Passo 1: Instalar o Servidor VNC
Acesse o Radxa via SSH e instale o pacote do servidor TigerVNC.

```bash
sudo apt update
sudo apt install tigervnc-standalone-server

```

## Passo 2: Configurar a Senha de Acesso
Crie a senha que será solicitada ao conectar pelo VNC Viewer.

```bash
vncpasswd

```
*Nota: Quando perguntado se deseja criar uma senha "view-only" (apenas visualização), você pode responder *`n`* (não).*

## Passo 3: Configurar o Script de Inicialização (xstartup)
Crie o arquivo que diz ao VNC qual interface gráfica deve ser carregada.

1. Abra o arquivo para edição:

```bash
nano ~/.vnc/xstartup

```

1. Cole o seguinte conteúdo (isso fará o VNC usar o ambiente gráfico padrão do sistema):

```bash
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
export XDG_SESSION_TYPE=x11
export DESKTOP_SESSION=plasma
exec startplasma-x11

```

1. Salve o arquivo e dê permissão de execução:

```bash
chmod +x ~/.vnc/xstartup

```

---

## Passo 4: Criar o Serviço para Inicialização Automática (systemd)
Para que o VNC inicie sozinho toda vez que a placa for ligada, criaremos um serviço no systemd.

1. Crie o arquivo de serviço:

```bash
sudo nano /etc/systemd/system/vncserver@.service

```

1. Cole o conteúdo abaixo. **Atenção:** Substitua todas as três ocorrências de `SEU_USUARIO` pelo seu nome de usuário real no Radxa:

```ini
[Unit]
Description=Servidor TigerVNC
After=syslog.target network.target

[Service]
Type=forking
User=SEU_USUARIO
Group=SEU_USUARIO
WorkingDirectory=/home/SEU_USUARIO

# A linha PIDFile foi intencionalmente omitida para evitar problemas de timeout de inicialização
ExecStartPre=-/usr/bin/vncserver -kill :%i > /dev/null 2>&1
ExecStart=/usr/bin/vncserver -localhost yes :%i
ExecStop=/usr/bin/vncserver -kill :%i

[Install]
WantedBy=multi-user.target

```

1. Salve e saia.

## Passo 5: Habilitar e Iniciar o Serviço
1. Recarregue a lista de serviços do sistema:

```bash
sudo systemctl daemon-reload

```

1. (Opcional) Limpe possíveis arquivos de trava residuais de execuções anteriores:

```bash
sudo rm -rf /tmp/.X1-lock /tmp/.X11-unix/X1

```

1. Habilite o serviço para rodar no boot (o `1` define o display na porta `:1` ou 5901):

```bash
sudo systemctl enable vncserver@1.service

```

1. Inicie o serviço:

```bash
sudo systemctl start vncserver@1.service

```

1. Verifique se está rodando corretamente (deve constar como *active (running)*):

```bash
sudo systemctl status vncserver@1.service

```

---

## Passo 6: Conectar a partir do Computador Host
Como configuramos o VNC com `-localhost yes` por segurança, o acesso deve ser feito via túnel SSH.

1. No seu computador (Windows/WSL ou outro Linux/Mac), abra um terminal e crie o túnel:

```bash
ssh -L 5901:localhost:5901 SEU_USUARIO@IP_DO_RADXA

```
*(Mantenha esta janela de terminal aberta enquanto estiver usando o VNC).*

1. Abra o **TigerVNC Viewer**.
2. No campo "VNC server", digite: `localhost:5901` (ou `127.0.0.1:5901`).
3. Conecte e insira a senha definida no Passo 2.