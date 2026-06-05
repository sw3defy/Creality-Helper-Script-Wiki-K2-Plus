# Install Menu

---

# Moonraker and Nginx — K2 Plus

!!! warning "K2 Plus differs significantly from K1"
    On the K1 Series, Moonraker and Nginx are installed by the helper script. On the K2 Plus, **both are pre-installed from the factory firmware** and run from the read-only `/usr/share/` partition. The approach here is therefore fundamentally different: instead of installing from scratch, you are **extending** the stock installation.

---

## What Ships From the Factory

The K2 Plus comes with the following already running:

| Component | Details |
|---|---|
| Fluidd | Served at `http://<printer-ip>:4408`, static files at `/usr/share/fluidd/` |
| Moonraker | Running at `127.0.0.1:7125`, config at `/usr/share/moonraker/moonraker.conf` |
| Nginx | Config at `/etc/nginx/nginx.conf`, single-file (no `conf.d/` directory) |
| Klipper | Running via `/usr/share/klippy-env/`, config at `/mnt/UDISK/printer_data/config/printer.cfg` |

You can verify all four are running over SSH:

```bash
ps aux | grep -E 'klipper|moonraker|nginx' | grep -v grep
```

---

## Architecture Overview

```
Browser → nginx (port 4408)
              ├── / → /usr/share/fluidd/          (static Fluidd files)
              ├── /websocket → 127.0.0.1:7125      (Moonraker WebSocket)
              ├── /printer|api|access|machine|server → 127.0.0.1:7125  (Moonraker REST)
              └── /webcam/ → 127.0.0.1:8080        (WebRTC/MJPEG streams)

Moonraker (7125) → /tmp/klippy_uds → Klipper (klippy.py)
```

Mainsail is not pre-installed. See [Mainsail](mainsail.md) to add it on port `4409`.

---

## Moonraker Config Location

The stock Moonraker config is at `/usr/share/moonraker/moonraker.conf` on the **read-only system partition**.

!!! danger "Do not edit /usr/share/moonraker/moonraker.conf directly"
    This file is on the read-only system partition and will be **overwritten on every firmware update**. Any changes made directly to this file will be lost. Use the helper script approach to apply persistent changes.

The stock config includes:

- `[machine]` with `provider: none` — meaning Moonraker has no system service management capability. Reboot/shutdown buttons in Fluidd will not work without Host Control Support (see below).
- No `[update_manager]` section — the Update Manager panel in Fluidd is empty by default.
- No `[timelapse]` component — see [Moonraker Timelapse](moonraker-timelapse-k2plus.md) to add it.

---

## Extending Moonraker with Include Files

Because the stock config is read-only, the helper script adds a persistent include directive by patching the moonraker startup. Additional config is written to:

```
/mnt/UDISK/printer_data/config/moonraker.conf
```

This file survives firmware updates because it lives on `/mnt/UDISK/`.

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the script's `[Install] Menu` install **Moonraker Extensions**:

The script will:

1. Write `/mnt/UDISK/printer_data/config/moonraker.conf` with the `[update_manager]` section and any additional components you enable.
2. Patch the Moonraker startup to load the include file.
3. Restart Moonraker via `/etc/init.d/S56moonraker restart`.

---

## Restarting Services

The K2 Plus uses OpenWrt rc.d init scripts. There is **no `supervisorctl`** command (unlike K1).

```bash
# Restart Moonraker
/etc/init.d/S56moonraker restart

# Restart Klipper
/etc/init.d/S55klipper restart

# Restart Nginx
/etc/init.d/S80nginx restart

# Restart the low-level MCU bridge
/etc/init.d/S54klipper_mcu restart
```

---

## Host Control Support

By default, the Reboot and Shutdown buttons in Fluidd do nothing on the K2 Plus because Moonraker's `[machine]` provider is set to `none`.

The helper script installs a lightweight host control shim that intercepts these commands and routes them to the appropriate system call.

Install it from the `[Install] Menu` → **Host Control Support**.

Once installed, reboot/shutdown from the Fluidd power menu will work correctly.

---

## Adding Mainsail

Mainsail is not pre-installed. To add it on port `4409`, see [Mainsail](mainsail.md). The helper script adds a second `server` block to the nginx config for Mainsail alongside the existing Fluidd block.

---

## Update Manager

Once the helper script has written `/mnt/UDISK/printer_data/config/moonraker.conf` with the `[update_manager]` section, the Update Manager panel in Fluidd will become active and show available updates for:

- Creality Helper Script itself
- Any additional components you have installed (Fluidd update, Mainsail, timelapse plugin, etc.)

Updates performed via Update Manager do **not** affect the firmware itself or the read-only `/usr/share/` partitions.


---

# Fluidd — K2 Plus

Fluidd is the primary web interface on the K2 Plus, pre-installed at port `4408` from the factory. This page covers updating, repairing, and restoring Fluidd using the Helper Script.

