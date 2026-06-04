import os

files = {}

files["docs/firmwares/install-and-update-rooted-firmware-k2plus.md"] = """# Install & Update Firmware — K2 Plus

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
"""

files["docs/others/files-location-k2plus.md"] = """# Files Location — K2 Plus

All persistent data on the K2 Plus lives under `/mnt/UDISK/`. There is no `/usr/data/` path — this differs from the K1 Series.

---

## Klipper & Printer Data

| Resource | Path |
|---|---|
| Klipper configuration files | `/mnt/UDISK/printer_data/config/` |
| GCode files | `/mnt/UDISK/printer_data/gcodes/` |
| Klipper log | `/mnt/UDISK/printer_data/logs/klippy.log` |
| Moonraker log | `/mnt/UDISK/printer_data/logs/moonraker.log` |
| Moonraker database | `/mnt/UDISK/printer_data/` |
| Moonraker timelapse videos | `/mnt/UDISK/printer_data/timelapse/` |

---

## Creality System Data

| Resource | Path |
|---|---|
| System config | `/mnt/UDISK/creality/userdata/config/system_config.json` |
| Creality timelapse videos | `/mnt/UDISK/creality/userdata/delay_image/video/` |
| AI image data | `/mnt/UDISK/ai_image/` |
| Layer image data | `/mnt/UDISK/layers_image/` |

---

## Read-Only System Paths

These paths live on a read-only partition and **cannot be edited in place**.

| Resource | Path |
|---|---|
| Klipper Python env | `/usr/share/klippy-env/bin/python` |
| Klipper source | `/usr/share/klipper/klippy/klippy.py` |
| Klipper config templates | `/usr/share/klipper/config/F008_CR0CN240319C13_1/` |
| Moonraker Python env | `/usr/share/moonraker-env/bin/python` |
| Moonraker source | `/usr/share/moonraker/` |
| Moonraker config | `/usr/share/moonraker/moonraker.conf` |
| Fluidd static files | `/usr/share/fluidd/` |
| Nginx config | `/etc/nginx/nginx.conf` |

---

## Service Scripts

The K2 Plus uses OpenWrt-style rc.d init scripts. There is no `systemd` or `supervisord`.

| Service | Script |
|---|---|
| Klipper MCU bridge | `/etc/init.d/S54klipper_mcu` |
| Klipper (klippy) | `/etc/init.d/S55klipper` |
| Moonraker | `/etc/init.d/S56moonraker` |
| Nginx | `/etc/init.d/S80nginx` |
| WebRTC (camera) | `/etc/init.d/S97webrtc` |

To restart a service over SSH:

```bash
/etc/init.d/S55klipper restart
/etc/init.d/S56moonraker restart
/etc/init.d/S80nginx restart
```

!!! note "No supervisorctl on K2 Plus"
    The `supervisorctl` command is not available. Use the rc.d init scripts above instead.
"""

files["docs/helper-script/moonraker-k2plus.md"] = """# Moonraker and Nginx — K2 Plus

!!! warning "K2 Plus differs significantly from K1"
    On the K1 Series, Moonraker and Nginx are installed by the helper script. On the K2 Plus, **both are pre-installed from the factory firmware** and run from the read-only `/usr/share/` partition. Instead of installing from scratch, you are **extending** the stock installation.

---

## What Ships From the Factory

| Component | Details |
|---|---|
| Fluidd | Served at `http://<printer-ip>:4408`, static files at `/usr/share/fluidd/` |
| Moonraker | Running at `127.0.0.1:7125`, config at `/usr/share/moonraker/moonraker.conf` |
| Nginx | Config at `/etc/nginx/nginx.conf`, single-file (no `conf.d/` directory) |
| Klipper | Config at `/mnt/UDISK/printer_data/config/printer.cfg` |

Verify all four are running over SSH:

```bash
ps aux | grep -E 'klipper|moonraker|nginx' | grep -v grep
```

---

## Moonraker Config Location

!!! danger "Do not edit /usr/share/moonraker/moonraker.conf directly"
    This file is on the read-only system partition and will be **overwritten on every firmware update**.

The stock config has no `[update_manager]` or `[timelapse]` section, and `[machine]` is set to `provider: none` — meaning reboot/shutdown buttons in Fluidd do not work by default.

---

## Extending Moonraker with Include Files

The helper script writes persistent config to:

```
/mnt/UDISK/printer_data/config/moonraker.conf
```

From the `[Install] Menu` install **Moonraker Extensions**. The script will:

1. Write `/mnt/UDISK/printer_data/config/moonraker.conf` with the `[update_manager]` section.
2. Patch the Moonraker startup to load the include file.
3. Restart Moonraker via `/etc/init.d/S56moonraker restart`.

---

## Restarting Services

```bash
/etc/init.d/S56moonraker restart
/etc/init.d/S55klipper restart
/etc/init.d/S80nginx restart
/etc/init.d/S54klipper_mcu restart
```

!!! note "No supervisorctl on K2 Plus"
    The `supervisorctl` command is not available. Use the rc.d init scripts above.

---

## Host Control Support

By default the Reboot and Shutdown buttons in Fluidd do nothing because `[machine]` provider is `none`. Install **Host Control Support** from the `[Install] Menu` to enable them.

---

## Adding Mainsail

Mainsail is not pre-installed. See [Mainsail](mainsail.md) to add it on port `4409`.
"""

