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