!!! note "Pre-installed"
    You do not need to install Fluidd — it ships with the K2 Plus. This page is for updating to the latest version or repairing a broken installation.

---

## Access Fluidd

Open your browser and navigate to:

```
http://<printer-ip>:4408
```

Replace `<printer-ip>` with your printer's IP address (found in **Settings → Network** on the touchscreen).

---

## Update / Repair Fluidd

From the helper script menu, select **option 8 — Fluidd (install/update/repair)**. 

When Fluidd is already installed you will be offered:

- **Update** — download and install the latest release
- **Repair** — re-download and reinstall the current latest (fixes corrupted files)
- **Restore nginx block only** — fixes port 4408 access without re-downloading Fluidd

---

## Manual Update via SSH

```bash
# Download latest Fluidd
wget -O /tmp/fluidd.zip https://github.com/fluidd-core/fluidd/releases/latest/download/fluidd.zip

# Install
mkdir -p /usr/share/fluidd
unzip -q -o /tmp/fluidd.zip -d /usr/share/fluidd
rm /tmp/fluidd.zip

# Restart nginx
/etc/init.d/S80nginx restart
```

---

## Fluidd Configuration

Key Fluidd settings are stored in Moonraker. Once Moonraker Extensions are installed, configure Fluidd from **Settings** in the web interface.

### Camera Setup

If the camera is not visible in Fluidd after opening the interface:

- Go to **Settings → Cameras**
- Enable the existing camera entry, or delete and recreate with:
    - **URL Stream:** `http://<printer-ip>:4408/webcam/?action=stream`
    - **URL Snapshot:** `http://<printer-ip>:4408/webcam/?action=snapshot`

---

## Nginx Configuration

Fluidd is served by nginx from `/usr/share/fluidd/` on port `4408`. The nginx config is at `/etc/nginx/nginx.conf`.

The K2 Plus nginx config proxies all Moonraker API requests (`/printer/`, `/api/`, `/machine/`, etc.) to `127.0.0.1:7125`, and webcam streams to `127.0.0.1:8080–8083`.

!!! warning "Do not edit nginx.conf directly"
    `/etc/nginx/nginx.conf` is on the writable partition but the Helper Script backs it up before modifying it. If you edit it manually and break nginx, restore the backup:
    ```bash
    cp /mnt/UDISK/helper-script/.nginx.conf.bak /etc/nginx/nginx.conf
    /etc/init.d/S80nginx restart
    ```


---

# Mainsail — K2 Plus

Mainsail is an alternative web interface to Fluidd. It is not pre-installed on the K2 Plus but can be added by the Helper Script on port `4409`, running alongside the stock Fluidd installation.

---

## Installation

From the helper script menu, select **option 9 — Mainsail (port 4409)**.

The script will:
1. Download the latest Mainsail release
2. Install static files to `/usr/share/mainsail/`
3. Add a new nginx server block for port `4409`
4. Restart nginx

---

## Access Mainsail

After installation:

```
http://<printer-ip>:4409
```

---

## Update / Repair Mainsail

Run the helper script and select option 9 again. If Mainsail is already installed you will be offered:

- **Update** — download and install the latest release
- **Repair** — re-download and reinstall
- **Restore nginx block only** — restore port 4409 without re-downloading

---

## Fluidd vs Mainsail

Both interfaces connect to the same Moonraker instance and offer equivalent functionality. Key differences:

| Feature | Fluidd | Mainsail |
|---|---|---|
| Port | 4408 (pre-installed) | 4409 (helper script) |
| UI style | Clean, dashboard-focused | Feature-rich, more settings |
| Timelapse UI | Via plugin | Built-in |
| Spoolman | Via plugin | Built-in |

You can use both simultaneously — they share the same Moonraker backend and printer state.

---

## Mainsail Configuration

Mainsail stores its configuration in `mainsail.cfg`. After installation, add this include to your `printer.cfg` if you want Mainsail-specific features:

```bash
# From SSH
echo "[include mainsail.cfg]" >> /mnt/UDISK/printer_data/config/printer.cfg
```

Or add it via the Fluidd/Mainsail editor.


---

# Fans Control Macros — K2 Plus

The K2 Plus has a more complex fan topology than the K1 Series. There are three independently controllable output fans, a hotend cooling fan (automatic), and a chamber fan that doubles as both a cooling `temperature_fan` and a PTC heater companion. This page documents what each fan does, how to control them, and what the helper script macros provide.

!!! note "K2 Plus fan map differs from K1"
    The K1 Series has a part cooling fan and a nozzle cleaning fan. The K2 Plus has no nozzle cleaning fan. Do not apply K1 fan macro configs to the K2 Plus.

---

## Fan Hardware Map

