# Notes about integrating an ST7735S display on the Radxa Cubie A7S

[Português (Brasil)](./0012-notas-display-tft-st7735s-radxa-cubie-a7s-pt-br.md)

This document describes how to connect and program a colour display (ST7735 or ST7735S controller, 160x80 resolution) on the Radxa Cubie A7S. It covers two software integration approaches.

## 1. Physical connections (30-pin header)

The display must be powered correctly and its logic signals connected. The Cubie A7S GPIO ports operate at 3.3 V, which is suitable for this component.

**Important:** The BLK (backlight) pin must be connected to 3.3 V for the backlight to illuminate; otherwise, the screen will remain completely black.

| Display pin | Radxa Cubie A7S (30-pin header) | Board function |
| --------------- | ------------------------------------ | -------------------------------- |
| GND             | Pin 6                                | GND (earth)                      |
| VCC             | Pin 1                                | 3.3 V (power)                    |
| BLK             | Pin 17                               | 3.3 V (backlight)                |
| SCL / SCK       | Pin 23                               | SPI1-CLK (alternate function 4)  |
| SDA / MOSI      | Pin 19                               | SPI1-MOSI (alternate function 4) |
| CS              | Pin 24                               | SPI1-CS0 (alternate function 6)  |
| DC / RS         | Pin 11                               | PB1 (line 33 on gpiochip0)       |
| RES / RST       | Pin 29                               | PB2 (line 34 on gpiochip0)       |

> **Note:** Additional GND pins on the board are 9, 14, 20, 26, and 30.

## 2. Option A: user-space approach

With this approach, the operating system exposes the pins and the application sends drawing commands to the display. It is suitable for standalone C++ or Python applications using `spidev` and `libgpiod`.

### 2.1. OS configuration (`rsetup`)

1. Run `rsetup` in the terminal.
2. Go to **Overlays**.
3. Select `[*] Enable spidev on SPI1`.
4. Leave the framebuffer overlay unchecked so that it does not claim the DC and RST pins.
5. Select `<Ok>` and reboot the board with `sudo reboot`.
6. After rebooting, `/dev/spidev1.0` should be available.

### 2.2. Understanding pin mapping (`gpiochip0`)

The Allwinner A733 processor driver groups all 352 logical pins under a single controller named `gpiochip0`.

Many processor-internal pins have no label (`unnamed`), but the kernel assigns friendly names (for example, `"PIN_11"`, `"PIN_29"`) to pins exposed on the 30-pin header.

You can access these pins in code in either of two ways:

1. **By name (recommended):** Use the `libgpiod` library’s `find_line("PIN_11")` function.
2. **By calculated index:** If you prefer the raw hardware address (`get_line(33)`), use this universal formula:

> **Numeric index = (bank index x 32) + pin number**

The banks follow alphabetical order (PA=0, PB=1, PC=2, PD=3):

- **DC pin (PB1):** bank 1 x 32 + 1 = **line 33**
- **RST pin (PB2):** bank 1 x 32 + 2 = **line 34**

### 2.3. Python implementation

Because of limitations and dependencies in third-party libraries (`Adafruit-Blinka` and `periphery`), this guide uses the native kernel API through `libgpiod`.

#### 2.3.1. Installing dependencies

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev python3-libgpiod
pip3 install spidev pillow

```

#### 2.3.2. Test script (`display_test.py`)

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

### 2.4. C++ implementation (CMake)

For maximum performance with C++20 or C++23, the bus is controlled with `ioctl` and the control pins with `libgpiod`.

#### 2.4.1. Installing dependencies

```bash
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install cmake
sudo apt-get install gpiod libgpiod-dev libgpiodcxx-dev

# no debian
sudo apt-get install libgpiod-dev

```

`CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.18)
project(ST7735_Driver VERSION 1.0)
set(CMAKE_CXX_STANDARD 20)

# Criamos o executável apontando para o seu arquivo fonte
add_executable(spi-test spi-test.cpp)

# Linkamos diretamente as bibliotecas do sistema (equivale ao -lgpiodcxx -lgpiod)
target_link_libraries(spi-test PRIVATE gpiodcxx gpiod)

```

`main.cpp` (complete, with line buffer and ST7735S adjustments):

For the original C++ program using the `gpiodcxx` bindings, update the object instantiation in `main.cpp` to use the correct `gpiochip0` addresses and configure the line direction with default values, as in the Python solution:

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

#### 2.4.2. Compiling directly with g++

```bash
g++ -std=c++20 spi-test.cpp -o spi-test -lgpiodcxx
g++ spi-test.cpp -o spi-test -lgpiodcxx -lgpiod
```

#### 2.4.3. Compiling with CMake

```bash
mkdir build
cd build
cmake ..
make
sudo ./spi-test
```

## 3. Option B: kernel framebuffer approach

With this approach, the Linux `fb_st7735r` driver takes exclusive control of SPI. The display then operates as a secondary monitor (`/dev/fbX`). This option is suitable for rendering terminal interfaces such as FTXUI, or graphical interfaces such as Dear ImGui, directly through operating-system abstractions.

### 3.1. Preparation

In `rsetup`, make sure that `[ ] Enable spidev on SPI1` is unchecked.

### 3.2. Creating the Device Tree overlay (`.dts`)

Create a file named `st7735s-cubie-a7s.dts`:

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

### 3.3. Compiling and enabling

Compile the overlay:

```bash
dtc -@ -I dts -O dtb -o st7735s-cubie-a7s.dtbo st7735s-cubie-a7s.dts

```

Copy the file to the Radxa overlays directory:

```bash
sudo cp st7735s-cubie-a7s.dtbo /boot/dtbo/

```

Run `rsetup`, go to **Overlays**, enable the corresponding option, and reboot the board.

### 3.4. Testing the framebuffer (`/dev/fbX`)

To clear the screen:

```bash
sudo dd if=/dev/zero of=/dev/fbX bs=10k count=1

```

To send an image:

```bash
ffmpeg -i imagem.jpg -f rawvideo -pix_fmt rgb565 -s 160x80 /dev/fbX

```

### 3.5. Running applications on the framebuffer

The board’s main monitor, connected via USB-C, remains the primary display (`fb0`). To direct interfaces to the secondary panel, use the examples below.

#### 3.5.1. Linux console or TUI (FTXUI)

Map a virtual terminal, such as `tty2`, to the SPI framebuffer, such as `fb1`:

```bash
sudo con2fbmap 2 1

```

Then run the FTXUI C++ binary, directing rendering to that terminal:

```bash
sudo ./meu_app_ftxui < /dev/tty2 > /dev/null 2>&1

```

#### 3.5.2. Graphical interface (Dear ImGui via SDL2)

Set the environment variables to use the `linuxfb` backend and draw directly to the device:

```bash
SDL_VIDEODRIVER=linuxfb SDL_FBDEV=/dev/fb1 ./meu_app_imgui

```

## 4. SPI loopback test

The idea is simple: connect the MOSI output, which sends data, directly to the MISO input, which receives data. Everything Linux sends should be received back.

### 4.1. Physical connection

Since `spidev` was enabled in `rsetup` for Option A, connect a single jumper wire:

- Connect pin 19 (SPI1-MOSI) directly to pin 21 (SPI1-MISO).
- Disconnect the SPI display during the test.

### 4.2. Test script

Create a file named `teste_spi.py`:

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

Run the script:

```bash
python3 teste_spi.py

```

If the **Received** line exactly matches the **Sent** line, the Linux kernel, processor hardware controller, and board pins are working together.

If the SPI display still does not work after this test, check the display and cables; the loopback test has isolated the board’s basic operation.
