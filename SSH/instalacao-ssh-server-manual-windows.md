
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
O comando tradicional `ssh-copy-id` do Linux falha ao interagir com o Windows. A configuração deve ser feita inserindo a chave pública dentro do arquivo de chaves autorizadas do Host. 

Se você tiver mais de uma chave pública (de computadores diferentes), basta adicioná-las uma abaixo da outra, dedicando **uma linha inteira para cada chave**.

### Cenário A: O seu Usuário no Host é um Usuário Comum
O arquivo de destino deve ser um arquivo de texto simples (sem extensão) localizado no perfil do usuário. No PowerShell do Host, execute:

```powershell
# 1. Garante a existência do diretório .ssh no perfil do usuário
New-Item -ItemType Directory -Force -Path "C:\Users\u46099\.ssh"

# 2. Cria ou adiciona a primeira chave pública ao arquivo authorized_keys
# Substitua 'sua-chave-publica-aqui' pelo conteúdo real do seu arquivo .pub
Set-Content -Path "C:\Users\u46099\.ssh\authorized_keys" -Value "sua-chave-publica-aqui"

# NOTA: Para adicionar chaves secundárias futuramente sem apagar as anteriores, use:
# Add-Content -Path "C:\Users\u46099\.ssh\authorized_keys" -Value "nova-chave-publica-aqui"

# 3. Ajusta estritamente as permissões do arquivo (Obrigatório por segurança)
# Remove a herança e concede acesso apenas ao Sistema e ao próprio Usuário comum
icacls "C:\Users\u46099\.ssh\authorized_keys" /inheritance:r /grant "NT AUTHORITY\SYSTEM:F" /grant "u46099:F"
```

### Cenário B: O seu Usuário no Host é um Administrador
Por padrão de segurança do OpenSSH no Windows, as chaves de contas do grupo de Administradores não ficam na pasta do usuário, mas sim em uma pasta central do sistema. No PowerShell do Host:

```powershell
# 1. Cria ou adiciona a primeira chave pública ao arquivo global de administradores
Set-Content -Path "C:\ProgramData\ssh\administrators_authorized_keys" -Value "sua-chave-publica-aqui"

# 2. Ajusta as permissões do arquivo (Obrigatório por segurança)
# Remove a herança e concede acesso apenas ao Sistema e ao grupo de Administradores
icacls "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r /grant "NT AUTHORITY\SYSTEM:F" /grant "BUILTIN\Administrators:F"
```

### Aplicando as Novas Chaves
Toda vez que o arquivo de chaves for modificado ou criado, reinicie o serviço SSH no Host para carregar as novas credenciais:
```powershell
Restart-Service sshd
```

---

## Passo 6: Configuração do Firewall do Windows
Para que o WinSCP ou outros clientes consigam se conectar, é necessário abrir a porta padrão (`22`) nas regras de tráfego de entrada.

Execute este comando no PowerShell de Administrador para criar a regra automaticamente:
```powershell
New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH SSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

---

## Passo 7: Validação da Instalação
Para confirmar se o servidor SSH está ativo e respondendo na porta local, execute:
```powershell
Test-NetConnection -ComputerName localhost -Port 22
```
O retorno deve exibir o campo `TcpTestSucceeded : True`.
