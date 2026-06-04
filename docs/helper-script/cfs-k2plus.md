# CFS — Color Filament System (K2 Plus Combo)

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
