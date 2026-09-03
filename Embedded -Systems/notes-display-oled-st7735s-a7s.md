# Plano de Integração: Display LCD TFT/OLED (ST7735 / ST7735S) na Radxa Cubie A7S
Este documento detalha o plano completo para conectar e programar o display colorido (controlador ST7735 ou sua variante ST7735S, resolução 160x80) na placa Radxa Cubie A7S. Estão descritas duas abordagens distintas para integração via software.

## 1. Conexões Físicas (Header de 30 Pinos)
O display precisa ser alimentado corretamente e ter seus sinais lógicos conectados. As portas GPIO da Cubie A7S operam em uma tensão de 3.3 V, ideal para este componente.

**Importante:** É obrigatório ligar o pino BLK (Backlight) em 3.3 V para que a luz de fundo acenda; caso contrário, a tela ficará completamente preta.

| Pino do display | Radxa Cubie A7S (header de 30 pinos) | Função na placa |
| --- | --- | --- |
| GND | Pino 6 | GND (terra) |
| VCC | Pino 1 | 3.3 V (alimentação) |
| BLK | Pino 17 | 3.3 V (luz de fundo) |
| SCL / SCK | Pino 23 | SPI1-CLK (função alternativa 4) |
| SDA / MOSI | Pino 19 | SPI1-MOSI (função alternativa 4) |
| CS | Pino 24 | SPI1-CS0 (função alternativa 6) |
| DC / RS | Pino 11 | PB1 (linha 33 do gpiochip0) |
| RES / RST | Pino 29 | PB2 (linha 34 do gpiochip0) |

> **Nota:** Pinos GND adicionais disponíveis na placa incluem 9, 14, 20, 26 e 30.

## 2. Opção A: Método de Espaço de Usuário
Nesta abordagem, o sistema operacional expõe os pinos, e a aplicação fica responsável por enviar os comandos de desenho para a tela. É adequada para aplicações autônomas construídas em C++ ou Python, usando `spidev` e `libgpiod`.

### 2.1. Configuração do SO (`rsetup`)
1. Execute `rsetup` no terminal.
2. Navegue até **Overlays**.
3. Marque a opção `[] Enable spidev on SPI1`.
4. Mantenha o overlay do framebuffer desmarcado para não bloquear os pinos DC e RST.
5. Selecione `<Ok>` e reinicie a placa com `sudo reboot`.
6. Depois da reinicialização, o dispositivo `/dev/spidev1.0` deverá estar disponível.

### 2.2. Entendendo o Mapeamento de Pinos (`gpiochip0`)

O driver do processador Allwinner A733 agrupa todos os 352 pinos lógicos em um único controlador chamado `gpiochip0`.

Grande parte dos pinos de uso interno do processador não possui rótulos (`unnamed`), mas felizmente os pinos expostos no header de 30 pinos foram nomeados amigavelmente pelo kernel (ex: `"PIN_11"`, `"PIN_29"`).

Você pode acessar esses pinos no código de duas maneiras:

1. **Por Nome (Recomendado):** Utilizando a função `find_line("PIN_11")` da biblioteca `libgpiod`.
2. **Por Índice Matemático:** Caso prefira usar o endereço bruto de hardware (`get_line(33)`), utiliza-se a seguinte fórmula universal:

> **Índice Numérico = (Índice do Banco x 32) + Número do Pino**

Lembrando que os bancos seguem ordem alfabética (PA=0, PB=1, PC=2, PD=3):

- **Pino DC (PB1):** Banco 1 x 32 + 1 = **Linha 33**
- **Pino RST (PB2):** Banco 1 x 32 + 2 = **Linha 34**

### 2.3. Implementação em Python
Devido a limitações e dependências de bibliotecas de terceiros (`Adafruit-Blinka` e `periphery`), será utilizada a API nativa do kernel por meio da `libgpiod`.

#### Instalação de dependências

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev python3-libgpiod
pip3 install spidev pillow

```

#### Script de teste (`display_test.py`)

```python
import time

import gpiod
import spidev
from PIL import Image, ImageDraw