| Fan | Klipper name | Pin | Type | Notes |
|---|---|---|---|---|
| Hotend (heatsink) | `hotend_fan` | `nozzle_mcu:PB7` + `PB1` | `heater_fan` | Auto — on when extruder > 50°C |
| Part cooling | `fan0` | `nozzle_mcu:PB15` | `output_pin` PWM | Controlled by slicer `M106/M107` |
| Chamber cooling | `chamber_fan` | `PA0` | `temperature_fan` | Auto watermark at 35°C target |
| Aux fan | `fan2` | `PB4` + `PB3` | `output_pin` PWM | Electronics bay / aux cooling |
| Chamber heater fan (PTC) | `chamber_fan` (heater companion) | `PB14` (inverted) | `heater_fan` | Tied to `chamber_heater`, enable pin `PB2` |

!!! note "fan0_en"
    There is an additional `output_pin fan0_en` on `nozzle_mcu:PB6` which acts as an enable gate for the part cooling fan circuit. The helper script macros manage this automatically — do not drive `fan0` without first ensuring `fan0_en` is high.

---

## Controlling Fans via Macros

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **Fans Control Macros**.

The installed macros give you named controls usable from Fluidd, Mainsail, or G-code:

### Part cooling fan (`fan0`)

```gcode
SET_FAN0 S=255        ; full speed (255 = 100%)
SET_FAN0 S=128        ; 50%
SET_FAN0 S=0          ; off
```

The slicer's standard `M106 S[value]` also controls `fan0` directly.

### Aux fan (`fan2`)

```gcode
SET_FAN2 S=255
SET_FAN2 S=0
```

### Chamber temperature target

The chamber fan runs in `watermark` control mode with a default target of `35°C`. To raise or lower the cooling setpoint:

```gcode
SET_TEMPERATURE_FAN_TARGET TEMPERATURE_FAN=chamber_fan TARGET=40
```

### Chamber heater

The chamber heater is a `heater_generic` named `chamber_heater`. Set target temperature:

```gcode
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=40   ; heat to 40°C
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=0    ; off
```

The PTC heater companion fan (`chamber_fan` heater_fan) runs automatically when `chamber_heater` is active and the heater exceeds the configured threshold.

---

## Useful Macros Added by Helper Script

| Macro | Purpose |
|---|---|
| `SAVE_FANS` | Saves current fan speeds to variables |
| `RESTORE_FANS` | Restores previously saved fan speeds |
| `FANS_OFF` | Turns off all output fans (does not affect `hotend_fan` autocontrol) |
| `CHAMBER_HEAT TARGET=` | Sets `chamber_heater` target and waits if `WAIT=1` |
| `CHAMBER_COOL` | Disables chamber heater, sets cooling fan to full speed |

These are particularly useful in `START_PRINT` and `END_PRINT` macros — the helper script's [Useful Macros](useful-macros-k2plus.md) page shows complete START/END examples that include chamber pre-heat.

---

## START_PRINT Chamber Pre-heat Example

For materials requiring a warm chamber (ABS, ASA, PA), add chamber pre-heating to your `START_PRINT`:

```gcode
[gcode_macro START_PRINT]
gcode:
  {% set BED_TEMP = params.BED_TEMP|default(60)|float %}
  {% set EXTRUDER_TEMP = params.EXTRUDER_TEMP|default(200)|float %}
  {% set CHAMBER_TEMP = params.CHAMBER_TEMP|default(0)|float %}

  ; Heat bed first
  M140 S{BED_TEMP}

  ; If a chamber temp is requested, start heating the chamber now
  {% if CHAMBER_TEMP > 0 %}
    SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET={CHAMBER_TEMP}
  {% endif %}

  M190 S{BED_TEMP}           ; wait for bed

  ; Wait for chamber if needed
  {% if CHAMBER_TEMP > 0 %}
    TEMPERATURE_WAIT SENSOR="heater_generic chamber_heater" MINIMUM={CHAMBER_TEMP - 2}
  {% endif %}

  M109 S{EXTRUDER_TEMP}      ; wait for extruder
  ; ... homing, leveling, purge, print start
```

---

## Notes on `duplicate_pin_override`

The K2 Plus `printer.cfg` contains a large `[duplicate_pin_override]` section because several pins are shared between the `temperature_fan`, `heater_fan`, and `output_pin` definitions (most notably `PA0` and `PC5`). Do not remove this section — Klipper will refuse to start if shared pins are not declared in `duplicate_pin_override`.

```ini
[duplicate_pin_override]
pins: PC5,PA0,PC7,PB7,PB8,PB9,PB10,PB5,PB6,PA1,PB15,PB11,PB12,PB13,PA10,PA9,PB2,PB14,PB1
```


---

# Useful Macros — K2 Plus

The helper script installs a set of commonly used macros adapted for the K2 Plus hardware. These replace the K1 Series macro set and account for the K2 Plus's dual-Z, actively heated chamber, CoreXY kinematics, and CFS.

!!! note "K1 macros are not compatible"
    Do not copy K1 Series macros to the K2 Plus. Fan pin names, chamber references, and bed dimensions all differ.

---

## Installation

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **Useful Macros**.

Macros are written to `/mnt/UDISK/printer_data/config/useful_macros.cfg` and included from `printer.cfg`.

---

