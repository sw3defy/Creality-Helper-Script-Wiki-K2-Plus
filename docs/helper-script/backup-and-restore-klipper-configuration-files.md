# Backup & Restore Klipper Configuration Files — K2 Plus

Regular backups protect your Klipper configuration from accidental deletion, factory resets, and firmware updates.

---

## Backup from Helper Script

From the helper script menu, select **option 18 — Backup Klipper configuration**.

The script creates a compressed archive of your entire `/mnt/UDISK/printer_data/config/` directory and saves it to `/mnt/UDISK/helper-script/backups/`. The last 5 backups are kept automatically.

---

## Restore from Helper Script

From the helper script menu, select **option 19 — Restore Klipper configuration**.

The script shows a numbered list of available backups with dates and sizes. Select the one you want to restore, confirm, and Klipper restarts automatically.

---

## Backup from Fluidd / Mainsail Console

Once **Useful Macros** are installed, you can trigger a backup directly from the printer interface:

```gcode
KLIPPER_BACKUP_CONFIG
```

The backup is saved as `backup_config.tar.gz` in your config folder, accessible via the Fluidd file manager.

---

## Backup via SSH

```bash
# Create a timestamped backup
tar -czf /mnt/UDISK/printer_data/config_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
    -C /mnt/UDISK/printer_data config/

# List backups
ls -lh /mnt/UDISK/printer_data/config_backup_*.tar.gz
```

---

## Download Backups

You can download config backups via:

- **Fluidd File Manager** — navigate to the config folder, select the `.tar.gz` file, and download
- **SCP** from your computer:
    ```bash
    scp root@<printer-ip>:/mnt/UDISK/printer_data/config_backup_20260601.tar.gz ./
    ```
- **MobaXterm** — use the left panel file browser to download any file

---

## What to Back Up

At minimum, back up these files before any firmware update or factory reset:

| File | Contains |
|---|---|
| `printer.cfg` | Main Klipper config including SAVE_CONFIG block (Z offset, input shaper, CFS cut position) |
| `box.cfg` | CFS positions and calibration |
| `gcode_macro.cfg` | Stock Creality macros |
| `printer_params.cfg` | Print parameters |
| `useful_macros.cfg` | Helper script macros |
| `moonraker.conf` | Moonraker extensions config |

The `SAVE_CONFIG` block at the bottom of `printer.cfg` is especially important — it contains your calibrated values for bed mesh, input shaper, and CFS cut position.

!!! warning "After factory reset"
    All data under `/mnt/UDISK/printer_data/` is wiped by a factory reset. Always download a backup to your computer before performing a reset.
