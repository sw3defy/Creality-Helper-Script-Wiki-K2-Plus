# Improved Shapers Calibrations — K2 Plus

The K2 Plus uses a **LIS2DW** accelerometer connected via SPI to the nozzle MCU. This differs from the K1 Series which uses an ADXL345.

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

Your calibrated input shaper values:

```ini
[input_shaper]
shaper_type_x = ei
shaper_freq_x = 39.2
shaper_type_y = zv
shaper_freq_y = 42.0
```

---

## Installation

From the `[Install] Menu` install **Improved Shapers Calibrations**.

---

## Running Resonance Tests

!!! warning "Home the printer first"

```gcode
SHAPER_CALIBRATE AXIS=X
SHAPER_CALIBRATE AXIS=Y
SHAPER_CALIBRATE
```

After calibration completes:

```gcode
SAVE_CONFIG
```

---

## Belt Tension Check

Target tension for both X and Y belts is **140 N** (configured in `printer.cfg`). Re-run shaper calibration after any belt adjustment.
