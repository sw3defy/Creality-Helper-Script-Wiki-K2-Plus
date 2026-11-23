# HelixScreen — K2 Plus

!!! danger "Mandatory reboot after installation"
    On the K2 Plus, HelixScreen installation must be followed by an immediate, explicit printer reboot, regardless of when HelixScreen is installed in the feature sequence. The planned Helper Script flow will ask for confirmation **before** installation and reboot. Allow extra time for the first boot after installation; do not hard-reset merely because startup is slower. This is a required design change, not a claim that the current published installer already enforces it. Verify backups and a recovery plan before proceeding.


HelixScreen is a modern, lightweight touchscreen interface for Klipper 3D printers. It replaces the stock Creality touchscreen UI with a feature-rich Klipper-native interface.

!!! success "Tested and working on K2 Plus"
    HelixScreen v0.99.72 was previously tested on a K2 Plus. This does not establish compatibility for newer releases or firmware.

---

## Features

- Modern touch UI for Klipper
- Temperature control and monitoring
- Print management and history
- Bed mesh visualization
- Input shaper graphs
- Multi-material (CFS) management
- Auto-updates via Fluidd/Mainsail update manager

---

## Installation — currently paused

!!! danger "Do not run the historical remote installer"
    Fresh HelixScreen installation is blocked in the unmerged Helper Script maintenance branch until the upstream K2 package, backups, and recovery steps are verified. Do not execute an unverified remote shell script on the printer.

**Required future flow:** confirm the installation and mandatory immediate reboot *before* proceeding; install; reboot immediately on success; then allow additional time for first startup. HelixScreen does not have to be installed last in the feature sequence.

## Known Limitations

**WiFi management unavailable** — HelixScreen shows a "WiFi unavailable" warning on the K2 Plus. This is cosmetic only — your printer's WiFi connection is not affected. The K2 Plus uses a proprietary WiFi management system that HelixScreen cannot access.

---

## Updating and removal

Updates and removal require a firmware-compatible, backed-up recovery procedure. The Helper Script's maintenance update path is under review; do not assume the newest upstream version is compatible or that the web UI Update Manager can update HelixScreen safely.

Do not hard-reset the printer because HelixScreen takes longer to start after installation.

See [Safe Update Audit](safe-update-audit.md).

## More Information

- [HelixScreen Website](https://helixscreen.org)
- [HelixScreen GitHub](https://github.com/prestonbrown/helixscreen)
- [K2 Series Documentation](https://helixscreen.org/dev/printers/creality-k2/)
