# Change WiFi Location — K2 Plus

The K2 Plus connects to your local WiFi network during initial setup. If you move the printer or change your network, you can reconnect directly from the touchscreen.

---

## Change WiFi from Touchscreen

- On the touchscreen go to **Settings → Network**
- Tap your current network to disconnect, or tap **+** to add a new network
- Select your network from the list and enter the password
- The printer reconnects and displays the new IP address

---

## Find Your Printer's IP Address

After connecting, the IP address is shown in **Settings → Network**.

You can also find it from your router's DHCP client list — look for a device named `K2Plus-XXXX` where `XXXX` is the last 4 characters of your printer's MAC address.

---

## Set a Static IP

For a stable IP that does not change between reboots, configure a DHCP reservation on your router (recommended). Assign a permanent IP to the printer's MAC address — this requires no changes on the printer itself and survives factory resets.

---

## Reconnect After Factory Reset

After a factory reset the printer loses its WiFi credentials. Reconnect from the touchscreen:

**Settings → Network → select your network → enter password**

Root access must also be re-enabled after a factory reset. See [Enable Root Access](../firmwares/install-and-update-rooted-firmware-k2plus.md#enable-root-access).
