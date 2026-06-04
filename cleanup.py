import os
import shutil

# ============================================================
# Files to DELETE — K1 and Ender-3 specific pages
# ============================================================
files_to_delete = [
    # Firmwares
    "docs/firmwares/install-and-update-rooted-firmware-k1.md",
    "docs/firmwares/restore-previous-firmware-k1.md",
    "docs/firmwares/firmware-recovery-k1.md",
    "docs/firmwares/install-and-update-rooted-firmware-ender3.md",
    "docs/firmwares/restore-previous-firmware-ender3.md",

    # Helper script — K1
    "docs/helper-script/moonraker-k1.md",
    "docs/helper-script/fluidd-k1.md",
    "docs/helper-script/buzzer-support.md",
    "docs/helper-script/nozzle-cleaning-fan-control.md",
    "docs/helper-script/fans-control-macros.md",
    "docs/helper-script/improved-shapers-calibrations.md",
    "docs/helper-script/useful-macros.md",
    "docs/helper-script/save-z-offset-macros.md",
    "docs/helper-script/screws-tilt-adjust-support.md",
    "docs/helper-script/m600-support.md",
    "docs/helper-script/moonraker-timelapse.md",
    "docs/helper-script/camera-settings-control.md",
    "docs/helper-script/mobileraker-companion.md",
    "docs/helper-script/simplyprint.md",
    "docs/helper-script/custom-boot-display.md",
    "docs/helper-script/remove-and-restore-creality-web-interface.md",
    "docs/helper-script/backup-and-restore-moonraker-database.md",
    "docs/helper-script/restore-a-previous-firmware-k1.md",
    "docs/helper-script/klipper-adaptive-meshing-and-purging.md",

    # Helper script — Ender-3
    "docs/helper-script/moonraker-ender3.md",
    "docs/helper-script/fluidd-ender3.md",
    "docs/helper-script/nebula-camera-settings-control.md",
    "docs/helper-script/restore-a-previous-firmware-ender3.md",

    # Improvements — K1
    "docs/improvements/improve-hotend-cooling-k1.md",
    "docs/improvements/bondtech-lgx-pro-lite-upgrade-kit.md",

    # Others — K1
    "docs/others/boards-layout-k1.md",
    "docs/others/files-location.md",
]

deleted = []
skipped = []

for f in files_to_delete:
    if os.path.exists(f):
        os.remove(f)
        deleted.append(f)
    else:
        skipped.append(f)

print(f"Deleted {len(deleted)} files:")
for f in deleted:
    print(f"  ✓ {f}")

if skipped:
    print(f"\nSkipped {len(skipped)} (already gone):")
    for f in skipped:
        print(f"  - {f}")

