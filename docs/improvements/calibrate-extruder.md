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
