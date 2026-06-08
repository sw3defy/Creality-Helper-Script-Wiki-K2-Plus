# OctoEverywhere — K2 Plus

OctoEverywhere provides free remote access to your printer from anywhere in the world — including live webcam, full Fluidd/Mainsail control, and AI print failure detection.

---

## Installation

From the Helper Script menu, select **option 14 — OctoEverywhere**.

---

## Setup

1. After installation, check the Moonraker log for the OctoEverywhere plugin URL:
    ```bash
    tail -50 /mnt/UDISK/printer_data/logs/moonraker.log | grep -i octoeverywhere
    ```

2. Open the URL shown in the log in your browser to link your printer to your OctoEverywhere account.

3. Create a free account at [octoeverywhere.com](https://octoeverywhere.com) if you don't have one.

4. Once linked, access your printer from anywhere at [octoeverywhere.com](https://octoeverywhere.com) or via the OctoEverywhere app.

---

## Features

- **Remote access** — full Fluidd or Mainsail interface from any device
- **Live webcam** — view your print from anywhere
- **AI failure detection** — Gadget AI monitors your print and pauses on spaghetti detection
- **Notifications** — print start, finish, pause, and failure alerts
- **Secure** — end-to-end encrypted, no port forwarding required

---

## Notes for K2 Plus

OctoEverywhere has been confirmed working on the K2 Plus. The Moonraker plugin installs as a component and starts automatically with Moonraker.

If OctoEverywhere loses connection after a Moonraker restart:

```bash
/etc/init.d/S56moonraker restart
```

Then check the log again for the connection status.
