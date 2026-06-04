# Save Z-Offset Macros — K2 Plus

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
