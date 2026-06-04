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
