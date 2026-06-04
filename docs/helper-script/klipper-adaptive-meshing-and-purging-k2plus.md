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
