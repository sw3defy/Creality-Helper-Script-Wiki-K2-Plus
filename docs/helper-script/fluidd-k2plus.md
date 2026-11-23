# Fluidd — K2 Plus

!!! warning "November 2026 compatibility review"
    Fluidd updates and nginx repair must be verified against the active K2 firmware and existing camera routing before changing stock web assets. Native fan sliders have **not** been confirmed to invoke Creality's stock `M106`/`M107`; do not assume stock-equivalent behavior.


Fluidd is the primary web interface on the K2 Plus, pre-installed at port `4408` from the factory. This page covers updating, repairing, and restoring Fluidd using the Helper Script.

!!! note "Pre-installed"
    You do not need to install Fluidd — it ships with the K2 Plus. This page is for updating to the latest version or repairing a broken installation.

---

## Access Fluidd

Open your browser and navigate to:

```
http://<printer-ip>:4408
```

Replace `<printer-ip>` with your printer's IP address (found in **Settings → Network** on the touchscreen).

---

## Update / Repair Fluidd

!!! warning "Development update path — not yet hardware validated"
    The safety-reviewed updater is currently in [Helper Script PR #7](https://github.com/sw3defy/Creality-Helper-Script-K2-Plus/pull/7), **not the released main branch**. It stages official web assets, attempts to preserve the existing camera JavaScript and retains a rollback directory. Passing offline tests does not prove compatibility with the K2 Plus firmware or newer Fluidd versions.

    Do not replace the live `/usr/share/fluidd` directory until the printer-side compatibility checks are complete. In particular, the current camera integration uses a private Vue store API that may change in upstream Fluidd.

The existing printer includes Fluidd on port `4408`. The maintenance updater changes only the web UI assets and does not restart nginx, Moonraker, Klipper or the camera services. It requires an explicit `INSTALL` confirmation, and an existing `/usr/share/fluidd.previous-helper` rollback directory is never overwritten.

For the planned controlled test procedure, see [Safe Update Audit](safe-update-audit.md) and the [camera compatibility checklist](https://github.com/sw3defy/Creality-Helper-Script-K2-Plus/blob/maintenance/2026-11-safe-update-audit/docs/web-ui-camera-compatibility.md).

---

## Fluidd Configuration

Key Fluidd settings are stored in Moonraker. Once Moonraker Extensions are installed, configure Fluidd from **Settings** in the web interface.

### Camera Setup

If the camera is not visible in Fluidd after opening the interface:

- Go to **Settings → Cameras**
- Enable the existing camera entry, or delete and recreate with:
    - **URL Stream:** `http://<printer-ip>:4408/webcam/?action=stream`
    - **URL Snapshot:** `http://<printer-ip>:4408/webcam/?action=snapshot`

---

## Nginx Configuration

Fluidd is served by nginx from `/usr/share/fluidd/` on port `4408`. The nginx config is at `/etc/nginx/nginx.conf`.

The K2 Plus nginx config proxies all Moonraker API requests (`/printer/`, `/api/`, `/machine/`, etc.) to `127.0.0.1:7125`, and webcam streams to `127.0.0.1:8080–8083`.

!!! warning "Do not edit nginx.conf directly"
    `/etc/nginx/nginx.conf` is on the writable partition but the Helper Script backs it up before modifying it. If you edit it manually and break nginx, restore the backup:
    ```bash
    cp /mnt/UDISK/helper-script/.nginx.conf.bak /etc/nginx/nginx.conf
    /etc/init.d/S80nginx restart
    ```
