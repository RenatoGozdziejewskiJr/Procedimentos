
# Procedimento de Instalação Manual do Servidor OpenSSH no Windows

Este guia descreve os passos para realizar a instalação manual do Servidor OpenSSH no Windows 11 utilizando o repositório oficial da Microsoft, contornando bloqueios de rede corporativa ou falhas no Windows Update (como o erro `0x80244022`).

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

## Passo 5: Configuração do Firewall do Windows
Para que o WinSCP ou outros clientes consigam se conectar, é necessário abrir a porta padrão (`22`) nas regras de tráfego de entrada.

Execute este comando no PowerShell de Administrador para criar a regra automaticamente:
```powershell
New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH SSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

---

## Passo 6: Validação da Instalação
Para confirmar se o servidor SSH está ativo e respondendo na porta local, execute:
```powershell
Test-NetConnection -ComputerName localhost -Port 22
```
O retorno deve exibir o campo `TcpTestSucceeded : True`.

A partir deste momento, o servidor está pronto para aceitar conexões do WinSCP utilizando as credenciais de usuário e senha da sua própria máquina Windows.
