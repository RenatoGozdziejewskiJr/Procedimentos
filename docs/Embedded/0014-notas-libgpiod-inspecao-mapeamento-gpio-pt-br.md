# Notas sobre inspeção e mapeamento de pinos GPIO com libgpiod

[English](./0014-notes-libgpiod-gpio-inspection-mapping.md)

A `libgpiod` é a API oficial e moderna do kernel Linux para manipulação de GPIOs, substituindo o antigo e obsoleto sistema `sysfs` (`/sys/class/gpio`). Além das bibliotecas para C++ e Python, ela fornece utilitários de linha de comando essenciais para investigar o estado do hardware em tempo real.

## 1. Identificando os Controladores (`gpiodetect`)

O primeiro passo em qualquer placa nova é descobrir como o kernel agrupou os pinos. Em vez de adivinhar o nome do chip, usamos o comando de detecção.

**Comando:**

```bash
gpiodetect
```

**Exemplo de Saída (Radxa Cubie A7S):**

```text
gpiochip0 [2000000.pinctrl] (352 lines)
gpiochip1 [7025000.pinctrl] (64 lines)
```

> **Interpretação:** O sistema possui dois controladores. O `gpiochip0` é o controlador principal que gerencia as 352 linhas lógicas do processador Allwinner.

---

## 2. Inspecionando o Status dos Pinos (`gpioinfo`)

Com o nome do chip em mãos, podemos listar todos os pinos pertencentes a ele para descobrir seus nomes amigáveis (se houver), se são entradas ou saídas, e o mais importante: se estão bloqueados por outro hardware.

**Comando para listar todas as linhas de um chip específico:**

```bash
gpioinfo 0
```

*(Onde `0` representa o `gpiochip0`)*

**Comando para buscar linhas específicas (usando filtro `grep`):**

```bash
gpioinfo 0 | grep -E "line +(33|34):"
```

**Anatomia da Resposta:**

```text
line  33:      "PIN_11"       unused   input  active-high
line   2:      unnamed  "usb0-vbus"  output  active-high [used]
```

- **Nome do pino (ex.: `"PIN_11"` ou `unnamed`):** Rótulo amigável definido no Device Tree. Pinos roteados para os conectores externos geralmente recebem nomes, enquanto pinos de uso interno do processador ficam como `unnamed`.
- **Consumidor (ex.: `"usb0-vbus"`):** Se o pino estiver em uso, o kernel informa qual driver ou processo é dono dele no momento.
- **Status de bloqueio (`[used]` ou `unused`):**
	- `unused`: o pino está livre e pode ser requisitado pelo seu código Python/C++.
	- `[used]`: o pino está bloqueado pelo kernel, por exemplo, quando ativado via overlay no `rsetup`. Se o código tentar acessá-lo, o sistema retornará um erro (`Errno 22 - Invalid argument`).



---

## 3. A Fórmula de Mapeamento (Processadores Allwinner)

Quando você sabe o nome técnico do pino (ex: `PB1`), mas o kernel o lista apenas por números lógicos no `gpiochip0`, é necessário usar a fórmula universal de indexação para encontrar a linha correta.

**A Fórmula:**

> **Índice da Linha = (Índice do Banco x 32) + Número do Pino**

**Tabela de Índices de Banco:**

| Letra do Banco | Índice Numérico |
| --- | --- |
| PA | 0 |
| PB | 1 |
| PC | 2 |
| PD | 3 |
| PE | 4 |
| PF | 5 |

**Exemplo Prático (Encontrando o Pino PB1):**

- Banco: **B** (índice 1)
- Pino: **1**
- Cálculo: `(1 x 32) + 1 = 33`
- **Resultado:** o pino PB1 corresponde à **linha 33** do `gpiochip0`.

---

## 4. Requisitando Pinos no Código

Sabendo o mapeamento e garantindo que o pino está `unused`, você pode requisitá-lo no seu código de duas maneiras:

> **Nota sobre a versão da API:** Os exemplos `find_line()` e `get_line()` abaixo usam a API legada de linhas da libgpiod 1.x. A libgpiod 2.x usa a API de requisição de linhas. Verifique a versão instalada e use a API correspondente; a versão da ABI de dispositivos de caractere GPIO do kernel é uma questão separada.

**Busca por Nome (Recomendada):**
Utilize caso o `gpioinfo` tenha mostrado um rótulo amigável. É mais seguro contra mudanças de arquitetura.

- **Python:** `self.chip.find_line("PIN_11")`
- **C++:** `chip.find_line("PIN_11")`

**Busca por Índice (Fallback Matemático):**
Utilize caso o pino seja listado como `unnamed`.

- **Python:** `self.chip.get_line(33)`
- **C++:** `chip.get_line(33)`

> **Dica de prevenção de erros:** Ao requisitar um pino de saída (`DIRECTION_OUTPUT`), sempre defina um valor padrão inicial (`default_val`). Versões mais recentes da arquitetura ABI v2 do kernel exigem que o estado elétrico inicial seja declarado no momento da posse; caso contrário, rejeitarão a requisição.