## START_PRINT

The installed `START_PRINT` macro accepts the following parameters from your slicer:

| Parameter | Default | Description |
|---|---|---|
| `BED_TEMP` | 60 | Bed target temperature |
| `EXTRUDER_TEMP` | 200 | Extruder target temperature |
| `CHAMBER_TEMP` | 0 | Chamber target (0 = no chamber pre-heat) |
| `FILAMENT_TYPE` | PLA | Used to set sensible defaults |

### What it does

1. Homes all axes (`G28`)
2. Performs Z-tilt adjustment (`Z_TILT_ADJUST`) — K2 Plus has dual Z motors
3. If `CHAMBER_TEMP > 0`: starts chamber heater and waits for temperature
4. Waits for bed temperature (`M190`)
5. Heats nozzle to 80% to avoid ooze during leveling (`M109 S{temp * 0.8}`)
6. Runs KAMP adaptive bed mesh (`BED_MESH_CALIBRATE`) if enabled
7. Heats nozzle to full temperature (`M109`)
8. Runs purge line (`LINE_PURGE`) at print boundary
9. Starts print

### Slicer start G-code

In OrcaSlicer (or any Klipper-aware slicer), set your machine start G-code to:

```gcode
START_PRINT BED_TEMP=[bed_temperature_initial_layer_single] EXTRUDER_TEMP=[nozzle_temperature_initial_layer] CHAMBER_TEMP=[chamber_temperature]
```

---

## END_PRINT

```gcode
END_PRINT
```

What it does:

1. Turns off heaters (`M104 S0`, `M140 S0`, `SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=0`)
2. Moves toolhead to safe park position
3. Disables steppers (except Z — holds position to prevent Z drop)
4. Turns off fans
5. Presents the part (moves bed forward)

---

## PAUSE / RESUME / CANCEL_PRINT

The helper script installs improved versions of these macros that:

- Park the toolhead at a configurable safe position on pause
- Save and restore extruder position on resume
- Handle CFS state correctly if a tool change was in progress

```gcode
PAUSE
RESUME
CANCEL_PRINT
```

---

## WARMUP

Pre-heats the printer to a target without starting a print. Useful for letting the chamber stabilize before a critical print.

```gcode
WARMUP BED=100 EXTRUDER=200 CHAMBER=45 DURATION=600
```

| Parameter | Description |
|---|---|
| `BED` | Bed target temperature |
| `EXTRUDER` | Extruder target (holds at temp for duration) |
| `CHAMBER` | Chamber heater target |
| `DURATION` | Soak time in seconds after all temps reached |

---

## Z_TILT_ADJUST Note

The K2 Plus has two independent Z stepper motors (`stepper_z` and `stepper_z1`) and requires `Z_TILT_ADJUST` before every print to level the gantry. This is called automatically by `START_PRINT`. The probe points are:

```ini
[z_tilt]
points:
    5,175
    345,175
```

Do not remove the `Z_TILT_ADJUST` call from `START_PRINT` — without it, gantry tilt accumulates over time and causes first-layer inconsistency.

---

## RELOAD_CAMERA

Restarts the WebRTC camera service without rebooting the printer:

```gcode
RELOAD_CAMERA
```

This calls `/etc/init.d/S97webrtc restart` via a gcode shell command. Useful when the camera feed drops without a hardware fault.

!!! note "Requires Klipper Gcode Shell Command"
    `RELOAD_CAMERA` requires the [Klipper Gcode Shell Command](klipper-gcode-shell-command.md) feature to be installed.


---

# Save Z-Offset Macros — K2 Plus

The K2 Plus uses a `prtouch_v3` strain-gauge probe for bed leveling. Z-offset is stored in the `SAVE_CONFIG` block of `printer.cfg` at `/mnt/UDISK/printer_data/config/printer.cfg`.

!!! note "Path difference from K1"
    On K1, config lives under `/usr/data/printer_data/config/`. On K2 Plus it is `/mnt/UDISK/printer_data/config/`.

---

## Installation

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **Save Z-Offset Macros**.

---

## Usage

Adjust Z-offset live during a print using babystepping, then save it permanently:

```gcode
SAVE_Z_OFFSET
```

This writes the current live Z-offset to the `[prtouch_v3]` section in `printer.cfg` via `SAVE_CONFIG`.

To set a specific offset value:

```gcode
SET_GCODE_OFFSET Z=0.05     ; apply offset
SAVE_Z_OFFSET               ; persist it
```

---

## Notes on prtouch_v3

The K2 Plus probe uses temperature compensation (`enable_not_linear_comp: True`) and performs automatic re-probing when the bed or nozzle temperature changes significantly. This means Z-offset can shift slightly between cold and hot starts — the temperature compensation accounts for this. If you notice first-layer variation between cold and warm starts, let the printer reach full print temperature before running `Z_TILT_ADJUST` and `BED_MESH_CALIBRATE`.


---

# M600 Support — K2 Plus

