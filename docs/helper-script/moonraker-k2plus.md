# Moonraker and Nginx — K2 Plus

!!! warning "K2 Plus differs significantly from K1"
    On the K1 Series, Moonraker and Nginx are installed by the helper script. On the K2 Plus, **both are pre-installed from the factory firmware** and run from the read-only `/usr/share/` partition. Instead of installing from scratch, you are **extending** the stock installation.

---

## What Ships From the Factory

| Component | Details |
|---|---|
| Fluidd | Served at `http://<printer-ip>:4408`, static files at `/usr/share/fluidd/` |
| Moonraker | Running at `127.0.0.1:7125`, config at `/usr/share/moonraker/moonraker.conf` |
| Nginx | Config at `/etc/nginx/nginx.conf`, single-file (no `conf.d/` directory) |
| Klipper | Config at `/mnt/UDISK/printer_data/config/printer.cfg` |

Verify all four are running over SSH:

```bash
ps aux | grep -E 'klipper|moonraker|nginx' | grep -v grep
```

---

## Moonraker Config Location

!!! danger "Do not edit /usr/share/moonraker/moonraker.conf directly"
    This file is on the read-only system partition and will be **overwritten on every firmware update**.

The stock config has no `[update_manager]` or `[timelapse]` section, and `[machine]` is set to `provider: none` — meaning reboot/shutdown buttons in Fluidd do not work by default.

---

## Extending Moonraker with Include Files

The helper script writes persistent config to:

```
/mnt/UDISK/printer_data/config/moonraker.conf
```

From the `[Install] Menu` install **Moonraker Extensions**. The script will:

1. Write `/mnt/UDISK/printer_data/config/moonraker.conf` with the `[update_manager]` section.
2. Patch the Moonraker startup to load the include file.
3. Restart Moonraker via `/etc/init.d/S56moonraker restart`.

---

## Restarting Services

```bash
/etc/init.d/S56moonraker restart
/etc/init.d/S55klipper restart
/etc/init.d/S80nginx restart
/etc/init.d/S54klipper_mcu restart
```

!!! note "No supervisorctl on K2 Plus"
    The `supervisorctl` command is not available. Use the rc.d init scripts above.

---

## Host Control Support

By default the Reboot and Shutdown buttons in Fluidd do nothing because `[machine]` provider is `none`. Install **Host Control Support** from the `[Install] Menu` to enable them.

---

## Adding Mainsail

Mainsail is not pre-installed. See [Mainsail](mainsail.md) to add it on port `4409`.
