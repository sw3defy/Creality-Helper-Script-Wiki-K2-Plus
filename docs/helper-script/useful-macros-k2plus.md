# Useful Macros — K2 Plus

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
