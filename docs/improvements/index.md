# Improvements

---

# Heated Chamber — K2 Plus

The K2 Plus has an actively heated chamber with a dedicated PTC (Positive Temperature Coefficient) heater element. This page explains how the chamber system works in Klipper and how to get the best results from it.

---

## Hardware Overview

| Component | Klipper name | Pin | Type |
|---|---|---|---|
| Chamber heater element | `chamber_heater` | `PC12` | `heater_generic` |
| Chamber temperature sensor | `chamber_temp` | `PC5` | EPCOS 100K thermistor |
| Chamber cooling fan | `chamber_fan` (temperature_fan) | `PA0` | PWM, watermark control |
| PTC fan (heater companion) | `chamber_fan` (heater_fan) | `!PB14`, enable `PB2` | Auto with heater |
| PTC power enable | `ptc_power` | `PB2` | `output_pin`, default value 1 |

The PTC fan (`!PB14`) runs automatically when `chamber_heater` is active. The cooling fan (`PA0`) runs in `temperature_fan` watermark mode to maintain a `target_temp` of 35°C when cooling is needed.

---

## Temperature Ranges

| Setting | Value | Notes |
|---|---|---|
| Chamber heater max temp | 80°C | Hard limit in Klipper config |
| Chamber sensor max | 125°C | Safety limit |
| Cooling fan target (passive) | 35°C | Maintains ambient when not actively heating |
| `verify_heater` check_gain_time | 345600 s (4 days) | Effectively disabled — chamber heats slowly |

!!! warning "80°C is the hard maximum"
    The `chamber_heater` max_temp is set to 80°C. Setting a target above this will cause Klipper to shut down. For most materials, 40–60°C is sufficient.

---

## Recommended Chamber Temperatures by Material

| Material | Chamber temp | Notes |
|---|---|---|
| PLA | 0 (off) | PLA warps in warm chamber; leave off or run cooling |
| PETG | 30–40°C | Mild warmth reduces warping |
| ABS | 45–55°C | Critical for preventing layer delamination |
| ASA | 45–55°C | Same as ABS |
| PA (Nylon) | 50–60°C | Reduces moisture absorption during print |
| PC | 55–70°C | High-temp materials benefit from maximum chamber heat |

---

## Controlling the Chamber

### Set chamber temperature

```gcode
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=45
```

### Wait for chamber to reach temperature

```gcode
TEMPERATURE_WAIT SENSOR="heater_generic chamber_heater" MINIMUM=43
```

### Turn off chamber heater

```gcode
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=0
```

### Check current chamber temperature

In Fluidd, the chamber heater appears in the **Temperatures** panel as `chamber_heater` with both current and target temperatures displayed.

---

## Chamber Pre-heat in START_PRINT

For ABS/ASA prints, add chamber pre-heating before bed leveling so the chamber is warm before the first layer:

```gcode
[gcode_macro START_PRINT]
gcode:
  {% set CHAMBER_TEMP = params.CHAMBER_TEMP|default(0)|float %}
  {% set BED_TEMP = params.BED_TEMP|default(60)|float %}
  {% set EXTRUDER_TEMP = params.EXTRUDER_TEMP|default(200)|float %}

  G28

  {% if CHAMBER_TEMP > 0 %}
    SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET={CHAMBER_TEMP}
    M140 S{BED_TEMP}
    ; Soak until both bed and chamber are close to target
    M190 S{BED_TEMP}
    TEMPERATURE_WAIT SENSOR="heater_generic chamber_heater" MINIMUM={CHAMBER_TEMP - 3}
  {% else %}
    M190 S{BED_TEMP}
  {% endif %}

  Z_TILT_ADJUST
  BED_MESH_CALIBRATE
  M109 S{EXTRUDER_TEMP}
  LINE_PURGE
```

---

## Chamber Cooling After Print

For materials that must cool slowly to avoid warping (ABS, PC), keep the chamber warm during the cool-down phase by leaving the heater on at a reduced temperature for a period after the print ends:

```gcode
[gcode_macro END_PRINT]
gcode:
  ; ... park toolhead, disable steppers ...
  ; Slow cool: hold chamber at 40°C for 10 minutes then turn off
  SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=40
  G4 P600000   ; wait 10 minutes
  SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=0
  M140 S0
  M104 S0
```

---

## PTC Power Pin

The `ptc_power` output pin (`PB2`, default value `1`) keeps the PTC circuit enabled. Do not set this to `0` during printing — it would cut power to the chamber heater entirely. The helper script macros do not touch this pin.


---

# CFS Maintenance — K2 Plus Combo

Regular maintenance of the CFS (Color Filament System) keeps filament changes reliable and prevents clogs, failed cuts, and feed errors.

---

## Maintenance Schedule

| Interval | Task |
|---|---|
| Every 500g of filament | Clean the purge chute |
| Every 1kg of filament | Inspect and clean the cutter blade |
| Every 2kg | Lubricate the CFS feed rollers |
| As needed | Re-run cutter calibration |
| After any filament jam | Full inspection before resuming |

---

## Cutter Maintenance

The cutter is the most maintenance-sensitive part of the CFS. A dull or misaligned cutter causes failed filament changes.

### Cleaning the Cutter

1. Unload all filament from the active slot.
2. Navigate to the cut position manually using the touchscreen or via Fluidd console:
    ```gcode
    G90
    G1 X10 Y200 F12000  ; move to pre-cut position
    ```
3. Use a soft brush or compressed air to remove filament debris from the cutter blade area.
4. Check the blade for nicks or buildup.

