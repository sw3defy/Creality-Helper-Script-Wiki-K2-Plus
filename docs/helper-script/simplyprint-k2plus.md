# SimplyPrint — K2 Plus

SimplyPrint has a dedicated K2 Series setup guide separate from the K1 guide.

!!! warning "Use the K2-specific guide"
    Do not follow the K1/K1C SimplyPrint setup guide for a K2 Plus. SimplyPrint provides a separate onboarding flow for the K2 series.

Refer to the official SimplyPrint K2 setup guide for current instructions:

[SimplyPrint K2 Series Setup Guide :material-open-in-new:](https://simplyprint.io/setup-guide/creality/k2){ .md-button }

---

## SSH Root Access

SimplyPrint requires SSH root access to install its companion. Follow the [Enable Root Access](../firmwares/install-and-update-rooted-firmware-k2plus.md#enable-root-access) section first.

- **User:** `root`
- **Password:** `creality_2024`

---

## Data Path Note

If SimplyPrint's installer asks for the printer data path or Moonraker config location, use:

```
/mnt/UDISK/printer_data/
```

Not `/usr/data/printer_data/` as stated in the K1 guide.
