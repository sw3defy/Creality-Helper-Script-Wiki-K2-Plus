# Configuration / Use

---

# Access to Web Interface — K2 Plus

The K2 Plus ships with **Fluidd pre-installed** at port `4408`. No installation is required to access it.

---

## Fluidd Web Interface

Fluidd is the primary web interface on the K2 Plus.

Open your browser and navigate to:

```
http://<printer-ip>:4408
```

Replace `<printer-ip>` with your printer's IP address (found in **Settings → Network** on the touchscreen).

<img src="../../assets/img/Access-to-Web-Interface/Fluidd_Web_Interface.png">

---

## Mainsail Web Interface

Mainsail is not pre-installed. Install it via the Helper Script (option 9) to access it on port `4409`:

```
http://<printer-ip>:4409
```

<img src="../../assets/img/Access-to-Web-Interface/Mainsail_Web_Interface.png">

---

## Creality Web Interface

The original Creality web interface is accessible on port 80:

```
http://<printer-ip>
```

This is used by **Creality Print** for WiFi printing.

!!! warning
    If you remove the Creality Web Interface using the Helper Script Customize Menu, WiFi printing with Creality Print will stop working. You can restore it at any time from the same menu.

---

## Setting Fluidd or Mainsail as Default (Port 80)

With the Helper Script you can replace the Creality Web Interface with Fluidd or Mainsail on port 80. Useful for hardware that does not support custom port numbers.

Configure from Helper Script → Customize Menu → **Remove & Restore Creality Web Interface**.

- **Fluidd** as default: accessible at both `http://<ip>/` and `http://<ip>:4408/`
- **Mainsail** as default: accessible at both `http://<ip>/` and `http://<ip>:4409/`


---

---

# Camera Support for Fluidd and Mainsail — K2 Plus

The K2 Plus camera is now supported in both Fluidd and Mainsail via a custom WebRTC bridge. See the [Camera Support page](configure-camera.md) for full details.

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


---

