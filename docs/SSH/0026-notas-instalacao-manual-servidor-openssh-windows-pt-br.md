# Notas sobre instalação manual do OpenSSH Server no Windows

[English (UK)](0026-notes-manual-openssh-server-installation-windows.md)

Este guia descreve como instalar manualmente o OpenSSH Server no Windows 11 usando o repositório oficial da Microsoft e como configurar chaves públicas para acesso sem senha.

## 1. Baixar o pacote oficial

1. Acesse a página de lançamentos oficiais do projeto no GitHub:
   [PowerShell/Win32-OpenSSH Releases](https://github.com/powershell/win32-openssh/releases)
2. Localize a versão estável mais recente.
3. Na seção **Assets**, baixe o arquivo compactado de 64 bits:
   `OpenSSH-Win64.zip`

## 2. Extrair e posicionar os arquivos

1. Abra o arquivo `.zip` baixado e extraia todo o conteúdo.
2. Renomeie a pasta extraída para `OpenSSH`.
3. Mova essa pasta para o diretório padrão de programas do sistema:
   `C:\Program Files\OpenSSH`

## 3. Executar o script de instalação

1. Clique com o botão direito no menu Iniciar e selecione **Terminal (Administrador)** ou **PowerShell (Administrador)**.
2. Navegue até a pasta para onde os arquivos foram movidos:
   ```powershell
   cd "C:\Program Files\OpenSSH"
   ```
3. Execute o script oficial de instalação incluído no pacote:
   ```powershell
   .\install-sshd.ps1
   ```
4. Confirme se a mensagem retornada no console indica que a instalação foi bem-sucedida.

## 4. Configurar e iniciar o serviço

Ainda no PowerShell com privilégios de Administrador, execute os comandos abaixo para configurar o serviço para iniciar com o Windows e iniciá-lo imediatamente:

```powershell
# Define a inicialização do serviço como Automática
Set-Service -Name sshd -StartupType 'Automatic'

# Inicia o serviço do servidor OpenSSH
Start-Service sshd
```

## 5. Copiar manualmente as chaves públicas (acesso sem senha)

O comando tradicional `ssh-copy-id` do Linux falha ao interagir com o Windows porque não há um interpretador bash nativo. Configure a chave inserindo diretamente o texto da chave pública no host de destino.

### 5.1 Formato do arquivo `authorized_keys`

O arquivo `authorized_keys` deve ser um arquivo de texto simples **sem extensão** (por exemplo, não deve ser `.txt`). Cada chave pública deve ocupar **exatamente uma linha inteira**. Se houver chaves de vários computadores, acrescente cada uma em uma linha separada.

**Exemplo do conteúdo do arquivo:**
```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK... usuario@computador1
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQ... usuario@computador2
```

### 5.2 Criar o arquivo e definir as permissões (usuário comum)

No PowerShell do host, execute os comandos abaixo para criar o diretório, inserir a chave e definir a codificação. O OpenSSH **rejeita** arquivos que não estejam em UTF-8 puro (sem BOM):

```powershell
# 1. Garante a existência do diretório .ssh no perfil do usuário atual
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.ssh"

# 2. Cria o arquivo authorized_keys com o conteúdo da sua chave pública
# Substitua 'sua-chave-publica-aqui' pelo conteúdo real do seu arquivo .pub
Set-Content -Path "$env:USERPROFILE\.ssh\authorized_keys" -Value "sua-chave-publica-aqui"

# NOTA: Para adicionar chaves secundárias futuramente sem apagar as anteriores, use:
# Add-Content -Path "$env:USERPROFILE\.ssh\authorized_keys" -Value "nova-chave-publica-aqui"

# 3. Força a codificação correta para UTF-8 sem BOM (Obrigatório para o OpenSSH aceitar)
[System.IO.File]::WriteAllLines("$env:USERPROFILE\.ssh\authorized_keys", [System.IO.File]::ReadAllLines("$env:USERPROFILE\.ssh\authorized_keys"))

# 4. Restringe o acesso à pasta .ssh e ao arquivo de chaves
icacls "$env:USERPROFILE\.ssh" /inheritance:r /grant "$($env:USERNAME):F" /grant "NT AUTHORITY\SYSTEM:F"
icacls "$env:USERPROFILE\.ssh\authorized_keys" /inheritance:r /grant "$($env:USERNAME):F" /grant "NT AUTHORITY\SYSTEM:F"
```

## 6. Fazer alterações críticas em `sshd_config`

Por padrão, o OpenSSH do Windows usa `C:\ProgramData\ssh\administrators_authorized_keys` para contas do grupo Administradores. As demais contas usam o arquivo `authorized_keys` no próprio perfil. Mantenha habilitada a verificação rigorosa de permissões; não defina `StrictModes no`, pois isso desativa essas verificações.

Para usar o arquivo de chaves do perfil de uma conta do grupo Administradores, edite o arquivo de configuração somente se essa for uma escolha intencional e se o arquivo de chaves e a pasta `.ssh` tiverem permissões restritas:

1. Abra o **Bloco de Notas como Administrador**.
2. Abra `C:\ProgramData\ssh\sshd_config`. *(Altere o filtro de arquivos do Bloco de Notas para “Todos os arquivos” para encontrá-lo.)*
3. Modifique ou adicione as diretivas abaixo:

```text
# Vá até o final do arquivo e COMENTE as duas linhas abaixo adicionando '#' no início.
# Isso faz com que contas de administradores usem o arquivo authorized_keys do próprio perfil.
#Match Group administrators
#    AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
```

4. Salve o arquivo e **reinicie o serviço SSH** no PowerShell para aplicar as alterações:
```powershell
Restart-Service sshd
```

## 7. Configurar o Firewall do Windows

Para que o WinSCP ou outros clientes consigam se conectar, a porta padrão (`22`) precisa ser permitida nas regras de tráfego de entrada.

Execute este comando no PowerShell como Administrador para criar a regra automaticamente:
```powershell
New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH SSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

## 8. Validar a instalação

Para confirmar se o servidor SSH está ativo e respondendo na porta local, execute:
```powershell
Test-NetConnection -ComputerName localhost -Port 22
```
O retorno deve exibir o campo `TcpTestSucceeded : True`.
