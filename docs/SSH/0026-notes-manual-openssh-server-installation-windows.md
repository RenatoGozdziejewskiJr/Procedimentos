# Notes about manual OpenSSH Server installation on Windows

[Português (Brasil)](0026-notas-instalacao-manual-servidor-openssh-windows-pt-br.md)

This guide describes how to install the OpenSSH Server manually on Windows 11 using Microsoft's official repository, and how to configure public keys for passwordless access.

## 1. Download the official package

1. Go to the project's official releases page on GitHub:
   [PowerShell/Win32-OpenSSH Releases](https://github.com/powershell/win32-openssh/releases)
2. Find the latest stable version.
3. Under **Assets**, download the 64-bit archive:
   `OpenSSH-Win64.zip`

## 2. Extract and place the files

1. Open the downloaded `.zip` file and extract all its contents.
2. Rename the extracted folder to `OpenSSH`.
3. Move that folder to the system's default programme directory:
   `C:\Program Files\OpenSSH`

## 3. Run the installation script

1. Right-click the Start menu and select **Terminal (Administrator)** or **PowerShell (Administrator)**.
2. Navigate to the folder where the files were moved:
   ```powershell
   cd "C:\Program Files\OpenSSH"
   ```
3. Run the official installation script included in the package:
   ```powershell
   .\install-sshd.ps1
   ```
4. Confirm that the message returned in the console indicates that installation succeeded.

## 4. Configure and start the service

Still in PowerShell with Administrator privileges, run the commands below to configure the service to start with Windows and start it immediately:

```powershell
# Define a inicialização do serviço como Automática
Set-Service -Name sshd -StartupType 'Automatic'

# Inicia o serviço do servidor OpenSSH
Start-Service sshd
```

## 5. Manually copy public keys (passwordless access)

The traditional Linux `ssh-copy-id` command fails when interacting with Windows because there is no native bash interpreter. Configure the key by inserting its public-key text directly on the destination host.

### 5.1 `authorized_keys` file format

The `authorized_keys` file must be a plain-text file **without an extension** (for example, not `.txt`). Each public key must occupy **exactly one complete line**. If you have keys from multiple computers, append each one on a separate line.

**Example file contents:**
```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK... usuario@computador1
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQ... usuario@computador2
```

### 5.2 Create the file and set permissions (standard user)

In PowerShell on the host, run the commands below to create the directory, insert the key and set the encoding. OpenSSH **rejects** files that are not in plain UTF-8 format (without a BOM):

```powershell
# 1. Create the .ssh directory in the current user's profile
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.ssh"

# 2. Create the authorized_keys file with your public key
# Replace 'your-public-key-here' with the contents of your .pub file
Set-Content -Path "$env:USERPROFILE\.ssh\authorized_keys" -Value "your-public-key-here"

# NOTE: To add secondary keys later without removing existing ones, use:
# Add-Content -Path "$env:USERPROFILE\.ssh\authorized_keys" -Value "your-second-public-key-here"

# 3. Força a codificação correta para UTF-8 sem BOM (Obrigatório para o OpenSSH aceitar)
[System.IO.File]::WriteAllLines("$env:USERPROFILE\.ssh\authorized_keys", [System.IO.File]::ReadAllLines("$env:USERPROFILE\.ssh\authorized_keys"))

# 4. Restrict access to the .ssh directory and key file
icacls "$env:USERPROFILE\.ssh" /inheritance:r /grant "$($env:USERNAME):F" /grant "NT AUTHORITY\SYSTEM:F"
icacls "$env:USERPROFILE\.ssh\authorized_keys" /inheritance:r /grant "$($env:USERNAME):F" /grant "NT AUTHORITY\SYSTEM:F"
```

## 6. Make critical changes to `sshd_config`

By default, Windows OpenSSH uses `C:\ProgramData\ssh\administrators_authorized_keys` for accounts in the Administrators group. Other accounts use the `authorized_keys` file in their profile. Keep strict permission checking enabled; do not set `StrictModes no`, which disables these checks.

To use the profile-based key file for an account in the Administrators group instead, edit the configuration file only if this is an intentional choice and the key file and `.ssh` directory have restrictive permissions:

1. Open **Notepad as Administrator**.
2. Open `C:\ProgramData\ssh\sshd_config`. *(Change Notepad's file filter to “All files” to find it.)*
3. Modify or add the directives below:

```text
# Go to the end of the file and COMMENT out the two lines below by adding '#' at the beginning.
# This makes administrator accounts use the authorized_keys file in their own profile.
#Match Group administrators
#    AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
```

4. Save the file and **restart the SSH service** in PowerShell to apply the changes:
```powershell
Restart-Service sshd
```

## 7. Configure Windows Firewall

For WinSCP or other clients to connect, the default port (`22`) must be allowed by inbound traffic rules.

Run this command in PowerShell as an Administrator to create the rule automatically:
```powershell
New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH SSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

## 8. Validate the installation

To confirm that the SSH server is active and responding on the local port, run:
```powershell
Test-NetConnection -ComputerName localhost -Port 22
```
The output should show the field `TcpTestSucceeded : True`.
