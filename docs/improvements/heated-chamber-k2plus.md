# Heated Chamber — K2 Plus

The K2 Plus has an actively heated chamber with a dedicated PTC heater element.

---

## Hardware Overview

| Component | Klipper name | Pin | Type |
|---|---|---|---|
| Chamber heater | `chamber_heater` | `PC12` | `heater_generic` |
| Chamber temp sensor | `chamber_temp` | `PC5` | EPCOS 100K |
| Chamber cooling fan | `chamber_fan` | `PA0` | PWM watermark |
| PTC companion fan | `chamber_fan` (heater_fan) | `!PB14`, enable `PB2` | Auto with heater |

---

## Temperature Ranges

| Setting | Value |
|---|---|
| Chamber heater max | 80°C |
| Cooling fan target | 35°C |

!!! warning "80°C is the hard maximum"
    Setting a target above 80°C will cause Klipper to shut down.

---

## Recommended Temperatures by Material

| Material | Chamber temp |
|---|---|
| PLA | Off |
| PETG | 30–40°C |
| ABS | 45–55°C |
| ASA | 45–55°C |
| PA (Nylon) | 50–60°C |
| PC | 55–70°C |

---

## Controlling the Chamber

```gcode
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=45
TEMPERATURE_WAIT SENSOR="heater_generic chamber_heater" MINIMUM=43
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=0
```

---

## PTC Power Pin

The `ptc_power` output pin (`PB2`, default value `1`) keeps the PTC circuit enabled. Do not set this to `0` during printing.
