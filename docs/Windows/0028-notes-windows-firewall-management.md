# Notes about Windows Firewall management

[Português (Brasil)](0028-notas-gerenciamento-firewall-windows-pt-br.md)

Useful commands for allowing ports through Windows Firewall from the command line (Administrator privileges are required).

> **Security warning:** Port 23 is normally used by Telnet, which does not encrypt credentials or traffic. Allow it only for a specific legacy requirement on a trusted, restricted network; prefer SSH for remote access.

## 1. Use Command Prompt (CMD / `netsh`)

### 1.1 Create rules (allow ports)

To allow inbound traffic on specific ports:
```cmd
netsh advfirewall firewall add rule name="Liberar Porta 23 - Telnet" dir=in action=allow protocol=TCP localport=23
netsh advfirewall firewall add rule name="Liberar Porta 5002" dir=in action=allow protocol=TCP localport=5002
```

Example with separate inbound and outbound rules:
```cmd
# Regra de Entrada
netsh advfirewall firewall add rule name="Telnet - Entrada" dir=in action=allow protocol=TCP localport=23

# Regra de Saída
netsh advfirewall firewall add rule name="Telnet - Saída" dir=out action=allow protocol=TCP localport=23
```

### 1.2 View rules

Check whether the rule was created successfully:
```cmd
netsh advfirewall firewall show rule name="Liberar Porta 23 - Telnet"
```

## 2. Use PowerShell

PowerShell provides more modern cmdlets for firewall management.

### 2.1 Create rules

You can allow multiple ports at once:
```powershell
New-NetFirewallRule -DisplayName "Liberar Portas 23 e 5002" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 23,5002
```

Example for inbound and outbound traffic:
```powershell
# Liberar Entrada
New-NetFirewallRule -DisplayName "Telnet In" -Direction Inbound -Protocol TCP -LocalPort 23 -Action Allow

# Liberar Saída
New-NetFirewallRule -DisplayName "Telnet Out" -Direction Outbound -Protocol TCP -LocalPort 23 -Action Allow
```
