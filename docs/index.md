# Creality K2 Plus — Helper Script Wiki

This wiki covers the full process to root the **Creality K2 Plus** and **K2 Plus Combo** and add features using the Creality Helper Script.

The advantage is having full access to the firmware and configuration files to make changes.

!!! warning "K2 Plus specific"
    This wiki is written specifically for the **Creality K2 Plus** and **K2 Plus Combo**.
    For K1 Series or Ender-3 V3 Series, see the [original wiki](https://guilouz.github.io/Creality-Helper-Script-Wiki/).

!!! danger "Read before proceeding"
    If you don't know what you're doing, I don't recommend following this guide.
    Rooting your printer and modifying system files can cause issues if done incorrectly.

---

## Key Differences from K1 Series

| Item | K1 Series | K2 Plus |
|---|---|---|
| Persistent data path | `/usr/data/` | `/mnt/UDISK/` |
| Root password | `creality_2023` | `creality_2024` |
| Service manager | Supervisor Lite | OpenWrt rc.d |
| Restart services | `supervisorctl restart` | `/etc/init.d/S55klipper restart` |
| Fluidd pre-installed | No | **Yes** (port 4408) |
| Chamber heater | No | **Yes** (heater_generic) |
| Multi-material (CFS) | No | **Yes** (Combo model) |
| Accelerometer | ADXL345 | LIS2DW |
| Kinematics | CoreXY | CoreXY |
| Print volume | 220×220×250 (K1) | **350×350×360** |

---

## Wiki

Guide is available here: [Wiki](https://sw3defy.github.io/Creality-Helper-Script-Wiki-K2-Plus/)