class ST7735S:
    def __init__(self):
        self.chip = gpiod.Chip("gpiochip0")
        self.dc = self.chip.get_line(33)  # PB1 -> pino 11
        self.rst = self.chip.get_line(34)  # PB2 -> pino 29

	 # ou podes usar os pinos nomeados:
	 # self.dc = self.chip.find_line("PIN_11")
	 # self.rst = self.chip.find_line("PIN_29")

        # default_val evita que o kernel negue acesso com "Errno 22".
        self.dc.request(
            consumer="st7735", type=gpiod.LINE_REQ_DIR_OUT, default_val=0
        )
        self.rst.request(
            consumer="st7735", type=gpiod.LINE_REQ_DIR_OUT, default_val=1
        )

        self.spi = spidev.SpiDev()
        self.spi.open(1, 0)
        self.spi.max_speed_hz = 15000000
        self.spi.mode = 0

    def send_cmd(self, cmd):
        self.dc.set_value(0)
        self.spi.xfer2([cmd])

    def send_data(self, data):
        self.dc.set_value(1)
        self.spi.xfer2(data if isinstance(data, list) else [data])

    def init_display(self):
        self.rst.set_value(0)
        time.sleep(0.1)
        self.rst.set_value(1)
        time.sleep(0.1)

        self.send_cmd(0x01)  # SWRESET
        time.sleep(0.15)
        self.send_cmd(0x11)  # SLPOUT
        time.sleep(0.2)

        self.send_cmd(0x3A)  # COLMOD
        self.send_data(0x05)  # 16-bit
        self.send_cmd(0x36)  # MADCTL
        self.send_data(0x68)  # BGR
        self.send_cmd(0x21)  # INVON
        self.send_cmd(0x29)  # DISPON
        time.sleep(0.1)

    def display_image(self, image):
        self.send_cmd(0x2A)  # CASET
        self.send_data([0x00, 1, 0x00, image.width])
        self.send_cmd(0x2B)  # RASET
        self.send_data([0x00, 26, 0x00, image.height + 25])
        self.send_cmd(0x2C)  # RAMWR

        pixels = list(image.getdata())
        buffer = bytearray()
        for red, green, blue in pixels:
            color = ((red & 0xF8) << 8) | ((green & 0xFC) << 3) | (blue >> 3)
            buffer.append(color >> 8)
            buffer.append(color & 0xFF)

        self.dc.set_value(1)
        for index in range(0, len(buffer), 4096):
            self.spi.xfer2(list(buffer[index:index + 4096]))

if __name__ == "__main__":
    display = ST7735S()
    display.init_display()
    image = Image.new("RGB", (160, 80), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 10, 150, 70), outline=(0, 255, 0), width=2)
    display.display_image(image)

```

### 2.4. Implementação em C++ (CMake)
Para obter o máximo de desempenho com C++20 ou C++23, manipula-se o barramento com `ioctl` e os pinos de controle com a `libgpiod`.

#### Instalação das dependências

```bash
sudo apt-get update
sudo apt-get install gpiod libgpiod-dev libgpiodcxx-dev

```
`CMakeLists.txt`***:***

```cmake
cmake_minimum_required(VERSION 3.20)
project(ST7735_Driver VERSION 1.0)
set(CMAKE_CXX_STANDARD 20)
find_package(gpiod REQUIRED)
add_executable(display_main main.cpp)
target_link_libraries(display_main PRIVATE gpiodcxx)

```
`main.cpp`*** (Completo com buffer de linha e ajustes ST7735S):***

Para o script original em C++ que utiliza os bindings `gpiodcxx`, atualize a instanciação do objeto no `main.cpp` para refletir os endereços corretos do `gpiochip0` e configure a direção da linha com valores padrão, de forma semelhante à solução em Python:

```cpp
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <gpiod.hpp>
#include <vector>

// Cores básicas no formato RGB565
#define COLOR_BLACK 0x0000
#define COLOR_GREEN 0x07E0
#define COLOR_RED   0xF800
#define COLOR_BLUE  0x001F

class ST7735 {
private:
    int spi_fd;
    gpiod::line dc_line;
    gpiod::line res_line;
    int width, height;

    void spi_transfer(const uint8_t* tx_buf, size_t len) {
        spi_ioc_transfer tr = {};
        tr.tx_buf = (unsigned long)tx_buf;
        tr.rx_buf = 0;
        tr.len = len;
        tr.speed_hz = 15000000; // 15 MHz
        tr.bits_per_word = 8;
        ioctl(spi_fd, SPI_IOC_MESSAGE(1), &tr);
    }

    void send_command(uint8_t cmd) {
        dc_line.set_value(0); // DC = 0 (Comando)
        spi_transfer(&cmd, 1);
    }

    void send_data(uint8_t data) {
        dc_line.set_value(1); // DC = 1 (Dado)
        spi_transfer(&data, 1);
    }

    void send_data_buffer(const uint8_t* buffer, size_t len) {
        dc_line.set_value(1);
        spi_transfer(buffer, len);
    }

