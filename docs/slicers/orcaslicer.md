# OrcaSlicer — K2 Plus

OrcaSlicer is the recommended slicer for the K2 Plus. It has a built-in K2 Plus printer profile with the correct 350×350×360mm build volume and chamber temperature support.

Download: :material-github: [GitHub Releases](https://github.com/SoftFever/OrcaSlicer/releases/latest)

---

## Printer Profile

Select the built-in K2 Plus profile when setting up your printer:

**Printer → Creality → Creality K2 Plus**

Key profile values:

| Setting | Value |
|---|---|
| Build volume | 350 × 350 × 360 mm |
| Kinematics | CoreXY |
| Max speed | 800 mm/s |
| Max acceleration | 30,000 mm/s² |
| Chamber temperature | Supported |

---

## Machine G-codes

In OrcaSlicer, edit your printer preset and go to the **Machine G-code** tab. Set:

**Machine start G-code:**
```gcode
SET_PRINT_STATS_INFO TOTAL_LAYER=[total_layer_count]
M140 S0
M104 S0
START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single] CHAMBER_TEMP=[chamber_temperature]
```

**Machine end G-code:**
```gcode
END_PRINT
```

**Before layer change G-code:**
```gcode
;BEFORE_LAYER_CHANGE
;[layer_z]
G92 E0
```

**Layer change G-code:**
```gcode
SET_PRINT_STATS_INFO CURRENT_LAYER={layer_num + 1}
;AFTER_LAYER_CHANGE
;[layer_z]
```

**Time lapse G-code** (if Moonraker Timelapse is installed):
```gcode
TIMELAPSE_TAKE_FRAME
```

**Change filament G-code** (if M600 Support is installed):
```gcode
M600
```

---

## Chamber Temperature by Material

OrcaSlicer supports chamber temperature per filament profile. This maps directly to the `CHAMBER_TEMP` parameter in `START_PRINT`.

| Material | Chamber temp |
|---|---|
| PLA | 0 (off) |
| PETG | 35°C |
| ABS | 50°C |
| ASA | 50°C |
| PA (Nylon) | 55°C |
| PC | 65°C |
| TPU | 0 (off) |

---

## Multi-Material Setup (K2 Plus Combo with CFS)

For the K2 Plus Combo, configure OrcaSlicer as a multi-material printer:

- Set the number of extruders to match your loaded CFS slots (up to 16)
- The slicer's `T0`–`T15` tool change commands are translated automatically to CFS slot addresses by the `M8200` macro in `box.cfg`
- Set flush/purge volume to match your `box.cfg` settings (default ~140mm³)
- Purging occurs at the CFS purge chute position (X=133–160, Y=378) — not as a line on the bed

See [CFS — Color Filament System](../helper-script/cfs-k2plus.md) for the full tool-change sequence.

---

## Upload G-code Files to Printer

- Click the **Connection** icon in OrcaSlicer
- Enter your printer's IP address:
    - For **Fluidd**: `http://<printer-ip>:4408/`
    - For **Mainsail**: `http://<printer-ip>:4409/`
- Click **Connect** — you can now upload and start prints directly from the slicer
