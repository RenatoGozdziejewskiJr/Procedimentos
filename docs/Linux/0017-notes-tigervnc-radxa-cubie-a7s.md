# Notes about configuring the TigerVNC server on the Radxa Cubie A7S

[Português (Brasil)](./0017-notas-tigervnc-radxa-cubie-a7s-pt-br.md)

This procedure explains how to install and configure the VNC server (**TigerVNC**) on the **Radxa Cubie A7S**, allowing the graphical desktop to be controlled remotely over the local network, based on the official Radxa documentation.

---

## 1. Prerequisites

- A **Radxa Cubie A7S** with an operating system and graphical environment installed (for example, Radxa OS with KDE Plasma).
- Access to the Radxa terminal (directly through the console or via SSH).
- Both devices (the client computer and the Radxa) connected to the same local network.
- To access the remote desktop from the client computer, use a VNC client of your choice, such as **TigerVNC Viewer** or **RealVNC Viewer**.

---

## 2. Installing the VNC server

Open a terminal on the Radxa A7S and install the required packages:

```bash
sudo apt update
sudo apt install tigervnc-standalone-server tigervnc-common -y
```

---

## 3. Setting the remote-access password

Set the password that will be requested when connecting over VNC:

```bash
vncpasswd
```

- Enter and confirm the password (the characters will not be displayed).
- When asked whether to create a *view-only password*:
  ```text
  Would you like to enter a view-only password (y/n)? n
  ```
Enter `n` and press Enter.

---

## 4. Configuring the VNC startup file (`xstartup`)

Create and edit `~/.vnc/xstartup` to define the graphical desktop environment to load:

1. Open the file with the `nano` editor:

```bash
nano ~/.vnc/xstartup
```

2. Add the following content:

```bash
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
export XDG_SESSION_TYPE=x11
export DESKTOP_SESSION=plasma
exec startplasma-x11
```

3. Save the file (`Ctrl + O`, `Enter`) and exit (`Ctrl + X`).

4. Make the file executable:

```bash
chmod +x ~/.vnc/xstartup
```

---

## 5. Managing the VNC server

### 5.1. Starting the VNC server
To start the server and allow remote connections from other devices on the network, use the `-localhost no` parameter:

```bash
vncserver -localhost no
```

After startup, the terminal displays the display number and port in use (by default, display `:1` on port `5901`):
```text
New Xtigervnc server 'radxa:1 (radxa)' on port 5901 for display :1.
```

### 5.2. Checking active-session status
To list running VNC sessions:

```bash
vncserver -list
```

The output shows the display identifier (`X DISPLAY #`), port (`RFB PORT #`), and process ID.

### 5.3. Stopping the VNC server
To end a specific session, provide the display number (for example, `:1`):

```bash
vncserver -kill :1
```

---

## 6. Connecting from a VNC client

1. Open a VNC client on the remote computer (**RealVNC Viewer** or **TigerVNC Viewer**).
2. In the address/server field, enter the Radxa IP address followed by the display number or port:
   - Example: `<IP_DO_RADXA>:1` or `<IP_DO_RADXA>:5901`
3. Connect and enter the password created in **Step 3**.

---

## 7. Tips and troubleshooting

- **Black screen when connecting over VNC:**
If the screen is black after authentication, check whether **auto-login** is enabled. If so, disable it in the Radxa system settings to avoid session conflicts with the X server.
- **Ports and displays:**
Each VNC session uses a port based on `5900 + display number` (for example, `:1` = `5901`, `:2` = `5902`).

---

## 8. Automatic startup at boot (systemd)

For devices running *headless* (without a monitor), the recommended method integrated with current TigerVNC versions on Debian/Ubuntu is to use the native `tigervncserver@.service`.

This starts the VNC server automatically at system boot, without requiring a prior manual SSH connection.

---

### 8.1. Configuration steps

#### 8.1.1. Assigning a display to a user
Edit the global user-assignment file `/etc/tigervnc/vncserver.users`:

```bash
sudo nano /etc/tigervnc/vncserver.users
```

Add the following line to map display `:1` to your user (replace `radxa` with your actual username if it differs):
```text
:1=radxa
```
Save with `Ctrl + O`, `Enter`, and exit with `Ctrl + X`.

#### 8.1.2. Configuring user session parameters
Create or edit `~/.vnc/config` in the user’s directory:

```bash
nano ~/.vnc/config
```

Add the environment, resolution, and network-access settings:
```text
session=plasma
geometry=1280x720
localhost=0
```

> **Performance tip:** A resolution of `1280x720` (HD) or `1366x768` provides a smoother experience and reduces CPU/RAM usage and board temperature compared with `1920x1080` (Full HD). If you need more screen space, change it to `1920x1080`.

#### 8.1.3. Enabling and starting the service at boot
Reload the systemd manager and enable the service (note the colon `:` before the 1):

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now tigervncserver@:1.service
```

#### 8.1.4. Checking the service status
Confirm that the service is active and running:

```bash
sudo systemctl status tigervncserver@:1.service
```

To inspect logs in real time for diagnostics:
```bash
journalctl -u tigervncserver@:1.service -e --no-pager
```

#### 8.1.5. Stopping or restarting the service (when required)
- To restart: `sudo systemctl restart tigervncserver@:1.service`
- To stop: `sudo systemctl stop tigervncserver@:1.service`
- To disable startup at boot: `sudo systemctl disable tigervncserver@:1.service`
