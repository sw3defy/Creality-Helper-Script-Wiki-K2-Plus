# Fans Control Macros — K2 Plus

The K2 Plus has a more complex fan topology than the K1 Series. There are three independently controllable output fans, a hotend cooling fan (automatic), and a chamber fan that doubles as both a cooling `temperature_fan` and a PTC heater companion. This page documents what each fan does, how to control them, and what the helper script macros provide.

!!! note "K2 Plus fan map differs from K1"
    The K1 Series has a part cooling fan and a nozzle cleaning fan. The K2 Plus has no nozzle cleaning fan. Do not apply K1 fan macro configs to the K2 Plus.

---

## Fan Hardware Map

| Fan | Klipper name | Pin | Type | Notes |
|---|---|---|---|---|
| Hotend (heatsink) | `hotend_fan` | `nozzle_mcu:PB7` + `PB1` | `heater_fan` | Auto — on when extruder > 50°C |
| Part cooling | `fan0` | `nozzle_mcu:PB15` | `output_pin` PWM | Controlled by slicer `M106/M107` |
| Chamber cooling | `chamber_fan` | `PA0` | `temperature_fan` | Auto watermark at 35°C target |
| Aux fan | `fan2` | `PB4` + `PB3` | `output_pin` PWM | Electronics bay / aux cooling |
| Chamber heater fan (PTC) | `chamber_fan` (heater companion) | `PB14` (inverted) | `heater_fan` | Tied to `chamber_heater`, enable pin `PB2` |

!!! note "fan0_en"
    There is an additional `output_pin fan0_en` on `nozzle_mcu:PB6` which acts as an enable gate for the part cooling fan circuit. The helper script macros manage this automatically — do not drive `fan0` without first ensuring `fan0_en` is high.

---

## Controlling Fans via Macros

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **Fans Control Macros**.

The installed macros give you named controls usable from Fluidd, Mainsail, or G-code:

### Part cooling fan (`fan0`)

```gcode
SET_FAN0 S=255        ; full speed (255 = 100%)
SET_FAN0 S=128        ; 50%
SET_FAN0 S=0          ; off
```

The slicer's standard `M106 S[value]` also controls `fan0` directly.

### Aux fan (`fan2`)

```gcode
SET_FAN2 S=255
SET_FAN2 S=0
```

### Chamber temperature target

The chamber fan runs in `watermark` control mode with a default target of `35°C`. To raise or lower the cooling setpoint:

```gcode
SET_TEMPERATURE_FAN_TARGET TEMPERATURE_FAN=chamber_fan TARGET=40
```

### Chamber heater

The chamber heater is a `heater_generic` named `chamber_heater`. Set target temperature:

```gcode
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=40   ; heat to 40°C
SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET=0    ; off
```

The PTC heater companion fan (`chamber_fan` heater_fan) runs automatically when `chamber_heater` is active and the heater exceeds the configured threshold.

---

## Useful Macros Added by Helper Script

| Macro | Purpose |
|---|---|
| `SAVE_FANS` | Saves current fan speeds to variables |
| `RESTORE_FANS` | Restores previously saved fan speeds |
| `FANS_OFF` | Turns off all output fans (does not affect `hotend_fan` autocontrol) |
| `CHAMBER_HEAT TARGET=` | Sets `chamber_heater` target and waits if `WAIT=1` |
| `CHAMBER_COOL` | Disables chamber heater, sets cooling fan to full speed |

These are particularly useful in `START_PRINT` and `END_PRINT` macros — the helper script's [Useful Macros](useful-macros-k2plus.md) page shows complete START/END examples that include chamber pre-heat.

---

## START_PRINT Chamber Pre-heat Example

For materials requiring a warm chamber (ABS, ASA, PA), add chamber pre-heating to your `START_PRINT`:

```gcode
[gcode_macro START_PRINT]
gcode:
  {% set BED_TEMP = params.BED_TEMP|default(60)|float %}
  {% set EXTRUDER_TEMP = params.EXTRUDER_TEMP|default(200)|float %}
  {% set CHAMBER_TEMP = params.CHAMBER_TEMP|default(0)|float %}

  ; Heat bed first
  M140 S{BED_TEMP}

  ; If a chamber temp is requested, start heating the chamber now
  {% if CHAMBER_TEMP > 0 %}
    SET_HEATER_TEMPERATURE HEATER=chamber_heater TARGET={CHAMBER_TEMP}
  {% endif %}

  M190 S{BED_TEMP}           ; wait for bed

  ; Wait for chamber if needed
  {% if CHAMBER_TEMP > 0 %}
    TEMPERATURE_WAIT SENSOR="heater_generic chamber_heater" MINIMUM={CHAMBER_TEMP - 2}
  {% endif %}

  M109 S{EXTRUDER_TEMP}      ; wait for extruder
  ; ... homing, leveling, purge, print start
```

---

## Notes on `duplicate_pin_override`

The K2 Plus `printer.cfg` contains a large `[duplicate_pin_override]` section because several pins are shared between the `temperature_fan`, `heater_fan`, and `output_pin` definitions (most notably `PA0` and `PC5`). Do not remove this section — Klipper will refuse to start if shared pins are not declared in `duplicate_pin_override`.

```ini
[duplicate_pin_override]
pins: PC5,PA0,PC7,PB7,PB8,PB9,PB10,PB5,PB6,PA1,PB15,PB11,PB12,PB13,PA10,PA9,PB2,PB14,PB1
```
