# Plano de Integração: Display OLED I2C (SSD1306) na Radxa Cubie A7S

Este documento detalha o plano para conectar e programar um display OLED com comunicação I2C (controlador SSD1306, tipicamente 128x64) na placa Radxa Cubie A7S.

## 1. Conexões Físicas (Header 30 Pinos)

Para este guia, utilizaremos o barramento **TWI2** (I2C) disponível no header da placa. A tensão lógica será de 3.3 V.

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
3. Marque a opção `[*] Enable TWI2`.
4. Selecione `<Ok>`, saia e reinicie a placa (`sudo reboot`).
5. *(Opcional)* Verifique se o display foi reconhecido instalando o `i2c-tools` (`sudo apt install i2c-tools`) e rodando no terminal:
   `sudo i2cdetect -y 2`
   O endereço do display (normalmente `3c`, que significa 0x3C) deve aparecer na matriz.

---

## 3. Implementação em Python

Devido à incompatibilidade da biblioteca `adafruit-blinka` com o sistema da Radxa, utilizaremos a biblioteca `luma.oled`, que interage diretamente com o arquivo nativo `/dev/i2c-2` do kernel, oferecendo excelente suporte para a biblioteca gráfica Pillow.

**Instalação de Dependências:**

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-smbus i2c-tools python3-dev
pip3 install luma.oled pillow
```

### 3.1. Script de Teste (`oled_test.py`)

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

## 4. Implementação em C++ (CMake)

Ao usar I2C no Linux via C++, interagimos diretamente com a interface de dispositivos do kernel `/dev/i2c-X`. Não precisamos da `libgpiod` porque não estamos manipulando pinos individuais; o controlador I2C lida com os bits para nós.

### 4.1. Instalação de Dependências

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
