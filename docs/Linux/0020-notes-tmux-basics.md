# Notes about tmux basics

[Português (Brasil)](./0020-notas-fundamentos-tmux-pt-br.md)

**tmux** (Terminal Multiplexer) lets you create virtual “windows” that continue running in the background even if your SSH connection drops.

## 1. Installation

To install tmux on Debian/Ubuntu-based systems (such as Raspberry Pi OS):

```bash
sudo apt install tmux -y
```

## 2. Useful commands (in the terminal)

| Command | Description |
|---------|-----------|
| `tmux new -s meuserver` | Starts a new session named "meuserver" |
| `tmux ls` | Lists the tmux processes/sessions currently running |
| `tmux attach -t meuserver` | Returns to (attaches to) the active "meuserver" session |
| `tmux kill-session -t meuserver` | Ends (kills) the "meuserver" session |
| `tmux kill-server` | Ends (kills) all tmux sessions |
| `exit` (or `Ctrl+D`) | Ends the active session from within it |

## 3. Keyboard shortcuts (inside tmux)

All tmux shortcuts require you to press a **prefix** before the command. The default prefix is `Ctrl + B`.

Press and release `Ctrl + B`, then press one of the following keys:

| Shortcut | Action |
|--------|-----------|
| `%` | Splits the screen vertically (side by side) |
| `"` | Splits the screen horizontally (top and bottom) |
| `Arrow keys` | Moves from one pane to another |
| `x` | Closes the pane under the cursor |
| `c` | Creates a new, empty window |
| `n` | Moves to the next window (Next) |
| `p` | Returns to the previous window (Prev) |
| `d` | Detaches from the session, leaving everything running in the background |
