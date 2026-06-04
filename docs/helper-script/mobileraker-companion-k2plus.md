# Mobileraker Companion — K2 Plus

Mobileraker Companion enables push notifications for Klipper using Moonraker.

---

## Installation

From the `[Install] Menu` install **Mobileraker Companion**.

---

## Known Issue — HeaterFan Parse Error

!!! warning "Known compatibility issue"
    There is a known crash in Mobileraker when connecting to a K2 Plus. The K2 Plus `printer.cfg` uses a `[heater_fan]` configuration that Mobileraker's printer builder does not handle correctly:

    ```
    Found _$HeaterFanImpl, parentException: null
    ```

    **Status:** Open issue in the Mobileraker project. Check for an updated release before installing. The companion daemon installs and runs correctly — the issue is in the mobile app's parsing of the K2 Plus fan configuration.

---

## Configuration

After installation, companion config is at:

```
/mnt/UDISK/printer_data/config/mobileraker.conf
```

Restart with:

```bash
/etc/init.d/S56moonraker restart
```
