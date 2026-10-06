# Notes about troubleshooting package update failures
If `apt update` fails with hash-mismatch errors or corrupted package lists, the root cause is often your ISP transparently caching stale content, or a Canonical mirror (`security.ubuntu.com`) being temporarily out of sync. The fix is to tell `apt` to bypass network caches entirely and skip hash-based download optimizations.

## 1. Create a rule to bypass network caches

Paste the entire block below into the terminal and press Enter. It creates a configuration file that disables HTTP pipelining, ignores intermediate caches, and forces direct file downloads:

```
echo -e "Acquire::http::Pipeline-Depth 0;\nAcquire::http::No-Cache true;\nAcquire::BrokenProxy true;\nAcquire::By-Hash no;" | sudo tee /etc/apt/apt.conf.d/99fixbadproxy
```
## 2. Clear the corrupted package lists

Any partial downloads from the failed attempt must be removed before retrying:

```
sudo rm -rf /var/lib/apt/lists/*
```
## 3. Update and install

With the bypass rules in place, `apt` will now download package metadata as directly as possible:

```
sudo apt update
```
If `apt update` completes successfully, proceed with your `sudo apt install -y ...` command normally.

> **Tip:** Once the installation is complete, remove the bypass file so that Ubuntu reverts to its default network behaviour in the future:

```
sudo rm /etc/apt/apt.conf.d/99fixbadproxy 
```
