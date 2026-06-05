# Creality K2 Plus — Helper Script Wiki

<div style="display:flex;gap:20px;margin-bottom:20px;">
<div style="flex:1;text-align:center;"><img src="https://drive.google.com/thumbnail?id=1CIxSAh3cxYCOOIXIYoKQgjuqBXqa_m67&sz=w600" alt="Creality K2 Plus"><br><strong>Creality K2 Plus</strong></div>
<div style="flex:1;text-align:center;"><img src="https://drive.google.com/thumbnail?id=1rho-b_3_4d2JEmcygVluVi7r-sPNvQe9&sz=w600" alt="Creality K2 Plus Combo"><br><strong>Creality K2 Plus Combo (with CFS)</strong></div>
</div>


This wiki covers the complete process to root the **Creality K2 Plus** and **K2 Plus Combo**, and add features using the Creality K2 Plus Helper Script.

The advantage of rooting your printer is having full access to the firmware and configuration files, enabling you to install community tools, improve print quality, and extend your printer far beyond its factory defaults.

!!! danger "Read before proceeding"
    If you don't know what you're doing, I don't recommend following this guide.
    Modifying system files can cause issues if done incorrectly. Always back up your configuration before making changes.

!!! note "This wiki is for the K2 Plus only"
    This wiki is written specifically for the **Creality K2 Plus** and **K2 Plus Combo (with CFS)**.
    For K1 Series, K1C, K1 Max, or Ender-3 V3 Series — see the [original Guilouz wiki](https://guilouz.github.io/Creality-Helper-Script-Wiki/).

---


---

## Support This Project

If you find this wiki and helper script useful, consider supporting the work!

<a href="https://buymeacoffee.com/sw3defy" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50"></a>
&nbsp;&nbsp;
<a href="https://ko-fi.com/sw3defy" target="_blank"><img src="https://storage.ko-fi.com/cdn/kofi2.png?v=3" alt="Support me on Ko-fi" height="50"></a>

## About This Wiki

This project is a fork of the excellent [Guilouz Creality Helper Script Wiki](https://github.com/Guilouz/Creality-Helper-Script-Wiki), adapted from the ground up for the K2 Plus. The K2 Plus has a fundamentally different architecture from the K1 Series — different filesystem paths, service manager, pre-installed software, and unique hardware (heated chamber, dual Z motors, CFS multi-material system).

All content specific to the K2 Plus has been verified on live hardware via SSH. See [Special Thanks](special-thanks.md) for full attribution.

---

## Key Differences from K1 Series

Understanding these differences is important before following any guide. K1-targeted instructions will not work on the K2 Plus without modification.

| Feature | K1 Series | K2 Plus |
|---|---|---|
| Persistent data path | `/usr/data/` | `/mnt/UDISK/` |
| Root password | `creality_2023` | **`creality_2024`** |
| Service manager | Supervisor Lite (`supervisorctl`) | OpenWrt rc.d (`/etc/init.d/`) |
| Restart Klipper | `supervisorctl restart klipper` | `/etc/init.d/S55klipper restart` |
| Restart Moonraker | `supervisorctl restart moonraker` | `/etc/init.d/S56moonraker restart` |
| Fluidd pre-installed | No | **Yes** (port 4408) |
| Moonraker pre-installed | No | **Yes** (read-only at `/usr/share/`) |
| Heated chamber | No | **Yes** (`heater_generic chamber_heater`) |
| Multi-material (CFS) | No | **Yes** (Combo model, `box.cfg`) |
| Accelerometer | ADXL345 | **LIS2DW** (SPI on nozzle_mcu) |
| Kinematics | CoreXY | CoreXY |
| Print volume | 220×220×250mm | **350×350×360mm** |
| Bed mesh | 7×7 | **9×9 (5,5 → 345,345)** |
| Z axis | Single Z motor | **Dual Z motors (z_tilt)** |
| Probe type | Inductive | **prtouch_v3 (strain gauge)** |
| OS | Tina 4.x / OpenWrt | **Tina 5.0 / OpenWrt 21.02** |
| Board ID | `K1_CR4CU220812S12` | **`F008_CR0CN240319C13_1`** |

---

## Quick Start

1. [Enable root access and connect via SSH](firmwares/install-and-update-rooted-firmware-k2plus.md#enable-root-access)
2. [Install the Helper Script](helper-script/helper-script-installation.md)
3. Install features in the [recommended order](helper-script/helper-script-installation.md#recommended-installation-order)
4. [Configure OrcaSlicer](slicers/orcaslicer.md) with the correct K2 Plus start/end G-code

---

## Wiki

Full wiki available at: [sw3defy.github.io/Creality-Helper-Script-Wiki-K2-Plus](https://sw3defy.github.io/Creality-Helper-Script-Wiki-K2-Plus/)

Helper Script repository: [github.com/sw3defy/Creality-Helper-Script-K2-Plus](https://github.com/sw3defy/Creality-Helper-Script-K2-Plus)
