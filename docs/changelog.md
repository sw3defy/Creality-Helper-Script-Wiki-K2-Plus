# Changelog

## CFS Load/Unload Fix — June 17, 2026

### Bug Fixes

**`box.cfg` and `gcode_macro.cfg` — Macro underscore prefix bug:**
The stock Creality firmware ships `box.cfg` and `gcode_macro.cfg` with all
CFS-related macros prefixed with an underscore (e.g. `_BOX_QUIT_MATERIAL`,
`_WAIT_TEMP_START`, `_END_PRINT_POINT`). In Klipper, a leading underscore
makes a macro private/hidden — it cannot be called by the CFS system, the UI,
or other macros. This caused the entire CFS load/unload sequence to silently
fail with a cascade of errors.

The helper script now automatically patches both files on every startup via
`patch_stock_configs()` in `system.sh`.

Errors resolved by this fix:

- `key865` — retrude error, failed to exit connections
- `key789` — position tracking error on X/Y axes
- `key22` — no trigger on Y after full movement
- `key274` — unknown g-code state: helix_cfs_load
- `Unknown command: WAIT_TEMP_START`
- `Unknown command: END_PRINT_POINT`
- `Unknown command: CANCEL_CHAMBER_FAN_SWITCH`

**`useful_macros.sh` — Conflicting macro override:**
`useful_macros.sh` was installing its own versions of `START_PRINT`,
`END_PRINT`, `PAUSE`, `RESUME`, and `CANCEL_PRINT`, overwriting the stock
Creality versions which have full CFS integration (`BOX_START_PRINT`,
`BOX_END`, `BOX_END_PRINT` etc.). This broke filament loading and unloading
during prints. These macros have been removed from `useful_macros.sh` — the
stock versions are used instead.

---

## Mainsail Macro Fixes — June 17, 2026

Systematic testing of all Mainsail macros revealed and fixed several bugs in the helper script and installed config files.

### Bug Fixes

**`fans.sh` — SET_FAN0 / SET_FAN2 PWM scaling bug:**
`SET_FAN0` and `SET_FAN2` were converting the S parameter (0-255) to a 0.0-1.0 PWM value before passing it to `SET_PIN`. However, `fan0` and `fan2` in `printer.cfg` have `scale: 255`, which means `SET_PIN` already expects 0-255 values. The double conversion was causing fans to run at tiny fractions of the requested speed. Fixed by removing the PWM conversion — raw 0-255 values are now passed directly.

**`z_offset.sh` — SET_Z_OFFSET / RESET_Z_OFFSET require homing first:**
`SET_Z_OFFSET` and `RESET_Z_OFFSET` were calling `SET_GCODE_OFFSET Z=x MOVE=1` without first homing the printer. `MOVE=1` requires a homed toolhead or Klipper errors. Fixed by adding `G28` before the offset is applied in both macros.

**`useful_macros.sh` — post-install patch for stock `gcode_macro.cfg`:**
The stock Creality `gcode_macro.cfg` contains two bugs that cause Mainsail macros to fail:

- **`PROBE_COUNT=` bug:** `G29` and `BED_MESH_CALIBRATE_START_PRINT` build the `PROBE_COUNT` parameter as `'PROBE_COUNT' + params.PROBE_COUNT`, missing the `=` sign, producing invalid gcode like `PROBE_COUNT9,9` instead of `PROBE_COUNT=9,9`.
- **Internal macro name references:** `END_PRINT` and `START_PRINT` call internal helper macros (`END_PRINT_Z_SAFE`, `Qmode_exit`, `PRINT_PREPARE_CLEAR`, `END_PRINT_POINT`, `WAIT_TEMP_START`) that have been renamed with a `_` prefix to hide them from Mainsail. The call sites were not updated.

`useful_macros.sh` now runs a python3 patch on `gcode_macro.cfg` after install to fix both issues automatically.

**`shapers.sh` — BELTS_SHAPER_CALIBRATION / EXCITATE_AXIS_AT_FREQ homing crash:**
Both macros call `G28` when the printer is not homed. If a bed mesh is loaded, `G28` triggers `BED_MESH_PROFILE LOAD=default` at the end of homing which then causes a crash because the mesh probe points conflict with the current toolhead position. Fixed by adding `BED_MESH_CLEAR` before `G28` in both macros. `EXCITATE_AXIS_AT_FREQ` also adds `M400` after `G28` to ensure homing completes before the resonance test begins.

### Macro Visibility (Mainsail)

All internal and touchscreen-only macros in `gcode_macro.cfg`, `box.cfg`, `timelapse.cfg`, `sensorless.cfg`, and `printer_params.cfg` were prefixed with `_` to hide them from the Mainsail macro list. This leaves only user-facing macros visible. The `useful_macros.sh` post-install patch handles the renames in `gcode_macro.cfg` automatically on fresh installs.

