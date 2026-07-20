PORT FOWARDING:

How to Create Rules - Port forwarding: ‘Any request that reaches my network internal IP (listenaddress) on port listenport, forward it to the IP (connectaddress) on port connectport.’”

SEQ port fowarding:
netsh interface portproxy add v4tov4 listenaddress=10.232.80.23 listenport=5341 connectaddress=172.34.1.222 connectport=5341

OPC UA port fowarding:
 netsh interface portproxy add v4tov4 listenaddress=10.232.80.23 listenport=4840 connectaddress=172.34.1.228 connectport=4840

SC port fowarding:
 netsh interface portproxy add v4tov4 listenaddress=10.232.80.23 listenport=50713 connectaddress=172.34.1.222 connectport=50713

Remote Debugger port fowarding:
 netsh interface portproxy add v4tov4 listenaddress=10.232.80.23 listenport=4026 connectaddress=172.34.1.222 connectport=4026

 
Consultar Regras:
netsh interface portproxy show all

(com filtro)
netsh interface portproxy show v4tov4

Remover:

Remover Regras:
netsh interface portproxy delete v4tov4 listenaddress=10.232.80.23 listenport=5341
netsh interface portproxy delete v4tov4 listenaddress=10.232.80.23 listenport=4840

Remover tudo:
netsh interface portproxy reset

UTIL:

Verificar Porta em uso:

netstat -ano | findstr " :4201"

Matar o processo:

taskkill /PID <PID> /F

tasklist | findstr "NUMERO_DO_PID"

Verificar IP's que a maquina enxergou:

via cmd:
arp -a

via powershell:
1..254 | ForEach-Object {Test-Connection -ComputerName "192.168.2.$_" -Count 1 -Quiet}