M600 is the standard filament change G-code command. On the K2 Plus, M600 behavior differs depending on whether you are using single-filament mode or the CFS.

---

## Installation

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **M600 Support**.

---

## Single-Filament Mode

In single-filament mode, `M600` triggers a filament change pause:

1. The print pauses (`PAUSE`)
2. The toolhead parks at the configured park position
3. The extruder retracts and the nozzle cools slightly to prevent ooze
4. A notification is sent (via Fluidd/Mainsail alert, and companion apps if installed)
5. You manually swap the filament, then resume with `RESUME`

---

## CFS Mode (K2 Plus Combo)

When the CFS is active, `M600` at a tool-change boundary is handled automatically by the CFS `M8200` macro sequence rather than pausing for manual intervention. See [CFS — Color Filament System](cfs-k2plus.md) for the full tool-change sequence.

For an unplanned filament runout during a CFS print, the `BOX_CHECK_MATERIAL_REFILL` macro (triggered by `filament_switch_sensor`) handles recovery automatically if a loaded backup spool is available.

---

## Config Location

The M600 macro is written to `/mnt/UDISK/printer_data/config/m600.cfg` and included from `printer.cfg`.

!!! note "Path difference from K1"
    On K1, config lives under `/usr/data/printer_data/config/`. On K2 Plus it is `/mnt/UDISK/printer_data/config/`.


---

# Klipper Adaptive Meshing & Purging — K2 Plus

KAMP (Klipper Adaptive Meshing & Purging) is integrated into the Creality Helper Script. It generates a bed mesh only over the area being printed, reducing homing and leveling time significantly on a large 350×350mm bed.

---

## K2 Plus Bed Mesh Configuration

The stock bed mesh covers the full usable bed area:

```ini
[bed_mesh]
mesh_min: 5, 5
mesh_max: 345, 345
probe_count: 9, 9
```

KAMP will generate an adaptive sub-mesh within these bounds based on your print's actual footprint. A small print in the center of the bed will probe only the center region rather than all 81 points.

---

## Installation

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **Klipper Adaptive Meshing & Purging**.

The script installs KAMP to `/mnt/UDISK/printer_data/config/` and adds the required `[include]` directives to `printer.cfg`.

!!! note "K2 Plus path"
    KAMP config files are written to `/mnt/UDISK/printer_data/config/` — not `/usr/data/` as on K1.

---

## Enabling Object Processing in Moonraker

KAMP requires Moonraker's object processing to be enabled so it can read the object boundaries from your G-code file.

Because the stock Moonraker config is on the read-only `/usr/share/` partition, the helper script adds the following to `/mnt/UDISK/printer_data/config/moonraker.conf`:

```ini
[file_manager]
enable_object_processing: True
```

This is applied automatically when you install KAMP. Moonraker restarts after installation to pick up the change.

---

## Using KAMP in START_PRINT

After installation, update your `START_PRINT` macro to call `BED_MESH_CALIBRATE` with KAMP:

```gcode
[gcode_macro START_PRINT]
gcode:
  {% set BED_TEMP = params.BED_TEMP|default(60)|float %}
  {% set EXTRUDER_TEMP = params.EXTRUDER_TEMP|default(200)|float %}

  G28                          ; home all axes
  M190 S{BED_TEMP}             ; wait for bed temp
  M109 S{EXTRUDER_TEMP * 0.8} ; pre-heat nozzle (not full temp yet, avoid ooze)

  BED_MESH_CALIBRATE            ; KAMP adaptive mesh (uses object boundaries)

  M109 S{EXTRUDER_TEMP}        ; full nozzle temp
  LINE_PURGE                    ; KAMP purge line at print edge
```

### Purge options

KAMP provides two purge methods:

- `LINE_PURGE` — draws a purge line at the edge of the print area. Recommended for single-material prints.
- `VORON_PURGE` — draws a small purge blob. Less commonly used on the K2 Plus.

For **CFS multi-material prints**, the CFS `box.cfg` macros handle purging via the purge chute (X=133–160, Y=378). Do not use `LINE_PURGE` during CFS tool changes — it is only appropriate for the initial purge before the first layer.

---

## KAMP Mesh Name

When KAMP is enabled, it creates and loads a bed mesh named `kamp` for the current print. This does not overwrite your saved `default` mesh.

To view the active mesh in Fluidd: **Tune → Bed Mesh → kamp**

---

## Disabling KAMP per Print

You can disable KAMP for a specific print from Fluidd by toggling the **KAMP** button in the tune panel (added by the helper script). When disabled, `BED_MESH_CALIBRATE` falls back to a full 9×9 mesh across the entire bed.


---

# Improved Shapers Calibrations — K2 Plus

The K2 Plus uses a **LIS2DW** accelerometer connected via SPI to the nozzle MCU. This is different from the K1 Series which uses an ADXL345. The helper script's improved resonance testing procedure works on both, but the Klipper config sections differ.

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
| SPI speed | 5 MHz |

The stock `printer.cfg` section:

