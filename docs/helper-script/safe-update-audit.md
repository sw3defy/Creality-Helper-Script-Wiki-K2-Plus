# Safe update audit — November 2026

The K2 Plus Helper Script supports multiple independent add-ons. An entry in
`/mnt/UDISK/helper-script/.installed` records that an installer ran; it is **not**
evidence of the installed application version or of compatibility.

## Read-only audit

After obtaining the reviewed Helper Script branch, run:

```sh
sh /mnt/UDISK/helper-script/scripts/check_updates.sh
```

This prints installed feature flags, the HelixScreen version from
`/opt/helixscreen/release_info.json`, local web interface information and
available stable upstream GitHub release tags when online. It does **not**
install, update, modify configuration, restart services, or reboot the printer.
A version marked `unknown` is not evidence that software is absent.

## Update policy

| Feature | Version source | Safety review before changing |
| --- | --- | --- |
| HelixScreen | `/opt/helixscreen/release_info.json` and upstream stable releases | Verify K2 package, firmware compatibility, backup and reboot procedure |
| Fluidd | Installed web assets and official release | Check K2 Moonraker and Nginx compatibility |
| Mainsail | Installed web assets and official release | Check K2 Moonraker and Nginx compatibility |
| KAMP | Installed files/source revision and upstream repository | Check purge moves, CFS, and slicer behavior |
| Moonraker Timelapse | Installed component revision and upstream repository | Check Moonraker dependencies and camera integration; do not alter camera support |
| Moonraker Extensions | Helper Script source and active Moonraker configuration | Do not blindly overwrite stock configuration |
| Fans, Useful Macros, M600, Z-offset | Active Klipper includes and Helper Script source | Check collisions with stock CFS loading, unloading, cutting and purge macros |
| Improved Shapers | Active Klipper config and Helper Script source | Check Creality firmware and LIS2DW support |
| Entware | `opkg --version` and package list | Review dependencies; no blanket upgrade |
| OctoEverywhere, Mobileraker | Actual installation state and upstream project | Check service compatibility |
| Git Backup | Helper Script source | Test restore from an isolated backup first |
| Camera Support | Protected | **No changes without explicit approval** |

### Printer-specific safeguards

- Back up active Klipper configuration, including `printer.cfg`'s
  `SAVE_CONFIG` section and calibrated CFS cutter position.
- Do not overwrite `motor_control.cfg` from a firmware ROM copy just because
  the files differ.
- Do not automatically rewrite `box.cfg` or `gcode_macro.cfg`. Macro naming
  and visibility require firmware-specific verification.
- Test CFS loading, unloading, cutting, purging, homing and endstop behavior
  after changes that can affect them.
- Do not power-cycle the printer during HelixScreen's first startup. Follow a
  verified reboot/recovery plan.
- Do not update by replacing the entire existing helper directory: local
  protected files and installation state may be lost.

**Status:** This is an audit procedure, not a certification that any upstream
release is safe for every K2 Plus firmware.

## Installer review — in progress

The maintenance branch has additional fail-safe changes:

- Entware removal no longer deletes all of `/opt`, which is shared with
  HelixScreen. An Entware-specific removal procedure remains to be designed.
- The HelixScreen update path now requires a second explicit confirmation,
  checks the updater's exit status, and offers a controlled reboot. **This does
  not establish compatibility of the newest HelixScreen with K2 Plus.**
- The older Moonraker Extensions installer is temporarily blocked. Its
  stock-config wrapper and include topology require firmware-specific testing
  before the installer can safely be re-enabled.
- KAMP and Timelapse installers no longer automatically invoke that blocked
  Moonraker Extensions path when the dependency is missing. Their own upgrade
  paths still require review.

**Do not install this draft on a production printer yet.** These safeguards
are staged in GitHub only; existing printer installations and pre-existing
`rc.local` hooks are unchanged.
