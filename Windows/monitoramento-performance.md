# Ferramentas de Monitoramento de Performance (Windows)

## Monitoramento de Rede e Tráfego (Pacotes)

Para capturar tráfego de rede no Windows, você pode utilizar ferramentas nativas ou de terceiros:

### 1. PktMon (Nativo do Windows 10/11)
O `pktmon` é excelente para capturar tráfego "externo".

```cmd
# Iniciar a captura sem limite de tamanho de pacote (0)
pktmon start --capture --pkt-size 0

# Aguardar um tempo (ex: 240 segundos)
timeout /t 240

# Parar a captura
pktmon stop
```
Isso criará um arquivo `PktMon.etl`. Para analisá-arlo no Wireshark, você deve convertê-lo para o formato `pcapng`:
```cmd
pktmon etl2pcap PktMon.etl --out test.pcapng
```

### 2. RawCap
O [RawCap](https://www.netresec.com/?page=RawCap) é uma ferramenta simples de linha de comando muito útil para capturar tráfego **interno** (localhost / interface de loopback `127.0.0.1`), que às vezes é difícil de capturar nativamente em algumas versões do Windows.

---

## Monitoramento de CPU, Memória e Disco

### 1. WPR (Windows Performance Recorder)
Ferramenta robusta (já incluída no Windows 10) para gravar eventos do sistema para análise detalhada de performance.
* [Documentação Oficial do WPR](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/wpr-command-line-options)

### 2. Typeperf
Grava dados de desempenho (Performance Counters) no terminal ou em um arquivo de log.
* [Documentação Oficial do Typeperf](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/typeperf)

### 3. ProcDump (Sysinternals)
Excelente utilitário para monitorar um aplicativo por picos de CPU e gerar "crash dumps" automaticamente durante o pico, facilitando a identificação de gargalos.
* [Página de Download do ProcDump](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump)