```ini
[lis2dw]
cs_pin: nozzle_mcu:PA4
spi_speed: 5000000
axes_map: x,z,y
spi_software_sclk_pin: nozzle_mcu:PA5
spi_software_mosi_pin: nozzle_mcu:PA7
spi_software_miso_pin: nozzle_mcu:PA6

[resonance_tester]
accel_chip: lis2dw
probe_points:
   175,175,175
min_freq: 20
max_freq: 120
accel_per_hz: 100
```

Your calibrated input shaper values (from the `SAVE_CONFIG` block):

```ini
[input_shaper]
shaper_type_x = ei
shaper_freq_x = 39.2
shaper_type_y = zv
shaper_freq_y = 42.0
```

---

## Installation

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **Improved Shapers Calibrations**.

---

## Running Resonance Tests

!!! warning "Home the printer first"
    The resonance tester moves to `probe_points` (175, 175, 175 by default). Ensure the printer is homed and the bed is clear before running.

From Fluidd or Mainsail console:

```gcode
; Test X axis
SHAPER_CALIBRATE AXIS=X

; Test Y axis  
SHAPER_CALIBRATE AXIS=Y

; Test both axes sequentially
SHAPER_CALIBRATE
```

The test generates CSV data that the helper script processes to recommend a shaper type and frequency. Results are shown in the console and can be applied to `printer.cfg` via `SAVE_CONFIG`.

### Manual test (raw data)

```gcode
TEST_RESONANCES AXIS=X
TEST_RESONANCES AXIS=Y
```

Raw CSV files are saved to `/mnt/UDISK/printer_data/config/` and can be downloaded via Fluidd's file manager for external analysis.

---

## Applying Results

After `SHAPER_CALIBRATE` completes, run:

```gcode
SAVE_CONFIG
```

This writes the recommended shaper type and frequency to the `SAVE_CONFIG` block in `printer.cfg`. Klipper restarts automatically to apply the changes.

---

## Re-running After Hardware Changes

Re-run `SHAPER_CALIBRATE` after:

- Changing the nozzle or hotend assembly
- Tightening or replacing belts
- Changing print speed profiles significantly
- Any significant modification to the toolhead mass

The K2 Plus CoreXY kinematics means X and Y shaper values are independent. A change to toolhead mass (e.g. adding a heavier nozzle) primarily affects X; belt tension changes affect both.

---

## Belt Tension Check

The K2 Plus includes a `[belt_mdl]` module for belt tension measurement. Check belt tension via the touchscreen (**Settings → Self-check → Belt Tension**) or with:

```gcode
BELT_CHECK
```

Target tension for both X and Y belts is **140 N** with a tolerance of ±0.15 (as configured in `printer.cfg`). Re-run shaper calibration after any belt adjustment.


---

# Moonraker Timelapse — K2 Plus

Moonraker Timelapse is a third-party Moonraker component that creates timelapse recordings of prints by capturing a frame at each layer change.

---

## Installation

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **Moonraker Timelapse**.

The component is installed to `/mnt/UDISK/printer_data/` and registered in `/mnt/UDISK/printer_data/config/moonraker.conf`.

---

## Timelapse Video Location

Completed timelapse videos are saved to:

```
/mnt/UDISK/printer_data/timelapse/
```

!!! note "Path difference from K1"
    On K1, timelapse videos are saved to `/usr/data/printer_data/timelapse/`. On K2 Plus the path is `/mnt/UDISK/printer_data/timelapse/`.

Videos can be downloaded directly from Fluidd's file manager under the **Timelapse** section, or via SCP:

```bash
scp root@<printer-ip>:/mnt/UDISK/printer_data/timelapse/my_print.mp4 ./
```

---

## Slicer Setup

Add the following to your slicer's layer change G-code:

```gcode
TIMELAPSE_TAKE_FRAME
```

And add this to your `END_PRINT` macro or slicer end G-code:

```gcode
TIMELAPSE_RENDER
```

---

## Camera

The K2 Plus streams video via WebRTC (service `S97webrtc`). Moonraker Timelapse captures frames from the MJPEG stream on `127.0.0.1:8080`. Ensure the camera is working in Fluidd before enabling timelapse.


---

# OctoEverywhere — K2 Plus

OctoEverywhere provides free remote access to your printer from anywhere in the world — including live webcam, full Fluidd/Mainsail control, and AI print failure detection.

---

## Installation

From the Helper Script menu, select **option 11 — OctoEverywhere**.

---

## Setup

1. After installation, check the Moonraker log for the OctoEverywhere plugin URL:
    ```bash
    tail -50 /mnt/UDISK/printer_data/logs/moonraker.log | grep -i octoeverywhere
    ```

2. Open the URL shown in the log in your browser to link your printer to your OctoEverywhere account.

