# Notes about GPIO inspection and pin mapping with libgpiod

[Português (Brasil)](./0014-notas-libgpiod-inspecao-mapeamento-gpio-pt-br.md)

`libgpiod` is the official modern Linux kernel API for GPIO access, replacing the old, obsolete `sysfs` system (`/sys/class/gpio`). Alongside its C++ and Python libraries, it provides essential command-line utilities for inspecting hardware state in real time.

## 1. Identifying controllers (`gpiodetect`)

On a new board, first find out how the kernel has grouped the pins. Use the detection command rather than guessing the chip name.

**Command:**

```bash
gpiodetect
```

**Example output (Radxa Cubie A7S):**

```text
gpiochip0 [2000000.pinctrl] (352 lines)
gpiochip1 [7025000.pinctrl] (64 lines)
```

> **Interpretation:** The system has two controllers. `gpiochip0` is the main controller and manages the Allwinner processor’s 352 logical lines.

---

## 2. Inspecting pin status (`gpioinfo`)

Once you know the chip name, list all its pins to find their friendly names (if any), whether they are inputs or outputs, and—most importantly—whether other hardware has claimed them.

**Command to list every line on a specific chip:**

```bash
gpioinfo 0
```

*(`0` represents `gpiochip0`.)*

**Command to search for specific lines (using the `grep` filter):**

```bash
gpioinfo 0 | grep -E "line +(33|34):"
```

**Reading the output:**

```text
line  33:      "PIN_11"       unused   input  active-high
line   2:      unnamed  "usb0-vbus"  output  active-high [used]
```

- **Pin name (for example, `"PIN_11"` or `unnamed`):** A friendly label defined in the Device Tree. Pins routed to external connectors are generally named, while pins used internally by the processor are shown as `unnamed`.
- **Consumer (for example, `"usb0-vbus"`):** If a pin is in use, the kernel reports which driver or process currently owns it.
- **Claim status (`[used]` or `unused`):**
	- `unused`: the pin is free and can be requested by your Python/C++ code.
	- `[used]`: the pin has been claimed by the kernel, for example, by an overlay enabled in `rsetup`. Attempting to access it from code returns an error (`Errno 22 - Invalid argument`).



---

## 3. The mapping formula (Allwinner processors)

When you know a pin’s technical name (for example, `PB1`) but the kernel lists only its logical number on `gpiochip0`, use the universal indexing formula to find the corresponding line.

**Formula:**

> **Line index = (bank index x 32) + pin number**

**Bank index table:**

| Bank letter | Numeric index |
| --- | --- |
| PA | 0 |
| PB | 1 |
| PC | 2 |
| PD | 3 |
| PE | 4 |
| PF | 5 |

**Worked example (finding pin PB1):**

- Bank: **B** (index 1)
- Pin: **1**
- Calculation: `(1 x 32) + 1 = 33`
- **Result:** pin PB1 corresponds to **line 33** on `gpiochip0`.

---

## 4. Requesting pins in code

Once you know the mapping and have confirmed that the pin is `unused`, you can request it in code in either of two ways:

> **API version note:** The `find_line()` and `get_line()` examples below use the legacy libgpiod 1.x line API. Libgpiod 2.x uses the line-request API instead. Check the installed library version and use the matching API; the kernel GPIO character-device ABI version is a separate concern.

**Search by name (recommended):**
Use this when `gpioinfo` shows a friendly label. It is more robust against architectural changes.

- **Python:** `self.chip.find_line("PIN_11")`
- **C++:** `chip.find_line("PIN_11")`

**Search by index (mathematical fallback):**
Use this when the pin is listed as `unnamed`.

- **Python:** `self.chip.get_line(33)`
- **C++:** `chip.get_line(33)`

> **Tip to prevent errors:** When requesting an output pin (`DIRECTION_OUTPUT`), always set an initial default value (`default_val`). Newer kernel ABI v2 versions require the initial electrical state to be declared when the pin is claimed; otherwise, the request is rejected.
