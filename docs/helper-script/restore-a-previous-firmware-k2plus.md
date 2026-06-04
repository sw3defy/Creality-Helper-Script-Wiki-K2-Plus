# Restore a Previous Firmware — K2 Plus

---

## Finding Previous Firmware

[Creality Cloud — K2 Series Firmware :material-open-in-new:](https://www.crealitycloud.com/software-firmware/firmware/k2-series){ .md-button }

---

## Procedure

1. Back up your config files:

    ```bash
    cp -r /mnt/UDISK/printer_data/config/ /mnt/UDISK/printer_data/config_backup_$(date +%Y%m%d)/
    ```

2. Format a USB drive as FAT32 with 4096 allocation size.
3. Copy the `.img` file to the root of the USB drive.
4. Turn on the printer, plug in the USB drive from the home screen.
5. Accept the upgrade prompt and wait for completion.
6. After restart, re-enable root access: **Settings → Root account information**.
7. Reinstall the helper script and any features you had installed.
