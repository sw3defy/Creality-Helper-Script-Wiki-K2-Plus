# Mainsail — K2 Plus

Mainsail is an alternative web interface to Fluidd. It is not pre-installed on the K2 Plus but can be added by the Helper Script on port `4409`, running alongside the stock Fluidd installation.

---

## Installation

From the helper script menu, select **option 9 — Mainsail (port 4409)**.

The script will:
1. Download the latest Mainsail release
2. Install static files to `/usr/share/mainsail/`
3. Add a new nginx server block for port `4409`
4. Restart nginx

---

## Access Mainsail

After installation:

```
http://<printer-ip>:4409
```

---

## Update / Repair Mainsail

Run the helper script and select option 9 again. If Mainsail is already installed you will be offered:

- **Update** — download and install the latest release
- **Repair** — re-download and reinstall
- **Restore nginx block only** — restore port 4409 without re-downloading

---

## Fluidd vs Mainsail

Both interfaces connect to the same Moonraker instance and offer equivalent functionality. Key differences:

| Feature | Fluidd | Mainsail |
|---|---|---|
| Port | 4408 (pre-installed) | 4409 (helper script) |
| UI style | Clean, dashboard-focused | Feature-rich, more settings |
| Timelapse UI | Via plugin | Built-in |
| Spoolman | Via plugin | Built-in |

You can use both simultaneously — they share the same Moonraker backend and printer state.

---

## Mainsail Configuration

Mainsail stores its configuration in `mainsail.cfg`. After installation, add this include to your `printer.cfg` if you want Mainsail-specific features:

```bash
# From SSH
echo "[include mainsail.cfg]" >> /mnt/UDISK/printer_data/config/printer.cfg
```

Or add it via the Fluidd/Mainsail editor.

---

## Camera Setup

Camera support is installed separately via option **11) Camera Support for Fluidd and Mainsail**. Once installed, the camera feed appears automatically in the Mainsail dashboard after boot — no manual configuration required. See the [Camera Support page](../../configurations/configure-camera.md) for details.
