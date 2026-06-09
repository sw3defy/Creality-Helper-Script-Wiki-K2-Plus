# Tools Menu

---

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

