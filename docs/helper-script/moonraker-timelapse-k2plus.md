# Moonraker Timelapse — K2 Plus

!!! warning "November 2026: installation and removal blocked"
    The legacy Timelapse installer can overwrite Moonraker component files and Klipper macros. Existing K2 Plus configurations may already contain `[timelapse]`; do not blindly reinstall, delete, or replace it. The unmerged development branch blocks both operations until component ownership, camera compatibility, and a reversible migration are verified. The instructions below document historical usage, not a currently approved installation procedure.


Moonraker Timelapse is a third-party Moonraker component that creates timelapse recordings of prints by capturing a frame at each layer change.

---

## Installation

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **Moonraker Timelapse**.

The component is installed to `/mnt/UDISK/printer_data/` and registered in `/mnt/UDISK/printer_data/config/moonraker.conf`.

---

## Timelapse Video Location

Completed timelapse videos are saved to:

```
/mnt/UDISK/printer_data/timelapse/
```

!!! note "Path difference from K1"
    On K1, timelapse videos are saved to `/usr/data/printer_data/timelapse/`. On K2 Plus the path is `/mnt/UDISK/printer_data/timelapse/`.

Videos can be downloaded directly from Fluidd's file manager under the **Timelapse** section, or via SCP:

```bash
scp root@<printer-ip>:/mnt/UDISK/printer_data/timelapse/my_print.mp4 ./
```

---

## Slicer Setup

Add the following to your slicer's layer change G-code:

```gcode
TIMELAPSE_TAKE_FRAME
```

And add this to your `END_PRINT` macro or slicer end G-code:

```gcode
TIMELAPSE_RENDER
```

---

## Camera

Moonraker Timelapse uses the snapshot URL from the camera configuration to capture frames. With the K2 Plus camera solution installed, the snapshot URL is:

```
http://<printer-ip>:4409/go2rtc/api/frame.jpeg?src=k2plus
```

Ensure [Camera Support](../../configurations/configure-camera.md) is installed before enabling timelapse.
