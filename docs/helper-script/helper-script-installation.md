# Install Helper Script — K2 Plus

!!! warning "Maintenance audit — November 2026"
    The instructions on this page describe the historical published Helper Script and may not match the **unmerged maintenance branch**. Moonraker Extensions, fan macros, improved shapers, and Timelapse installation/removal are currently blocked in that branch while stock-compatible migration is reviewed. Do **not** follow old directions to patch `S56moonraker`, add reverse Moonraker includes, or replace Creality's `M106`/`M107`. HelixScreen requires a confirmed installation followed by an immediate reboot, with extra patience during startup. See [Safe Update Audit](safe-update-audit.md) for the actual status.


The Creality K2 Plus Helper Script is a native shell-based tool built specifically for the K2 Plus and K2 Plus Combo. It installs features by writing Klipper `.cfg` files to `/mnt/UDISK/printer_data/config/` and extending Moonraker non-destructively — but some existing startup and configuration patch paths can modify stock or active files. Review and back up those files before running it.

!!! warning "K2 Plus only"
    This helper script is written specifically for the **Creality K2 Plus** and **K2 Plus Combo**.
    It will not work on K1, K1C, K1 Max, or Ender-3 V3 Series printers.

!!! note "Before you begin"
    - Root access must be enabled. See [Enable Root Access](../firmwares/install-and-update-rooted-firmware-k2plus.md#enable-root-access).
    - The printer must have completed its startup sequence and be on the home screen.
    - An internet connection is required for features that download additional components (Mainsail, KAMP, Timelapse).

---

## How It Works

The helper script takes a safe, reversible approach to every feature:

| What it does | How |
|---|---|
| Extends Moonraker | The inspected K2 Plus already starts Moonraker with the UDISK user configuration. Extension installation is blocked pending a verified migration; never add a reverse include to the stock configuration. |
| Adds Klipper features | Writes `.cfg` files to `/mnt/UDISK/printer_data/config/` and adds `[include]` lines to `printer.cfg` |
| Service restarts | Firmware-specific service commands must be inspected before use. The observed startup script is `/etc/rc.d/S56moonraker`; do not assume `/etc/init.d/S56moonraker` exists. |
| Uninstall | Only remove files proven to be owned by the Helper Script after backup and validation. Moonraker extension removal is currently blocked in the maintenance branch. |
| Stock files | **Do not assume untouched.** Review `scripts/system.sh` and its startup patches before running the Helper Script; some paths modify active/stock configurations. |

---

## Installation

Connect via SSH. See [SSH Connection](../firmwares/ssh-connection.md).

The K2 Plus does **not** have `git`, `wget`, or `curl` available in the stock firmware. Use Python3 to download and install the helper script.

Connect via SSH and run:

```bash
python3 -c "
import urllib.request, zipfile, os, shutil
print('Downloading...')
urllib.request.urlretrieve(
    'https://github.com/sw3defy/Creality-Helper-Script-K2-Plus/archive/refs/heads/main.zip',
    '/tmp/helper.zip'
)
print('Extracting...')
with zipfile.ZipFile('/tmp/helper.zip', 'r') as z:
    z.extractall('/tmp/')
if os.path.exists('/mnt/UDISK/helper-script'):
    raise RuntimeError('Existing install detected: stop and use reviewed selective update procedure')
shutil.move('/tmp/Creality-Helper-Script-K2-Plus-main', '/mnt/UDISK/helper-script')
os.remove('/tmp/helper.zip')
print('Done')
"
```

Make the scripts executable and run:

```bash
chmod +x /mnt/UDISK/helper-script/helper.sh
chmod +x /mnt/UDISK/helper-script/scripts/*.sh
sh /mnt/UDISK/helper-script/helper.sh
```

!!! note "Install path"
    The K2 Plus helper script installs to `/mnt/UDISK/helper-script/` — not `/usr/data/helper-script/` as on K1 Series.

!!! note "No git/wget/curl on K2 Plus"
    Unlike the K1 Series, the K2 Plus stock firmware does not include `git`, `wget`, or `curl`. Python3 is the only download tool available without installing Entware first.

---

## Main Menu

When you run the script you will see:

```
======================================================
   Creality K2 Plus Helper Script
======================================================
   https://sw3defy.github.io/Creality-Helper-Script-Wiki-K2-Plus
======================================================

  [Install] Menu
  --- Step 1: Foundation (install first) ---
    1) Moonraker Extensions & Update Manager  [recommended first]

  --- Step 2: Print macros ---
    2) Fans Control Macros                    [needed by START_PRINT]
    3) Useful Macros (START_PRINT / END_PRINT)
    4) Save Z-Offset Macros
    5) M600 Filament Change Support

  --- Step 3: Leveling & calibration ---
    6) Klipper Adaptive Meshing & Purging (KAMP)
    7) Improved Shapers Calibrations

  --- Step 4: Web interface & camera ---
    8) Fluidd (install/update/repair - port 4408)
    9) Mainsail (install/update/repair - port 4409)
   10) Moonraker Timelapse
   11) Camera Support for Fluidd and Mainsail
   12) HelixScreen (touchscreen UI)

  --- Step 5: Remote access & notifications ---
   13) OctoEverywhere
   14) Mobileraker Companion
   15) Entware Package Manager
   16) Git Backup

  [Remove] Menu
   17) Remove a feature

  [Backup & Restore] Menu
   18) Backup Klipper configuration
   19) Restore Klipper configuration

  [Tools] Menu
   20) Restart Klipper
   21) Restart Moonraker
   22) Restart Nginx
   23) View Klipper log
   24) View Moonraker log
   25) Show installed features

    0) Exit

  Enter choice:
```

---

## Installation order and safety gates

The historical menu order is **not** a validated installation plan. In the unmerged maintenance branch, Moonraker Extensions, Fans Control, Improved Shapers, KAMP, Timelapse, and several other installers are blocked pending review. Never install all features in one pass.

HelixScreen can appear anywhere in the intended feature sequence, but its installation requires explicit confirmation and an immediate reboot afterward. First startup may be slower. The installer must implement and validate this before it is enabled.

See [Safe Update Audit](safe-update-audit.md) for the current development status.

## Update

Read the [Safe update audit](safe-update-audit.md) before making changes.\n
Once Moonraker Extensions is installed, the Update Manager panel in Fluidd shows available updates:

- Go to **Settings → Software Updates** in Fluidd
- Click **Update** next to `creality-helper-script`

Do **not** run the former bulk-copy update procedure: it could overwrite local camera integration files and other printer-specific changes. First back up the existing Helper Script and active Klipper configuration, then use a reviewed selective update plan. See [Safe update audit](safe-update-audit.md).\n
---

## Uninstall and rollback

!!! danger "Do not use the old bulk uninstall procedure"
    The old procedure repointed the Moonraker service to the stock configuration and removed shared files. The inspected printer already starts from the UDISK user configuration. Do **not** change the service config path, delete the helper directory, or restart services as a blanket uninstall. Back up first, inventory ownership, and wait for the reviewed selective migration/removal procedure.

## Installed Features Location

All files written by the helper script:

| Feature | Config file | Location |
|---|---|---|
| Moonraker Extensions | `moonraker.conf` | `/mnt/UDISK/printer_data/config/` |
| Fans Control Macros | `fans_control.cfg` | `/mnt/UDISK/printer_data/config/` |
| Useful Macros | `useful_macros.cfg` | `/mnt/UDISK/printer_data/config/` |
| KAMP | `KAMP/KAMP_Settings.cfg` | `/mnt/UDISK/printer_data/config/` |
| Improved Shapers | `shapers_calibration.cfg` | `/mnt/UDISK/printer_data/config/` |
| Save Z-Offset Macros | `z_offset_macros.cfg` | `/mnt/UDISK/printer_data/config/` |
| M600 Support | `m600.cfg` | `/mnt/UDISK/printer_data/config/` |
| Moonraker Timelapse | `timelapse.cfg` | `/mnt/UDISK/printer_data/config/` |
| Mainsail | static files | `/usr/share/mainsail/` |
| Backups | `backups/` | `/mnt/UDISK/helper-script/backups/` |
| Installed feature log | `.installed` | `/mnt/UDISK/helper-script/` |
| Moonraker startup patch backup | `S56moonraker.orig` | `/etc/rc.d/` |
| Nginx backup (if modified) | `.nginx.conf.bak` | `/mnt/UDISK/helper-script/` |

---

## Troubleshooting

**Klipper fails to start after installing a feature**

Check the log:
```bash
tail -50 /mnt/UDISK/printer_data/logs/klippy.log
```
Most errors are caused by a syntax problem in a new `.cfg` file. The log will show the exact line.

**Moonraker fails to start after installing extensions**

Check the log:
```bash
tail -50 /mnt/UDISK/printer_data/logs/moonraker.log
```
If the include directive is causing the issue, restore the stock moonraker startup:
```bash
cp /etc/rc.d/S56moonraker.orig /etc/rc.d/S56moonraker
/etc/init.d/S56moonraker restart
```

**Script says "printer.cfg not found"**

The printer has not finished booting. Wait until you can see the Fluidd interface, then run the script again.

**Git clone fails with "SSL certificate problem"**

```bash
git config --global http.sslVerify false
```
Then retry the clone.

**Permission denied running helper.sh**

```bash
chmod +x /mnt/UDISK/helper-script/helper.sh
chmod +x /mnt/UDISK/helper-script/scripts/*.sh
```