### Re-running Cutter Calibration

After cleaning or if cuts are inconsistent, re-calibrate:

- Touchscreen: **Settings → CFS → Cutter Calibration**

The calibrated `cut_pos_x` value is saved to the `SAVE_CONFIG` block in `printer.cfg`:
```ini
#*# [box]
#*# cut_pos_x = -7.40
```

Check this value is within the valid range: `-5.5` to `-9.5` (as defined by `check_cut_pos_x_max` and `check_cut_pos_x_min` in `box.cfg`).

---

## Purge Chute Maintenance

Purged filament collects in the chute area at X=133–160, Y=378. Over time this can build up and cause the wiper to miss.

### Cleaning

1. Cool the printer fully.
2. Open the front enclosure panel.
3. Remove any accumulated purge strings and blobs from the chute area.
4. Clean the silicone wiper pad (at X=160–170, Y=374) with IPA if filament residue has built up.

---

## Feed Roller Maintenance

The CFS units use motorised rollers to push filament. Debris on the rollers causes slipping and under-extrusion during filament changes.

1. Open each CFS unit.
2. Clean the drive rollers with IPA and a cotton swab.
3. Apply a small amount of PTFE-safe lubricant to the roller shafts if they feel stiff.

---

## RS-485 Cable Check

The CFS communicates with the printer over an RS-485 cable on `/dev/ttyS5`. If the CFS stops responding:

1. Check both ends of the RS-485 cable are seated firmly.
2. Restart Klipper: `/etc/init.d/S55klipper restart`
3. Verify the bus is active: `ls /dev/ttyS*` — `/dev/ttyS5` should be present.

---

## Filament Sensor Calibration

If the filament sensor (`filament_switch_sensor filament_sensor` on `nozzle_mcu:PA11`) gives false positives or misses runout:

Check sensor status in Fluidd under **Sensors → filament_sensor**.

The sensor pin is `^!nozzle_mcu:PA11` — the `^` is a pull-up and `!` inverts logic. Do not modify these unless you have replaced the sensor hardware.

---

## CFS Troubleshooting Quick Reference

| Symptom | Likely cause | Fix |
|---|---|---|
| Filament not cut cleanly | Dull blade or miscalibrated cut_pos_x | Clean blade, re-run cutter calibration |
| Filament not feeding to nozzle | Roller debris or RS-485 disconnect | Clean rollers, check cable, restart Klipper |
| `BOX_CHECK_MATERIAL_REFILL` triggers constantly | Filament sensor false positive | Check sensor wiring and pin |
| CFS not responding in Fluidd | RS-485 bus fault | Check cable, restart Klipper |
| Purge string not wiped off | Silicone wiper dirty or wiper position off | Clean wiper, adjust `clean_pos_*` in box.cfg |
| Cut position error after factory reset | SAVE_CONFIG block wiped | Re-run cutter calibration from touchscreen |


---

# Calibrate Extruder — K2 Plus

Extruder calibration (also called e-step calibration) ensures the printer extrudes exactly the amount of filament requested. This improves dimensional accuracy and reduces under/over-extrusion.

---

## When to Calibrate

Calibrate your extruder when:

- Installing a new extruder or drive gear
- Changing filament diameter significantly
- Noticing consistent under or over-extrusion that is not resolved by slicer flow rate adjustments
- After any extruder hardware modification

The K2 Plus uses a direct drive extruder. The stock `rotation_distance` in `printer.cfg` is `6.9` — this is a good starting point but may need fine-tuning for your specific hardware.

---

## Method 1 — Mark and Measure (Cold)

This is the most accurate method.

1. Remove the bowden tube from the extruder or work with filament loaded.

2. Mark the filament **120mm** from the extruder entry point with a marker.

3. From the Fluidd console, command the extruder to move 100mm:

    ```gcode
    M83          ; relative extrusion
    G1 E100 F100 ; extrude 100mm slowly
    ```

4. Measure the distance from the extruder entry to your mark. If the printer extruded exactly 100mm, the distance should now be 20mm.

5. Calculate the actual distance extruded:
    ```
    actual_extruded = 120 - remaining_distance
    ```

6. Calculate the new `rotation_distance`:
    ```
    new_rotation_distance = current_rotation_distance × (100 / actual_extruded)
    ```

7. Update `rotation_distance` in the `[extruder]` section of `/mnt/UDISK/printer_data/config/printer.cfg` and run `FIRMWARE_RESTART`.

---

## Method 2 — Flow Rate Calibration (Hot, Recommended for Fine Tuning)

After setting a baseline rotation_distance, fine-tune flow with a calibration cube:

1. Print a single-wall calibration cube (20×20×20mm, 1 perimeter, 0% infill).
2. Measure wall thickness with calipers.
3. Expected thickness = nozzle diameter (0.4mm).
4. Adjust flow in OrcaSlicer or via `M221 S[value]` until walls measure correctly.
5. Once happy, bake the flow rate into your filament profile rather than changing `rotation_distance` further.

---

## K2 Plus Extruder Notes

The K2 Plus uses a high-torque dual-drive extruder. Key values in stock `printer.cfg`:

```ini
[extruder]
rotation_distance: 6.9
microsteps: 16
max_extrude_only_distance: 1000.0
pressure_advance: 0.038
pressure_advance_smooth_time: 0.038
```

After calibrating rotation_distance, also consider tuning **Pressure Advance** for better corner quality. Run:

```gcode
SET_PRESSURE_ADVANCE ADVANCE=0.04
```

and adjust while printing until corners are sharp without bulging. Save the final value in `printer.cfg`.


---

