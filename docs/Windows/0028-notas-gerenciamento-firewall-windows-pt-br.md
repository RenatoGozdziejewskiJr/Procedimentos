# Notas sobre gerenciamento do Firewall do Windows

[English (UK)](0028-notes-windows-firewall-management.md)

> **Aviso de segurança:** A porta 23 é normalmente usada pelo Telnet, que não criptografa credenciais nem tráfego. Libere-a apenas quando houver uma necessidade legada específica em uma rede confiável e restrita; prefira SSH para acesso remoto.

Comandos úteis para permitir portas no Firewall do Windows pela linha de comando (requer privilégios de Administrador).

## 1. Usar o Prompt de Comando (CMD / `netsh`)

### 1.1 Criar regras (permitir portas)

Para permitir tráfego de entrada em portas específicas:
```cmd
netsh advfirewall firewall add rule name="Liberar Porta 23 - Telnet" dir=in action=allow protocol=TCP localport=23
netsh advfirewall firewall add rule name="Liberar Porta 5002" dir=in action=allow protocol=TCP localport=5002
```

Exemplo com regras separadas de entrada e saída:
```cmd
# Regra de Entrada
netsh advfirewall firewall add rule name="Telnet - Entrada" dir=in action=allow protocol=TCP localport=23

# Regra de Saída
netsh advfirewall firewall add rule name="Telnet - Saída" dir=out action=allow protocol=TCP localport=23
```

### 1.2 Consultar regras

Verifique se a regra foi criada com sucesso:
```cmd
netsh advfirewall firewall show rule name="Liberar Porta 23 - Telnet"
```

## 2. Usar o PowerShell

O PowerShell oferece cmdlets mais modernos para gerenciamento do firewall.

### 2.1 Criar regras

É possível permitir várias portas de uma só vez:
```powershell
New-NetFirewallRule -DisplayName "Liberar Portas 23 e 5002" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 23,5002
```

Exemplo para tráfego de entrada e saída:
```powershell
# Liberar Entrada
New-NetFirewallRule -DisplayName "Telnet In" -Direction Inbound -Protocol TCP -LocalPort 23 -Action Allow

# Liberar Saída
New-NetFirewallRule -DisplayName "Telnet Out" -Direction Outbound -Protocol TCP -LocalPort 23 -Action Allow
```
