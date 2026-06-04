# Install Helper Script — K2 Plus

The Creality K2 Plus Helper Script is a native shell-based tool built specifically for the K2 Plus and K2 Plus Combo. It installs features by writing Klipper `.cfg` files to `/mnt/UDISK/printer_data/config/` and extending Moonraker non-destructively — without overwriting any stock firmware files.

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
| Extends Moonraker | Writes `/mnt/UDISK/printer_data/config/moonraker.conf` with `[include /usr/share/moonraker/moonraker.conf]` at the top, then patches the startup script to load it |
| Adds Klipper features | Writes `.cfg` files to `/mnt/UDISK/printer_data/config/` and adds `[include]` lines to `printer.cfg` |
| Service restarts | Uses `/etc/init.d/S55klipper`, `S56moonraker`, `S80nginx` — **not** `supervisorctl` (which does not exist on K2 Plus) |
| Uninstall | Removes the `.cfg` file, removes the `[include]` line, restarts Klipper. Moonraker patch is reversible via the Remove menu. |
| Stock files | Never modified. `/usr/share/moonraker/moonraker.conf`, `/etc/nginx/nginx.conf`, and all `/usr/share/klipper/` files are left untouched. |

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
    shutil.rmtree('/mnt/UDISK/helper-script')
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
    8) Mainsail (port 4409)
    9) Moonraker Timelapse

  --- Step 5: Remote access & notifications ---
   10) OctoEverywhere
   11) Mobileraker Companion
   12) Git Backup

  [Remove] Menu
   20) Remove a feature

  [Backup & Restore] Menu
   30) Backup Klipper configuration
   31) Restore Klipper configuration

  [Tools] Menu
   40) Restart Klipper
   41) Restart Moonraker
   42) Restart Nginx
   43) View Klipper log
   44) View Moonraker log
   45) Show installed features

    0) Exit

  Enter choice:
```

---

## Recommended Installation Order

The menu is already arranged in the correct dependency order — install top to bottom:

1. **Moonraker Extensions** (option 1) — always first. Sets up the Update Manager, enables object processing, and creates the persistent Moonraker config that all other features build on.
2. **Fans Control Macros** (option 2) — before Useful Macros. The `START_PRINT` macro references the `CHAMBER_HEAT` and `FANS_OFF` macros that this installs.
3. **Useful Macros** (option 3) — installs `START_PRINT`, `END_PRINT`, `PAUSE`, `RESUME`. Configure your slicer start/end G-code after this step.
4. **Save Z-Offset Macros** (option 4) and **M600** (option 5) — optional, in any order.
5. **KAMP** (option 6) — requires Moonraker Extensions (object processing). Install after option 1.
6. **Improved Shapers** (option 7) — independent, any time after Klipper is running.
7. **Mainsail, Timelapse, remote access** (options 8–12) — install in any order, any time.

---

## Update

Once Moonraker Extensions is installed, the Update Manager panel in Fluidd shows available updates:

- Go to **Settings → Software Updates** in Fluidd
- Click **Update** next to `creality-helper-script`

Or update manually via SSH:

```bash
python3 -c "
import urllib.request, zipfile, os, shutil
print('Downloading update...')
urllib.request.urlretrieve(
    'https://github.com/sw3defy/Creality-Helper-Script-K2-Plus/archive/refs/heads/main.zip',
    '/tmp/helper.zip'
)
with zipfile.ZipFile('/tmp/helper.zip', 'r') as z:
    z.extractall('/tmp/')
for f in os.listdir('/tmp/Creality-Helper-Script-K2-Plus-main'):
    src = '/tmp/Creality-Helper-Script-K2-Plus-main/' + f
    dst = '/mnt/UDISK/helper-script/' + f
    if os.path.isdir(src):
        if os.path.exists(dst): shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
shutil.rmtree('/tmp/Creality-Helper-Script-K2-Plus-main')
os.remove('/tmp/helper.zip')
print('Update complete')
"
```

---

## Uninstall Everything

To completely remove the helper script and all installed features:

```bash
# Remove all installed .cfg files and includes
sh /mnt/UDISK/helper-script/helper.sh
# Select option 20 (Remove menu) and remove each feature

# Restore Moonraker startup to stock
cp /etc/rc.d/S56moonraker.orig /etc/rc.d/S56moonraker 2>/dev/null || \
  sed -i 's|CONF=/mnt/UDISK/printer_data/config/moonraker.conf|CONF=/usr/share/moonraker/moonraker.conf|g' /etc/rc.d/S56moonraker

# Restart services
/etc/init.d/S55klipper restart
/etc/init.d/S56moonraker restart

# Remove the helper script directory
rm -rf /mnt/UDISK/helper-script
```

---

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
