# Change Date & Time — K2 Plus

The K2 Plus syncs its clock via NTP (Network Time Protocol) when connected to the internet. If the date and time are incorrect it can cause SSL certificate errors when cloning the Helper Script.

---

## Check Current Date and Time

```bash
date
```

---

## Sync Time via NTP (Recommended)

If connected to the internet, restart the NTP service:

```bash
/etc/init.d/S98sysntpd restart
sleep 5
date
```

---

## Set Time Manually

If the printer is not connected to the internet:

```bash
# Format: MMDDhhmm[[CC]YY][.ss]
# Example: June 4, 2026, 14:30
date 060414302026
```

---

## Set Timezone

The K2 Plus timezone is configured in `system_config.json`. To change it:

```bash
# View current timezone setting
python3 -c "import json; d=json.load(open('/mnt/UDISK/creality/userdata/config/system_config.json')); print(d['user_info']['time_zone'])"

# The timezone is set by the Creality UI — change it from
# Settings → System → Time Zone on the touchscreen
```

---

## Fix TLS certificate errors safely

First check the clock with `date`, synchronize time using the printer's supported NTP settings, and confirm that trusted CA certificates are installed. Do **not** disable Git SSL verification globally; that makes downloads vulnerable to interception. If certificate validation still fails, stop and resolve the trust-store or network issue before downloading firmware or scripts.

