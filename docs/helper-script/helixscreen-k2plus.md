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

## Installation

Install from the helper script:


Select **12) HelixScreen (touchscreen UI)**.

Or install manually via SSH:

```bash
python3 -c "import urllib.request as u; open('/tmp/install.sh','wb').write(u.urlopen(u.Request('http://dl.helixscreen.org/install.sh', headers={'User-Agent':'helixscreen-installer/1.0'}), timeout=30).read())" && sh /tmp/install.sh
```

Reboot after installation:

```bash
reboot
```

---

## Known Limitations

**WiFi management unavailable** — HelixScreen shows a "WiFi unavailable" warning on the K2 Plus. This is cosmetic only — your printer's WiFi connection is not affected. The K2 Plus uses a proprietary WiFi management system that HelixScreen cannot access.

---

## Updating\n\n!!! warning "Review before updating"\n    A K2 Plus was observed running HelixScreen v0.99.74 in November 2026. Newer versions exist, but an upstream version number alone does not establish safe compatibility. The Helper Script's existing update path has not been certified for newer releases. Do not run it blindly.\n

To update HelixScreen run the helper script and select option 12 again, or via SSH:

```bash
/opt/helixscreen/install.sh --update
```

Do **not** assume the Fluidd/Mainsail update manager supports HelixScreen on K2 Plus. Verify the upstream K2-specific upgrade path first. An upgrade requires a planned reboot and a verified backup/recovery procedure. See [Safe update audit](safe-update-audit.md).

---

## Removing

To restore the stock Creality touchscreen UI:
Select **Remove a feature** → **HelixScreen**, or via SSH:

```bash
/opt/helixscreen/install.sh --uninstall
reboot
```

---

## More Information

- [HelixScreen Website](https://helixscreen.org)
- [HelixScreen GitHub](https://github.com/prestonbrown/helixscreen)
- [K2 Series Documentation](https://helixscreen.org/dev/printers/creality-k2/)