    void setAddrWindow(uint8_t x0, uint8_t y0, uint8_t x1, uint8_t y1) {
        // OFFSET PARA ST7735S (se houver lixo na borda, some +1 no X e +26 no Y)
        uint8_t off_x = 1;
        uint8_t off_y = 26;
        
        send_command(0x2A); // CASET
        send_data(0x00); send_data(x0 + off_x);
        send_data(0x00); send_data(x1 + off_x);

        send_command(0x2B); // RASET
        send_data(0x00); send_data(y0 + off_y);
        send_data(0x00); send_data(y1 + off_y);

        send_command(0x2C); // RAMWR
    }

public:
    ST7735(const std::string& spi_dev, const std::string& gpio_chip, int dc_offset, int res_offset, int w, int h) 
        : width(w), height(h) {
        spi_fd = open(spi_dev.c_str(), O_RDWR);
        uint8_t mode = SPI_MODE_0;
        ioctl(spi_fd, SPI_IOC_WR_MODE, &mode);

        gpiod::chip chip(gpio_chip);
        dc_line = chip.get_line(dc_offset);
        res_line = chip.get_line(res_offset);

	 // ou podemos escrever usando os pinos nomeados:
	 // dc_line = chip.find_line("PIN_11");
	 // res_line = chip.find_line("PIN_29");
        
        gpiod::line_request config;
        config.request_type = gpiod::line_request::DIRECTION_OUTPUT;
        config.consumer = "st7735"; // Identificação para o kernel
        
        // O segundo parâmetro é o default_val, essencial para evitar Errno 22
        dc_line.request(config, 0); 
        res_line.request(config, 1);
    }
    
    void init() {
        res_line.set_value(0);
        usleep(100000);
        res_line.set_value(1);
        usleep(100000);
        
        send_command(0x01); // SWRESET
        usleep(150000);
        send_command(0x11); // SLPOUT
        usleep(200000);
        
        send_command(0x3A); // COLMOD
        send_data(0x05);    // 16-bit / pixel (RGB565)

        // AJUSTE ST7735S: 0x68 ativa BGR (corrige Vermelho/Azul trocado).
        send_command(0x36); // MADCTL
        send_data(0x68);    

        send_command(0x29); // DISPON
        usleep(100000);

        // AJUSTE ST7735S: Inversão de cores (corrige efeito "Negativo").
        send_command(0x21); // INVON
    }

    void drawRectangle(int x, int y, int w, int h, uint16_t color) {
        setAddrWindow(x, y, x + w - 1, y + h - 1);
        uint8_t color_high = color >> 8;
        uint8_t color_low = color & 0xFF;

        size_t bytes_per_row = w * 2;
        std::vector<uint8_t> row_buffer(bytes_per_row);
        
        for (int i = 0; i < w; ++i) {
            row_buffer[i * 2] = color_high;
            row_buffer[i * 2 + 1] = color_low;
        }

        for (int i = 0; i < h; ++i) {
            send_data_buffer(row_buffer.data(), bytes_per_row);
        }
    }

    void fillScreen(uint16_t color) {
        drawRectangle(0, 0, width, height, color);
    }

    ~ST7735() {
        close(spi_fd);
    }
};

int main() {
    // ATUALIZADO: Usando o gpiochip0, PB1 (Linha 33) e PB2 (Linha 34)
    ST7735 display("/dev/spidev1.0", "gpiochip0", 33, 34, 160, 80);
    display.init();
    
    display.fillScreen(COLOR_BLACK);
    usleep(500000);
    
    display.fillScreen(COLOR_GREEN);
    usleep(2000000);
    
    display.drawRectangle(40, 20, 80, 40, COLOR_RED);
    return 0;
}

```

## 3. Opção B: Método de Framebuffer do Kernel
Nesta abordagem, o driver `fb_st7735r` do Linux assume o controle exclusivo do SPI. O display passa a funcionar como um monitor secundário (`/dev/fbX`). Essa opção é adequada para renderizar interfaces de terminal, como FTXUI, ou interfaces gráficas, como Dear ImGui, diretamente pelas abstrações do sistema operacional.

### 3.1. Preparação
No `rsetup`, garanta que a opção `[ ] Enable spidev on SPI1` esteja desmarcada.

### 3.2. Criar o Device Tree Overlay (`.dts`)
Crie um arquivo chamado `st7735s-cubie-a7s.dts`:

```dts
/dts-v1/;
/plugin/;

/ {
    metadata {
        title = "Enable ST7735S SPI LCD on SPI1";
        compatible = "radxa,cubie-a7s";
        category = "display";
        description = "Ativa o display SPI ST7735S como framebuffer nativo.";
    };
};

