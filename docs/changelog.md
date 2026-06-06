# Changelog

## Helper Script Improvements — June 6, 2026

Full end-to-end test of all 23 menu options completed. The following improvements were made:

**Already-installed checks:**
All install scripts (options 1-11) now detect if a feature is already installed and prompt to reinstall rather than running blindly.

**Remove confirmations:**
All remove scripts now show a warning and require y/N confirmation before removing any feature.

**Backup confirmation:**
Option 16 (Backup Klipper configuration) now asks for confirmation before running.

**Restart confirmations:**
Options 18 (Restart Klipper), 19 (Restart Moonraker), and 20 (Restart Nginx) now ask for confirmation before restarting.

**Fluidd nginx restore:**
Option 8 (Fluidd) now includes a third sub-option to restore the nginx block only (port 4408), matching the same option already available for Mainsail (port 4409).

**Stub scripts for unimplemented features:**
Options 12 (OctoEverywhere), 13 (Mobileraker Companion), and 14 (Git Backup) now show a friendly message instead of crashing. These features are not yet implemented for K2 Plus.

**HelixScreen moonraker.conf cleanup:**
HelixScreen installer adds an `[update_manager]` section to moonraker.conf which is not supported on K2 Plus. The helixscreen.sh script now automatically removes this section after installation.

---

## HelixScreen Integration — June 6, 2026

HelixScreen v0.99.72 was successfully installed and tested on the Creality K2 Plus.

**What works:**

- Modern touchscreen UI replacing the stock Creality interface
- Temperature monitoring and control
- Print management and history
- Homing, movement, and all Klipper controls
- Auto-updates via Fluidd/Mainsail update manager
- CFS (Color Filament System) support

**Known limitation:**

- WiFi management shows as unavailable in HelixScreen — this is cosmetic only. The K2 Plus uses a proprietary WiFi management system that HelixScreen cannot access. The printer WiFi connection is not affected.

HelixScreen has been added to the helper script as option 11 and documented in the wiki. Full credit goes to [prestonbrown](https://github.com/prestonbrown) and the HelixScreen contributors for their excellent work and explicit K2 series support.

---

## Camera Investigation — June 5, 2026

Extensive investigation was conducted to enable the K2 Plus camera in Fluidd and Mainsail. All known approaches were exhausted:

- **WebRTC** — `webrtc_local` runs on port 8000 but uses a proprietary Creality protocol incompatible with Fluidd/Mainsail's WebRTC camera types (camera-streamer, go2rtc, MediaMTX)
- **Direct V4L2 access** — `/dev/video0` reports `capabilities: 0x0`, meaning the camera hardware is completely locked behind `cam_app` and cannot be accessed via standard Linux V4L2 APIs
- **Entware + mjpg-streamer** — Entware is incompatible with the K2 Plus due to ARM ABI mismatch (K2 Plus uses armhf hard-float, Entware only provides armv7sf soft-float binaries)
- **Python3 MJPEG streamer** — Attempted to read frames directly from `/dev/video0` using Python3 ctypes and the V4L2 API. Failed because the device reports no capabilities
- **cam_app socket interception** — `cam_app` outputs to `/tmp/delivery_socket100` using an undocumented binary protocol. No community documentation exists for this protocol

**Conclusion:** The K2 Plus camera cannot currently be used in Fluidd or Mainsail. The camera works only in Creality Print and on the touchscreen. See [Configure Camera](configurations/configure-camera.md) for the full technical details.

If you find a working solution, please share it in the [Discussions](https://github.com/sw3defy/Creality-Helper-Script-Wiki-K2-Plus/discussions).

---

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
