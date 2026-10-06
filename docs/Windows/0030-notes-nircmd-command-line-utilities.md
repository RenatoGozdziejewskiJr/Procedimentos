# Notes about NirCmd command-line utilities

[Português (Brasil)](0030-notas-utilitarios-linha-comando-nircmd-pt-br.md)

[NirCmd](https://www.nirsoft.net/utils/nircmd.html) is a small Windows command-line utility that can perform various system tasks without displaying a graphical interface.

## 1. Useful commands

### 1.1 Keep a window always on top

Force an application to remain above other windows.
The example below keeps Wireshark on top:
```cmd
nircmd win settopmost process Wireshark.exe 1
```
*(To disable this, change `1` to `0`.)*

### 1.2 Activate or focus a specific window

Bring a window to the foreground based on its title:
```cmd
nircmd win activate title "TeamViewer"
```

### 1.3 Play a beep

Play a beep through the system speaker. Syntax: `nircmd beep [Frequência] [Duração_em_ms]`
```cmd
nircmd beep 800 2000 
```
