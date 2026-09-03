Markdown

# Plano de Integração Final: Display LCD TFT (ST7735S) na Radxa Cubie A7S

Este documento detalha o plano definitivo e validado para conectar o display colorido (ST7735S, 160x80) na Radxa Cubie A7S, contemplando as peculiaridades do kernel Linux e do processador Allwinner A733.

## 1. Conexões Físicas (Header 30 Pinos)

O display requer alimentação para a lógica, para a luz de fundo (Backlight) e os sinais de dados.

| Pino do Display | Radxa Cubie A7S (Header 30 Pinos) | Função na Placa                   |
| :-------------- | :-------------------------------- | :-------------------------------- |
| **GND**         | **Pino 6**                        | GND (Terra)                       |
| **VCC**         | **Pino 1**                        | 3.3V (Alimentação Lógica)         |
| **BLK**         | **Pino 17**                       | 3.3V (Luz de Fundo - Obrigatório) |
| **SCL / SCK**   | **Pino 23**                       | SPI1-CLK                          |
| **SDA / MOSI**  | **Pino 19**                       | SPI1-MOSI                         |
| **CS**          | **Pino 24**                       | SPI1-CS0                          |
| **DC / RS**     | **Pino 11**                       | PB1 (Linha 33 do gpiochip0)       |
| **RES / RST**   | **Pino 29**                       | PB2 (Linha 34 do gpiochip0)       |

---

## Opção A: Espaço de Usuário (Python / C++)

### A.1. Configuração do SO (`rsetup`)

1. Execute `rsetup` no terminal.
2. Navegue até **Overlays**.
3. Marque APENAS a opção: `[*] Enable spidev on SPI1` (garanta que o overlay do ST7735 Framebuffer não esteja marcado para não bloquear os pinos).
4. Reinicie a placa (`sudo reboot`).

### A.2. Implementação em Python

Usamos a biblioteca nativa `spidev` para os dados e a oficial `gpiod` para os pinos de controle.

**Instalação de Dependências:**

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev python3-libgpiod
pip3 install spidev pillow
Script Validado (spi_test.py):

Python
import spidev
import gpiod
import time
from PIL import Image, ImageDraw

class ST7735S:
    def __init__(self):
        self.chip = gpiod.Chip("gpiochip0")
        self.dc = self.chip.get_line(33) # Pino 11
        self.rst = self.chip.get_line(34) # Pino 29

        self.dc.request(consumer="st7735", type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
        self.rst.request(consumer="st7735", type=gpiod.LINE_REQ_DIR_OUT, default_val=1)

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

        self.send_cmd(0x01) # SWRESET
        time.sleep(0.15)
        self.send_cmd(0x11) # SLPOUT
        time.sleep(0.2)

        self.send_cmd(0x3A)
        self.send_data(0x05) # 16-bit
        self.send_cmd(0x36)
        self.send_data(0x68) # BGR
        self.send_cmd(0x21) # INVON
        self.send_cmd(0x29) # DISPON
        time.sleep(0.1)

    def display_image(self, image):
        self.send_cmd(0x2A)
        self.send_data([0x00, 1, 0x00, image.width])
        self.send_cmd(0x2B)
        self.send_data([0x00, 26, 0x00, image.height + 25])
        self.send_cmd(0x2C)

        pixels = list(image.getdata())
        buf = bytearray()
        for r, g, b in pixels:
            color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            buf.append(color >> 8)
            buf.append(color & 0xFF)

        self.dc.set_value(1)
        for i in range(0, len(buf), 4096):
            self.spi.xfer2(list(buf[i:i+4096]))

if __name__ == "__main__":
    disp = ST7735S()
    disp.init_display()
    img = Image.new("RGB", (160, 80), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((10, 10, 150, 70), outline=(0, 255, 0), width=2)
    disp.display_image(img)
A.3. Implementação em C++ (CMake)
Dependências:

Bash
sudo apt-get install gpiod libgpiod-dev libgpiodcxx-dev
Código C++ (main.cpp - Trecho principal atualizado):
No seu código C++, atualize a instanciação da classe para refletir o gpiochip0 e as linhas 33 e 34.

C++
// Instancia a classe: /dev/spidev1.0, GPIO Chip 0, DC=33, RST=34, 160x80
ST7735 display("/dev/spidev1.0", "gpiochip0", 33, 34, 160, 80);
Lembre-se de adicionar o default_val na requisição da linha, similar ao Python, dependendo da versão da libgpiodcxx instalada.

Opção B: Framebuffer do Kernel (.dtbo)
B.1. Criar o Device Tree Overlay (st7735s-cubie-a7s.dts)
Atualizado para refletir o uso do Pino 11 (PB1) para o comando DC.

DTS
/dts-v1/;
/plugin/;

/ {
    metadata {
        title = "Enable ST7735S SPI LCD on SPI1";
        compatible = "radxa,cubie-a7s";
        category = "display";
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

        bgr = <1>;
        color-invert = <1>;

        /* Mapeamento interno do Allwinner A733 */
        reset-gpios = <&pio 1 2 GPIO_ACTIVE_LOW>; /* PB2 -> Pino 29 */
        dc-gpios = <&pio 1 1 GPIO_ACTIVE_HIGH>;   /* PB1 -> Pino 11 */

        debug = <0>;
    };
};
```
