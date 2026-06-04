# Restore a Previous Firmware — K2 Plus

If a firmware update causes issues, you can restore a previous version using the same USB drive installation method.

---

## Finding Previous Firmware

Previous K2 Plus firmware versions are available on Creality Cloud:

[Creality Cloud — K2 Series Firmware :material-open-in-new:](https://www.crealitycloud.com/software-firmware/firmware/k2-series){ .md-button }

Download the `.img` file for the version you want to restore.

---

## Procedure

1. Back up your Klipper config files first — firmware installation does **not** erase `/mnt/UDISK/printer_data/config/`, but a factory reset (which you may need to do) will.

    ```bash
    cp -r /mnt/UDISK/printer_data/config/ /mnt/UDISK/printer_data/config_backup_$(date +%Y%m%d)/
    ```

2. Format a USB drive as FAT32 with 4096 allocation size.

3. Copy the `.img` file to the root of the USB drive.

4. Turn on the printer, plug in the USB drive from the home screen.

5. Accept the upgrade prompt and wait for completion.

6. After restart, re-enable root access: **Settings → Root account information**.

7. Reinstall the helper script and any features you had installed.

---

## Helper Script Restore Tool

The helper script also provides a firmware restore option in the **Tools Menu** → **Restore a previous Firmware**. This requires an active SSH connection and a firmware file accessible from the printer.
