# Klipper Adaptive Meshing & Purging — K2 Plus

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
