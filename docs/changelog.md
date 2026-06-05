# Changelog

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
