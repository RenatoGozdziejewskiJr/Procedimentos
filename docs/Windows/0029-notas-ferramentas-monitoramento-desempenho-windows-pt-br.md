# Notas sobre ferramentas de monitoramento de desempenho do Windows

[English (UK)](0029-notes-windows-performance-monitoring-tools.md)

## 1. Monitorar tráfego de rede (pacotes)

Para capturar tráfego de rede no Windows, você pode usar ferramentas nativas ou de terceiros.

### 1.1 PktMon (nativo do Windows 10/11)

O `pktmon` é útil para capturar tráfego “externo”.

```cmd
# Iniciar a captura sem limite de tamanho de pacote (0)
pktmon start --capture --pkt-size 0

# Aguardar um tempo (ex: 240 segundos)
timeout /t 240

# Parar a captura
pktmon stop
```

Isso cria um arquivo `PktMon.etl`. Para analisá-lo no Wireshark, converta-o para o formato `pcapng`:
```cmd
pktmon etl2pcap PktMon.etl --out test.pcapng
```

### 1.2 RawCap

[RawCap](https://www.netresec.com/?page=RawCap) é uma ferramenta simples de linha de comando, útil para capturar tráfego **interno** (localhost / interface de loopback `127.0.0.1`), que às vezes é difícil de capturar nativamente em algumas versões do Windows.

## 2. Monitorar CPU, memória e disco

### 2.1 WPR (Windows Performance Recorder)

Ferramenta robusta (incluída no Windows 10) para gravar eventos do sistema e realizar análises detalhadas de desempenho.
* [Documentação oficial do WPR](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/wpr-command-line-options)

### 2.2 Typeperf

Grava contadores de desempenho no terminal ou em um arquivo de log.
* [Documentação oficial do Typeperf](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/typeperf)

### 2.3 ProcDump (Sysinternals)

Utilitário útil para monitorar picos de CPU em um aplicativo e gerar automaticamente “crash dumps” durante esses picos, facilitando a identificação de gargalos.
* [Página de download do ProcDump](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump)