# ============================================================
# Rewrite mkdocs.yml — K2 Plus only
# ============================================================
new_nav = """nav:
    - About: index.md
    - Changelog: changelog.md
    - Discussions: https://github.com/sw3defy/Creality-Helper-Script-Wiki-K2-Plus/discussions
    - YouTube: youtube.md
    - Special Thanks: special-thanks.md
    - Firmwares:
        - Install & Update Firmware: firmwares/install-and-update-rooted-firmware-k2plus.md
        - Restore Previous Firmware: helper-script/restore-a-previous-firmware-k2plus.md
        - Reset Factory Settings: firmwares/reset-factory-settings.md
        - SSH Connection: firmwares/ssh-connection.md
        - Change Date & Time: firmwares/change-date-and-time.md
    - Helper Script for Creality K2 Plus:
        - Install Helper Script: helper-script/helper-script-installation.md
        - Install Menu:
            - Moonraker and Nginx: helper-script/moonraker-k2plus.md
            - Fans Control Macros: helper-script/fans-control-macros-k2plus.md
            - Improved Shapers Calibrations: helper-script/improved-shapers-calibrations-k2plus.md
            - Klipper Adaptive Meshing & Purging: helper-script/klipper-adaptive-meshing-and-purging-k2plus.md
            - Useful Macros: helper-script/useful-macros-k2plus.md
            - Save Z-Offset Macros: helper-script/save-z-offset-macros-k2plus.md
            - M600 Support: helper-script/m600-support-k2plus.md
            - Git Backup: helper-script/git-backup.md
            - Moonraker Timelapse: helper-script/moonraker-timelapse-k2plus.md
            - USB Camera Support: helper-script/usb-camera-support.md
            - OctoEverywhere: helper-script/octoeverywhere.md
            - Moonraker Obico: helper-script/moonraker-obico.md
            - GuppyFLO: helper-script/guppyflo.md
            - Mobileraker Companion: helper-script/mobileraker-companion-k2plus.md
            - OctoApp Companion: helper-script/octoapp-companion.md
            - SimplyPrint: helper-script/simplyprint-k2plus.md
            - CFS (Color Filament System): helper-script/cfs-k2plus.md
        - Customize Menu:
            - Remove & Restore Creality Web Interface: helper-script/remove-and-restore-creality-web-interface-k2plus.md
            - Guppy Screen: helper-script/guppy-screen.md
            - Creality Dynamic Logos for Fluidd: helper-script/creality-dynamic-logos-for-fluidd.md
        - Backup & Restore Menu:
            - Backup & Restore Klipper configuration files: helper-script/backup-and-restore-klipper-configuration-files.md
            - Backup & Restore Moonraker database: helper-script/backup-and-restore-moonraker-database-k2plus.md
        - Tools Menu:
            - Prevent & Allow updating Klipper configuration files: helper-script/prevent-and-allow-updating-klipper-configuration-files.md
            - Fix Printing Gcode files from Folder: helper-script/fix-printing-gcode-files-from-folder.md
            - Restore a previous Firmware: helper-script/restore-a-previous-firmware-k2plus.md
            - Reset Factory Settings: helper-script/reset-factory-settings.md
    - Configuration / Use:
        - Access to Web Interface: configurations/access-to-web-interface.md
        - Configure Camera: configurations/configure-camera.md
        - Change WiFi Location: configurations/change-wifi-location.md
    - Improvements:
        - Heated Chamber: improvements/heated-chamber-k2plus.md
        - Calibrate Extruder: improvements/calibrate-extruder.md
    - Others:
        - Files Location: others/files-location-k2plus.md
        - Useful Links: others/useful-links.md
    - Slicers:
        - OrcaSlicer: slicers/orcaslicer.md
    - STL Files:
        - Printables (Guilouz): https://www.printables.com/@Guilouz/models
        - Makerworld (Guilouz): https://makerworld.com/en/u/3879767814
        - Printables (Henlor): https://www.printables.com/fr/@Henlor_358992/models
"""

# Read existing mkdocs.yml and replace only the nav section
with open('mkdocs.yml', 'r') as f:
    content = f.read()

# Replace everything from 'nav:' to end of file
nav_start = content.find('\nnav:')
if nav_start == -1:
    nav_start = content.find('nav:')
    preamble = content[:nav_start]
else:
    preamble = content[:nav_start + 1]  # keep the newline before nav:

with open('mkdocs.yml', 'w') as f:
    f.write(preamble + new_nav)

print("\n✓ mkdocs.yml rewritten — K2 Plus only nav")

# ============================================================
# Update index.md
# ============================================================
index_content = """# Creality K2 Plus — Helper Script Wiki

This wiki covers the full process to root the **Creality K2 Plus** and **K2 Plus Combo** and add features using the Creality Helper Script.

The advantage is having full access to the firmware and configuration files to make changes.

!!! warning "K2 Plus specific"
    This wiki is written specifically for the **Creality K2 Plus** and **K2 Plus Combo**.
    For K1 Series or Ender-3 V3 Series, see the [original wiki](https://guilouz.github.io/Creality-Helper-Script-Wiki/).

!!! danger "Read before proceeding"
    If you don't know what you're doing, I don't recommend following this guide.
    Rooting your printer and modifying system files can cause issues if done incorrectly.

---

## Key Differences from K1 Series

| Item | K1 Series | K2 Plus |
|---|---|---|
| Persistent data path | `/usr/data/` | `/mnt/UDISK/` |
| Root password | `creality_2023` | `creality_2024` |
| Service manager | Supervisor Lite | OpenWrt rc.d |
| Restart services | `supervisorctl restart` | `/etc/init.d/S55klipper restart` |
| Fluidd pre-installed | No | **Yes** (port 4408) |
| Chamber heater | No | **Yes** (heater_generic) |
| Multi-material (CFS) | No | **Yes** (Combo model) |
| Accelerometer | ADXL345 | LIS2DW |
| Kinematics | CoreXY | CoreXY |
| Print volume | 220×220×250 (K1) | **350×350×360** |

---

## Wiki

Guide is available here: [Wiki](https://sw3defy.github.io/Creality-Helper-Script-Wiki-K2-Plus/)
"""

with open('docs/index.md', 'w') as f:
    f.write(index_content)

print("✓ docs/index.md updated for K2 Plus")
print("\nAll done! Run: git add . && git commit -m 'Strip K1/Ender-3 content, K2 Plus only'")