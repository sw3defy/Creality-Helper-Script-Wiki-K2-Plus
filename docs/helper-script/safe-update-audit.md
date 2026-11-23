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

## Fluidd and Mainsail — staged web-asset updates

The maintenance branch includes `scripts/web_ui_release.py`, which fetches
the official latest published release metadata, requires the user to type
`INSTALL`, downloads the selected release, validates archive paths and
size limits, and stages the new static files before replacing the web UI
directory. It preserves the previous directory as
`/usr/share/fluidd.previous-helper` or
`/usr/share/mainsail.previous-helper` for manual rollback.

The installer **does not edit nginx configuration, change camera routes, or
restart nginx, Moonraker, or Klipper**. A pre-existing rollback directory
blocks another update until a recovery plan is reviewed. It is deliberately
not an unattended update mechanism.

This is a **code-stage implementation**, not yet validated on the K2 Plus
against its installed Moonraker API. In particular, the reported Fluidd
configuration-editing issue still needs reproduction and compatibility
testing before recommending a version.

## Moonraker configuration audit (menu option 27)

The maintenance branch now provides a **read-only** Moonraker audit
(`scripts/moonraker_audit.sh`). It reports the selected startup config,
the include directives in the stock and UDISK files, relevant sections, and
a direct two-file recursive-include pattern. It does not modify the
printer. This is a diagnostic, not a comprehensive Moonraker parser.

The existing Moonraker Extensions **install and remove** paths are both
blocked pending an ownership-aware migration. KAMP and Timelapse **install,
upgrade and removal** are likewise blocked because the legacy scripts can
overwrite custom settings, duplicate sections or delete components whose
ownership is unknown. Their old implementations are retained for review
but must not be treated as validated upgrade procedures.

The main menu's previous automatic startup patch invocations have been
removed. No pre-existing printer boot hooks are removed automatically.

## Full installation test readiness — NOT YET READY (23 November 2026)

A full install-all test on a physical K2 Plus must **not** be attempted
from this draft branch. The review identified duplicate CHAMBER_* macros
between Fans Control and Useful Macros, possible collisions with stock
calibration commands, unverified M600/PAUSE_BASE behavior with CFS, and
firmware-dependent shaper and Z-offset commands. These feature installers
are now fail-closed while replacements are developed.

Fresh HelixScreen installation is also paused because the legacy path
downloads and executes an unverified HTTP script. The update path now
requires a reboot after a successful update. HelixScreen removal remains
blocked until the uninstall/recovery sequence is verified.

The Helper Script repository now includes offline shell-syntax and safety
invariant checks in `tests/test_safety.py`, triggered by a GitHub Actions
workflow. Passing static checks is necessary but **not sufficient** for
hardware testing.

**Hardware test entry criteria:** static checks pass; every intended
installer has an implemented, reversible and version-compatible path;
a full printer/firmware/config backup and verified recovery procedure
exist; the exact K2 Plus firmware and board revision are recorded; the
camera is confirmed working before and after; and CFS load, unload,
cut, purge, homing and printing are tested incrementally. Run one
feature at a time, never an unattended install-all sequence.

## K2 Plus Firmware Inspector — menu option 28

The development branch includes a read-only firmware inspector. Select
**28) K2 Plus Firmware Inspector (read-only)** to generate
`/tmp/k2-inspection.txt`. Retrieve the report through WinSCP and
**review it before sharing**. The inspector lists configuration file
paths, short SHA-256 digests, selected macro/extension section names,
and include references, and compares matching relative paths across
ROM, shared and active configuration trees.

The inspector does **not** read out full configuration contents or
write to the printer's persistent configuration. The report itself
is written to the temporary `/tmp` directory. It does not access
camera settings, restart services or perform installation.

**Limitations:** this is an initial inventory, not a full firmware
compatibility certification. Stock firmware configuration may live in
board-specific nested directories; relative-path comparison does not
automatically pair these with active files. Macro definitions outside
the scanned trees are not covered. Inspect the output for sensitive
path or macro names before uploading.

For first use without updating the installed Helper Script, transfer
`scripts/firmware_inspector.py` from the development branch to
`/tmp/firmware_inspector.py` using WinSCP, then run:

```sh
python3 /tmp/firmware_inspector.py > /tmp/k2-inspection.txt
```

Download `/tmp/k2-inspection.txt` with WinSCP. Do **not** replace
the installed Helper Script with this untested maintenance branch just
to run the inspector.

## Firmware Inspector v2 — include graph and collision detection

The inspector now omits timestamped `printer-YYYYMMDD_HHMMSS.cfg`
and `moonraker-YYYYMMDD_HHMMSS.conf` backup snapshots from the
inventory, walks literal Klipper `[include ...]` references starting
at `printer.cfg`, and reports duplicate `[gcode_macro NAME]`
definitions in the resolved include graph. Wildcard includes are
reported as unresolved rather than guessed. This is a **static
inspection**, not a live Klipper parser or compatibility test.

### Findings from first printer report (November 2026)

The uploaded inventory showed these macro-name collisions among
directly included files:

- `M106`: `gcode_macro.cfg` and `fans_control.cfg`
- `M107`: `gcode_macro.cfg` and `fans_control.cfg`
- `AUTOTUNE_SHAPERS`: `gcode_macro.cfg` and `shapers_calibration.cfg`

Do not automatically remove or replace either definition. Inspect
actual macro implementations, `rename_existing` usage, and the
live Klipper status before planning any repair. Preserve stock
CFS, camera, fan, homing, and print-start/end behavior.

The development menu explicitly labels guarded installation
features as **BLOCKED** while safety review is pending.
