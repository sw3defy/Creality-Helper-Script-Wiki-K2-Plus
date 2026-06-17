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


**CFS load/unload fails with key865, key789, key22 errors**

This is a known bug in the stock Creality firmware where all CFS-related macros
in `box.cfg` and `gcode_macro.cfg` are prefixed with an underscore (e.g.
`_BOX_QUIT_MATERIAL`, `_WAIT_TEMP_START`). In Klipper, a leading underscore
makes a macro private/hidden — it cannot be called by the CFS system, the UI,
or other macros. This causes the entire load/unload sequence to silently fail.

The helper script automatically patches this on startup. If you are not using
the helper script, apply the fix manually:

```bash
cp /mnt/UDISK/printer_data/config/box.cfg /mnt/UDISK/printer_data/config/box.cfg.bak
sed -i 's/\[gcode_macro _BOX_/[gcode_macro BOX_/g' /mnt/UDISK/printer_data/config/box.cfg
```

Then do a `FIRMWARE_RESTART` from Mainsail or Fluidd.

Errors resolved by this fix:

- `key865` — retrude error, failed to exit connections
- `key789` — position tracking error on X/Y axes (位置跟踪误差过大)
- `key22` — no trigger on Y after full movement
- `key274` — unknown g-code state: helix_cfs_load
- `Unknown command: WAIT_TEMP_START`
- `Unknown command: END_PRINT_POINT`
- `Unknown command: CANCEL_CHAMBER_FAN_SWITCH`

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
