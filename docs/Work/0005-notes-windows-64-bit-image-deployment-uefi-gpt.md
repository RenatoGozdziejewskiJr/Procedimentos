# Notes about Writing a 64-bit Windows Image (UEFI / GPT Mode)

[Português (Brasil)](0005-notas-gravacao-imagem-windows-64-bits-uefi-gpt-pt-br.md)

This procedure is suitable for **64-bit** Windows images and takes advantage of the native UEFI architecture of the Advantech AIMB-216 board.

## 1. Requirements

- A 64-bit Windows image (`.win` or `.wim`).
- A 64-bit host (the computer on which the procedure is run).
- A blank SSD.

## 2. Partitioning the SSD (Diskpart)

In Command Prompt (cmd) as Administrator, run `diskpart` and enter the commands in sequence.

**Warning:** Before running `clean`, use `list disk` to confirm that the target disk is disk 0.

```cmd
diskpart
select disk 0
clean
convert gpt
create partition efi size=100
format quick fs=fat32 label="System"
assign letter="S"
create partition msr size=16
create partition primary
format quick fs=ntfs label="Windows"
assign letter="W"
exit
```

## 3. Applying the Image (DISM)

Apply the Windows image to the main partition (`W:`). Replace `D:\sua_imagem.win` with the correct path to the image file.

```cmd
dism /Apply-Image /ImageFile:D:\sua_imagem.win /Index:1 /ApplyDir:W:
```

## 4. Configuring Boot (Bcdboot)

Generate the boot files on the EFI partition (`S:`):

```cmd
bcdboot W:\Windows /s S: /f UEFI
```

**Tip:** If copying fails because of the locale, force the language with the `/l pt-br` or `/l en-us` parameter.

## 5. BIOS Configuration (AIMB-216 Board)

For optimal startup in UEFI mode:

1. Power on the equipment and press **<Del>** during startup (POST) to access BIOS Setup.
2. Ensure that the boot priority on the Boot tab is set to the **Windows Boot Manager** partition.
3. Press **<F10>** to save the changes and exit.
