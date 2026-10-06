# Notas sobre geração de chaves SSH

[English (UK)](0025-notes-ssh-key-generation.md)

Este guia explica como gerar um par de chaves SSH no computador e configurá-lo no Raspberry Pi para acesso sem senha.

## 1. Gerar o par de chaves

Abra o terminal do computador (Windows, Mac ou Linux) e digite o seguinte comando:

```bash
ssh-keygen -t ed25519
```

O terminal perguntará onde salvar a chave e se deseja adicionar uma senha. Pressione **Enter** para aceitar o local padrão do arquivo; em seguida, defina e confirme uma senha forte. Deixar a senha vazia reduz a proteção caso alguém obtenha a chave privada.

## 2. Enviar a chave pública para o Raspberry Pi

Agora, envie a chave pública (o “cadeado”) para o Raspberry Pi. O comando depende do seu sistema operacional.

### 2.1 Mac, Linux ou Git Bash no Windows

```bash
ssh-copy-id pi@raspberrypi
```
*(Substitua `pi@raspberrypi` pelo seu usuário e endereço IP, ou pelo IP do Tailscale, se aplicável.)*

Se você gerou a chave no Windows e vai enviá-la pelo WSL:

```bash
ssh-copy-id -i /mnt/c/Users/WINDOWS_USERNAME/.ssh/id_ed25519.pub engenharia@renato-pi
```

> **Nota:** Será solicitada sua senha pela última vez para instalar a chave no servidor.

### 2.2 Prompt de Comando (CMD) ou PowerShell no Windows

Como o Windows não inclui o comando `ssh-copy-id` nativamente, copie e cole o comando abaixo (substituindo `pi@raspberrypi` pelo seu usuário e endereço IP):

```cmd
type %USERPROFILE%\.ssh\id_ed25519.pub | ssh pi@raspberrypi "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## 3. Testar a conexão

No terminal do computador, tente conectar-se novamente:

```bash
ssh pi@raspberrypi
```

Se tudo deu certo, você entrará diretamente no terminal do Raspberry Pi sem que uma senha seja solicitada.

Outro exemplo de conexão especificando o caminho da chave:

```bash
ssh -i /mnt/c/Users/WINDOWS_USERNAME/.ssh/id_ed25519 engenharia@renato-pi
```

## 4. Copiar a chave do Windows para o WSL

### 4.1 Copiar a chave para a pasta nativa do WSL

No terminal do WSL, digite o comando abaixo para copiar a chave do disco C do Windows para o diretório oculto `.ssh` do Linux virtual:

```bash
cp /mnt/c/Users/WINDOWS_USERNAME/.ssh/id_ed25519 ~/.ssh/
```

### 4.2 Ajustar as permissões da chave

Informe ao Linux que somente você pode ler esse arquivo. Execute:

```bash
chmod 600 ~/.ssh/id_ed25519
```

### 4.3 Testar o acesso simplificado

Como a chave agora está no local padrão e seguro do Linux (`~/.ssh/`), você não precisa mais especificar o caminho completo. Digite:

```bash
ssh engenharia@renato-pi
```
