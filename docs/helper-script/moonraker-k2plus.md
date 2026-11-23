# Moonraker and Nginx — K2 Plus

!!! warning "November 2026 safety review — migration pending"
    The Moonraker Extensions installer and removal path are **blocked in the unmerged maintenance branch**. This page describes verified observations, not a new installation procedure. Do not patch startup scripts or add reverse includes.

## Verified K2 Plus startup configuration

A targeted diagnostic of an actual K2 Plus found:

- `/etc/rc.d/S56moonraker` sets `CONF=/mnt/UDISK/printer_data/config/moonraker.conf`.
- The service passes that config to `/usr/share/moonraker/moonraker.py` with `-c`.
- `/usr/share/moonraker/moonraker.conf` includes `/mnt/UDISK/printer_data/config/moonraker.conf`.
- The user configuration contains `[file_manager]` and `[timelapse]` sections.

These are observations from the inspected printer, not a guarantee for every firmware version.

## Do not create a recursive include

**Do not add** `[include /usr/share/moonraker/moonraker.conf]` to the user config when the stock file already includes the user config. That produces an include cycle.

The previous installer tried to add this reverse include, patch the service startup, and restart Moonraker. The mutation code was removed from `scripts/moonraker.sh` in the development branch. Both install and remove now fail closed until a reviewed migration is available.

## Update Manager

The Helper Script's intended Update Manager support must preserve the existing Moonraker configuration, avoid duplicate sections, and distinguish stock components from Helper Script-owned files. **Update Manager installation is not yet validated by this review.** Do not infer that installing Mainsail or Fluidd requires replacing Moonraker.

## Timelapse and camera compatibility

Existing `[timelapse]` configuration may be used by other features. Never delete or archive the entire `moonraker.conf` as an uninstall shortcut. The camera, streaming routes, and installed Moonraker components must be inventoried before migration.

## Read-only audit

The maintenance branch provides `scripts/moonraker_audit.sh` for a read-only topology inspection and `scripts/migration_assessment.py` for **offline copies** of configuration files. These tools do not authorize modifying the live printer.

## Before enabling installation

A safe implementation must verify the active service config path, follow includes in both directions, detect duplicate sections, back up owned files, propose exact changes, and provide a tested rollback. Restart commands must be verified for the firmware in use. No service restart or printer reboot is part of this documentation update.

See [Safe Update Audit](safe-update-audit.md) and [Moonraker Timelapse](moonraker-timelapse-k2plus.md).
