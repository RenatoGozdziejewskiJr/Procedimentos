# Notes about Windows port forwarding

[Português (Brasil)](0023-notas-redirecionamento-portas-windows-pt-br.md)

The `netsh interface portproxy` command configures Windows to listen on a specific local IP address and port, then forward all traffic arriving there to another IP address and port.

**General rule:** “Any request that reaches my internal IP address (`listenaddress`) on port X (`listenport`) should be forwarded to IP address Y (`connectaddress`) on port Z (`connectport`).”

*(Run these commands in Command Prompt or PowerShell as an Administrator.)*

## 1. Create port forwarding rules

Practical examples of forwarding traffic from IPv4 to IPv4:

```cmd
# Redirecionar SEQ (Porta 5341)
netsh interface portproxy add v4tov4 listenaddress=10.232.80.23 listenport=5341 connectaddress=172.34.1.222 connectport=5341

# Redirecionar OPC UA (Porta 4840)
netsh interface portproxy add v4tov4 listenaddress=10.232.80.23 listenport=4840 connectaddress=172.34.1.228 connectport=4840

# Redirecionar System Controller (SC - Porta 50713)
netsh interface portproxy add v4tov4 listenaddress=10.232.80.23 listenport=50713 connectaddress=172.34.1.222 connectport=50713

# Redirecionar Remote Debugger (Porta 4026)
netsh interface portproxy add v4tov4 listenaddress=10.232.80.23 listenport=4026 connectaddress=172.34.1.222 connectport=4026
```

## 2. View active rules

Use these commands to view all configured forwarding rules:

```cmd
# Mostra todas as regras
netsh interface portproxy show all

# Mostra apenas regras v4tov4
netsh interface portproxy show v4tov4
```

## 3. Remove rules

To remove individual rules:

```cmd
netsh interface portproxy delete v4tov4 listenaddress=10.232.80.23 listenport=5341
netsh interface portproxy delete v4tov4 listenaddress=10.232.80.23 listenport=4840
```

To reset (delete) **all** rules at once:

```cmd
netsh interface portproxy reset
```

## 4. Related networking commands

### 4.1 Check port usage and stop processes

```cmd
# Verificar qual processo está usando a porta 4201
netstat -ano | findstr " :4201"

# Ver o nome do processo usando o número do PID
tasklist | findstr "NUMERO_DO_PID"

# Forçar a parada do processo pelo PID
taskkill /PID <PID> /F
```

### 4.2 Check local network IP addresses

To find IP addresses detected by the machine (the ARP table) or test network connections:

In CMD:
```cmd
arp -a
```

In PowerShell (a quick ping scan of the 192.168.2.x subnet):
```powershell
1..254 | ForEach-Object {Test-Connection -ComputerName "192.168.2.$_" -Count 1 -Quiet}
```
