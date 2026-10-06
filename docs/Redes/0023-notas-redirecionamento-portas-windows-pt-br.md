# Notas sobre redirecionamento de portas no Windows

[English (UK)](0023-notes-windows-port-forwarding.md)

O comando `netsh interface portproxy` configura o Windows para escutar em um endereço IP e uma porta local específicos e, em seguida, encaminhar todo o tráfego recebido para outro endereço IP e outra porta.

**Regra geral:** “Qualquer solicitação que chegar ao meu endereço IP interno (`listenaddress`) na porta X (`listenport`) deve ser encaminhada para o endereço IP Y (`connectaddress`) na porta Z (`connectport`).”

*(Execute estes comandos no Prompt de Comando ou no PowerShell como Administrador.)*

## 1. Criar regras de redirecionamento de portas

Exemplos práticos de redirecionamento de IPv4 para IPv4:

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

## 2. Consultar regras ativas

Use estes comandos para consultar todas as regras de redirecionamento configuradas:

```cmd
# Mostra todas as regras
netsh interface portproxy show all

# Mostra apenas regras v4tov4
netsh interface portproxy show v4tov4
```

## 3. Remover regras

Para remover regras individuais:

```cmd
netsh interface portproxy delete v4tov4 listenaddress=10.232.80.23 listenport=5341
netsh interface portproxy delete v4tov4 listenaddress=10.232.80.23 listenport=4840
```

Para redefinir (apagar) **todas** as regras de uma só vez:

```cmd
netsh interface portproxy reset
```

## 4. Comandos relacionados à rede

### 4.1 Verificar o uso de portas e encerrar processos

```cmd
# Verificar qual processo está usando a porta 4201
netstat -ano | findstr " :4201"

# Ver o nome do processo usando o número do PID
tasklist | findstr "NUMERO_DO_PID"

# Forçar a parada do processo pelo PID
taskkill /PID <PID> /F
```

### 4.2 Verificar endereços IP da rede local

Para descobrir endereços IP detectados pela máquina (tabela ARP) ou testar conexões de rede:

No CMD:
```cmd
arp -a
```

No PowerShell (varredura rápida de ping na sub-rede 192.168.2.x):
```powershell
1..254 | ForEach-Object {Test-Connection -ComputerName "192.168.2.$_" -Count 1 -Quiet}
```
