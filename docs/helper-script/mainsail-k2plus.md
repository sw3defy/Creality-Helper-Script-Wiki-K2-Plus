# Mainsail — K2 Plus

!!! warning "November 2026 compatibility review"
    Mainsail is an alternative UI over the existing Moonraker/Klipper services. Its native fan sliders have **not** been verified to call Creality's stock `M106`/`M107` macros. The requested stock-equivalent slider behavior is a pending implementation requirement; adding a custom macro button is not the same as fixing the native slider.


Mainsail is an alternative web interface to Fluidd. It is not pre-installed on the K2 Plus but can be added by the Helper Script on port `4409`, running alongside the stock Fluidd installation.

---

## Installation and update status

Mainsail is served on port `4409` when installed. The existing Helper Script includes a Mainsail installation path, but the **reviewed maintenance updater is not yet a released, hardware-validated procedure**.

!!! warning "Camera-preserving UI update under review"
    [Helper Script PR #7](https://github.com/sw3defy/Creality-Helper-Script-K2-Plus/pull/7) stages official Mainsail assets, preserves the existing camera UI injection when it can identify it safely, and retains a rollback copy of the previous UI. The new UI may no longer expose the private Vue store API used by the existing camera script. Do not treat passing CI tests as proof that the camera will work after upgrading.

The updater requires explicit `INSTALL` confirmation. It does **not** modify nginx, Moonraker, Klipper, or camera services. An existing `/usr/share/mainsail.previous-helper` backup prevents a second replacement until reviewed.

Before updating, follow the [Safe Update Audit](safe-update-audit.md) and [hardware camera compatibility checklist](https://github.com/sw3defy/Creality-Helper-Script-K2-Plus/blob/maintenance/2026-11-safe-update-audit/docs/web-ui-camera-compatibility.md).

### Access Mainsail

Once installed, open `http://<printer-ip>:4409`.

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
