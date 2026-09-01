# Plano de Integração: Display LCD TFT/OLED (ST7735 / ST7735S) na Radxa Cubie A7S
Este documento detalha o plano completo para conectar e programar o display colorido (controlador ST7735 ou sua variante ST7735S, resolução 160x80) na placa Radxa Cubie A7S. Estão descritas duas abordagens distintas para integração via software.

## 1. Conexões Físicas (Header 30 Pinos)
O display precisa ser alimentado corretamente e ter seus sinais lógicos conectados. As portas GPIO da Cubie A7S operam em uma tensão de 3.3V, ideal para este componente.

| Pino do Display | Radxa Cubie A7S (Header 30 Pinos) | Função na Placa |
| --- | --- | --- |
| GND | Pino 6 | GND (Terra) |
| VCC | Pino 1 | 3.3V (Alimentação) |
| SCL / SCK | Pino 23 | SPI1-CLK (Função alternativa 4) |
| SDA / MOSI | Pino 19 | SPI1-MOSI (Função alternativa 4) |
| CS | Pino 24 | SPI1-CS0 (Função alternativa 6) |
| DC / RS | Pino 27 | PD17 (Saída GPIO comum) |
| RES / RST | Pino 29 | PB2 (Saída GPIO comum) |

*(Nota: Pinos GND adicionais disponíveis na placa incluem 9, 14, 20, 26 e 30).*

---

## Opção A: Método "Espaço de Usuário" (via `spidev`)
Nesta abordagem, o sistema operacional expõe os pinos, e a sua aplicação é totalmente responsável por enviar os comandos de desenho para a tela. Excelente para aplicações autônomas construídas em C++ ou Python.

### A.1. Configuração do SO (`rsetup`)

1. Execute `rsetup` no terminal.
2. Navegue até **Overlays**.
3. Marque a opção: `[] Enable spidev on SPI1`
4. *Selecione *`<Ok>`* e reinicie a placa (*`sudo reboot`*). O dispositivo *`/dev/spidev1.0`* será criado.*

### *A.2. Implementação em Python*
*Evite bibliotecas que dependam do *`RPI.GPIO`*. Utilize a abstração *`Blinka`* da Adafruit.*

***Instalação de Dependências:***

```bash
sudo apt-get install python3-pip python3-spidev python3-libgpiod
pip3 install adafruit-blinka adafruit-circuitpython-rgb-display pillow

```

***Script de Teste (***`display_test.py`***):***

```python
import board
import digitalio
import adafruit_rgb_display.st7735 as st7735
from PIL import Image, ImageDraw

cs_pin = digitalio.DigitalInOut(board.D24) 
dc_pin = digitalio.DigitalInOut(board.D27)
reset_pin = digitalio.DigitalInOut(board.D29)

spi = board.SPI()

# NOTA PARA CHIP ST7735S: Se as cores ficarem invertidas ou a imagem deslocada,
# ajuste as flags abaixo (bgr=True, invert=True, x_offset=1, y_offset=26).
disp = st7735.ST7735R(
    spi, 
    rotation=90, 
    cs=cs_pin, 
    dc=dc_pin, 
    rst=reset_pin, 
    width=160, 
    height=80,
    bgr=True,          # Corrige Vermelho/Azul trocado
    invert=True,       # Corrige Cores tipo "Negativo"
    x_offset=1,        # Ajuste fino de borda (ST7735S)
    y_offset=26        # Ajuste fino de borda (ST7735S)
)

image = Image.new("RGB", (disp.width, disp.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=(0, 255, 0))
disp.image(image)

```

### *A.3. Implementação em C++ (CMake)*
*Para obter o máximo de desempenho com C++ (ideal para C++20/23), manipula-se o barramento com *`ioctl`* e os pinos de controle usando a *`libgpiod`*.*

***Instalação de Dependências (Headers C++):***

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
        
        gpiod::line_request config;
        config.request_type = gpiod::line_request::DIRECTION_OUTPUT;
        dc_line.request(config);
        res_line.request(config);
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
    ST7735 display("/dev/spidev1.0", "gpiochip1", 17, 2, 160, 80);
    display.init();
    
    display.fillScreen(COLOR_BLACK);
    usleep(500000);
    
    display.fillScreen(COLOR_GREEN);
    usleep(2000000);
    
    display.drawRectangle(40, 20, 80, 40, COLOR_RED);
    return 0;
}

```

---

## *Opção B: Método "Framebuffer do Kernel" (Monitor Nativo)*
*Nesta abordagem, o driver *`fb_st7735r`* do Linux assume o controle exclusivo do SPI. O display vira um monitor secundário (*`/dev/fbX`*). Excelente para renderizar interfaces Text User Interface (como ****FTXUI****) ou Graphical User Interfaces (como ****Dear ImGui****) diretamente através das abstrações do sistema operacional.*

### *B.1. Preparação*
*No *`rsetup`*, garanta que a opção *`[ ] Enable spidev on SPI1`* esteja ****desmarcada****.*

### *B.2. Criar o Device Tree Overlay (.dts)*
*Crie um arquivo chamado *`st7735s-cubie-a7s.dts`*:*

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
        
        /* Ajustes específicos para o ST7735S no kernel */
        bgr = <1>;
        color-invert = <1>;
        
        /* Mapeamento interno do Allwinner A733 */
        reset-gpios = <&pio 1 2 GPIO_ACTIVE_LOW>; /* PB2 -> Pino 29 */
        dc-gpios = <&pio 3 17 GPIO_ACTIVE_HIGH>;  /* PD17 -> Pino 27 */
        
        debug = <0>;
    };
};

```

### *B.3. Compilação e Ativação*

1. *Compile: *`dtc -@ -I dts -O dtb -o st7735s-cubie-a7s.dtbo st7735s-cubie-a7s.dts`
2. *Copie para a pasta de overlays da Radxa: *`sudo cp st7735s-cubie-a7s.dtbo /boot/dtbo/`
3. *Execute *`rsetup`*, vá em Overlays, ative a opção e reinicie a placa.*

### *B.4. Testando o Framebuffer (*`/dev/fbX`*)*
**Limpar a tela (preto):** `sudo dd if=/dev/zero of=/dev/fbX bs=10k count=1`

***Enviar uma imagem:**** *`ffmpeg -i imagem.jpg -f rawvideo -pix_fmt rgb565 -s 160x80 /dev/fbX`

### *B.5. Executando Aplicações no Framebuffer*
*O monitor principal da placa (via USB-C) continuará sendo a tela primária (*`fb0`*). Para direcionar suas interfaces para o painel secundário:*

**Para Console do Linux ou TUI (FTXUI):**

Mapeie um terminal virtual (ex: `tty2`) para o framebuffer SPI (ex: `fb1`):

`sudo con2fbmap 2 1`

Depois, execute o binário C++ do FTXUI direcionando a renderização para lá:

`sudo ./meu_app_ftxui <> /dev/tty2 >&0 2>&1`

**Para Interfaces Gráficas (Dear ImGui via SDL2):**

Injete variáveis de ambiente para fazer o backend gráfico saltar o servidor de janelas (X11/Wayland) e desenhar diretamente no dispositivo:

`SDL_VIDEODRIVER=linuxfb SDL_FBDEV=/dev/fb1 ./meu_app_imgui`