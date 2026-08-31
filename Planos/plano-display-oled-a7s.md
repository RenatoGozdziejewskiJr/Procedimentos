# Plano de Integração: Display LCD TFT/OLED (ST7735) na Radxa Cubie A7S

Este documento detalha o plano completo para conectar e programar o seu display colorido com controlador ST7735 na placa Radxa Cubie A7S.

## 1. Conexões Físicas (Header 30 Pinos)

O display precisa ser alimentado corretamente e ter seus sinais lógicos conectados. As portas GPIO da Cubie A7S operam em uma tensão de 3.3V, ideal para este componente.

| Pino do Display (ST7735) | Radxa Cubie A7S (Header 30 Pinos) | Função na Placa |
| :--- | :--- | :--- |
| **GND** | **Pino 6** | GND (Terra) |
| **VCC** | **Pino 1** | 3.3V (Alimentação) |
| **SCL / SCK** | **Pino 23** | SPI1-CLK (Função alternativa 4) |
| **SDA / MOSI**| **Pino 19** | SPI1-MOSI (Função alternativa 4) |
| **CS** | **Pino 24** | SPI1-CS0 (Função alternativa 6) |
| **DC / RS** | **Pino 27** | PD17 (Saída GPIO comum) |
| **RES / RST** | **Pino 29** | PB2 (Saída GPIO comum) |

*(Nota: Pinos GND adicionais disponíveis na placa incluem 9, 14, 20, 26 e 30).*

---

## 2. Configuração do Sistema Operacional (Device Tree)

Para que a placa exponha o barramento de hardware SPI para o Linux, é necessário ativá-lo via utilitário de configuração de Overlays.

1. No terminal SSH da placa, execute o comando de configuração (ex: `rsetup`).
2. Navegue até o menu de **Overlays**.
3. Selecione a opção com a barra de espaço para que fique marcada assim:
   `[*] Enable spidev on SPI1`
4. Selecione `<Ok>` e saia do configurador.
5. Reinicie a placa com `sudo reboot`. 
6. Após reiniciar, você deve encontrar o dispositivo exposto em `/dev/spidev1.0`.

---

## 3. Implementação em C++

Abaixo está uma estrutura de projeto usando **CMake** e recursos nativos do ecossistema Linux (`libgpiod` para os pinos de controle e `ioctl` para o barramento SPI).

### `CMakeLists.txt`
```cmake
cmake_minimum_required(VERSION 3.20)
project(ST7735_Driver VERSION 1.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Requer a biblioteca C++ do gpiod previamente instalada no sistema
find_package(gpiod REQUIRED)

add_executable(display_main main.cpp)
target_link_libraries(display_main PRIVATE gpiodcxx)
```

### `main.cpp`
```cpp
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <gpiod.hpp>

class ST7735 {
private:
    int spi_fd;
    gpiod::line dc_line;
    gpiod::line res_line;

    void spi_transfer(uint8_t val) {
        spi_ioc_transfer tr = {};
        tr.tx_buf = (unsigned long)&val;
        tr.len = 1;
        tr.speed_hz = 10000000; // 10MHz
        tr.bits_per_word = 8;
        ioctl(spi_fd, SPI_IOC_MESSAGE(1), &tr);
    }

    void send_command(uint8_t cmd) {
        dc_line.set_value(0);
        spi_transfer(cmd);
    }

    void send_data(uint8_t data) {
        dc_line.set_value(1);
        spi_transfer(data);
    }

public:
    ST7735(const std::string& spi_dev, const std::string& gpio_chip, int dc_offset, int res_offset) {
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
        // Reset de Hardware
        res_line.set_value(0);
        usleep(100000);
        res_line.set_value(1);
        usleep(100000);
        
        // Sequência Inicialização SW (Exemplo ST7735)
        send_command(0x01); // SWRESET
        usleep(150000);
        send_command(0x11); // SLPOUT
        usleep(200000);
        send_command(0x29); // DISPON
    }
    
    ~ST7735() {
        close(spi_fd);
    }
};

int main() {
    // Atenção: O nome correto do gpiochip e os offsets lógicos de PD17 e PB2 
    // dependem da enumeração no kernel da A7S. 
    ST7735 display("/dev/spidev1.0", "gpiochip1", 17, 2);
    display.init();
    
    std::cout << "Display inicializado via C++!" << std::endl;
    return 0;
}
```

---

## 4. Implementação em Python

Para rodar gráficos de forma rápida, é possível utilizar a abstração *Blinka* da Adafruit em conjunto com o `Pillow` para processamento de imagem.

**Instalação de Dependências:**
```bash
sudo apt-get install python3-pip python3-spidev python3-libgpiod
pip3 install adafruit-circuitpython-rgb-display pillow
```

**Script `display_test.py`:**
```python
import board
import digitalio
import adafruit_rgb_display.st7735 as st7735
from PIL import Image, ImageDraw

# Configuração dos pinos de controle GPIO
cs_pin = digitalio.DigitalInOut(board.D24) 
dc_pin = digitalio.DigitalInOut(board.D27)
reset_pin = digitalio.DigitalInOut(board.D29)

# Inicializa o barramento SPI do Linux
spi = board.SPI()

# Inicializa o driver do display
disp = st7735.ST7735R(
    spi, 
    rotation=90, 
    cs=cs_pin, 
    dc=dc_pin, 
    rst=reset_pin, 
    width=160, 
    height=80
)

# Cria uma imagem/buffer em branco do tamanho da tela
image = Image.new("RGB", (disp.width, disp.height))
draw = ImageDraw.Draw(image)

# Preenche a tela com a cor verde para teste
draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=(0, 255, 0))
disp.image(image)

print("Tela preenchida de verde. Teste SPI e Python concluído com sucesso!")
```
