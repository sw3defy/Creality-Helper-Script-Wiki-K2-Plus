# M600 Support — K2 Plus

M600 is the standard filament change G-code command. On the K2 Plus, M600 behavior differs depending on whether you are using single-filament mode or the CFS.

---

## Installation

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **M600 Support**.

---

## Single-Filament Mode

In single-filament mode, `M600` triggers a filament change pause:

1. The print pauses (`PAUSE`)
2. The toolhead parks at the configured park position
3. The extruder retracts and the nozzle cools slightly to prevent ooze
4. A notification is sent (via Fluidd/Mainsail alert, and companion apps if installed)
5. You manually swap the filament, then resume with `RESUME`

---

## CFS Mode (K2 Plus Combo)

When the CFS is active, `M600` at a tool-change boundary is handled automatically by the CFS `M8200` macro sequence rather than pausing for manual intervention. See [CFS — Color Filament System](cfs-k2plus.md) for the full tool-change sequence.

For an unplanned filament runout during a CFS print, the `BOX_CHECK_MATERIAL_REFILL` macro (triggered by `filament_switch_sensor`) handles recovery automatically if a loaded backup spool is available.

---

## Config Location

The M600 macro is written to `/mnt/UDISK/printer_data/config/m600.cfg` and included from `printer.cfg`.

!!! note "Path difference from K1"
    On K1, config lives under `/usr/data/printer_data/config/`. On K2 Plus it is `/mnt/UDISK/printer_data/config/`.
