# Improved Shapers Calibrations — K2 Plus

The K2 Plus uses a **LIS2DW** accelerometer connected via SPI to the nozzle MCU. This is different from the K1 Series which uses an ADXL345. The helper script's improved resonance testing procedure works on both, but the Klipper config sections differ.

---

## Hardware Details

| Item | Value |
|---|---|
| Accelerometer chip | LIS2DW |
| Interface | SPI (software) |
| CS pin | `nozzle_mcu:PA4` |
| SCLK | `nozzle_mcu:PA5` |
| MOSI | `nozzle_mcu:PA7` |
| MISO | `nozzle_mcu:PA6` |
| Axes map | `x, z, y` |
| SPI speed | 5 MHz |

The stock `printer.cfg` section:

```ini
[lis2dw]
cs_pin: nozzle_mcu:PA4
spi_speed: 5000000
axes_map: x,z,y
spi_software_sclk_pin: nozzle_mcu:PA5
spi_software_mosi_pin: nozzle_mcu:PA7
spi_software_miso_pin: nozzle_mcu:PA6

[resonance_tester]
accel_chip: lis2dw
probe_points:
   175,175,175
min_freq: 20
max_freq: 120
accel_per_hz: 100
```

Your calibrated input shaper values (from the `SAVE_CONFIG` block):

```ini
[input_shaper]
shaper_type_x = ei
shaper_freq_x = 39.2
shaper_type_y = zv
shaper_freq_y = 42.0
```

---

## Installation

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **Improved Shapers Calibrations**.

---

## Running Resonance Tests

!!! warning "Home the printer first"
    The resonance tester moves to `probe_points` (175, 175, 175 by default). Ensure the printer is homed and the bed is clear before running.

From Fluidd or Mainsail console:

```gcode
; Test X axis
SHAPER_CALIBRATE AXIS=X

; Test Y axis  
SHAPER_CALIBRATE AXIS=Y

; Test both axes sequentially
SHAPER_CALIBRATE
```

The test generates CSV data that the helper script processes to recommend a shaper type and frequency. Results are shown in the console and can be applied to `printer.cfg` via `SAVE_CONFIG`.

### Manual test (raw data)

```gcode
TEST_RESONANCES AXIS=X
TEST_RESONANCES AXIS=Y
```

Raw CSV files are saved to `/mnt/UDISK/printer_data/config/` and can be downloaded via Fluidd's file manager for external analysis.

---

## Applying Results

After `SHAPER_CALIBRATE` completes, run:

```gcode
SAVE_CONFIG
```

This writes the recommended shaper type and frequency to the `SAVE_CONFIG` block in `printer.cfg`. Klipper restarts automatically to apply the changes.

---

## Re-running After Hardware Changes

Re-run `SHAPER_CALIBRATE` after:

- Changing the nozzle or hotend assembly
- Tightening or replacing belts
- Changing print speed profiles significantly
- Any significant modification to the toolhead mass

The K2 Plus CoreXY kinematics means X and Y shaper values are independent. A change to toolhead mass (e.g. adding a heavier nozzle) primarily affects X; belt tension changes affect both.

---

## Belt Tension Check

The K2 Plus includes a `[belt_mdl]` module for belt tension measurement. Check belt tension via the touchscreen (**Settings → Self-check → Belt Tension**) or with:

```gcode
BELT_CHECK
```

Target tension for both X and Y belts is **140 N** with a tolerance of ±0.15 (as configured in `printer.cfg`). Re-run shaper calibration after any belt adjustment.
