# Changelog

## Sw3Defy K2 Plus Helper Script Wiki

### v1.0.0 — June 2026

Initial release of the Creality K2 Plus Helper Script Wiki and companion helper script.

**Wiki:**

- Full K2 Plus documentation written from scratch based on live hardware verification
- All paths updated to `/mnt/UDISK/` (K2 Plus filesystem)
- All service commands updated to OpenWrt rc.d (`/etc/init.d/S55klipper restart` etc.)
- Root password documented as `creality_2024`
- K2 Plus-specific pages: CFS, heated chamber, dual-Z, LIS2DW accelerometer
- Removed all K1/Ender-3 specific content
- OrcaSlicer page updated for 350×350×360mm build volume and chamber temperature support

**Helper Script:**

- Built from scratch for K2 Plus — not a port of the K1 script
- Installs to `/mnt/UDISK/helper-script/`
- Moonraker extension approach: wraps stock read-only config with persistent `/mnt/UDISK/printer_data/config/moonraker.conf`
- No `supervisorctl` dependency — uses OpenWrt rc.d throughout
- Features included: Moonraker Extensions, Fluidd (repair/update), Mainsail, KAMP, Fans Control Macros, Useful Macros, Improved Shapers Calibrations, Save Z-Offset Macros, M600 Support, Moonraker Timelapse, Git Backup, OctoEverywhere, Mobileraker Companion
- CFS-aware macros for K2 Plus Combo
- Chamber heater integration in START_PRINT and WARMUP
- Full K1 Max macro set ported: BELTS_SHAPER_CALIBRATION, EXCITATE_AXIS_AT_FREQ, TEST_RESONANCES_GRAPHS, AUTOTUNE_SHAPERS

---

## Original Guilouz Creality Helper Script

This wiki is forked from [Guilouz/Creality-Helper-Script-Wiki](https://github.com/Guilouz/Creality-Helper-Script-Wiki).
For the K1 Series changelog, see the [original changelog](https://guilouz.github.io/Creality-Helper-Script-Wiki/changelog/).
