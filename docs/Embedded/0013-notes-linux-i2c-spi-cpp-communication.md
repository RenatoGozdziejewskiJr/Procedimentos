# Notes about I2C and SPI communication in Linux C++

[Português (Brasil)](./0013-notas-comunicacao-i2c-spi-cpp-linux-pt-br.md)

The Linux ecosystem follows the principle that **"everything is a file"**. This means complex hardware buses are exposed to the programmer as ordinary files in the `/dev` directory.

In theory, you can use the classic POSIX C/C++ operations — `open()`, `read()`, `write()`, and `close()` — to communicate with any hardware. However, the electrical and logical properties of I2C and SPI require different approaches when writing robust drivers.

---

## 1. I2C (TWI): the simplicity of `write()` and `read()`

The I2C (Inter-Integrated Circuit) bus is designed as a simplified local-network protocol.

*   **Half-duplex:** Communication uses a single data line (SDA). Either the master (Radxa) or the slave (display) transmits; they never transmit at the same time.
*   **Address-based:** There is no physical pin to "wake" the display. The master sends an address on the bus (for example, `0x3C`), and only the matching device responds.

### 1.1. Why is `write()` sufficient?
Because I2C operates in turns, using `write()` to send commands or pixels is natural and safe. The Linux kernel takes the byte array, prepends the I2C address to the packet, and handles transmission. To read a sensor, a simple `read()` performs the reverse operation.

---

## 2. SPI: the power and need for `ioctl`

SPI (Serial Peripheral Interface) is a very high-speed bus designed to move large amounts of data quickly. It has dedicated transmit (MOSI) and receive (MISO) pins.

Although it is technically possible to use `write()` on `/dev/spidevX.Y` (and it would even work for our receive-only display), the C++ engineering community has adopted `ioctl` (Input/Output Control) as the **official standard**. There are three critical reasons:

### 2.1. Full-duplex operation (simultaneous two-way communication)
SPI requires reads and writes to occur **on exactly the same clock pulse**. For each bit sent on MOSI, a bit is received on MISO.
*   If you use `write()`, the Linux kernel discards the hardware response.
*   If you use `read()`, the kernel sends zeroes (dummy data) over MOSI to generate the clock and read the response.
*   **The solution (`ioctl`):** The `spi_ioc_transfer` structure lets you provide two buffers at once (`tx_buf` and `rx_buf`). The kernel ensures simultaneous transfer, which is essential for complex sensors.

### 2.2. The risk of the CS (Chip Select) pin
Unlike I2C, SPI selects chips through a physical pin (CS). The specification requires CS to be pulled **LOW (0 V)** at the start of a transaction and returned **HIGH (3.3 V)** only when it ends.
*   If you send data with two consecutive `write()` calls (one for the command and one for the data), the kernel may deactivate CS (pull it HIGH) for a fraction of a second between the calls.
*   For many displays and flash memories, this "flicker" on CS means "operation aborted", causing the operation to fail.
*   **The solution (`ioctl`):** `ioctl` allows a vector of messages to be sent as a single operation. The kernel keeps CS LOW until every message in the transfer has been sent.

### 2.3. Precise per-message control
With `write()`, the hardware uses the default bus speed. SPI can, however, have devices with different speed requirements connected to the same wires.
*   **The solution (`ioctl`):** The `spi_ioc_transfer` structure lets you set the speed in hertz (`speed_hz`), word size (`bits_per_word`), and transmission-specific delays **for that transfer only**, without changing the global `/dev` configuration.

---

## 3. Summary
*   Use `write()` and `read()` for **I2C**. The protocol is turn-based, address-synchronised, and half-duplex.
*   Use `ioctl` with the `spi_ioc_transfer` structure for **SPI**. It provides precise Chip Select synchronisation, simultaneous read/write, and fine-grained real-time speed control.
