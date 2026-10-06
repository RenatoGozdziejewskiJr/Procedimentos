# Notes about configuring and operating OverlayRoot on the Radxa A7S

[Português (Brasil)](./0015-notas-overlayroot-radxa-a7s-pt-br.md)

## 1. Recommended configuration order
To avoid problems, configure `overlayroot` **last**, once the device is ready for production. Follow this order:
1. Partition the disk (SD card, SSD, or hard drive).
2. Create the mount-point directories.
3. Configure `/etc/fstab` with security options (`noexec`).
4. Install and test your program (on the system partition).
5. Install and enable `overlayroot`.

## 2. Partitioning and formatting (Windows 11 + WSL + GParted)
Native Windows cannot manage `ext4` partitions (the Linux standard). Use WSL to access and resize the disk.

1. Open PowerShell as Administrator in Windows and install the USB manager:
   `winget install --interactive --exact dorssel.usbipd-win`
2. List the USB devices and note the card reader/hard drive "BUSID":
   `usbipd list`
3. Share the device and attach it to WSL:
   `usbipd bind --busid <BUSID>`
   `usbipd attach --wsl --busid <BUSID>`
4. Open your WSL terminal (for example, Ubuntu) and install GParted:
   `sudo apt update && sudo apt install gparted`
5. Launch the graphical GParted application:
   `sudo gparted`
6. **In GParted:**
- Select the correct disk in the upper-right corner.
- Right-click the main partition and select **“Resize/Move”**.
- Reduce it to create unallocated space.
- Right-click the free space and select **“New”**.
- Set the file system to `ext4` and add the partition.
- Click the green “Apply” (tick) icon to write the changes.

## 3. Understanding mount points and fstab
Linux has no drive letters such as `D:` or `E:`. Create an ordinary directory anywhere in the system and use `/etc/fstab` (File System Table) to tell Linux to “attach” a physical partition to that directory during boot.

When you create a directory (for example, `mkdir /dados`), it resides on the main partition. When the new/external partition is mounted there, the directory becomes a direct "window" into the other disk. Anything written there is physically stored on the new partition.

## 4. Configuring a persistent, secure mount (fstab)
After returning the partitioned disk to the Radxa and powering it on:

1. Identify the exact name of the new partition you created:
   `lsblk` (This lists all disks; for example, `/dev/mmcblk0p3`).
2. Create the directory where your program will write data:
   `mkdir -p /home/radxa/meu_programa/dados`
3. Edit the fstab file:
   `sudo nano /etc/fstab`
4. Add the following line at the end of the file (applying the `noexec` security option):
   `/dev/mmcblk0p3  /home/radxa/meu_programa/dados  ext4  defaults,noexec  0  2`
   * **Column 1:** Physical device.
   * **Column 2:** Directory path (mount point).
   * **Column 3:** File system (`ext4`).
   * **Column 4 (options):** `defaults` (standard read/write) + `noexec` (prevents programs from being executed from this partition, improving security).
   * **Column 5:** Dump (use `0`).
   * **Column 6:** File-system check order (`2` for secondary partitions).
5. Save (`Ctrl+O`, `Enter`) and exit (`Ctrl+X`).
6. Test that the configuration works:
   `sudo mount -a`
7. Reboot the board to ensure that the partition is mounted automatically.

## 5. OverlayFS and overlayroot concepts
`overlayroot` stacks two layers:
1. **Lowerdir:** The real physical disk (protected as read-only).
2. **Upperdir:** A virtual layer in RAM (`tmpfs`).

Writes made outside the data partitions go to RAM and are lost on reboot. Because the data directory is configured in fstab, writes there bypass the overlay and go to the physical disk.

## 6. Installing and enabling overlayroot
1. `sudo apt update`
2. `sudo apt install overlayroot`
3. `sudo nano /etc/overlayroot.conf`
4. Change `overlayroot=""` to `overlayroot="tmpfs"`
5. Reboot the Radxa: `sudo reboot`

## 7. Architecture and update best practices
**Where should the executable be kept?**
To make the industrial machine resilient to power failures and data corruption, the program executable **must remain on the main partition** (which is frozen by `overlayroot`). Only logs, databases, and reports should be stored in the `/dados` directory.

Because the data partition is mounted with the `noexec` flag in fstab, no malicious or corrupted file can be executed from it.

**To update the executable remotely (WinSCP + SSH):**
1. Send the new executable to the Radxa via WinSCP (it will land in RAM).
2. In the terminal, unlock the hidden original physical disk:
   `sudo mount -o remount,rw /media/root-ro`
3. Copy the executable into the real physical system:
   `sudo cp /home/radxa/novo_executavel /media/root-ro/home/radxa/meu_programa/executavel_principal`
4. Lock the system as read-only again:
   `sudo mount -o remount,ro /media/root-ro`
