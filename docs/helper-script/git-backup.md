# Git Backup — K2 Plus

Git Backup watches the Klipper configuration folder and automatically backs it up to a GitHub repository whenever a change is made.

!!! note "Entware required"
    Git Backup requires git to be installed. Install **Entware** (option 15) first, then install git via `opkg install git git-http`.

---

## Prerequisites

1. Create a [GitHub account](https://github.com/signup) if you don't have one.
2. Create a new **private** repository on GitHub for your printer config.
3. Generate a GitHub Personal Access Token:
    - Go to [GitHub → Settings → Tokens (classic)](https://github.com/settings/tokens)
    - Click **Generate new token (classic)**
    - Set expiration to **No expiration**
    - Check **repo** scope
    - Copy the token — you will not be able to see it again

---

## Installation

Install from the helper script:

```sh
sh /mnt/UDISK/helper-script/helper.sh
```

Select **16) Git Backup**.

When prompted, enter:
- Your GitHub username
- Your email address
- Your repository name
- Your branch name (usually `main`)
- Your personal access token

---

## Usage

Control Git Backup with these Klipper macros:

| Macro | Description |
|---|---|
| `GIT_BACKUP_STOP` | Stop watching and pushing to GitHub |
| `GIT_BACKUP_PAUSE` | Pause until next reboot or resume |
| `GIT_BACKUP_RESUME` | Resume watching and pushing |

Or via SSH:

```bash
sh /mnt/UDISK/helper-script/scripts/git_backup.sh <option>
```

Options: `-i` (install), `-p` (pause), `-r` (resume), `-s` (stop)
