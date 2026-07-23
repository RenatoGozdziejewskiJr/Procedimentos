
# Procedimento de Instalação Manual e Configuração de Chaves SSH no Windows

Este guia descreve os passos para realizar a instalação manual do Servidor OpenSSH no Windows 11 utilizando o repositório oficial da Microsoft, além da configuração correta de chaves públicas para acesso sem senha.

---

## Passo 1: Download do Pacote Oficial
1. Acesse a página de lançamentos oficiais do projeto no GitHub:
   [PowerShell/Win32-OpenSSH Releases](https://github.com/powershell/win32-openssh/releases)
2. Localize a versão estável mais recente.
3. Na seção **Assets**, faça o download do arquivo compactado de 64 bits:
   `OpenSSH-Win64.zip`

---

## Passo 2: Extração e Posicionamento dos Arquivos
1. Abra o arquivo `.zip` baixado e extraia todo o seu conteúdo.
2. Renomeie a pasta extraída para `OpenSSH`.
3. Mova essa pasta para o diretório padrão de programas do sistema:
   `C:\Program Files\OpenSSH`

---

## Passo 3: Execução do Script de Instalação
1. Clique com o botão direito no menu Iniciar e selecione **Terminal (Administrador)** ou **PowerShell (Administrador)**.
2. Navegue até a pasta onde os arquivos foram movidos executando:
   ```powershell
   cd "C:\Program Files\OpenSSH"
   ```
3. Execute o script oficial de instalação incluído no pacote:
   ```powershell
   .\install-sshd.ps1
   ```
4. Certifique-se de que a mensagem retornada no console confirme o sucesso da instalação.

---

## Passo 4: Configuração e Ativação do Serviço
Ainda no PowerShell com privilégios de administrador, execute os comandos abaixo para configurar o serviço para iniciar junto com o Windows e ativá-lo imediatamente:

```powershell
# Define a inicialização do serviço como Automática
Set-Service -Name sshd -StartupType 'Automatic'

# Inicia o serviço do servidor OpenSSH
Start-Service sshd
```

---

## Passo 5: Cópia Manual de Chaves Públicas (Acesso Sem Senha)
O comando tradicional `ssh-copy-id` do Linux falha ao interagir com o Windows devido à falta do interpretador bash nativo. A configuração deve ser feita inserindo o texto da chave pública diretamente no Host de destino.

### Formato do Arquivo authorized_keys
O arquivo `authorized_keys` deve ser um arquivo de texto simples, **sem nenhuma extensão** (ex: `.txt`). Cada chave pública adicionada deve ocupar **exatamente uma linha inteira**. Se você tiver chaves de múltiplos computadores, faça o *append* inserindo uma abaixo da outra.

**Exemplo interno do arquivo:**
```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK... usuario@computador1
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQ... usuario@computador2
```

### Script de Criação e Permissões (Usuário Comum)
No PowerShell do Host, execute os comandos abaixo para estruturar a pasta, injetar a chave e ajustar a codificação. O OpenSSH **rejeita** arquivos que não estejam no formato UTF-8 puro (sem BOM):

```powershell
# 1. Garante a existência do diretório .ssh no perfil do usuário
New-Item -ItemType Directory -Force -Path "C:\Users\u46099\.ssh"

# 2. Cria o arquivo authorized_keys com o conteúdo da sua chave pública
# Substitua 'sua-chave-publica-aqui' pelo conteúdo real do seu arquivo .pub
Set-Content -Path "C:\Users\u46099\.ssh\authorized_keys" -Value "sua-chave-publica-aqui"

# NOTA: Para adicionar chaves secundárias futuramente sem apagar as anteriores, use:
# Add-Content -Path "C:\Users\u46099\.ssh\authorized_keys" -Value "nova-chave-publica-aqui"

# 3. Força a codificação correta para UTF-8 sem BOM (Obrigatório para o OpenSSH aceitar)
[System.IO.File]::WriteAllLines("C:\Users\u46099\.ssh\authorized_keys", [System.IO.File]::ReadAllLines("C:\Users\u46099\.ssh\authorized_keys"))

# 4. Ajusta estritamente as permissões do arquivo (Obrigatório por segurança)
# Remove a herança e concede acesso completo apenas ao Sistema e ao próprio Usuário
icacls "C:\Users\u46099\.ssh\authorized_keys" /inheritance:r /grant "NT AUTHORITY\SYSTEM:F" /grant "u46099:F"
```

---

## Passo 6: Ajustes Críticos no arquivo `sshd_config`
Por padrão, o Windows redireciona contas que possuem quaisquer privilégios administrativos para um arquivo global e realiza checagens rígidas de permissões na pasta pai, o que frequentemente bloqueia a autenticação por chaves. 

Para forçar o uso da pasta do usuário e evitar rejeições de segurança, altere o arquivo de configuração:

1. Abra o **Bloco de Notas como Administrador**.
2. Abra o arquivo localizado em: `C:\ProgramData\ssh\sshd_config` *(Nota: mude o filtro do Bloco de Notas para "Todos os arquivos" para conseguir visualizá-lo)*.
3. Modifique ou adicione as diretivas abaixo:

```text
# 1. Desative o modo estrito de validação de diretórios se houver bloqueio de herança corporativa
StrictModes no

# 2. Vá até o final do arquivo e COMENTE as duas linhas abaixo adicionando '#' no início.
# Isso impede que o Windows ignore sua pasta de usuário e exija chaves de administrador globais.
#Match Group administrators
#    AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
```

4. Salve o arquivo e **reinicie o serviço SSH** no PowerShell para aplicar as alterações:
```powershell
Restart-Service sshd
```

---

## Passo 7: Configuração do Firewall do Windows
Para que o WinSCP ou outros clientes consigam se conectar, é necessário abrir a porta padrão (`22`) nas regras de tráfego de entrada.

Execute este comando no PowerShell de Administrador para criar a regra automaticamente:
```powershell
New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH SSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

---

## Passo 8: Validação da Instalação
Para confirmar se o servidor SSH está ativo e respondendo na porta local, execute:
```powershell
Test-NetConnection -ComputerName localhost -Port 22
```
O retorno deve exibir o campo `TcpTestSucceeded : True`.
