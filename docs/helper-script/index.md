# Creality K2 Plus Helper Script

The Helper Script extends the Creality K2 Plus and K2 Plus Combo with optional Klipper and web-interface features. **Preserving Creality's original printer functionality is the primary compatibility requirement.**

!!! warning "November 2026 development audit"
    Several legacy installers and removal paths are blocked on the unmerged maintenance branch pending compatibility, backup, and rollback validation. The published `main` script may still contain older behavior. Do not run an unattended install-all sequence.

## Start here

- [Installation and current limitations](helper-script-installation.md)
- [Safe update audit and verified findings](safe-update-audit.md)
- [Moonraker configuration and Update Manager](moonraker-k2plus.md)
- [Fan controls](fans-control-macros-k2plus.md)
- [HelixScreen](helixscreen-k2plus.md)
- [Backup and restore](backup-and-restore-klipper-configuration-files.md)

## Design rules

1. Do not override stock `M106`/`M107`, CFS, homing, motor, or print-control macros merely to add web-interface conveniences.
2. Verify that Mainsail and Fluidd fan sliders preserve stock behavior; this is **not yet implemented or confirmed**.
3. Respect existing Moonraker startup configuration and avoid recursive includes.
4. Never delete a shared configuration or component without confirming ownership and providing rollback.
5. HelixScreen installation requires a confirmed immediate reboot and extra patience during first startup.
6. Audit, back up, and test each feature independently before enabling it.

See the [November 2026 changelog](../changelog.md) for development changes.
