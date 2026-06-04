# SSH Connection — K2 Plus

SSH gives you full command-line access to the K2 Plus Linux system. It is required for installing the Helper Script and for most advanced configuration.

!!! note "Enable root access first"
    SSH root access must be enabled before you can connect. See [Enable Root Access](install-and-update-rooted-firmware-k2plus.md#enable-root-access).

---

## Connection Details

| Setting | Value |
|---|---|
| Host | Your printer's IP address |
| Port | 22 (default) |
| Username | `root` |
| Password | `creality_2024` |

!!! warning "K2 Plus password is different from K1"
    The default root password is **`creality_2024`** — not `creality_2023` as on K1 Series printers.

Find your printer's IP address in **Settings → Network** on the touchscreen.

---

## Connect with MobaXterm (Windows)

- Download and install **MobaXterm**: :material-download: <a href="https://mobaxterm.mobatek.net/download-home-edition.html">Here</a>

- Launch it and click the `Session` icon

- Click the `SSH` icon

- Enter your printer's IP address in `Remote Host`, check `Specify username`, enter `root`, then click `OK`

- Enter the password `creality_2024` when prompted (it is not displayed while typing — this is normal)

- Once connected, the left panel shows your printer's files and the right panel is the SSH terminal

---

## Connect from macOS or Linux

Open Terminal and run:

```bash
ssh root@<printer-ip>
```

Enter `creality_2024` when prompted for the password.

If you see a host key warning on reconnection after a firmware update:

```bash
ssh-keygen -R <printer-ip>
ssh root@<printer-ip>
```

---

## What You See After Connecting

```
BusyBox v1.33.2 built-in shell (ash)

 _____  _              __     _
|_   _||_| ___  _ _   |  |   |_| ___  _ _  _ _
  | |   _ |   ||   |  |  |__ | ||   || | ||_'_|
  | |  | || | || _ |  |_____||_||_|_||___||_,_|
  |_|  |_||_|_||_|_|  Tina is Based on OpenWrt!
 -----------------------------------------------------
 Tina 5.0, OpenWrt 21.02-SNAPSHOT r0-bdf710c83
 -----------------------------------------------------
root@K2Plus-XXXX:~#
```

The hostname suffix (e.g. `DE6C`) is the last 4 characters of your printer's MAC address.

---

## Transfer Files via SCP

Download a file from the printer:

```bash
scp root@<printer-ip>:/mnt/UDISK/printer_data/config/printer.cfg ./
```

Upload a file to the printer:

```bash
scp ./my_config.cfg root@<printer-ip>:/mnt/UDISK/printer_data/config/
```

MobaXterm users can drag and drop files in the left panel file browser.