files["docs/helper-script/fans-control-macros-k2plus.md"] = """# Fans Control Macros — K2 Plus

The K2 Plus has a more complex fan topology than the K1 Series. There are three independently controllable output fans, a hotend cooling fan (automatic), and a chamber fan system.

!!! note "K2 Plus fan map differs from K1"
    The K1 Series has a part cooling fan and a nozzle cleaning fan. The K2 Plus has no nozzle cleaning fan.

---

## Fan Hardware Map

| Fan | Klipper name | Pin | Type | Notes |
|---|---|---|---|---|
| Hotend (heatsink) | `hotend_fan` | `nozzle_mcu:PB7` + `PB1` | `heater_fan` | Auto — on when extruder > 50°C |
| Part cooling | `fan0` | `nozzle_mcu:PB15` | `output_pin` PWM | Controlled by slicer `M106/M107` |
| Chamber cooling | `chamber_fan` | `PA0` | `temperature_fan` | Auto watermark at 35°C target |
| Aux fan | `fan2` | `PB4` + `PB3` | `output_pin` PWM | Electronics bay cooling |
| Chamber heater fan | `chamber_fan` (heater companion) | `!PB14`, enable `PB2` | `heater_fan` | Tied to `chamber_heater` |

!!! note "fan0_en"
    `output_pin fan0_en` on `nozzle_mcu:PB6` acts as an enable gate for the part cooling fan. The helper script macros manage this automatically.

---

## Controlling Fans via Macros

From the `[Install] Menu` install **Fans Control Macros**.

### Part cooling fan

```gcode
SET_FAN0 S=255    ; full speed
SET_FAN0 S=128    ; 50%
SET_FAN0 S=0      ; off
```

### Aux fan

```gcode
SET_FAN2 S=255
SET_FAN2 S=0
```

### Chamber temperature target

```gcode
SET_TEMPERATURE_FAN_TARGET TEMPERATURE_FAN=chamber_fan TARGET=40
```

### Chamber heater

```gcode
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=40
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=0
```

---

## Notes on duplicate_pin_override

The K2 Plus `printer.cfg` contains a large `[duplicate_pin_override]` section because several pins are shared between fan definitions. Do not remove this section — Klipper will refuse to start.
"""

files["docs/helper-script/improved-shapers-calibrations-k2plus.md"] = """# Improved Shapers Calibrations — K2 Plus

The K2 Plus uses a **LIS2DW** accelerometer connected via SPI to the nozzle MCU. This differs from the K1 Series which uses an ADXL345.

---

## Hardware Details

| Item | Value |
|---|---|
| Accelerometer chip | LIS2DW |
| Interface | SPI (software) |
| CS pin | `nozzle_mcu:PA4` |
| SCLK | `nozzle_mcu:PA5` |
| MOSI | `nozzle_mcu:PA7` |
| MISO | `nozzle_mcu:PA6` |
| Axes map | `x, z, y` |

Your calibrated input shaper values:

```ini
[input_shaper]
shaper_type_x = ei
shaper_freq_x = 39.2
shaper_type_y = zv
shaper_freq_y = 42.0
```

---

## Installation

From the `[Install] Menu` install **Improved Shapers Calibrations**.

---

## Running Resonance Tests

!!! warning "Home the printer first"

```gcode
SHAPER_CALIBRATE AXIS=X
SHAPER_CALIBRATE AXIS=Y
SHAPER_CALIBRATE
```

After calibration completes:

```gcode
SAVE_CONFIG
```

---

## Belt Tension Check

Target tension for both X and Y belts is **140 N** (configured in `printer.cfg`). Re-run shaper calibration after any belt adjustment.
"""

