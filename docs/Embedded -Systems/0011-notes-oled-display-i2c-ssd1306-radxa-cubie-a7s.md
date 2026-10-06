# Notes about integrating an I2C OLED display (SSD1306) on the Radxa Cubie A7S

[Português (Brasil)](./0011-notas-display-oled-i2c-ssd1306-radxa-cubie-a7s-pt-br.md)

This document explains how to connect and program an OLED display over I2C (SSD1306 controller, typically 128x64) on the Radxa Cubie A7S.

## 1. Physical connections (30-pin header)

This guide uses the **TWI2** (I2C) bus available on the board header. The logic voltage is 3.3 V.

| Display pin | Radxa Cubie A7S (30-pin header) | Board function |
| :--- | :--- | :--- |
| **GND** | **Pin 6** | GND (Earth) |
| **VCC** | **Pin 1** | 3.3V (Power) |
| **SCL / SCK** | **Pin 28** | TWI2-SCK (Clock) |
| **SDA**| **Pin 27** | TWI2-SDA (Data) |

*(Note: Do not swap VCC and GND. Other GND pins are 9, 14, 20, and 26.)*

---

## 2. OS configuration (`rsetup`)

Linux needs to know that these pins are to be used for TWI/I2C communication rather than generic GPIOs.

1. In the SSH terminal, run `rsetup`.
2. Go to **Overlays**.
3. Select `[*] Enable TWI2`.
4. Select `<Ok>`, exit, and reboot the board (`sudo reboot`).
5. *(Optional)* Check whether the display was detected by installing `i2c-tools` (`sudo apt install i2c-tools`) and running this in the terminal:
   `sudo i2cdetect -y 2`

The display address (usually `3c`, meaning 0x3C) should appear in the matrix.

---

## 3. Python implementation

Because `adafruit-blinka` is incompatible with the Radxa system, this guide uses `luma.oled`, which communicates directly with the kernel device `/dev/i2c-2` and provides excellent support for the Pillow graphics library.

**Install dependencies:**

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-smbus i2c-tools python3-dev
pip3 install luma.oled pillow
```

### 3.1. Test script (`oled_test.py`)

```python
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageDraw

# Inicializa a comunicação I2C nativamente no barramento 2 (/dev/i2c-2)
# O endereço padrão 0x3C é assumido automaticamente pela biblioteca
serial = i2c(port=2, address=0x3C)

# Cria o dispositivo do display (ajuste width e height se o seu for 128x32)
device = ssd1306(serial, width=128, height=64)

# O gerenciador de contexto 'canvas' lida automaticamente com o envio da imagem (disp.show())
print("Desenhando na tela...")
with canvas(device) as draw:
    # Desenha um retângulo na borda externa
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    
    # Adiciona um texto simples
    draw.text((15, 25), "Radxa A7S - I2C!", fill="white")

print("Teste concluído!")
```

## 4. C++ implementation (CMake)

When using I2C on Linux through C++, we interact directly with the kernel device interface `/dev/i2c-X`. `libgpiod` is not needed because individual pins are not being manipulated; the I2C controller handles the bits.

### 4.1. Installing dependencies

```bash
sudo apt-get update
sudo apt-get install libi2c-dev
```

### 4.2. `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.20)
project(SSD1306_Driver VERSION 1.0)
set(CMAKE_CXX_STANDARD 20)
add_executable(oled_main main.cpp)
```

### 4.3. `main.cpp`

```cpp
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <vector>

class SSD1306 {
private:
    int i2c_fd;
    uint8_t address;

    void send_command(uint8_t cmd) {
        // 0x00 é o byte de controle indicando que o próximo byte é um Comando
        uint8_t buffer[2] = {0x00, cmd}; 
        write(i2c_fd, buffer, 2);
    }

    void send_data_block(const std::vector<uint8_t>& data) {
        std::vector<uint8_t> buffer;
        // 0x40 é o byte de controle indicando que o restante são Dados (pixels)
        buffer.push_back(0x40); 
        buffer.insert(buffer.end(), data.begin(), data.end());
        write(i2c_fd, buffer.data(), buffer.size());
    }

public:
    SSD1306(const std::string& i2c_dev, uint8_t addr) : address(addr) {
        i2c_fd = open(i2c_dev.c_str(), O_RDWR);
        if (i2c_fd < 0) {
            std::cerr << "Erro ao abrir o barramento I2C!" << std::endl;
            exit(1);
        }
        if (ioctl(i2c_fd, I2C_SLAVE, address) < 0) {
            std::cerr << "Erro ao conectar no endereco do I2C!" << std::endl;
            exit(1);
        }
    }

    void init() {
        // Sequência de inicialização padrão do SSD1306 (para painel 128x64)
        uint8_t init_cmds[] = {
            0xAE,       // Display OFF
            0xD5, 0x80, // Set Display Clock Divide Ratio
            0xA8, 0x3F, // Set Multiplex Ratio (64)
            0xD3, 0x00, // Set Display Offset
            0x40,       // Set Start Line 0
            0x8D, 0x14, // Charge Pump Setting
            0x20, 0x00, // Set Memory Addressing Mode (Horizontal)
            0xA1,       // Set Segment Re-map
            0xC8,       // Set COM Output Scan Direction
            0xDA, 0x12, // Set COM Pins Hardware Configuration
            0x81, 0xCF, // Set Contrast Control
            0xD9, 0xF1, // Set Pre-charge Period
            0xDB, 0x40, // Set VCOMH Deselect Level
            0xA4,       // Entire Display ON (Resume)
            0xA6,       // Normal Display (nao invertido)
            0xAF        // Display ON
        };
        for (uint8_t cmd : init_cmds) {
            send_command(cmd);
        }
    }

    void fillScreen(uint8_t color_pattern) {
        // Posiciona os ponteiros de coluna e página na origem (Canto Superior Esquerdo)
        send_command(0x21); send_command(0); send_command(127); // Colunas 0 a 127
        send_command(0x22); send_command(0); send_command(7);   // Paginas 0 a 7 (8 paginas * 8 bits = 64 pixels)

        // 128 colunas * 8 páginas = 1024 bytes para preencher a tela inteira
        std::vector<uint8_t> buffer(1024, color_pattern);
        
        // O kernel muitas vezes tem limite no tamanho do payload I2C. 
        // Enviamos o buffer em pequenos blocos de 128 bytes (uma linha inteira da tela).
        for(size_t i = 0; i < buffer.size(); i += 128) {
            std::vector<uint8_t> chunk(buffer.begin() + i, buffer.begin() + i + 128);
            send_data_block(chunk);
        }
    }

    ~SSD1306() {
        close(i2c_fd);
    }
};

int main() {
    std::cout << "Inicializando OLED SSD1306 via I2C (/dev/i2c-2)..." << std::endl;
    
    // I2C-2 (TWI2), Endereço padrao 0x3C
    SSD1306 oled("/dev/i2c-2", 0x3C);
    
    oled.init();
    
    std::cout << "Limpando a tela (Preto)..." << std::endl;
    oled.fillScreen(0x00);
    usleep(1000000); // Aguarda 1 segundo
    
    std::cout << "Preenchendo a tela (Padrao Xadrez)..." << std::endl;
    oled.fillScreen(0x55); // 0x55 em binario eh 01010101
    
    std::cout << "Concluído!" << std::endl;
    return 0;
}
```
