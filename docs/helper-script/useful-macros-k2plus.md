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
