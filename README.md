# Creality K2 Plus - Helper Script Wiki

A complete wiki and helper script for the **Creality K2 Plus** and **K2 Plus Combo (with CFS)**.

Forked and adapted from the excellent [Guilouz Creality Helper Script Wiki](https://github.com/Guilouz/Creality-Helper-Script-Wiki) - rebuilt from the ground up for the K2 Plus architecture.

## Wiki

**[https://sw3defy.github.io/Creality-Helper-Script-Wiki-K2-Plus/](https://sw3defy.github.io/Creality-Helper-Script-Wiki-K2-Plus/)**

## Helper Script

**[https://github.com/sw3defy/Creality-Helper-Script-K2-Plus](https://github.com/sw3defy/Creality-Helper-Script-K2-Plus)**

## About

The K2 Plus has a fundamentally different architecture from the K1 Series:
- Different filesystem paths (`/mnt/UDISK/` instead of `/usr/data/`)
- Different service manager (OpenWrt procd instead of supervisorctl)
- Pre-installed Fluidd on port 4408
- Dual Z motors, CoreXY, 350x350x360mm build volume
- Heated chamber
- CFS (Color Filament System) multi-material support
- LIS2DW accelerometer (not ADXL345)

All content has been **verified on live K2 Plus hardware via SSH**.

## Features

- Moonraker Extensions & Update Manager
- Fluidd & Mainsail web interfaces
- Fans Control, Useful Macros, Z-Offset, M600 support
- KAMP (Klipper Adaptive Meshing & Purging)
- Improved Shapers Calibrations
- Moonraker Timelapse
- Camera Support for Fluidd (WebRTC bridge via go2rtc)
- HelixScreen (modern touchscreen UI)
- OctoEverywhere, Mobileraker, Git Backup
- Backup & Restore of Klipper configuration

## Support

<a href="https://buymeacoffee.com/sw3defy"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="60"></a>

<a href="https://ko-fi.com/sw3defy"><img src="https://ko-fi.com/img/githubbutton_sm.svg" height="60"></a>

## Discussions

[Join the discussion](https://github.com/sw3defy/Creality-Helper-Script-Wiki-K2-Plus/discussions)

## Credits

- [Guilouz](https://github.com/Guilouz) - Original Creality Helper Script Wiki for K1 Series
- [DnG-Crafts](https://github.com/DnG-Crafts/K2-Camera) - K2 camera WebRTC discovery
- [AlexxIT/go2rtc](https://github.com/AlexxIT/go2rtc) - Stream conversion software
- [prestonbrown/HelixScreen](https://github.com/prestonbrown/helixscreen) - Modern touchscreen UI for Klipper
- [Klipper](https://www.klipper3d.org) - 3D printer firmware
- [Moonraker](https://moonraker.readthedocs.io) - API server
- [Fluidd](https://docs.fluidd.xyz) - Web interface
- [Mainsail](https://docs.mainsail.xyz) - Web interface
- [KAMP](https://github.com/kyleisah/Klipper-Adaptive-Meshing-Purging) - Adaptive meshing
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - Wiki theme
