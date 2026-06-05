# Others

---

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


---

# Files Location — K2 Plus

All persistent data on the K2 Plus lives under `/mnt/UDISK/`. There is no `/usr/data/` path on the K2 Plus — this differs from the K1 Series.

Connect via [SSH](../firmwares/ssh-connection.md) to access these locations.

---

## Klipper & Printer Data

| Resource | Path |
|---|---|
| Klipper configuration files | `/mnt/UDISK/printer_data/config/` |
| GCode files | `/mnt/UDISK/printer_data/gcodes/` |
| Klipper log | `/mnt/UDISK/printer_data/logs/klippy.log` |
| Moonraker log | `/mnt/UDISK/printer_data/logs/moonraker.log` |
| Moonraker database | `/mnt/UDISK/printer_data/` |
| Moonraker timelapse videos | `/mnt/UDISK/printer_data/timelapse/` |

---

## Creality System Data

| Resource | Path |
|---|---|
| System config (self-check flag, etc.) | `/mnt/UDISK/creality/userdata/config/system_config.json` |
| Creality timelapse videos | `/mnt/UDISK/creality/userdata/delay_image/video/` |
| AI image data | `/mnt/UDISK/ai_image/` |
| Layer image data | `/mnt/UDISK/layers_image/` |

---

## Read-Only System Paths

These paths live on a read-only partition and **cannot be edited in place**. Modifying them requires overlaying or replacing the binary/file via the helper script approach.

| Resource | Path |
|---|---|
| Klipper Python env | `/usr/share/klippy-env/bin/python` |
| Klipper source | `/usr/share/klipper/klippy/klippy.py` |
| Klipper config templates | `/usr/share/klipper/config/F008_CR0CN240319C13_1/` |
| Moonraker Python env | `/usr/share/moonraker-env/bin/python` |
| Moonraker source | `/usr/share/moonraker/` |
| Moonraker config | `/usr/share/moonraker/moonraker.conf` |
| Fluidd static files | `/usr/share/fluidd/` |
| Nginx config | `/etc/nginx/nginx.conf` |

---

## Service Scripts

The K2 Plus uses OpenWrt-style rc.d init scripts. There is no `systemd` or `supervisord`.

| Service | Start script | Stop script |
|---|---|---|
| klipper MCU bridge | `/etc/init.d/S54klipper_mcu` | `/etc/rc.d/K54klipper_mcu` (if present) |
| Klipper (klippy) | `/etc/init.d/S55klipper` | — |
| Moonraker | `/etc/init.d/S56moonraker` | — |
| Nginx | `/etc/init.d/S80nginx` | — |
| WebRTC (camera) | `/etc/init.d/S97webrtc` | `/etc/rc.d/K97webrtc` |

To restart a service over SSH:

```bash
/etc/init.d/S55klipper restart
/etc/init.d/S56moonraker restart
/etc/init.d/S80nginx restart
```

!!! note "No supervisorctl on K2 Plus"
    Unlike the K1 Series, the K2 Plus does not use Supervisor Lite. The `supervisorctl` command is not available. Use the rc.d init scripts above instead.


---

# Useful Links — K2 Plus

---

## Sw3Defy K2 Plus Resources

| Resource | Link |
|---|---|
| This Wiki | [sw3defy.github.io/Creality-Helper-Script-Wiki-K2-Plus](https://sw3defy.github.io/Creality-Helper-Script-Wiki-K2-Plus/) |
| Helper Script (K2 Plus) | [github.com/sw3defy/Creality-Helper-Script-K2-Plus](https://github.com/sw3defy/Creality-Helper-Script-K2-Plus) |
| Wiki Repository | [github.com/sw3defy/Creality-Helper-Script-Wiki-K2-Plus](https://github.com/sw3defy/Creality-Helper-Script-Wiki-K2-Plus) |

---

## Original Guilouz Resources (K1 Series)

| Resource | Link |
|---|---|
| Guilouz Helper Script Wiki | [guilouz.github.io/Creality-Helper-Script-Wiki](https://guilouz.github.io/Creality-Helper-Script-Wiki/) |
| Guilouz Helper Script | [github.com/Guilouz/Creality-Helper-Script](https://github.com/Guilouz/Creality-Helper-Script) |
| Support Guilouz | [ko-fi.com/guilouz](https://ko-fi.com/guilouz) |

---

## Creality K2 Plus Official

| Resource | Link |
|---|---|
| K2 Series Firmware | [crealitycloud.com/software-firmware/firmware/k2-series](https://www.crealitycloud.com/software-firmware/firmware/k2-series) |
| Creality Open Source | [github.com/CrealityOfficial/K2_Series_Klipper](https://github.com/CrealityOfficial/K2_Series_Klipper) |
| Creality Cloud | [crealitycloud.com](https://www.crealitycloud.com/) |
| Creality Support | [crealitycloud.com/support](https://www.crealitycloud.com/support) |

---

## Klipper Ecosystem

| Resource | Link |
|---|---|
| Klipper Documentation | [klipper3d.org/Overview.html](https://www.klipper3d.org/Overview.html) |
| Klipper Config Reference | [klipper3d.org/Config_Reference.html](https://www.klipper3d.org/Config_Reference.html) |
| Klipper G-Code Reference | [klipper3d.org/G-Codes.html](https://www.klipper3d.org/G-Codes.html) |
| Moonraker Documentation | [moonraker.readthedocs.io](https://moonraker.readthedocs.io/) |
| Fluidd Documentation | [docs.fluidd.xyz](https://docs.fluidd.xyz/) |
| Mainsail Documentation | [docs.mainsail.xyz](https://docs.mainsail.xyz/) |
| KAMP (Adaptive Meshing) | [github.com/kyleisah/Klipper-Adaptive-Meshing-Purging](https://github.com/kyleisah/Klipper-Adaptive-Meshing-Purging) |

---

## Slicers

| Resource | Link |
|---|---|
| OrcaSlicer | [github.com/SoftFever/OrcaSlicer/releases](https://github.com/SoftFever/OrcaSlicer/releases/latest) |
| Creality Print | [creality.com/pages/download](https://www.creality.com/pages/download) |

---

## Community

| Resource | Link |
|---|---|
| Creality K2 Plus Reddit | [reddit.com/r/crealityk1](https://www.reddit.com/r/crealityk1/) |
| Guilouz Discussions | [github.com/Guilouz/Creality-Helper-Script-Wiki/discussions](https://github.com/Guilouz/Creality-Helper-Script-Wiki/discussions) |
| OctoEverywhere | [octoeverywhere.com](https://octoeverywhere.com/) |
| Mobileraker | [mobileraker.com](https://mobileraker.com/) |
| SimplyPrint K2 Guide | [simplyprint.io/setup-guide/creality/k2](https://simplyprint.io/setup-guide/creality/k2) |

---

## Stock K2 Plus Configuration Files

The stock Klipper config files for the K2 Plus are available in the Guilouz extracted firmware repository:

| Resource | Link |
|---|---|
| Guilouz K2 Plus Extracted Firmware | [github.com/Guilouz/Creality-K2Plus-Extracted-Firmwares](https://github.com/Guilouz/Creality-K2Plus-Extracted-Firmwares) |


---

