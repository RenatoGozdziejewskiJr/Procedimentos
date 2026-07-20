# Geração de Chaves SSH

Este guia explica como gerar um par de chaves SSH no seu computador e configurá-lo no Raspberry Pi para acesso sem senha.

## 1. Gerar o par de chaves

Abra o terminal do seu computador (Windows, Mac ou Linux) e digite o seguinte comando:

```bash
ssh-keygen -t ed25519
```

O terminal fará algumas perguntas (como o local para salvar e se deseja adicionar uma senha extra). Apenas **pressione Enter** para todas as perguntas, aceitando as opções padrão. Isso irá gerar sua chave privada e pública.

## 2. Enviar a chave pública para o Raspberry Pi

Agora, é necessário enviar a chave pública (o "cadeado") para o Raspberry Pi. O comando varia dependendo do seu sistema operacional.

### Para Mac, Linux ou Git Bash no Windows:

```bash
ssh-copy-id pi@raspberrypi
```
*(Substitua `pi@raspberrypi` pelo seu usuário e IP, ou IP do Tailscale, se aplicável).*

Se você gerou a chave no Windows e vai enviá-la pelo WSL:

```bash
ssh-copy-id -i /mnt/c/Users/renat/.ssh/id_ed25519.pub engenharia@renato-pi
```

> **Nota:** Será solicitada a sua senha pela última vez para instalar a chave no servidor.

### Para Prompt de Comando (CMD) ou PowerShell no Windows:

Como o Windows não possui o comando `ssh-copy-id` nativamente, copie e cole o comando abaixo (substituindo `pi@raspberrypi` pelo seu usuário/IP):

```cmd
type %USERPROFILE%\.ssh\id_ed25519.pub | ssh pi@raspberrypi "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## 3. Testar a conexão

No terminal do seu computador, tente conectar novamente:

```bash
ssh pi@raspberrypi
```

Se tudo deu certo, você entrará direto no terminal do Raspberry Pi, sem que nenhuma senha seja solicitada! 

Outro exemplo de conexão especificando o caminho da chave:

```bash
ssh -i /mnt/c/Users/renat/.ssh/id_ed25519 engenharia@renato-pi
```

---

## Bônus: Copiar a chave do Windows para o WSL

### 1. Copiar a chave para a pasta nativa do WSL

No terminal do WSL, digite o comando abaixo para copiar a chave do disco C do Windows para a pasta oculta `.ssh` do seu Linux virtual:

```bash
cp /mnt/c/Users/renat/.ssh/id_ed25519 ~/.ssh/
```

### 2. Ajustar as permissões da chave

É necessário informar ao Linux que apenas você pode ler esse arquivo. Execute o comando:

```bash
chmod 600 ~/.ssh/id_ed25519
```

### 3. Testar o acesso simplificado

Como a chave agora está no local padrão e seguro do Linux (`~/.ssh/`), você não precisa mais especificar o caminho completo. Basta digitar:

```bash
ssh engenharia@renato-pi
```