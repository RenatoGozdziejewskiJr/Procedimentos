# Notes about creating and managing systemd services on Linux

[Português (Brasil)](./0018-notas-criacao-gerenciamento-servicos-systemd-pt-br.md)

This guide is for beginners and explains how to create, configure, and manage services that start automatically on Linux using **systemd** and the **systemctl** utility.

---

## 1. What are systemd and systemctl?

- **systemd:** The default init system and service manager in most modern Linux distributions (Debian, Ubuntu, CentOS, Fedora, Arch, Radxa OS, Raspberry Pi OS). It is the first process to run (`PID 1`) and acts as the operating system’s "conductor", controlling what starts, stops, or restarts.
- **systemctl:** The terminal command used to interact with and control `systemd` (start, stop, enable at boot, view logs, and so on).

---

## 2. Anatomy of a service file (`.service`)

System service files are stored in this directory:
```text
/etc/systemd/system/nome-do-servico.service
```

A `.service` file is divided into three main sections (`[Unit]`, `[Service]`, and `[Install]`):

```ini
[Unit]
Description=Meu Servico Personalizado
After=network.target

[Service]
Type=simple
User=radxa
WorkingDirectory=/home/radxa/meu-projeto
ExecStart=/usr/bin/python3 /home/radxa/meu-projeto/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 2.1. What each section means:

#### 2.1.1. `[Unit]` (metadata and dependencies)
- **`Description=`**: A human-readable service description shown in logs and by the status command.
- **`After=`**: Sets start-up ordering; it does not by itself ensure that a dependency is fully ready. For example, `After=network.target` does not guarantee network connectivity. If a service requires the network to be online, use `Wants=network-online.target` together with `After=network-online.target`, and ensure the distribution's wait-online service is enabled.

#### 2.1.2. `[Service]` (how the program runs)
- **`Type=`**:
  - `simple` (default): For processes that run continuously in the foreground (for example, web servers, scripts in a loop, and bots).
  - `forking`: For programs that start and create a child process in the background (for example, TigerVNC and classic Nginx).
  - `oneshot`: For tasks that run a quick command, finish, and do not need to remain running (for example, backup or cleanup scripts).
- **`User=` and `Group=`**: Set the Linux user that runs the command (avoid running as `root` unless strictly necessary).
- **`WorkingDirectory=`**: The directory in which the command runs (equivalent to running `cd` first).
- **`ExecStart=`**: The exact command that starts the program. **Important:** Always use absolute executable paths (for example, `/usr/bin/python3` instead of just `python3`).
- **`Restart=`**:
  - `always`: If the program crashes or exits unexpectedly, systemd restarts it automatically.
  - `on-failure`: Restarts only if the program exits with an error code.
- **`RestartSec=`**: Number of seconds to wait before attempting a restart.

#### 2.1.3. `[Install]` (how the service is enabled at boot)
- **`WantedBy=multi-user.target`**: Specifies that the service should start in the system’s standard operating mode (text/graphical mode with networking).

---

## 3. Step by step: creating a service from scratch

This example creates a script that writes the date and time to a file every 10 seconds.

### 3.1. Step 1: Create the script
Create a script at `/home/radxa/meu_script.sh`:

```bash
#!/bin/bash
while true; do
    echo "Servico rodando em: $(date)" >> /home/radxa/servico.log
    sleep 10
done
```

Make it executable:
```bash
chmod +x /home/radxa/meu_script.sh
```

### 3.2. Step 2: Create the systemd service file
Open the `nano` editor with superuser privileges:

```bash
sudo nano /etc/systemd/system/meu-script.service
```

Paste in the following content:

```ini
[Unit]
Description=Script de Exemplo para Aprendizado
After=network.target

[Service]
Type=simple
User=radxa
ExecStart=/bin/bash /home/radxa/meu_script.sh
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```
Save (`Ctrl + O`, `Enter`) and exit (`Ctrl + X`).

### 3.3. Step 3: Reload systemd
Whenever you create or modify a `.service` file, you **must** notify systemd:

```bash
sudo systemctl daemon-reload
```

### 3.4. Step 4: Start and enable at boot
- **Start immediately:**
  ```bash
  sudo systemctl start meu-script.service
  ```
- **Enable it to start automatically when the board powers on:**
  ```bash
  sudo systemctl enable meu-script.service
  ```
- *(Tip: You can combine the two commands with `sudo systemctl enable --now meu-script.service`.)*

---

## 4. What does the `@` symbol mean in services (template services)?

You may have seen services with `@`, such as `tigervncserver@:1.service` or `openvpn@client.service`.

- `@` indicates that the file is a **template**.
- The file on disk is named `tigervncserver@.service`.
- The value after `@` (such as `:1` or `meu-cliente`) is passed to the service as the **`%i`** or **`%I`** variable.
- **Benefit:** This allows dynamic instances to be created without duplicating service files. For example:
  - `tigervncserver@:1.service` runs for display `:1`.
  - `tigervncserver@:2.service` runs for display `:2`.

---

## 5. Essential `systemctl` commands

| Action | Command | Description |
| :--- | :--- | :--- |
| **Reload definitions** | `sudo systemctl daemon-reload` | Reloads new or modified `.service` files |
| **Start** | `sudo systemctl start nome.service` | Starts the service now |
| **Stop** | `sudo systemctl stop nome.service` | Stops the service |
| **Restart** | `sudo systemctl restart nome.service` | Stops and starts the service again |
| **Check status** | `sudo systemctl status nome.service` | Shows whether it is running (`active`), its PID, and recent logs |
| **Enable at boot** | `sudo systemctl enable nome.service` | Starts the service automatically at boot |
| **Disable at boot** | `sudo systemctl disable nome.service` | Removes the service from automatic startup |
| **Enable and start** | `sudo systemctl enable --now nome.service` | Performs both actions in one command |
| **Check whether active** | `systemctl is-active nome.service` | Returns `active` or `inactive` (useful in scripts) |
| **Check whether enabled at boot**| `systemctl is-enabled nome.service` | Returns `enabled` or `disabled` |

---

## 6. Diagnosing problems and viewing logs (`journalctl`)

When a service fails to start (`Active: failed`), `journalctl` is the best tool for finding out what went wrong:

- **View the service logs in real time:**
  ```bash
  journalctl -u nome.service -f
  ```
- **View the latest log lines without a pager:**
  ```bash
  journalctl -u nome.service -e --no-pager
  ```
- **View logs from the current boot only:**
  ```bash
  journalctl -u nome.service -b
  ```

---

## 7. Best practices and important precautions

1. **Absolute paths:** In `ExecStart=`, never use relative commands such as `python main.py`. Use `/usr/bin/python3 /home/usuario/main.py`. Find an executable path with `which python3` or `which node`.
2. **File permissions:** Make sure the user specified in `User=` can read and execute the referenced scripts and directories.
3. **Infinite crash loop:** When using `Restart=always`, always set `RestartSec=5` to prevent systemd from trying to restart the program hundreds of times per second if the code contains a fatal syntax error.
