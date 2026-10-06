# Notes about Migrating from Docker Desktop to Podman

[Português (Brasil)](0009-notas-migracao-docker-para-podman-pt-br.md)

This guide documents the steps for replacing Docker Desktop with Podman Desktop on Windows while retaining full compatibility with VS Code Dev Containers through WSL 2.

## 1. Uninstalling Docker Desktop

Remove Docker Desktop before starting to avoid port conflicts, background services and, particularly, socket-mapping conflicts.

- Close Docker Desktop completely.
- In **Windows Settings > Apps > Installed apps**, uninstall **Docker Desktop**.
- Optionally, restart the computer to ensure that all services and virtual network interfaces have been released.

## 2. Installing and Configuring Podman Desktop

1. Download and install **Podman Desktop** for Windows.
2. During the initial setup, initialise **Podman Machine** (the virtual machine that runs the engine) and ensure that WSL integration is enabled.
3. In Podman Desktop, go to **Settings > Preferences**.
4. Find **Docker Socket Compatibility** and enable it. This redirects the standard Docker socket to Podman's socket, allowing third-party tools to continue working without modification.
5. Confirm that Podman Machine has **Running** status in the main panel.

## 3. Installing `podman-compose` in WSL

To orchestrate multiple containers and interpret compose files, install `podman-compose` directly in your Linux distribution (WSL) using its native package manager.

Open your WSL terminal and run:

```bash
sudo apt-get update
sudo apt-get install podman-compose
```

## 4. Configuring VS Code

For the *Dev Containers* extension to use the Podman engine and avoid forcing graphical integrations (WSLg) that cause permission errors in *rootless* mode, adjust the settings.

Open the VS Code `settings.json` file and add or update these keys:

```json
{
  "dev.containers.dockerComposePath": "podman-compose",
  "dev.containers.dockerPath": "podman",
  "dev.containers.mountWaylandSocket": false
}
```

> **Architecture note:** `mountWaylandSocket: false` is crucial. It prevents permission failures when attempting to mount the host's Wayland socket inside the rootless container. Graphical applications for debugging will be displayed using an X server (X11) running on the Windows host, so WSLg Wayland is not required inside the container.

## 5. Project File Compatibility (No Changes)

No changes to your project files are required for this migration. Keep these files unchanged:

- `Dockerfile`
- `docker-compose.yaml` (or `.yml`)
- `.devcontainer/devcontainer.json`

The Podman engine acts as a drop-in replacement and is 100% compatible with the OCI specification. This allows your environment to run in Podman while other team members continue to use Docker Desktop in the same repositories without conflicts.

## 6. Recommended Extra Step: Creating WSL Terminal Aliases

To make day-to-day use easier, add aliases to your shell so that existing habits and scripts continue to work:

```bash
echo "alias docker=podman" >> ~/.bashrc
echo "alias docker-compose=podman-compose" >> ~/.bashrc
source ~/.bashrc
```
