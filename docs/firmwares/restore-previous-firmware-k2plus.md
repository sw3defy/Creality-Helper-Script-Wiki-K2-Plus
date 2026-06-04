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
