# M600 Support — K2 Plus

M600 is the standard filament change G-code. Behavior differs depending on whether you are using single-filament mode or the CFS.

---

## Installation

From the `[Install] Menu` install **M600 Support**.

Config is written to `/mnt/UDISK/printer_data/config/m600.cfg`.

---

## Single-Filament Mode

`M600` triggers a pause, parks the toolhead, retracts, and waits for manual filament swap. Resume with `RESUME`.

---

## CFS Mode (K2 Plus Combo)

When the CFS is active, tool changes at boundaries are handled automatically by the `M8200` macro sequence. See [CFS](cfs-k2plus.md).

For unplanned runout during a CFS print, `BOX_CHECK_MATERIAL_REFILL` handles recovery automatically if a backup spool is loaded.
