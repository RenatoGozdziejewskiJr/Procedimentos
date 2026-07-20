# Port Forwarding (Redirecionamento de Portas no Windows)

O `netsh interface portproxy` permite configurar o Windows para escutar em uma porta específica (IP e Porta local) e redirecionar todo o tráfego que chega nela para outro endereço IP e porta.

**Regra geral:** "Qualquer requisição que chegar no meu IP interno (`listenaddress`) na porta X (`listenport`), encaminhe para o IP Y (`connectaddress`) na porta Z (`connectport`)."

*(Requer execução via Prompt de Comando ou PowerShell como Administrador)*

## Criar Regras de Port Forwarding

Exemplos práticos de redirecionamento (IPv4 para IPv4):

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

## Consultar Regras Ativas

Para ver todos os redirecionamentos configurados:
```cmd
# Mostra todas as regras
netsh interface portproxy show all

# Mostra apenas regras v4tov4
netsh interface portproxy show v4tov4
```

## Remover Regras

Para remover regras individuais:
```cmd
netsh interface portproxy delete v4tov4 listenaddress=10.232.80.23 listenport=5341
netsh interface portproxy delete v4tov4 listenaddress=10.232.80.23 listenport=4840
```

Para resetar (apagar) **todas** as regras de uma vez:
```cmd
netsh interface portproxy reset
```

---

## Comandos Úteis Relacionados a Rede

### Verificar uso de portas e matar processos
```cmd
# Verificar qual processo está usando a porta 4201
netstat -ano | findstr " :4201"

# Ver o nome do processo usando o número do PID
tasklist | findstr "NUMERO_DO_PID"

# Forçar a parada do processo pelo PID
taskkill /PID <PID> /F
```

### Verificar IPs na rede local
Se precisar descobrir IPs que sua máquina já detectou (tabela ARP) ou testar conexões na rede:

Via CMD:
```cmd
arp -a
```

Via PowerShell (Varredura rápida de Ping na subnet 192.168.2.x):
```powershell
1..254 | ForEach-Object {Test-Connection -ComputerName "192.168.2.$_" -Count 1 -Quiet}
```
