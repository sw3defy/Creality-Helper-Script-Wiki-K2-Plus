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