&spi1 {
    status = "okay";
    #address-cells = <1>;
    #size-cells = <0>;

    st7735: st7735@0 {
        compatible = "sitronix,st7735r";
        reg = <0>;
        spi-max-frequency = <15000000>;
        buswidth = <8>;
        regwidth = <16>;
        rotate = <90>;
        fps = <30>;
        width = <160>;
        height = <80>;
        txbuflen = <32768>;

        /* Ajustes específicos para o ST7735S no kernel. */
        bgr = <1>;
        color-invert = <1>;

        /* Mapeamento interno do Allwinner A733. */
        reset-gpios = <&pio 1 2 GPIO_ACTIVE_LOW>; /* PB2 -> pino 29 */
        dc-gpios = <&pio 1 1 GPIO_ACTIVE_HIGH>;   /* PB1 -> pino 11 */

        debug = <0>;
    };
};

```

### 3.3. Compilação e ativação
Compile o overlay:

```bash
dtc -@ -I dts -O dtb -o st7735s-cubie-a7s.dtbo st7735s-cubie-a7s.dts

```
Copie o arquivo para a pasta de overlays da Radxa:

```bash
sudo cp st7735s-cubie-a7s.dtbo /boot/dtbo/

```
Execute `rsetup`, vá até **Overlays**, ative a opção correspondente e reinicie a placa.

### 3.4. Testar o framebuffer (`/dev/fbX`)
Para limpar a tela:

```bash
sudo dd if=/dev/zero of=/dev/fbX bs=10k count=1

```
Para enviar uma imagem:

```bash
ffmpeg -i imagem.jpg -f rawvideo -pix_fmt rgb565 -s 160x80 /dev/fbX

```

### 3.5. Executar aplicações no framebuffer
O monitor principal da placa, conectado via USB-C, continuará sendo a tela primária (`fb0`). Para direcionar as interfaces ao painel secundário, use os exemplos abaixo.

#### Console do Linux ou TUI (FTXUI)
Mapeie um terminal virtual, por exemplo `tty2`, para o framebuffer SPI, por exemplo `fb1`:

```bash
sudo con2fbmap 2 1

```
Depois, execute o binário C++ do FTXUI direcionando a renderização para esse terminal:

```bash
sudo ./meu_app_ftxui < /dev/tty2 > /dev/null 2>&1

```

#### Interface gráfica (Dear ImGui via SDL2)
Defina as variáveis de ambiente para usar o backend `linuxfb` e desenhar diretamente no dispositivo:

```bash
SDL_VIDEODRIVER=linuxfb SDL_FBDEV=/dev/fb1 ./meu_app_imgui

```

## 4. Teste de Loopback do SPI
O conceito é simples: conecte a saída MOSI, que envia os dados, diretamente à entrada MISO, que recebe os dados. Tudo o que o Linux enviar deverá ser recebido de volta.

### 4.1. Ligação física
Como o `spidev` já foi habilitado no `rsetup` pela Opção A, conecte um único cabo jumper:

- Pino 19 (SPI1-MOSI) diretamente ao pino 21 (SPI1-MISO).
- Desconecte o display SPI durante o teste.

### 4.2. Script de teste
Crie um arquivo chamado `teste_spi.py`:

```python
import spidev

# Abre o barramento SPI 1, Chip Select 0 (/dev/spidev1.0).
spi = spidev.SpiDev()
spi.open(1, 0)
spi.max_speed_hz = 50000  # Velocidade baixa para o teste.

mensagem_enviada = [0xDE, 0xAD, 0xBE, 0xEF, 0x42]

print("Enviando: ", [hex(byte) for byte in mensagem_enviada])

# xfer2 envia e lê ao mesmo tempo.
mensagem_recebida = spi.xfer2(mensagem_enviada)

print("Recebido: ", [hex(byte) for byte in mensagem_recebida])

if mensagem_enviada == mensagem_recebida:
    print("\nSUCESSO! O hardware SPI da Radxa está funcionando perfeitamente!")
else:
    print("\nFALHA! Verifique o jumper entre os pinos 19 e 21.")

spi.close()

```
Execute o script:

```bash
python3 teste_spi.py

```
Se a linha **Recebido** for exatamente igual à linha **Enviando**, o kernel do Linux, o controlador de hardware do processador e os pinos físicos da placa estão funcionando em conjunto.

Se o display SPI não funcionar depois desse teste, verifique o display e os cabos, pois o loopback isolou o funcionamento básico da placa.