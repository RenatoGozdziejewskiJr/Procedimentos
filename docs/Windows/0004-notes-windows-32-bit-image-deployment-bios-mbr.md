# Notes about Writing a 32-bit Windows Image (BIOS / MBR Mode)

[Português (Brasil)](0004-notas-gravacao-imagem-windows-32-bits-bios-mbr-pt-br.md)

This procedure is **required** when the host performing the process is 64-bit and the image to be written is **32-bit**. It also addresses the technical limitation that 64-bit UEFI firmware cannot boot 32-bit operating systems.

## 1. Requirements

- A 32-bit Windows image (`.win` or `.wim`).
- A blank SSD.
- A motherboard with CSM (Compatibility Support Module) support enabled, such as the Advantech AIMB-216.

## 2. Partitioning the SSD (Diskpart)

In Command Prompt (cmd) as Administrator, run `diskpart` and enter the commands in sequence to create a classic MBR partition table.

**Warning:** Before running `clean`, use `list disk` to confirm that the target disk is disk 0.

```cmd
diskpart
select disk 0
clean
convert mbr
create partition primary size=100
format quick fs=ntfs label="System"
assign letter="S"
active
create partition primary
format quick fs=ntfs label="Windows"
assign letter="W"
exit
```

**Critical note:** The `active` command is essential for MBR partitioning because it indicates to the BIOS which partition contains the boot loader.

## 3. Applying the Image (DISM)

Apply the Windows image to the main partition (`W:`). Replace `D:\sua_imagem.win` with the correct path to the image file.

```cmd
dism /Apply-Image /ImageFile:D:\sua_imagem.win /Index:1 /ApplyDir:W:
```

## 4. Configuring Boot (Bcdboot)

Because the image is 32-bit and the current host is 64-bit, force generation of the classic Legacy/BIOS boot files with the appropriate parameter:

```cmd
bcdboot W:\Windows /s S: /f BIOS
```

## 5. Required BIOS Configuration (AIMB-216 Board)

The Advantech system will not boot the newly created MBR disk until legacy support is enabled.

1. Power on the equipment and press **<Del>** during POST to access BIOS Setup.
2. Use the arrow keys to navigate to the **Advanced** tab and select **Compatibility Support Module Configuration**.
3. Press Enter on **CSM Support** and change the value to **Enabled**.
4. Find **Boot Options Filter** and set it to prioritise **Legacy ROM**.
5. Press **<F10>** to save the changes and restart the equipment.
