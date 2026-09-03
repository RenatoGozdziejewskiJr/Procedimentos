# Plano de Integração Final: Display OLED I2C (SSD1306) na Radxa Cubie A7S

Este documento detalha o plano para conectar e programar um display OLED I2C (SSD1306) no barramento TWI2 da placa Radxa Cubie A7S.

## 1. Conexões Físicas (Header 30 Pinos)

| Pino do Display | Radxa Cubie A7S (Header 30 Pinos) | Função na Placa    |
| :-------------- | :-------------------------------- | :----------------- |
| **GND**         | **Pino 6**                        | GND (Terra)        |
| **VCC**         | **Pino 1**                        | 3.3V (Alimentação) |
| **SCL / SCK**   | **Pino 28**                       | TWI2-SCK           |
| **SDA**         | **Pino 27**                       | TWI2-SDA           |

---

## 2. Configuração do SO (`rsetup`)

1. No terminal, execute `rsetup`.
2. Vá em **Overlays**.
3. Marque a opção: `[*] Enable TWI2` e reinicie a placa.
4. Teste com `sudo i2cdetect -y 2` (O endereço `3c` deve aparecer sem travamentos).

---

## 3. Implementação em Python

**Instalação de Dependências:**

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-smbus i2c-tools python3-dev
pip3 install adafruit-blinka adafruit-circuitpython-ssd1306 pillow
Script de Teste (oled_test.py):

Python
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw

i2c = busio.I2C(board.SCL, board.SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

disp.fill(0)
disp.show()

image = Image.new("1", (disp.width, disp.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, disp.width - 1, disp.height - 1), outline=255, fill=0)
draw.text((10, 25), "Radxa A7S - I2C!", fill=255)

disp.image(image)
disp.show()
4. Implementação em C++
Em C++, utilizamos a API direta do kernel (<linux/i2c-dev.h>), dispensando configurações manuais de pinos. O código interage puramente com o arquivo /dev/i2c-2.
(Consulte a versão anterior do plano para a listagem completa da classe C++ para o SSD1306).
```