files["docs/helper-script/klipper-adaptive-meshing-and-purging-k2plus.md"] = """# Klipper Adaptive Meshing & Purging — K2 Plus

KAMP generates a bed mesh only over the area being printed, reducing leveling time significantly on the large 350x350mm bed.

---

## K2 Plus Bed Mesh Configuration

```ini
[bed_mesh]
mesh_min: 5, 5
mesh_max: 345, 345
probe_count: 9, 9
```

KAMP generates an adaptive sub-mesh within these bounds based on your print's actual footprint.

---

## Installation

From the `[Install] Menu` install **Klipper Adaptive Meshing & Purging**.

Files are written to `/mnt/UDISK/printer_data/config/`.

!!! note "K2 Plus path"
    KAMP config files use `/mnt/UDISK/printer_data/config/` — not `/usr/data/` as on K1.

---

## Enabling Object Processing

KAMP requires Moonraker's object processing. The helper script adds this to `/mnt/UDISK/printer_data/config/moonraker.conf`:

```ini
[file_manager]
enable_object_processing: True
```

---

## Using KAMP in START_PRINT

```gcode
G28
BED_MESH_CALIBRATE
LINE_PURGE
```

### Purge options

- `LINE_PURGE` — draws a purge line at the edge of the print area. Recommended for single-material prints.
- For **CFS multi-material prints**, the CFS macros handle purging via the purge chute. Do not use `LINE_PURGE` during CFS tool changes.
"""

files["docs/helper-script/cfs-k2plus.md"] = """# CFS — Color Filament System (K2 Plus Combo)

!!! note "Combo only"
    This page applies to the **K2 Plus Combo**. If you have the standalone K2 Plus without the CFS, this hardware is not present.

---

## How the CFS Works in Klipper

The CFS communicates over a dedicated RS-485 serial bus and is exposed through a custom `[box]` module. Config is split across two files:

| File | Location | Purpose |
|---|---|---|
| `box.cfg` | `/mnt/UDISK/printer_data/config/box.cfg` | All CFS hardware config and macros |
| `printer.cfg` | `/mnt/UDISK/printer_data/config/printer.cfg` | Includes `box.cfg` via `[include box.cfg]` |

Key hardware config:

```ini
[serial_485 serial485]
serial: /dev/ttyS5
baud: 230400

[box]
bus: serial485
filament_sensor: filament_sensor
```

---

## Filament Slot Addressing

Filaments use `TxY` notation:

- **x** = unit number (1–4)
- **Y** = slot letter (A, B, C, D)

Examples: `T1A`, `T1B`, `T2C`, `T4D`

---

## Filament Change Sequence

1. Pre-op — move to safe Z height
2. Move to cut position (X=10, Y=200)
3. Cut — cutter fires at calibrated `cut_pos_x`
4. Retract — pulls filament back to CFS unit
5. Load new filament — feeds new filament to toolhead
6. Purge — extrudes at purge position (X=133–160, Y=378)
7. End-op — restore fans, move to safe position

---

## Calibrated Cut Position

Your printer's calibrated cut position (from SAVE_CONFIG):

```ini
[box]
cut_pos_x = -7.40
```

!!! warning "Do not remove the SAVE_CONFIG block"
    If you wipe this block or restore factory settings, re-run the cutter calibration from the touchscreen before using the CFS.

---

## Key Macros

| Macro | Purpose |
|---|---|
| `BOX_LOAD_MATERIAL` | Full load sequence |
| `BOX_QUIT_MATERIAL` | Full unload sequence |
| `M8200 P` | Pre-op |
| `M8200 C` | Execute cut |
| `M8200 R` | Retract filament to CFS |
| `M8200 L I=[slot]` | Load filament from slot (0-based) |
| `M8200 F` | Purge/flush |
| `M8200 O` | End-op |

---

## Troubleshooting

**CFS not responding**
- Verify RS-485 cable is seated on both CFS unit and mainboard.
- Check `/dev/ttyS5` is present: `ls /dev/ttyS*`
- Restart Klipper: `/etc/init.d/S55klipper restart`

**Cut position error after factory reset**
- Re-run cutter calibration from **Settings → CFS → Cutter Calibration**.
"""