### Macros Tested and Confirmed Working

The following macros were tested end-to-end on a K2 Plus with firmware v1.1.260206:

`ACCURATE_G28`, `BED_LEVELING`, `BED_MANUAL_CAL`, `BELT_TENSION`, `BELTS_SHAPER_CALIBRATION`, `CALIBRATE_CUT_POS`, `CHAMBER_COOL`, `CHAMBER_HEAT`, `CHAMBER_STATUS`, `EXCITATE_AXIS_AT_FREQ`, `FANS_OFF`, `GET_TIMELAPSE_SETUP`, `INPUT_SHAPER_CALIBRATION`, `M141`, `M600`, `MAINSAIL_HOME`, `MAINTENANCE_ITEM`, `PID_CHAMBER`, `PID_HOTEND`, `RESET_Z_OFFSET`, `RESTORE_FANS`, `RESTORE_SHAPERS`, `SAVE_FANS`, `SAVE_Z_OFFSET`, `SET_FAN0`, `SET_FAN2`, `SET_Z_OFFSET`, `WARMUP`, `Z_AXIS_CALIBRATION`, `Z_TILT_CALIBRATE`

---

## Entware Package Manager — June 8, 2026

Entware package manager successfully installed on the K2 Plus using a Python-based wget shim to bootstrap the installer. This bypasses the ARM ABI incompatibility (K2 Plus uses armhf hard-float, Entware's armv7sf soft-float binaries work via the shim approach).

Added as **option 15** in the helper script.

**What Entware provides:**
- Hundreds of Linux packages via opkg
- git, nano, htop, curl, openssh-sftp-server and much more
- Persistent across reboots via rc.local

Full credit to [vsevolod-volkov](https://github.com/vsevolod-volkov/K2Plus-entware) for the wget shim solution.

---

## Mainsail Camera Support — June 7, 2026

Camera support extended to Mainsail in addition to Fluidd.

**Changes:**

- go2rtc proxy added to port 4409 (Mainsail) nginx block with `$args` passthrough for Mainsail WebSocket compatibility
- Mainsail index.html gets JavaScript injection to force `enabled: true` on webcams (Mainsail v2.17.0 filters cameras by enabled field which Moonraker does not store)
- Single camera entry in Moonraker named "K2 Camera" using port 4409, works for both Fluidd and Mainsail
- go2rtc config updated with `origin: '*'` to allow cross-origin WebSocket connections between ports 4408 and 4409

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

### Final Solution — June 7, 2026

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

## Helper Script Improvements — June 6, 2026

Full end-to-end test of all 24 menu options completed. The following improvements were made:

**Already-installed checks:**
All install scripts (options 1-12) now detect if a feature is already installed and prompt to reinstall rather than running blindly.

**Remove confirmations:**
All remove scripts now show a warning and require y/N confirmation before removing any feature.

**Backup confirmation:**
Option 16 (Backup Klipper configuration) now asks for confirmation before running.

**Restart confirmations:**
Options 18 (Restart Klipper), 19 (Restart Moonraker), and 20 (Restart Nginx) now ask for confirmation before restarting.

**Fluidd nginx restore:**
Option 8 (Fluidd) now includes a third sub-option to restore the nginx block only (port 4408), matching the same option already available for Mainsail (port 4409).

**Stub scripts for unimplemented features:**
Options 13 (OctoEverywhere), 14 (Mobileraker Companion), and 15 (Git Backup) now show a friendly message instead of crashing. These features are not yet implemented for K2 Plus.

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

HelixScreen has been added to the helper script as option 12 and documented in the wiki. Full credit goes to [prestonbrown](https://github.com/prestonbrown) and the HelixScreen contributors for their excellent work and explicit K2 series support.

---

## Sw3Defy K2 Plus Helper Script Wiki

### v1.0.0 — June 1, 2026

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
- Features included: Moonraker Extensions, Fluidd (repair/update), Mainsail, KAMP, Fans Control Macros, Useful Macros, Improved Shapers Calibrations, Save Z-Offset Macros, M600 Support, Moonraker Timelapse, Camera Support for Fluidd and Mainsail (WebRTC via go2rtc), HelixScreen, Entware Package Manager, Git Backup, OctoEverywhere, Mobileraker Companion
- CFS-aware macros for K2 Plus Combo
- Chamber heater integration in START_PRINT and WARMUP

---

## Original Guilouz Creality Helper Script

This wiki is forked from [Guilouz/Creality-Helper-Script-Wiki](https://github.com/Guilouz/Creality-Helper-Script-Wiki).
For the K1 Series changelog, see the [original changelog](https://guilouz.github.io/Creality-Helper-Script-Wiki/changelog/).
