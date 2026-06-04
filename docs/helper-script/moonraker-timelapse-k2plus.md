# Moonraker Timelapse — K2 Plus

Moonraker Timelapse captures a frame at each layer change to create a timelapse of your print.

---

## Installation

From the `[Install] Menu` install **Moonraker Timelapse**.

---

## Timelapse Video Location

```
/mnt/UDISK/printer_data/timelapse/
```

!!! note "Path difference from K1"
    On K1 timelapse videos are at `/usr/data/printer_data/timelapse/`. On K2 Plus: `/mnt/UDISK/printer_data/timelapse/`.

Download via Fluidd's file manager or SCP:

```bash
scp root@<printer-ip>:/mnt/UDISK/printer_data/timelapse/my_print.mp4 ./
```

---

## Slicer Setup

Layer change G-code:

```gcode
TIMELAPSE_TAKE_FRAME
```

End G-code:

```gcode
TIMELAPSE_RENDER
```
