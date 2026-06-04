# Boards Layout — K2 Plus

The K2 Plus uses two MCU boards: the main control board and a nozzle MCU board mounted on the toolhead.

---

## Main Control Board

**Board ID:** `CR4FN200338C15`  
**MCU chip:** GD32F303RET6

### Key Pin Assignments

| Function | Pin | Notes |
|---|---|---|
| Stepper X step | `PB8` | |
| Stepper X dir | `!PB7` | inverted |
| Stepper X enable | `!PA9` | shared enable |
| Stepper Y step | `PB10` | |
| Stepper Y dir | `PB9` | |
| Stepper Z step | `PB6` | |
| Stepper Z dir | `PB5` | |
| Stepper Z1 step | `PB15` | second Z motor |
| Stepper Z1 dir | `PA1` | |
| Stepper enable (all) | `!PA9` | |
| Endstop X | `PB11` | |
| Endstop Y | `PB12` | |
| Z endstop | `probe:z_virtual_endstop` | prtouch_v3 |
| Heated bed heater | `PC8` | |
| Heated bed thermistor | `PC4` | EPCOS 100K |
| Chamber heater (PTC) | `PC12` | heater_generic |
| Chamber thermistor | `PC5` | NTC 100K |
| Chamber cooling fan | `PA0` | temperature_fan, shared pin |
| Chamber PTC fan enable | `!PB14` | heater_fan |
| PTC power enable | `PB2` | output_pin, default 1 |
| Aux fan (fan2) | `PB4` + `PB3` | multi_pin |
| LED strip | `PB0` + `PA12` | multi_pin, PWM |
| Power output | `PC9` | |
| Z alignment endstops | `PA15`, `PA8` | z_align module |
| Filament rack sensor | `!PA5` | filament_rack |
| MCU serial (main) | `/dev/ttyS2` | baud 230400 |
| CFS RS-485 serial | `/dev/ttyS5` | baud 230400 |

---

## Nozzle MCU Board

**Board ID:** `CR1FN200338C15`  
**MCU chip:** GD32F303CBT6  
**Serial:** `/dev/ttyS3` baud 230400

### Key Pin Assignments

| Function | Pin | Notes |
|---|---|---|
| Extruder step | `nozzle_mcu:PB5` | |
| Extruder dir | `!nozzle_mcu:PB4` | inverted |
| Extruder enable | `!nozzle_mcu:PB2` | |
| Hotend heater | `nozzle_mcu:PB8` | |
| Hotend thermistor | `nozzle_mcu:PA0` | custom thermistor |
| Hotend fan (heatsink) | `nozzle_mcu:PB7` + `PB1` | multi_pin heater_fan |
| Part cooling fan enable | `nozzle_mcu:PB6` | fan0_en gate |
| Part cooling fan (fan0) | `!nozzle_mcu:PB15` | PWM |
| Extruder fan output | `nozzle_mcu:PB1` | |
| Filament sensor | `^!nozzle_mcu:PA11` | filament_switch_sensor |
| CFS cut switch | `!nozzle_mcu:PB9` | box switch_pin |
| LIS2DW CS | `nozzle_mcu:PA4` | SPI accelerometer |
| LIS2DW SCLK | `nozzle_mcu:PA5` | |
| LIS2DW MOSI | `nozzle_mcu:PA7` | |
| LIS2DW MISO | `nozzle_mcu:PA6` | |
| prtouch_v3 pressure CS | `nozzle_mcu:PB13`, `nozzle_mcu:PB14` | strain gauge |
| prtouch_v3 step swap | `!PC7` | main board |
| prtouch_v3 pres swap | `nozzle_mcu:PA15` | |

---

## Host MCU (Raspberry Pi style)

The K2 Plus runs a secondary Linux host MCU for accelerometer data collection.

```ini
[mcu rpi]
serial: /tmp/klipper_host_mcu
```

---

## Serial Port Map

| Device | Purpose |
|---|---|
| `/dev/ttyS2` | Main MCU (GD32F303RET6) |
| `/dev/ttyS3` | Nozzle MCU (GD32F303CBT6) |
| `/dev/ttyS5` | CFS RS-485 bus |

---

!!! note "Duplicate pin override"
    The K2 Plus `printer.cfg` requires a large `[duplicate_pin_override]` section because several pins are shared between multiple Klipper objects (e.g. `PA0` is used by both `temperature_fan chamber_fan` and `output_pin fan2`). Do not remove this section or Klipper will refuse to start.

```ini
[duplicate_pin_override]
pins: PC5,PA0,PC7,PB7,PB8,PB9,PB10,PB5,PB6,PA1,PB15,PB11,PB12,PB13,PA10,PA9,PB2,PB14,PB1
```
