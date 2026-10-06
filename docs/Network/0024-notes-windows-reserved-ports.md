# Notes about freeing a reserved port in Windows

[Português (Brasil)](0024-notas-portas-reservadas-windows-pt-br.md)

## 1. Release the port in Windows

If your programme must use port 50713, restarting WinNAT may cause Windows to assign different excluded port ranges. This is not guaranteed to release a particular port and may interrupt services that depend on NAT.

### 1.1 Open Command Prompt as an Administrator

Open the Start menu, type `cmd`, right-click it and select **Run as Administrator**.

### 1.2 Stop the NAT network service

Type the following command and press Enter:

`net stop winnat`

### 1.3 Start the service again

Start the service again by entering:

`net start winnat`

Check the current excluded TCP port ranges:

```powershell
netsh int ipv4 show excludedportrange protocol=tcp
```

Confirm that port 50713 is not within an excluded range, then verify that the programme can bind to and use it. If it remains unavailable, use a different port rather than assuming the restart released it.

### 1.4 Open your programme

When the WinNAT service restarts, it usually selects different port ranges. Try connecting to your programme again (or running the PowerShell script).
