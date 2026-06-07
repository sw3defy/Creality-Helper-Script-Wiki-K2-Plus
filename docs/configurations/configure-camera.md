# Camera Support for Fluidd and Mainsail — K2 Plus

The K2 Plus has a built-in camera that uses a proprietary WebRTC protocol on port 8000. Through reverse engineering, a working bridge has been developed that makes the camera available in both the Fluidd and Mainsail dashboards.

!!! success "Camera fix — tested and working!"
    The camera feed shows automatically in the Fluidd dashboard after boot with no manual steps required.

---

## How It Works

The K2 Plus camera uses a custom WebRTC signaling protocol (base64 encoded JSON over HTTP POST on port 8000). The solution consists of:

1. **k2rtc.py** — A Python bridge that translates go2rtc SDP format to the K2 Plus proprietary base64 JSON WebRTC format
2. **Hidden iframe** — Keeps a permanent background WebRTC connection open so go2rtc maintains correct internal stream routing
3. **Auto-reload** — JavaScript in Fluidd detects when the stream is ready and automatically reloads the page once to show the camera feed
4. **go2rtc v1.9.14** — ARM hard-float binary that converts the stream for Fluidd
5. **camera_watchdog.py** — Monitors the stream and reconnects if it drops
6. **Nginx proxy** — Routes WebSocket connections with correct stream source parameters
7. **Startup service** — Auto-starts everything on boot via rc.local

Full credit for the original WebRTC discovery goes to [DnG-Crafts](https://github.com/DnG-Crafts/K2-Camera).

---

## Installation

Install from the helper script:

```sh
sh /mnt/UDISK/helper-script/helper.sh
```

Select **11) Camera Support for Fluidd and Mainsail**.

---

## After Installation

The camera appears automatically in both Fluidd and Mainsail after boot:

1. Printer boots up
2. After ~60-90 seconds go2rtc connects to the K2 camera
3. Fluidd automatically reloads once and shows the camera feed

No manual steps required.

!!! note "First open after boot"
    When you first open Fluidd after boot, the page will auto-reload once within 60-90 seconds. This is normal — it happens when the background stream becomes ready.

---

## Direct Camera Access

The camera can also be accessed directly:

```
http://YOUR_PRINTER_IP:4408/camera.html
```

Or via go2rtc web interface:

```
http://YOUR_PRINTER_IP:1984/stream.html?src=k2plus&mode=webrtc
```

---

## Known Limitations

- **Startup delay** — Camera takes 60-90 seconds after boot to appear
- **Firmware updates** — A firmware update may remove the nginx and rc.local changes. Re-run the camera install after any firmware update.
- **Single stream** — Only one WebRTC connection to the K2 camera at a time

---

## Credits

- [DnG-Crafts](https://github.com/DnG-Crafts/K2-Camera) — Original K2 camera WebRTC discovery
- [AlexxIT/go2rtc](https://github.com/AlexxIT/go2rtc) — Stream conversion software
