# HelixScreen — K2 Plus

HelixScreen is a modern, lightweight touchscreen interface for Klipper 3D printers. It replaces the stock Creality touchscreen UI with a feature-rich Klipper-native interface.

!!! success "Tested and working on K2 Plus"
    HelixScreen v0.99.72 was tested and confirmed working on the Creality K2 Plus.

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


Select **11) HelixScreen (touchscreen UI)**.

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

## Updating

To update HelixScreen run the helper script and select option 11 again, or via SSH:

```bash
/opt/helixscreen/install.sh --update
```

You can also update from the Fluidd/Mainsail update manager — HelixScreen registers itself automatically.

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
