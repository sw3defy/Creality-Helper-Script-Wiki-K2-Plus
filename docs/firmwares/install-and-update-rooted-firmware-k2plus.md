# Install & Update Firmware — K2 Plus

This guide explains how to install firmware on the Creality K2 Plus and K2 Plus Combo, and how to enable root SSH access.

!!! warning "This is the K2 Plus guide"
    If you have a **K1, K1C, or K1 Max**, use the [K1 Series firmware guide](install-and-update-rooted-firmware-k1.md) instead. The K2 Plus uses a completely different filesystem, service manager, and firmware update path. Do not mix the two.

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

See the [SSH Connection](../firmwares/ssh-connection.md) guide for how to find your printer's IP address and connect from Windows, macOS, or Linux.

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
