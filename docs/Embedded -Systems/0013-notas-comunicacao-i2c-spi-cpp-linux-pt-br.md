# Notas sobre comunicação I2C e SPI em C++ no Linux

[English](./0013-notes-linux-i2c-spi-cpp-communication.md)

No ecossistema Linux, impera a filosofia de que **"tudo é um arquivo"** (*Everything is a file*). Isso significa que barramentos complexos de hardware são expostos ao programador como simples arquivos no diretório `/dev`.

Teoricamente, você pode usar as operações clássicas do POSIX C/C++ — `open()`, `read()`, `write()` e `close()` — para se comunicar com qualquer hardware. No entanto, a natureza elétrica e lógica dos protocolos I2C e SPI exige abordagens diferentes na hora de escrever drivers robustos.

---

## 1. I2C (TWI): A Simplicidade do `write()` e `read()`

O barramento I2C (Inter-Integrated Circuit) é projetado para ser um protocolo de rede local simplificado.

*   **Half-Duplex:** A comunicação acontece em uma única via de dados (SDA). Ou o mestre (Radxa) fala, ou o escravo (Display) fala. Eles nunca falam ao mesmo tempo.
*   **Baseado em Endereçamento:** Não há um pino físico para "acordar" o display. O mestre grita um endereço no barramento (ex: `0x3C`) e apenas o dispositivo correspondente responde.

### 1.1. Por que `write()` é suficiente?
Como o I2C funciona em turnos, usar a função `write()` para enviar comandos ou pixels é o caminho natural e perfeitamente seguro. O kernel do Linux pega o seu array de bytes, anexa o endereço I2C no início do pacote e cuida da transmissão. Para ler um sensor, um simples `read()` faria o caminho inverso sem complicações.

---

## 2. SPI: O Poder e a Necessidade do `ioctl`

O SPI (Serial Peripheral Interface) é um barramento de altíssima velocidade, projetado para mover muitos dados rapidamente. Ele possui pinos dedicados para enviar (MOSI) e receber (MISO).

Embora seja tecnicamente possível usar um `write()` em `/dev/spidevX.Y` (e até funcionaria para o nosso display que só recebe dados), a comunidade de engenharia C++ adotou o `ioctl` (Input/Output Control) como o **padrão oficial**. Existem três motivos críticos para isso:

### 2.1. A. Natureza Full-Duplex (Mão Dupla Simultânea)
O SPI exige que a leitura e a escrita ocorram **exatamente no mesmo pulso de clock**. A cada bit que sai pelo MOSI, um bit entra pelo MISO.
*   Se você usar `write()`, o kernel Linux literalmente joga fora a resposta do hardware.
*   Se você usar `read()`, o kernel envia zeros (lixo) pelo MOSI apenas para gerar o clock e conseguir ler a resposta.
*   **A Solução (`ioctl`):** Através da estrutura `spi_ioc_transfer`, você fornece dois buffers ao mesmo tempo (`tx_buf` e `rx_buf`). O kernel garante a troca simultânea perfeita, o que é vital para sensores complexos.

### 2.2. B. O Perigo do Pino CS (Chip Select)
Diferente do I2C, o SPI acorda os chips através de um pino físico (o CS). A especificação dita que o pino CS deve ser puxado para **BAIXO (0V)** no início da conversa e voltar para **ALTO (3.3V)** apenas quando a conversa terminar.
*   Se você enviar dados usando duas chamadas seguidas de `write()` (uma para o comando, outra para os dados), o kernel pode desativar o pino CS (puxar para ALTO) na fração de segundo entre as duas linhas de código.
*   Para muitos displays e memórias flash, essa "piscada" no pino CS significa "operação abortada", quebrando completamente o sistema.
*   **A Solução (`ioctl`):** O `ioctl` permite enviar um vetor de várias mensagens de uma só vez. O kernel se compromete a segurar o pino CS em nível BAIXO continuamente até que todas as mensagens do pacote tenham sido transmitidas.

### 2.3. C. Controle Cirúrgico por Mensagem
Com o `write()`, o hardware opera na velocidade padrão configurada para o barramento. Mas no SPI, você pode ter dispositivos de diferentes velocidades pendurados nos mesmos fios.
*   **A Solução (`ioctl`):** A estrutura `spi_ioc_transfer` permite que você altere a velocidade em Hertz (`speed_hz`), o tamanho da palavra (`bits_per_word`) e adicione delays específicos **somente para aquela transmissão exata**, sem bagunçar a configuração global do arquivo `/dev`.

---

## 3. Resumo
*   Use `write()` e `read()` para **I2C**. O protocolo é cadenciado, sincronizado por endereços e de via única (Half-Duplex).
*   Use `ioctl` com a estrutura `spi_ioc_transfer` para **SPI**. Ele garante a sincronia rigorosa do pino Chip Select, a leitura/escrita simultânea e o controle fino de velocidade em tempo real.