files["docs/helper-script/useful-macros-k2plus.md"] = """# Useful Macros — K2 Plus

!!! note "K1 macros are not compatible"
    Do not copy K1 Series macros to the K2 Plus. Fan pin names, chamber references, and bed dimensions all differ.

---

## Installation

From the `[Install] Menu` install **Useful Macros**.

Macros are written to `/mnt/UDISK/printer_data/config/useful_macros.cfg`.

---

## START_PRINT

| Parameter | Default | Description |
|---|---|---|
| `BED_TEMP` | 60 | Bed target temperature |
| `EXTRUDER_TEMP` | 200 | Extruder target temperature |
| `CHAMBER_TEMP` | 0 | Chamber target (0 = no pre-heat) |

Slicer start G-code:

```gcode
START_PRINT BED_TEMP=[bed_temperature_initial_layer_single] EXTRUDER_TEMP=[nozzle_temperature_initial_layer] CHAMBER_TEMP=[chamber_temperature]
```

What it does:

1. Homes all axes (`G28`)
2. Performs Z-tilt adjustment (`Z_TILT_ADJUST`) — required for dual-Z
3. If `CHAMBER_TEMP > 0`: starts chamber heater and waits
4. Waits for bed temperature
5. Heats nozzle to 80% to avoid ooze during leveling
6. Runs KAMP adaptive bed mesh
7. Heats nozzle to full temperature
8. Runs purge line
9. Starts print

---

## END_PRINT

1. Turns off all heaters including `chamber_heater`
2. Moves toolhead to safe park position
3. Disables steppers (except Z)
4. Turns off fans
5. Presents the part (moves bed forward)

---

## Z_TILT_ADJUST Note

The K2 Plus has two independent Z stepper motors and **requires `Z_TILT_ADJUST` before every print**. Do not remove this call from `START_PRINT`.

---

## RELOAD_CAMERA

Restarts the WebRTC camera service without rebooting:

```gcode
RELOAD_CAMERA
```

Calls `/etc/init.d/S97webrtc restart`. Requires [Klipper Gcode Shell Command](klipper-gcode-shell-command.md).
"""

files["docs/helper-script/save-z-offset-macros-k2plus.md"] = """# Save Z-Offset Macros — K2 Plus

The K2 Plus uses a `prtouch_v3` strain-gauge probe. Z-offset is stored in the `SAVE_CONFIG` block of `/mnt/UDISK/printer_data/config/printer.cfg`.

---

## Installation

From the `[Install] Menu` install **Save Z-Offset Macros**.

---

## Usage

Adjust Z-offset live during a print using babystepping, then save permanently:

```gcode
SAVE_Z_OFFSET
```

To set a specific value:

```gcode
SET_GCODE_OFFSET Z=0.05
SAVE_Z_OFFSET
```

---

## Notes on prtouch_v3

The K2 Plus probe uses temperature compensation (`enable_not_linear_comp: True`). Z-offset can shift slightly between cold and hot starts — this is normal. Let the printer reach full print temperature before running `Z_TILT_ADJUST` and `BED_MESH_CALIBRATE` if you notice first-layer variation.
"""

files["docs/helper-script/m600-support-k2plus.md"] = """# M600 Support — K2 Plus

M600 is the standard filament change G-code. Behavior differs depending on whether you are using single-filament mode or the CFS.

---

## Installation

From the `[Install] Menu` install **M600 Support**.

Config is written to `/mnt/UDISK/printer_data/config/m600.cfg`.

---

## Single-Filament Mode

`M600` triggers a pause, parks the toolhead, retracts, and waits for manual filament swap. Resume with `RESUME`.

---

## CFS Mode (K2 Plus Combo)

When the CFS is active, tool changes at boundaries are handled automatically by the `M8200` macro sequence. See [CFS](cfs-k2plus.md).

For unplanned runout during a CFS print, `BOX_CHECK_MATERIAL_REFILL` handles recovery automatically if a backup spool is loaded.
"""

