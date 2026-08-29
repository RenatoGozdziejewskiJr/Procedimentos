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