# Gerenciamento do Windows Firewall

Comandos úteis para liberar portas no Windows Firewall via linha de comando (requer privilégios de Administrador).

## Via Prompt de Comando (CMD / netsh)

### Criar Regras (Liberar Portas)
Para permitir tráfego de entrada em portas específicas:
```cmd
netsh advfirewall firewall add rule name="Liberar Porta 23 - Telnet" dir=in action=allow protocol=TCP localport=23
netsh advfirewall firewall add rule name="Liberar Porta 5002" dir=in action=allow protocol=TCP localport=5002
```

Exemplo separando regras de entrada (Inbound) e saída (Outbound):
```cmd
# Regra de Entrada
netsh advfirewall firewall add rule name="Telnet - Entrada" dir=in action=allow protocol=TCP localport=23

# Regra de Saída
netsh advfirewall firewall add rule name="Telnet - Saída" dir=out action=allow protocol=TCP localport=23
```

### Consultar Regras
Para checar se a regra foi criada com sucesso:
```cmd
netsh advfirewall firewall show rule name="Liberar Porta 23 - Telnet"
```

---

## Via PowerShell

O PowerShell oferece cmdlets mais modernos para gerenciamento do firewall.

### Criar Regras
Você pode liberar múltiplas portas de uma só vez:
```powershell
New-NetFirewallRule -DisplayName "Liberar Portas 23 e 5002" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 23,5002
```

Exemplo para Entrada e Saída:
```powershell
# Liberar Entrada
New-NetFirewallRule -DisplayName "Telnet In" -Direction Inbound -Protocol TCP -LocalPort 23 -Action Allow

# Liberar Saída
New-NetFirewallRule -DisplayName "Telnet Out" -Direction Outbound -Protocol TCP -LocalPort 23 -Action Allow
```