3. Create a free account at [octoeverywhere.com](https://octoeverywhere.com) if you don't have one.

4. Once linked, access your printer from anywhere at [octoeverywhere.com](https://octoeverywhere.com) or via the OctoEverywhere app.

---

## Features

- **Remote access** — full Fluidd or Mainsail interface from any device
- **Live webcam** — view your print from anywhere
- **AI failure detection** — Gadget AI monitors your print and pauses on spaghetti detection
- **Notifications** — print start, finish, pause, and failure alerts
- **Secure** — end-to-end encrypted, no port forwarding required

---

## Notes for K2 Plus

OctoEverywhere has been confirmed working on the K2 Plus. The Moonraker plugin installs as a component and starts automatically with Moonraker.

If OctoEverywhere loses connection after a Moonraker restart:

```bash
/etc/init.d/S56moonraker restart
```

Then check the log again for the connection status.


---

# Mobileraker Companion — K2 Plus

Mobileraker Companion enables push notifications for Klipper using Moonraker. It works on the K2 Plus with one known caveat.

---

## Installation

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **Mobileraker Companion**.

---

## Known Issue — HeaterFan Parse Error

!!! warning "Known compatibility issue"
    There is a known crash in Mobileraker when connecting to a K2 Plus. The K2 Plus `printer.cfg` uses a `[heater_fan]` configuration that Mobileraker's printer builder does not handle correctly, causing the app to fail with:

    ```
    Found _$HeaterFanImpl, parentException: null
    PrinterBuilder._updateTemperatureFan
    ```

    **Status:** This is an open issue in the Mobileraker project ([issue #429](https://github.com/Clon1998/mobileraker/issues/429)). Check the issue for the latest fix status before installing.

    **Workaround:** If the app crashes on connection, check for an updated Mobileraker release that includes the fix. The companion daemon itself (server-side) installs and runs correctly — the issue is in the mobile app's parsing of the K2 Plus fan configuration.

---

## Configuration

After installation, the companion config is at:

```
/mnt/UDISK/printer_data/config/mobileraker.conf
```

Follow the [Mobileraker setup guide](https://mobileraker.com) to link the companion to your mobile app.

---

## Restart

```bash
/etc/init.d/S56moonraker restart
```

The Mobileraker companion runs as a Moonraker component and restarts with Moonraker.


---

# SimplyPrint — K2 Plus

SimplyPrint has a dedicated K2 Series setup guide separate from the K1 guide.

!!! warning "Use the K2-specific guide"
    Do not follow the K1/K1C SimplyPrint setup guide for a K2 Plus. SimplyPrint provides a separate onboarding flow for the K2 series.

Refer to the official SimplyPrint K2 setup guide for current instructions:

[SimplyPrint K2 Series Setup Guide :material-open-in-new:](https://simplyprint.io/setup-guide/creality/k2){ .md-button }

---

## SSH Root Access

SimplyPrint requires SSH root access to install its companion. Follow the [Enable Root Access](../firmwares/install-and-update-rooted-firmware-k2plus.md#enable-root-access) section first.

- **User:** `root`
- **Password:** `creality_2024`

---

## Data Path Note

If SimplyPrint's installer asks for the printer data path or Moonraker config location, use:

```
/mnt/UDISK/printer_data/
```

Not `/usr/data/printer_data/` as stated in the K1 guide.


---

# CFS — Color Filament System (K2 Plus Combo)

This page covers the built-in CFS (Color Filament System) that ships with the K2 Plus Combo. The CFS is Creality's multi-material hub allowing automatic filament switching between up to 16 spools (4 units × 4 slots each).

!!! note "Combo only"
    This page applies to the **K2 Plus Combo**. If you have the standalone K2 Plus without the CFS, this hardware is not present and these config sections can be ignored.

---

## How the CFS Works in Klipper

The CFS is not a standalone Klipper component — it is fully integrated into the stock `printer.cfg` via `box.cfg`. It communicates over a dedicated RS-485 serial bus and is exposed to Klipper through a custom Creality module (`[box]`).

### Config files involved

| File | Location | Purpose |
|---|---|---|
| `box.cfg` | `/mnt/UDISK/printer_data/config/box.cfg` | All CFS hardware config, positions, and macros |
| `printer.cfg` | `/mnt/UDISK/printer_data/config/printer.cfg` | Includes `box.cfg` via `[include box.cfg]` |

### Key hardware sections in `box.cfg`

```ini
[serial_485 serial485]
serial: /dev/ttyS5          # dedicated RS-485 port for CFS
baud: 230400

[auto_addr]                 # automatic address discovery for CFS units

[filament_rack]
not_pin: !PA5               # filament presence sensor for the rack

[box]
bus: serial485
filament_sensor: filament_sensor
# ... cut positions, purge positions, temperatures, velocities
```

---

## Filament Slot Addressing

The CFS addresses filaments using a `TxY` notation:

- **T** — fixed prefix
- **x** — unit number (1–4, one per CFS box)
- **Y** — slot letter within that unit (A, B, C, D)

Examples: `T1A`, `T1B`, `T2C`, `T4D`

The M8200 macro translates between Klipper's `I` parameter (0-based integer index) and this notation:

```
I=0 → T1A,  I=1 → T1B,  I=2 → T1C,  I=3 → T1D
I=4 → T2A,  I=5 → T2B,  ...
```

---

## Filament Change Sequence

A full tool-change triggered by `M8200` or a slicer `Tx` command follows this sequence:

1. **Pre-op** (`CR_BOX_PRE_OPT`) — move toolhead to safe Z height, prepare state
2. **Move to cut position** — X=10 Y=200 (pre-cut), then execute cut
3. **Cut** (`CR_BOX_CUT` / `M8200 C`) — cutter fires at calibrated `cut_pos_x`
4. **Retract** (`CR_BOX_RETRUDE` / `M8200 R`) — pulls filament back to CFS unit
5. **Load new filament** (`CR_BOX_EXTRUDE` / `M8200 L I[slot]`) — feeds new filament to toolhead
6. **Purge/flush** (`CR_BOX_FLUSH` / `M8200 F`) — extrudes purge length at purge position (X=133–160, Y=378)
7. **End-op** (`CR_BOX_END_OPT`) — restore fans, move to safe position

### Purge and wipe positions (from your calibrated `box.cfg`)

| Position | X | Y |
|---|---|---|
| Pre-cut | 10 | 200 |
| Purge / extrude | 133 | 378 |
| Wipe left | 135–160 | 378 |
| Wipe right | 160–170 | 374 |
| Safe home | 225 | 345 |
| Clean left boundary | 135 | 378 |
| Clean right boundary | 160 | 378 |

---

## Calibrated Cut Position

Your printer's cut position has been auto-calibrated and saved in the `SAVE_CONFIG` block of `printer.cfg`:

```ini
#*# [box]
#*# cut_pos_x = -7.40
```

!!! warning "Do not remove the SAVE_CONFIG block"
    The `cut_pos_x` value is the result of the cutter calibration routine. If you wipe this block or restore factory settings, you will need to re-run the cutter calibration from the touchscreen before the CFS can operate correctly.

---

## Key Macros

These macros are defined in `box.cfg` and are available in Fluidd/Mainsail:

| Macro | Purpose |
|---|---|
| `BOX_LOAD_MATERIAL` | Full load sequence for a new spool |
| `BOX_QUIT_MATERIAL` | Full unload sequence |
| `BOX_INFO_REFRESH ADDR= NUM=` | Refresh RFID and remaining length for a slot |
| `M8200 P` | Pre-op (prepare for filament change) |
| `M8200 C` | Execute cut |
| `M8200 R` | Retract filament to CFS |
| `M8200 L I=[slot]` | Load filament from slot (0-based index) |
| `M8200 F` | Purge/flush new filament |
| `M8200 O` | End-op (restore state after change) |
| `BOX_CHECK_MATERIAL_REFILL` | Called automatically on runout |

---

## Slicer Setup (OrcaSlicer)

In OrcaSlicer, configure the K2 Plus Combo as a multi-material printer:

- **Tool change G-code**: Use the `M8200` sequence or the `T[next_extruder]` command.
- The stock firmware interprets `T0`–`T15` and translates them to the CFS slot addressing automatically.
- Set **flush/purge volume** to match the values in your `box.cfg` (`BOX_MATERIAL_CHANGE_FLUSH` uses the configured length and velocity).

See the [OrcaSlicer](../slicers/orcaslicer.md) page for full slicer configuration.

---

## Troubleshooting

**CFS not responding / filament not loading**
- Verify the RS-485 cable is seated on both the CFS unit and the printer mainboard.
- Check that `/dev/ttyS5` is present: `ls /dev/ttyS*`
- Restart Klipper: `/etc/init.d/S55klipper restart`

**Cut position error after factory reset**
- Re-run cutter calibration from **Settings → CFS → Cutter Calibration** on the touchscreen.
- The calibrated value is written back to the `SAVE_CONFIG` block in `printer.cfg`.

**Filament sensor always triggered / never triggered**
- Check `filament_switch_sensor filament_sensor` in Fluidd's sensor status.
- The sensor pin is `^!nozzle_mcu:PA11` — the `^` is a pull-up, `!` inverts logic. Do not remove these modifiers.

**Purge position leaving blobs on print**
- Adjust `extrude_pos_x` and `extrude_pos_y` in `box.cfg` to match your waste chute position.
- Adjust `clean_left_pos_x` / `clean_right_pos_x` to ensure the wiper fully removes the purge string.

---

## Backup Before Modifying

Before editing `box.cfg` or the CFS-related sections of `printer.cfg`, back up your config:

```bash
cp /mnt/UDISK/printer_data/config/box.cfg /mnt/UDISK/printer_data/config/box.cfg.bak
cp /mnt/UDISK/printer_data/config/printer.cfg /mnt/UDISK/printer_data/config/printer.cfg.bak
```

Or use the helper script's [Backup & Restore Klipper configuration files](backup-and-restore-klipper-configuration-files.md) feature.


---

