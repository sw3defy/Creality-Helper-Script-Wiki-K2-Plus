# Moonraker and Nginx — K2 Plus

!!! warning "K2 Plus differs significantly from K1"
    On the K1 Series, Moonraker and Nginx are installed by the helper script. On the K2 Plus, **both are pre-installed from the factory firmware** and run from the read-only `/usr/share/` partition. The approach here is therefore fundamentally different: instead of installing from scratch, you are **extending** the stock installation.

---

## What Ships From the Factory

The K2 Plus comes with the following already running:

| Component | Details |
|---|---|
| Fluidd | Served at `http://<printer-ip>:4408`, static files at `/usr/share/fluidd/` |
| Moonraker | Running at `127.0.0.1:7125`, config at `/usr/share/moonraker/moonraker.conf` |
| Nginx | Config at `/etc/nginx/nginx.conf`, single-file (no `conf.d/` directory) |
| Klipper | Running via `/usr/share/klippy-env/`, config at `/mnt/UDISK/printer_data/config/printer.cfg` |

You can verify all four are running over SSH:

```bash
ps aux | grep -E 'klipper|moonraker|nginx' | grep -v grep
```

---

## Architecture Overview

```
Browser → nginx (port 4408)
              ├── / → /usr/share/fluidd/          (static Fluidd files)
              ├── /websocket → 127.0.0.1:7125      (Moonraker WebSocket)
              ├── /printer|api|access|machine|server → 127.0.0.1:7125  (Moonraker REST)
              └── /webcam/ → 127.0.0.1:8080        (WebRTC/MJPEG streams)

Moonraker (7125) → /tmp/klippy_uds → Klipper (klippy.py)
```

Mainsail is not pre-installed. See [Mainsail](mainsail.md) to add it on port `4409`.

---

## Moonraker Config Location

The stock Moonraker config is at `/usr/share/moonraker/moonraker.conf` on the **read-only system partition**.

!!! danger "Do not edit /usr/share/moonraker/moonraker.conf directly"
    This file is on the read-only system partition and will be **overwritten on every firmware update**. Any changes made directly to this file will be lost. Use the helper script approach to apply persistent changes.

The stock config includes:

- `[machine]` with `provider: none` — meaning Moonraker has no system service management capability. Reboot/shutdown buttons in Fluidd will not work without Host Control Support (see below).
- No `[update_manager]` section — the Update Manager panel in Fluidd is empty by default.
- No `[timelapse]` component — see [Moonraker Timelapse](moonraker-timelapse-k2plus.md) to add it.

---

## Extending Moonraker with Include Files

Because the stock config is read-only, the helper script adds a persistent include directive by patching the moonraker startup. Additional config is written to:

```
/mnt/UDISK/printer_data/config/moonraker.conf
```

This file survives firmware updates because it lives on `/mnt/UDISK/`.

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the script's `[Install] Menu` install **Moonraker Extensions**:

The script will:

1. Write `/mnt/UDISK/printer_data/config/moonraker.conf` with the `[update_manager]` section and any additional components you enable.
2. Patch the Moonraker startup to load the include file.
3. Restart Moonraker via `/etc/init.d/S56moonraker restart`.

---

## Restarting Services

The K2 Plus uses OpenWrt rc.d init scripts. There is **no `supervisorctl`** command (unlike K1).

```bash
# Restart Moonraker
/etc/init.d/S56moonraker restart

# Restart Klipper
/etc/init.d/S55klipper restart

# Restart Nginx
/etc/init.d/S80nginx restart

# Restart the low-level MCU bridge
/etc/init.d/S54klipper_mcu restart
```

---

## Host Control Support

By default, the Reboot and Shutdown buttons in Fluidd do nothing on the K2 Plus because Moonraker's `[machine]` provider is set to `none`.

The helper script installs a lightweight host control shim that intercepts these commands and routes them to the appropriate system call.

Install it from the `[Install] Menu` → **Host Control Support**.

Once installed, reboot/shutdown from the Fluidd power menu will work correctly.

---

## Adding Mainsail

Mainsail is not pre-installed. To add it on port `4409`, see [Mainsail](mainsail.md). The helper script adds a second `server` block to the nginx config for Mainsail alongside the existing Fluidd block.

---

## Update Manager

Once the helper script has written `/mnt/UDISK/printer_data/config/moonraker.conf` with the `[update_manager]` section, the Update Manager panel in Fluidd will become active and show available updates for:

- Creality Helper Script itself
- Any additional components you have installed (Fluidd update, Mainsail, timelapse plugin, etc.)

Updates performed via Update Manager do **not** affect the firmware itself or the read-only `/usr/share/` partitions.
