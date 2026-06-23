# Camera Support for Fluidd and Mainsail — K2 Plus

The K2 Plus has a built-in camera that uses a proprietary WebRTC protocol on port 8000 (`webrtc_local`). go2rtc connects to it directly and re-serves the stream to both Fluidd and Mainsail.

!!! success "Camera fix — tested and working!"
    The camera feed shows automatically in both the Fluidd and Mainsail dashboards after boot, with no manual steps and no dependency between the two interfaces.

---

## How It Works

The K2 Plus's `webrtc_local` service sends RTP using a payload type that it never lists in its own SDP answer. Without accounting for this, a generic WebRTC client (including a default go2rtc connection) ends up with the actual video data routed to an internal receiver that nothing is consuming, so the connection reports "connected" while no video frame ever renders.

go2rtc has an official handler for exactly this quirk, added in v1.9.10, via the `#format=creality` source modifier:

```yaml
streams:
  k2plus:
    - "webrtc:http://127.0.0.1:8000/call/webrtc_local#format=creality"
```

This connects go2rtc directly to `webrtc_local` and correctly matches the camera's actual payload type to the receiver that Fluidd/Mainsail consume from.

The solution consists of:

1. **go2rtc v1.9.14+** — ARM binary, connects directly to `webrtc_local` on port 8000 using `#format=creality`
2. **Nginx proxy** — Routes WebSocket/HTTP connections on ports 4408 (Fluidd) and 4409 (Mainsail) to go2rtc's API on port 1984
3. **camera_watchdog.py** — Monitors the stream and reconnects if the producer drops
4. **Startup service** — Auto-starts go2rtc on boot via rc.local

An earlier version of this fix used a hand-rolled Python relay (`k2rtc.py`) plus a hidden keepalive iframe and auto-reload JavaScript in Fluidd to work around the payload-type issue indirectly. Those workarounds are no longer needed now that go2rtc's `#format=creality` handler addresses the root cause directly, and have been removed.

Full credit for the original WebRTC discovery goes to [DnG-Crafts](https://github.com/DnG-Crafts/K2-Camera), and to [AlexxIT/go2rtc](https://github.com/AlexxIT/go2rtc) for the official Creality format handler (see [go2rtc#2024](https://github.com/AlexxIT/go2rtc/issues/2024) for background on the underlying firmware quirk this works around).

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
3. The camera feed shows in both Fluidd and Mainsail independently — opening one does not affect the other

No manual steps required.

!!! note "First open after boot"
    The camera takes 60-90 seconds after boot to become available, since the startup service waits for the rest of the printer's services to come up first.

---

## Direct Camera Access

The camera can also be accessed directly:

```
http://YOUR_PRINTER_IP:4408/camera.html
```

Or via go2rtc's own web interface:

```
http://YOUR_PRINTER_IP:1984/stream.html?src=k2plus&mode=webrtc
```

---

## Known Limitations

- **Startup delay** — Camera takes 60-90 seconds after boot to appear
- **Firmware updates** — A firmware update may remove the nginx and rc.local changes. Re-run the camera install after any firmware update.

---

## Credits

- [DnG-Crafts](https://github.com/DnG-Crafts/K2-Camera) — Original K2 camera WebRTC discovery
- [AlexxIT/go2rtc](https://github.com/AlexxIT/go2rtc) — Stream conversion software and the official Creality format handler
