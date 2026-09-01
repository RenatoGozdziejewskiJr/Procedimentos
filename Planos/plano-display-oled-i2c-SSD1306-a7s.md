# Plano de Integração: Display OLED I2C (SSD1306) na Radxa Cubie A7S

Este documento detalha o plano para conectar e programar um display OLED com comunicação I2C (controlador SSD1306, tipicamente 128x64) na placa Radxa Cubie A7S.

## 1. Conexões Físicas (Header 30 Pinos)

Para este guia, utilizaremos o barramento **TWI2** (I2C) disponível no header da placa. A tensão lógica será de 3.3V.

| Pino do Display | Radxa Cubie A7S (Header 30 Pinos) | Função na Placa |
| :--- | :--- | :--- |
| **GND** | **Pino 6** | GND (Terra) |
| **VCC** | **Pino 1** | 3.3V (Alimentação) |
| **SCL / SCK** | **Pino 28** | TWI2-SCK (Clock) |
| **SDA**| **Pino 27** | TWI2-SDA (Dados) |

*(Nota: Certifique-se de não cruzar VCC e GND. Outros pinos de GND incluem 9, 14, 20, 26).*

---

## 2. Configuração do SO (`rsetup`)

O Linux precisa saber que você deseja usar esses pinos para comunicação TWI/I2C em vez de GPIOs genéricos.

1. No terminal SSH, execute `rsetup`.
2. Vá em **Overlays**.
3. Marque a opção: `[*] Enable TWI2`
4. Selecione `<Ok>`, saia e reinicie a placa (`sudo reboot`).
5. *(Opcional)* Verifique se o display foi reconhecido instalando o `i2c-tools` (`sudo apt install i2c-tools`) e rodando no terminal:
   `sudo i2cdetect -y 2`
   O endereço do display (normalmente `3c`, que significa 0x3C) deve aparecer na matriz.

---

## 3. Implementação em Python

A forma mais fácil de trabalhar com o SSD1306 no Python é utilizando a biblioteca Blinka (camada de hardware) e o Pillow (PIL) para desenhar gráficos.

**Instalação de Dependências:**
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-smbus i2c-tools
pip3 install adafruit-blinka adafruit-circuitpython-ssd1306 pillow
```

**Script de Teste (`oled_test.py`):**
```python
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Inicializa o barramento I2C do sistema (mapeado pelo Blinka)
i2c = busio.I2C(board.SCL, board.SDA)

# Configuração do display OLED (ajuste para 128x32 se for o modelo menor)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

# Limpa o display
disp.fill(0)
disp.show()

# Cria uma imagem em branco com 1-bit de cor
image = Image.new("1", (disp.width, disp.height))
draw = ImageDraw.Draw(image)

# Desenha um retângulo na borda e um texto no centro
draw.rectangle((0, 0, disp.width - 1, disp.height - 1), outline=255, fill=0)
draw.text((10, 25), "Radxa A7S - I2C!", fill=255)

# Envia a imagem para a tela
disp.image(image)
disp.show()
```

---

## 4. Implementação em C++ (CMake)

Ao usar I2C no Linux via C++, interagimos diretamente com a interface de dispositivos do kernel `/dev/i2c-X`. Não precisamos da `libgpiod` porque não estamos manipulando pinos individuais; o controlador I2C lida com os bits para nós.

**Instalação de Dependências:**
```bash
sudo apt-get update
sudo apt-get install libi2c-dev
```

**`CMakeLists.txt`:**
```cmake
cmake_minimum_required(VERSION 3.20)
project(SSD1306_Driver VERSION 1.0)
set(CMAKE_CXX_STANDARD 20)
add_executable(oled_main main.cpp)
```

**`main.cpp`:**
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
