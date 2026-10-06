# Notes about SSH key generation

[Português (Brasil)](0025-notas-geracao-chaves-ssh-pt-br.md)

This guide explains how to generate an SSH key pair on your computer and configure it on a Raspberry Pi for passwordless access.

## 1. Generate the key pair

Open your computer's terminal (Windows, Mac or Linux) and enter the following command:

```bash
ssh-keygen -t ed25519
```

The terminal will ask where to save the key and whether to add a passphrase. Press **Enter** to accept the default file location, then set and confirm a strong passphrase. Leaving the passphrase empty reduces protection if someone obtains the private key.

## 2. Send the public key to the Raspberry Pi

Now send the public key (the “padlock”) to the Raspberry Pi. The command depends on your operating system.

### 2.1 Mac, Linux or Git Bash on Windows

```bash
ssh-copy-id pi@raspberrypi
```
*(Replace `pi@raspberrypi` with your username and IP address, or your Tailscale IP address if applicable.)*

If you generated the key on Windows and are sending it through WSL:

```bash
ssh-copy-id -i /mnt/c/Users/WINDOWS_USERNAME/.ssh/id_ed25519.pub engenharia@renato-pi
```

> **Note:** You will be asked for your password one last time to install the key on the server.

### 2.2 Command Prompt (CMD) or PowerShell on Windows

As Windows does not include the `ssh-copy-id` command natively, copy and paste the following command (replacing `pi@raspberrypi` with your username and IP address):

```cmd
type %USERPROFILE%\.ssh\id_ed25519.pub | ssh pi@raspberrypi "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## 3. Test the connection

Try connecting again from your computer's terminal:

```bash
ssh pi@raspberrypi
```

If everything has worked, you will go straight to the Raspberry Pi terminal without being prompted for a password.

Another example of a connection specifying the key path:

```bash
ssh -i /mnt/c/Users/WINDOWS_USERNAME/.ssh/id_ed25519 engenharia@renato-pi
```

## 4. Copy the Windows key to WSL

### 4.1 Copy the key to the native WSL directory

In the WSL terminal, enter the following command to copy the key from the Windows C drive to the hidden `.ssh` directory in your virtual Linux environment:

```bash
cp /mnt/c/Users/WINDOWS_USERNAME/.ssh/id_ed25519 ~/.ssh/
```

### 4.2 Set the key permissions

Tell Linux that only you may read this file by running:

```bash
chmod 600 ~/.ssh/id_ed25519
```

### 4.3 Test simplified access

As the key is now in Linux's standard, secure location (`~/.ssh/`), you no longer need to specify the full path. Enter:

```bash
ssh engenharia@renato-pi
```