files["docs/helper-script/moonraker-timelapse-k2plus.md"] = """# Moonraker Timelapse — K2 Plus

Moonraker Timelapse captures a frame at each layer change to create a timelapse of your print.

---

## Installation

From the `[Install] Menu` install **Moonraker Timelapse**.

---

## Timelapse Video Location

```
/mnt/UDISK/printer_data/timelapse/
```

!!! note "Path difference from K1"
    On K1 timelapse videos are at `/usr/data/printer_data/timelapse/`. On K2 Plus: `/mnt/UDISK/printer_data/timelapse/`.

Download via Fluidd's file manager or SCP:

```bash
scp root@<printer-ip>:/mnt/UDISK/printer_data/timelapse/my_print.mp4 ./
```

---

## Slicer Setup

Layer change G-code:

```gcode
TIMELAPSE_TAKE_FRAME
```

End G-code:

```gcode
TIMELAPSE_RENDER
```
"""

files["docs/helper-script/mobileraker-companion-k2plus.md"] = """# Mobileraker Companion — K2 Plus

Mobileraker Companion enables push notifications for Klipper using Moonraker.

---

## Installation

From the `[Install] Menu` install **Mobileraker Companion**.

---

## Known Issue — HeaterFan Parse Error

!!! warning "Known compatibility issue"
    There is a known crash in Mobileraker when connecting to a K2 Plus. The K2 Plus `printer.cfg` uses a `[heater_fan]` configuration that Mobileraker's printer builder does not handle correctly:

    ```
    Found _$HeaterFanImpl, parentException: null
    ```

    **Status:** Open issue in the Mobileraker project. Check for an updated release before installing. The companion daemon installs and runs correctly — the issue is in the mobile app's parsing of the K2 Plus fan configuration.

---

## Configuration

After installation, companion config is at:

```
/mnt/UDISK/printer_data/config/mobileraker.conf
```

Restart with:

```bash
/etc/init.d/S56moonraker restart
```
"""

files["docs/helper-script/simplyprint-k2plus.md"] = """# SimplyPrint — K2 Plus

!!! warning "Use the K2-specific guide"
    Do not follow the K1/K1C SimplyPrint setup guide for a K2 Plus.

[SimplyPrint K2 Series Setup Guide :material-open-in-new:](https://simplyprint.io/setup-guide/creality/k2){ .md-button }

---

## SSH Root Access

- **User:** `root`
- **Password:** `creality_2024`

---

## Data Path Note

If the installer asks for the printer data path or Moonraker config location, use:

```
/mnt/UDISK/printer_data/
```

Not `/usr/data/printer_data/` as in the K1 guide.
"""

files["docs/helper-script/restore-a-previous-firmware-k2plus.md"] = """# Restore a Previous Firmware — K2 Plus

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
"""

files["docs/improvements/heated-chamber-k2plus.md"] = """# Heated Chamber — K2 Plus

The K2 Plus has an actively heated chamber with a dedicated PTC heater element.

---

## Hardware Overview

| Component | Klipper name | Pin | Type |
|---|---|---|---|
| Chamber heater | `chamber_heater` | `PC12` | `heater_generic` |
| Chamber temp sensor | `chamber_temp` | `PC5` | EPCOS 100K |
| Chamber cooling fan | `chamber_fan` | `PA0` | PWM watermark |
| PTC companion fan | `chamber_fan` (heater_fan) | `!PB14`, enable `PB2` | Auto with heater |

---

## Temperature Ranges

| Setting | Value |
|---|---|
| Chamber heater max | 80°C |
| Cooling fan target | 35°C |

!!! warning "80°C is the hard maximum"
    Setting a target above 80°C will cause Klipper to shut down.

---

## Recommended Temperatures by Material

| Material | Chamber temp |
|---|---|
| PLA | Off |
| PETG | 30–40°C |
| ABS | 45–55°C |
| ASA | 45–55°C |
| PA (Nylon) | 50–60°C |
| PC | 55–70°C |

---

## Controlling the Chamber

```gcode
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=45
TEMPERATURE_WAIT SENSOR="heater_generic chamber_heater" MINIMUM=43
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=0
```

---

## PTC Power Pin

The `ptc_power` output pin (`PB2`, default value `1`) keeps the PTC circuit enabled. Do not set this to `0` during printing.
"""

# Write all files
for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.lstrip())
    print(f"OK {path}")

print("\\nAll files created successfully!")