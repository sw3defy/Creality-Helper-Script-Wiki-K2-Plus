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
