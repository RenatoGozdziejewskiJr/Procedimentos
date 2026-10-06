# Notes about Windows performance monitoring tools

[Português (Brasil)](0029-notas-ferramentas-monitoramento-desempenho-windows-pt-br.md)

## 1. Monitor network traffic (packets)

To capture network traffic on Windows, you can use built-in or third-party tools.

### 1.1 PktMon (built into Windows 10/11)

`pktmon` is useful for capturing “external” traffic.

```cmd
# Iniciar a captura sem limite de tamanho de pacote (0)
pktmon start --capture --pkt-size 0

# Aguardar um tempo (ex: 240 segundos)
timeout /t 240

# Parar a captura
pktmon stop
```

This creates a `PktMon.etl` file. To analyse it in Wireshark, convert it to `pcapng` format:
```cmd
pktmon etl2pcap PktMon.etl --out test.pcapng
```

### 1.2 RawCap

[RawCap](https://www.netresec.com/?page=RawCap) is a simple command-line tool that is useful for capturing **internal** traffic (localhost / loopback interface `127.0.0.1`), which can sometimes be difficult to capture natively in some Windows versions.

## 2. Monitor CPU, memory and disk

### 2.1 WPR (Windows Performance Recorder)

A robust tool (included with Windows 10) for recording system events for detailed performance analysis.
* [Official WPR documentation](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/wpr-command-line-options)

### 2.2 Typeperf

Records performance counters in the terminal or in a log file.
* [Official Typeperf documentation](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/typeperf)

### 2.3 ProcDump (Sysinternals)

A useful utility for monitoring an application for CPU spikes and automatically generating “crash dumps” during a spike, which helps identify bottlenecks.
* [ProcDump download page](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump)
