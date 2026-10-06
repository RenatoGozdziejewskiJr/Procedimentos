# Notes about disabling SSH password authentication

[Português (Brasil)](0027-notas-remocao-senha-autenticacao-ssh-pt-br.md)

This procedure explains how to disable password authentication over SSH, allowing access **only** with SSH keys (which increases security).

> **Warning:** Before proceeding, make sure your SSH key is configured and tested. Otherwise, you will lose access to the server.

## 1. Connect to the Raspberry Pi

Connect over SSH as usual (now without a password, using your key):

```bash
ssh engenharia@renato-pi
```

## 2. Edit the SSH configuration

Open the main SSH server configuration file on your Raspberry Pi with Administrator privileges:

```bash
sudo nano /etc/ssh/sshd_config
```

## 3. Disable password logins

In the file, scroll down to the line for `PasswordAuthentication`.

Do the following:
1. Remove the `#` at the beginning of the line to uncomment and enable it.
2. Change the value from `yes` to `no`.

The line should read exactly:

```text
PasswordAuthentication no
```

## 4. Save and exit

If you are using the `nano` editor:
- Press `Ctrl + O` to save the file (confirm by pressing `Enter`).
- Press `Ctrl + X` to exit the editor.

## 5. Restart the SSH service

Restart the SSH service so that the Raspberry Pi applies the new security setting:

```bash
sudo systemctl restart ssh
```
