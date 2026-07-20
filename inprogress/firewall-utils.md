LIBERAR PORTA FIREWALL:

via cmd (admin)
netsh advfirewall firewall add rule name="Liberar Porta 23 - Telnet" dir=in action=allow protocol=TCP localport=23
netsh advfirewall firewall add rule name="Liberar Porta 5002" dir=in action=allow protocol=TCP localport=5002

Regra de Entrada (Inbound):
netsh advfirewall firewall add rule name="Telnet - Entrada" dir=in action=allow protocol=TCP localport=23

Regra de Saída (Outbound):
netsh advfirewall firewall add rule name="Telnet - Saída" dir=out action=allow protocol=TCP localport=23

para checar se funcionou:
netsh advfirewall firewall show rule name="Liberar Porta 23 - Telnet"
netsh advfirewall firewall show rule name="Liberar Porta 5002"

alternativa via powershell (admin):
New-NetFirewallRule -DisplayName "Liberar Portas 23 e 5002" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 23,5002

# Liberar Entrada
New-NetFirewallRule -DisplayName "Telnet In" -Direction Inbound -Protocol TCP -LocalPort 23 -Action Allow

# Liberar Saída
New-NetFirewallRule -DisplayName "Telnet Out" -Direction Outbound -Protocol TCP -LocalPort 23 -Action Allow