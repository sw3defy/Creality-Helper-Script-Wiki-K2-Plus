# Install & Update Firmware — K2 Plus

This guide explains how to install firmware on the Creality K2 Plus and K2 Plus Combo, and how to enable root SSH access.

!!! warning "This is the K2 Plus guide"
    If you have a **K1, K1C, or K1 Max**, use the [K1 Series firmware guide](install-and-update-rooted-firmware-k1.md) instead. The K2 Plus uses a completely different filesystem, service manager, and firmware update path. Do not mix the two.

---

## Prerequisites

- The K2 Plus ships with Fluidd pre-installed at port `4408`. You do not need to install it separately.
- Root SSH access must be **re-enabled after every factory reset**.
- The K2 Plus has **no `/usr/data/` path**. All persistent data lives under `/mnt/UDISK/`.
- There is **no upgrade path ladder** required on K2 Plus. You can update directly to the latest firmware via OTA or USB.

---

## Download Links

[Creality Cloud — K2 Series Firmware :material-open-in-new:](https://www.crealitycloud.com/software-firmware/firmware/k2-series){ .md-button }

---

## Installation & Update

- Format a USB drive as **FAT32** with 4096 allocation unit size.
- Copy the `.img` firmware file to the root of the USB drive and safely eject it.
- Turn on the K2 Plus.
- Once on the home screen, plug the USB drive into the **front** USB port.
- A popup should appear indicating a new available update.
- Press **Upgrade** and wait for the update to complete.
- When finished, the printer restarts automatically.
- Perform a new self-check: go to **Settings → Self-check**.

!!! warning "Reinstall after factory reset"
    After a factory reset, all features installed with Creality Helper Script must be reinstalled from scratch.

---

## Skip the Startup Self-Check

Connect via SSH and run:

```bash
sed -i 's/"self_test_sw":1/"self_test_sw":0/' /mnt/UDISK/creality/userdata/config/system_config.json
```

To re-enable:

```bash
sed -i 's/"self_test_sw":0/"self_test_sw":1/' /mnt/UDISK/creality/userdata/config/system_config.json
```

---

## Factory Reset via SSH

```bash
echo "all" | /usr/bin/nc -U /var/run/wipe.sock
```

!!! danger "This is irreversible"
    This immediately wipes all user data under `/mnt/UDISK/`. Backup your config files first.

---

## Enable Root Access

!!! note "Required after every factory reset"

- On the touchscreen go to **Settings → Root account information**.
- Scroll to the bottom, check the agreement box, wait 30 seconds, press **OK**.
- Connect via SSH:
    - **Host:** your printer IP
    - **User:** `root`
    - **Password:** `creality_2024`

!!! warning "Different password from K1"
    The K2 Plus default root password is **`creality_2024`** — not `creality_2023` as on K1.
