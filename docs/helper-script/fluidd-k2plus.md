# Fluidd — K2 Plus

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

From the helper script menu, select **option 8 — Fluidd (install/update/repair)**. 

When Fluidd is already installed you will be offered:

- **Update** — download and install the latest release
- **Repair** — re-download and reinstall the current latest (fixes corrupted files)
- **Restore nginx block only** — fixes port 4408 access without re-downloading Fluidd

---

## Manual Update via SSH

```bash
# Download latest Fluidd
wget -O /tmp/fluidd.zip https://github.com/fluidd-core/fluidd/releases/latest/download/fluidd.zip

# Install
mkdir -p /usr/share/fluidd
unzip -q -o /tmp/fluidd.zip -d /usr/share/fluidd
rm /tmp/fluidd.zip

# Restart nginx
/etc/init.d/S80nginx restart
```

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
