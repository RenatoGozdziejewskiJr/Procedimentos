# Guia de Configuração do Servidor VNC no Radxa Cubie A7S

Este procedimento descreve o passo a passo para instalar e configurar o servidor VNC (**TigerVNC**) no dispositivo **Radxa Cubie A7S**, permitindo o controle da área de trabalho gráfica remotamente via rede local, baseado na documentação oficial da Radxa.

---

## 1. Pré-requisitos

- Dispositivo **Radxa Cubie A7S** com sistema operacional e ambiente gráfico instalados (ex.: Radxa OS com KDE Plasma).
- Acesso ao terminal do Radxa (direto via console ou via SSH).
- Ambos os dispositivos (computador cliente e Radxa) conectados na mesma rede local.
- Para acessar a área de trabalho remota a partir do computador cliente, utilize um cliente VNC de sua preferência, como **TigerVNC Viewer** ou **RealVNC Viewer**.

---

## 2. Instalação do Servidor VNC

Acesse o terminal do Radxa A7S e instale os pacotes necessários:

```bash
sudo apt update
sudo apt install tigervnc-standalone-server tigervnc-common -y
```

---

## 3. Definir a Senha de Acesso Remoto

Defina a senha que será solicitada durante a conexão VNC:

```bash
vncpasswd
```

- Digite a senha e confirme-a (os caracteres não serão exibidos na tela).
- Quando questionado se deseja criar uma senha apenas para visualização (*view-only password*):
  ```text
  Would you like to enter a view-only password (y/n)? n
  ```
  Digite `n` e pressione Enter.

---

## 4. Configurar o Arquivo de Inicialização do VNC (`xstartup`)

Crie e edite o arquivo `~/.vnc/xstartup` para definir o ambiente de desktop gráfico que será carregado:

1. Abra o arquivo com o editor `nano`:

```bash
nano ~/.vnc/xstartup
```

2. Adicione o seguinte conteúdo:

```bash
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
export XDG_SESSION_TYPE=x11
export DESKTOP_SESSION=plasma
exec startplasma-x11
```

3. Salve o arquivo (`Ctrl + O`, `Enter`) e saia (`Ctrl + X`).

4. Torne o arquivo executável:

```bash
chmod +x ~/.vnc/xstartup
```

---

## 5. Gerenciamento do Servidor VNC

### Iniciar o Servidor VNC
Para iniciar o servidor permitindo conexões remotas de outros dispositivos da rede, utilize o parâmetro `-localhost no`:

```bash
vncserver -localhost no
```

Após a inicialização, o terminal exibirá uma mensagem indicando o número do display e a porta utilizada (por padrão, display `:1` na porta `5901`):
```text
New Xtigervnc server 'radxa:1 (radxa)' on port 5901 for display :1.
```

### Verificar o Status das Sessões Ativas
Para listar as sessões do VNC em execução:

```bash
vncserver -list
```

A saída mostrará o identificador do display (`X DISPLAY #`), a porta (`RFB PORT #`) e o ID do processo.

### Parar o Servidor VNC
Para encerrar uma sessão específica, informe o número do display (por exemplo, `:1`):

```bash
vncserver -kill :1
```

---

## 6. Conexão a partir do Cliente VNC

1. Abra o cliente VNC no computador remoto (**RealVNC Viewer** ou **TigerVNC Viewer**).
2. No campo de endereço/servidor, informe o endereço IP do Radxa seguido do display ou porta:
   - Exemplo: `<IP_DO_RADXA>:1` ou `<IP_DO_RADXA>:5901`
3. Conecte-se e insira a senha criada no **Passo 3**.

---

## 7. Dicas e Resolução de Problemas

- **Tela preta ao conectar via VNC:**
  Caso encontre uma tela preta após a autenticação, verifique se a opção de **auto-login** do sistema está ativada. Se estiver ativada, desative o auto-login nas configurações do sistema do Radxa para evitar conflitos de sessão com o servidor X.
- **Portas e Displays:**
  Cada sessão VNC utiliza uma porta baseada em `5900 + número do display` (ex.: `:1` = `5901`, `:2` = `5902`).

---

## 8. Inicialização Automática no Boot (systemd)

Para dispositivos que operam no modo *headless* (sem monitor), a forma recomendada e integrada às versões atuais do TigerVNC no Debian/Ubuntu é utilizar o serviço nativo `tigervncserver@.service`.

Dessa forma, o servidor VNC iniciará automaticamente com o boot do sistema, sem necessidade de conexão manual prévia por SSH.

---

### Passo a Passo de Configuração

#### 1. Associar o Display ao Usuário
Edite o arquivo global de atribuição de usuários `/etc/tigervnc/vncserver.users`:

```bash
sudo nano /etc/tigervnc/vncserver.users
```

Adicione a linha abaixo mapeando o display `:1` para o seu usuário (substitua `radxa` pelo seu nome de usuário real se for diferente):
```text
:1=radxa
```
Salve com `Ctrl + O`, `Enter` e saia com `Ctrl + X`.

#### 2. Configurar os Parâmetros da Sessão do Usuário
Crie ou edite o arquivo `~/.vnc/config` no diretório do usuário:

```bash
nano ~/.vnc/config
```

Adicione as configurações de ambiente, resolução e liberação de rede:
```text
session=plasma
geometry=1280x720
localhost=0
```

> **Dica de Desempenho:** A resolução `1280x720` (HD) ou `1366x768` proporciona uma experiência muito mais fluida e reduz o uso de CPU/RAM e temperatura da placa em comparação a `1920x1080` (Full HD). Caso precise de mais espaço de tela, altere para `1920x1080`.

#### 3. Habilitar e Iniciar o Serviço no Boot
Recarregue o gerenciador do systemd e ative o serviço (observe os dois pontos `:` antes do 1):

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now tigervncserver@:1.service
```

#### 4. Verificar o Status do Serviço
Confirme se o serviço está ativo e em execução:

```bash
sudo systemctl status tigervncserver@:1.service
```

Se precisar consultar os logs em tempo real para diagnóstico:
```bash
journalctl -u tigervncserver@:1.service -e --no-pager
```

#### 5. Parar ou Reiniciar o Serviço (quando necessário)
- Para reiniciar: `sudo systemctl restart tigervncserver@:1.service`
- Para parar: `sudo systemctl stop tigervncserver@:1.service`
- Para desativar da inicialização: `sudo systemctl disable tigervncserver@:1.service`