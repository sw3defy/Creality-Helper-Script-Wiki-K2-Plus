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

## Camera Support for Fluidd — Full Story — June 5-7, 2026

After extensive research, reverse engineering, and testing, a fully working camera solution was developed for the K2 Plus that integrates the camera feed directly into the Fluidd dashboard.

### Investigation (June 5, 2026)

All known approaches were investigated:

- **WebRTC (go2rtc, camera-streamer, MediaMTX)** — The K2 Plus camera uses a proprietary Creality WebRTC protocol that is incompatible with all standard Fluidd/Mainsail WebRTC camera types
- **Direct V4L2 access** —  reports  — completely locked behind Creality firmware
- **Entware + mjpg-streamer** — Incompatible due to ARM ABI mismatch (K2 Plus uses armhf hard-float, Entware only provides armv7sf soft-float)
- **Python3 MJPEG streamer** — Failed because V4L2 device reports no capabilities
- **cam_app socket interception** —  outputs to  using an undocumented binary protocol

### Breakthrough (June 6, 2026)

The K2 Plus camera WebRTC protocol was reverse engineered by inspecting the raw HTTP traffic to port 8000. Key findings:

- The camera accepts WebRTC SDP offers via HTTP POST to 
- The SDP offer must be wrapped in a JSON object  and base64 encoded
- The camera responds with a base64 encoded JSON answer containing the SDP response
- go2rtc sends plain SDP — a Python bridge was written to translate between the formats

**k2rtc.py** — A custom Python WebRTC bridge was developed that:
1. Receives plain SDP from go2rtc
2. Wraps it in JSON and base64 encodes it for the K2 camera
3. Decodes the base64 JSON response and returns plain SDP to go2rtc

With the correct ICE candidate configuration ( in go2rtc.yaml) the stream worked in go2rtc's stream.html.

### Fluidd Integration (June 6-7, 2026)

Getting the stream into Fluidd required solving several additional problems:

- **Fluidd enable toggle bug** — Fluidd v1.37.1 stores the camera  state separately from Moonraker. Our Moonraker version does not support the  field. A JavaScript injection in  was used to force-enable the camera widget.
- **WebSocket routing** — Fluidd connects to go2rtc via WebSocket at . Nginx needed a specific proxy rule to add  to the WebSocket URL.
- **Stream not found** — go2rtc reported  because the stream was not pre-connected. The k2rtc.py pre-connect function was added.
- **Dual receiver bug** — The root cause of intermittent failures: go2rtc creates two internal receivers when connecting to the K2 camera and routes video to the wrong one. A hidden iframe in Fluidd keeps a permanent background WebRTC connection open, forcing correct routing.
- **Auto-reload** — sessionStorage-based JavaScript detects when the stream is ready (500KB received) and automatically reloads Fluidd once to show the camera feed.

### Final Solution

The complete working solution consists of:

1. **k2rtc.py** — Python WebRTC bridge translating go2rtc SDP to K2 Plus base64 JSON format
2. **go2rtc v1.9.14** — ARM hard-float stream converter
3. **Hidden iframe** — Keeps background WebRTC connection open for correct go2rtc routing
4. **JavaScript injection** — Auto-enables camera widget and auto-reloads page when stream is ready
5. **camera_watchdog.py** — Monitors stream and reconnects if dropped
6. **Nginx proxy** — Routes WebSocket with  parameter
7. **rc.local startup** — Starts everything automatically after boot with 60 second delay

**Result:** Camera feed appears automatically in Fluidd dashboard after boot with no manual steps required.

Full credit to [DnG-Crafts](https://github.com/DnG-Crafts/K2-Camera) for the original WebRTC discovery and [AlexxIT](https://github.com/AlexxIT/go2rtc) for go2rtc.

---

## ## Sw3Defy K2 Plus Helper Script Wiki

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
