# Fans Control Macros — K2 Plus

The K2 Plus has a more complex fan topology than the K1 Series. There are three independently controllable output fans, a hotend cooling fan (automatic), and a chamber fan system.

!!! note "K2 Plus fan map differs from K1"
    The K1 Series has a part cooling fan and a nozzle cleaning fan. The K2 Plus has no nozzle cleaning fan.

---

## Fan Hardware Map

| Fan | Klipper name | Pin | Type | Notes |
|---|---|---|---|---|
| Hotend (heatsink) | `hotend_fan` | `nozzle_mcu:PB7` + `PB1` | `heater_fan` | Auto — on when extruder > 50°C |
| Part cooling | `fan0` | `nozzle_mcu:PB15` | `output_pin` PWM | Controlled by slicer `M106/M107` |
| Chamber cooling | `chamber_fan` | `PA0` | `temperature_fan` | Auto watermark at 35°C target |
| Aux fan | `fan2` | `PB4` + `PB3` | `output_pin` PWM | Electronics bay cooling |
| Chamber heater fan | `chamber_fan` (heater companion) | `!PB14`, enable `PB2` | `heater_fan` | Tied to `chamber_heater` |

!!! note "fan0_en"
    `output_pin fan0_en` on `nozzle_mcu:PB6` acts as an enable gate for the part cooling fan. The helper script macros manage this automatically.

---

## Controlling Fans via Macros

From the `[Install] Menu` install **Fans Control Macros**.

### Part cooling fan

```gcode
SET_FAN0 S=255    ; full speed
SET_FAN0 S=128    ; 50%
SET_FAN0 S=0      ; off
```

### Aux fan

```gcode
SET_FAN2 S=255
SET_FAN2 S=0
```

### Chamber temperature target

```gcode
SET_TEMPERATURE_FAN_TARGET TEMPERATURE_FAN=chamber_fan TARGET=40
```

### Chamber heater

```gcode
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=40
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=0
```

---

## Notes on duplicate_pin_override

The K2 Plus `printer.cfg` contains a large `[duplicate_pin_override]` section because several pins are shared between fan definitions. Do not remove this section — Klipper will refuse to start.
