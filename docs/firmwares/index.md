# Firmwares

---

# Install & Update Firmware — K2 Plus

This guide explains how to install firmware on the Creality K2 Plus and K2 Plus Combo, and how to enable root SSH access.

!!! warning "This is the K2 Plus guide"
    If you have a **K1, K1C, or K1 Max**, use the [K1 Series firmware guide](install-and-update-rooted-firmware-k2plus.md) instead. The K2 Plus uses a completely different filesystem, service manager, and firmware update path. Do not mix the two.

---

## Prerequisites

Before installing or updating firmware, note the following:

- The K2 Plus ships with Fluidd pre-installed at port `4408`. You do not need to install it separately.
- Root SSH access must be **re-enabled after every factory reset**.
- The K2 Plus has **no `/usr/data/` path**. All persistent data lives under `/mnt/UDISK/`. Any K1-targeted instructions referencing `/usr/data/` will not work.
- There is **no upgrade path ladder** required on K2 Plus (unlike K1). You can update directly to the latest firmware from any recent version via OTA or USB.

---

## Download Links

Download firmware from the Creality Cloud K2 Plus firmware page:

[Creality Cloud — K2 Series Firmware :material-open-in-new:](https://www.crealitycloud.com/software-firmware/firmware/k2-series){ .md-button }

---

## Installation & Update

- Follow the [Reset Factory Settings](../helper-script/reset-factory-settings.md) section before installing a new firmware version.

- When the factory reset is complete, insert a USB drive into your computer.

- Format the USB drive as **FAT32** with 4096 allocation unit size (or exFAT on some drives).

- Copy the `.img` firmware file to the root of the USB drive and safely eject it.

- Turn on the K2 Plus.

- Once on the home screen, plug the USB drive into the **front** USB port.

- A popup should appear indicating a new available update.

- Press **Upgrade** and wait for the update to complete.

- When finished, the printer restarts automatically.

- Once back on the home screen, remove the USB drive.

- Perform a new self-check: go to **Settings → Self-check**.

!!! warning "Reinstall after factory reset"
    After a factory reset, all features installed with Creality Helper Script must be reinstalled from scratch.

---

## Skip the Startup Self-Check

This is useful if you have modified the printer (e.g. probe replacement, toolhead changes) and can no longer complete the startup self-check.

Connect via SSH and run:

```bash
sed -i 's/"self_test_sw":1/"self_test_sw":0/' /mnt/UDISK/creality/userdata/config/system_config.json
```

!!! note "K2 Plus path"
    This path uses `/mnt/UDISK/` — not `/usr/data/` as on the K1 Series.

To re-enable the self-check later:

```bash
sed -i 's/"self_test_sw":0/"self_test_sw":1/' /mnt/UDISK/creality/userdata/config/system_config.json
```

---

## Factory Reset via SSH

The K2 Plus supports a socket-based factory reset command in addition to the screen UI method:

```bash
echo "all" | /usr/bin/nc -U /var/run/wipe.sock
```

!!! danger "This is irreversible"
    This immediately wipes all user data under `/mnt/UDISK/`. Backup your Klipper config files first. See [Backup & Restore Klipper configuration files](../helper-script/backup-and-restore-klipper-configuration-files.md).

---

## Enable Root Access

!!! note "Required after every factory reset"
    Root access must be re-enabled each time you restore the printer to factory settings.

- On the printer's touchscreen, go to **Settings → Root account information**.

- Read the disclaimer, scroll to the bottom, check the agreement box, wait 30 seconds, then press **OK**.

- Root access is now enabled.

- You can now connect via SSH:
    - **Host:** your printer's IP address
    - **User:** `root`
    - **Password:** `creality_2024`

!!! warning "Different password from K1"
    The K2 Plus default root password is **`creality_2024`** — not `creality_2023` as used on K1 Series printers.

---

## SSH Connection

See the [SSH Connection](ssh-connection.md) guide for how to find your printer's IP address and connect from Windows, macOS, or Linux.

Once connected you will see:

```
BusyBox v1.33.2 built-in shell (ash)

Tina 5.0, OpenWrt 21.02-SNAPSHOT
root@K2Plus-XXXX:~#
```

The hostname suffix (e.g. `DE6C`) is derived from the last 4 characters of your printer's MAC address.

---

## Restore a Previous Firmware

See [Restore a Previous Firmware — K2 Plus](restore-previous-firmware-k2plus.md).


---

# Restore a Previous Firmware — K2 Plus

If a firmware update causes issues, you can restore a previous version using the same USB installation method used for regular updates.

!!! warning "Back up first"
    Restoring firmware triggers a factory reset. Back up your Klipper config before proceeding:
    ```bash
    cp -r /mnt/UDISK/printer_data/config/ /mnt/UDISK/printer_data/config_backup_$(date +%Y%m%d)/
    ```

---

## Finding Previous Firmware

Previous K2 Plus firmware versions are available on the Creality Cloud firmware page:

[Creality Cloud — K2 Series Firmware :material-open-in-new:](https://www.crealitycloud.com/software-firmware/firmware/k2-series){ .md-button }

Download the `.img` file for the version you want to restore.

---

## Restore Procedure

1. Format a USB drive as **FAT32** with 4096 allocation size.

2. Copy the `.img` file to the **root** of the USB drive (not inside any folder).

3. Turn on the printer and wait for the home screen.

4. Plug the USB drive into the **front** USB port.

5. A firmware update prompt will appear. Accept it and wait for the process to complete — the printer will restart automatically.

6. After restart, re-enable root access:
    **Settings → Root account information**

7. Reinstall the helper script and all features. See [Install Helper Script](../helper-script/helper-script-installation.md).

---

## Firmware Recovery (Brick Recovery)

If the printer will not boot at all, see the stock Creality recovery procedure using a USB drive with a specific file layout. Contact Creality support or check the [Creality community forum](https://www.crealitycloud.com/) for the latest recovery image for your firmware version.

---

## After Restoring

After any firmware restore or factory reset:

- Root access password resets to **`creality_2024`**
- All data under `/mnt/UDISK/printer_data/` is wiped
- The helper script and all installed features must be reinstalled from scratch
- Run **Settings → Self-check** before printing


---

# Reset Factory Settings — K2 Plus

A factory reset wipes all user data and returns the printer to its out-of-box state. Use this before installing a new firmware version or when troubleshooting persistent issues.

!!! danger "This is irreversible"
    A factory reset permanently deletes all data under `/mnt/UDISK/`. Back up your Klipper config files first.

    ```bash
    tar -czf /tmp/config_backup.tar.gz -C /mnt/UDISK/printer_data config/
    scp root@<printer-ip>:/tmp/config_backup.tar.gz ./
    ```

!!! warning "Reinstall required after reset"
    After a factory reset, root access must be re-enabled and all Helper Script features must be reinstalled from scratch.

---

## Method 1 — SSH Command (Recommended)

Connect via [SSH](ssh-connection.md) and run:

```bash
echo "all" | nc -U /var/run/wipe.sock
```

The printer restarts automatically with all settings reset.

Reconnect to your WiFi network from **Settings → Network** after restarting.

---

## Method 2 — SSH with Helper Script

!!! note
    Only available if the Helper Script is already installed.

```bash
/etc/init.d/S58factoryreset reset
```

This preserves user preferences and network settings while resetting printer configuration.

---

## Method 3 — USB Drive

Useful if the printer is not connected to the network or SSH is not available.

1. Format a USB drive as **FAT32**.
2. Create an empty file named `wipe_all` (no extension) at the root of the drive.

    !!! tip "Creating the file on Windows"
        Open Notepad, do not type anything, go to **File → Save As**, navigate to the USB drive, set **Save as type** to **All Files (\*.\*)**, and name the file `wipe_all` with no extension.
3. Plug the USB drive into the **front** USB port while the printer is on.
4. The factory reset executes at the next startup.

---

## After Factory Reset Checklist

1. **Re-enable root access:** Settings → Root account information
2. **Reconnect to WiFi:** Settings → Network
3. **Run Self-check:** Settings → Self-check
4. **Reinstall Helper Script:** See [Install Helper Script](../helper-script/helper-script-installation.md)
5. **Reinstall all features** from the Helper Script Install Menu
6. **Restore config backup** if available


---

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


---

# Change Date & Time — K2 Plus

The K2 Plus syncs its clock via NTP (Network Time Protocol) when connected to the internet. If the date and time are incorrect it can cause SSL certificate errors when cloning the Helper Script.

---

## Check Current Date and Time

```bash
date
```

---

## Sync Time via NTP (Recommended)

If connected to the internet, restart the NTP service:

```bash
/etc/init.d/S98sysntpd restart
sleep 5
date
```

---

## Set Time Manually

If the printer is not connected to the internet:

```bash
# Format: MMDDhhmm[[CC]YY][.ss]
# Example: June 4, 2026, 14:30
date 060414302026
```

---

## Set Timezone

The K2 Plus timezone is configured in `system_config.json`. To change it:

```bash
# View current timezone setting
python3 -c "import json; d=json.load(open('/mnt/UDISK/creality/userdata/config/system_config.json')); print(d['user_info']['time_zone'])"

# The timezone is set by the Creality UI — change it from
# Settings → System → Time Zone on the touchscreen
```

---

## Fix SSL Errors When Cloning

If you see SSL certificate errors when running `git clone`:

```bash
# Sync time first
/etc/init.d/S98sysntpd restart
sleep 10

# If still failing, disable SSL verification temporarily
git config --global http.sslVerify false
git clone --depth 1 https://github.com/sw3defy/Creality-Helper-Script-K2-Plus.git /mnt/UDISK/helper-script

# Re-enable after cloning
git config --global http.sslVerify true
```


---

