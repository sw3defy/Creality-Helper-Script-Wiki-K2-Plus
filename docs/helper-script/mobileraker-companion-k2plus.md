# Mobileraker Companion — K2 Plus

Mobileraker Companion enables push notifications for Klipper using Moonraker. It works on the K2 Plus with one known caveat.

---

## Installation

Make sure you have followed the [Install Helper Script](helper-script-installation.md) section, then from the `[Install] Menu` install **Mobileraker Companion**.

---

## Known Issue — HeaterFan Parse Error

!!! warning "Known compatibility issue"
    There is a known crash in Mobileraker when connecting to a K2 Plus. The K2 Plus `printer.cfg` uses a `[heater_fan]` configuration that Mobileraker's printer builder does not handle correctly, causing the app to fail with:

    ```
    Found _$HeaterFanImpl, parentException: null
    PrinterBuilder._updateTemperatureFan
    ```

    **Status:** This is an open issue in the Mobileraker project ([issue #429](https://github.com/Clon1998/mobileraker/issues/429)). Check the issue for the latest fix status before installing.

    **Workaround:** If the app crashes on connection, check for an updated Mobileraker release that includes the fix. The companion daemon itself (server-side) installs and runs correctly — the issue is in the mobile app's parsing of the K2 Plus fan configuration.

---

## Configuration

After installation, the companion config is at:

```
/mnt/UDISK/printer_data/config/mobileraker.conf
```

Follow the [Mobileraker setup guide](https://mobileraker.com) to link the companion to your mobile app.

---

## Restart

```bash
/etc/init.d/S56moonraker restart
```

The Mobileraker companion runs as a Moonraker component and restarts with Moonraker.
