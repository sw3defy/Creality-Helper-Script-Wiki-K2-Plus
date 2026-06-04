Let me update all the source files and push everything:Now push everything to GitHub from the codespace. In the codespace terminal:

```bash
cd /tmp/helper-extract/helper-script

# Download and apply all fixed scripts
python3 << 'PYEOF'
import urllib.request, os

base = 'https://raw.githubusercontent.com/sw3defy/Creality-Helper-Script-K2-Plus/main/'
# We'll push our local fixes instead
PYEOF

# Copy fixed files from our source
cp /home/claude/helper-script/scripts/moonraker.sh scripts/moonraker.sh
cp /home/claude/helper-script/scripts/useful_macros.sh scripts/useful_macros.sh
cp /home/claude/helper-script/scripts/kamp.sh scripts/kamp.sh
cp /home/claude/helper-script/scripts/mainsail.sh scripts/mainsail.sh
cp /home/claude/helper-script/scripts/fluidd.sh scripts/fluidd.sh
cp /home/claude/helper-script/scripts/timelapse.sh scripts/timelapse.sh
cp /home/claude/helper-script/scripts/system.sh scripts/system.sh

git add -A
git status
```

Wait — the codespace can't access `/home/claude/`. Let me generate a push script instead:Download **`push fixes`** (`push_fixes.py`), drag it into the codespace Explorer panel, then in the codespace terminal:

```bash
cd /tmp/helper-extract/helper-script
python3 /workspaces/Creality-Helper-Script-Wiki-K2-Plus/push_fixes.py
git add -A
git commit -m "Fix: Python3 downloads, remove update_manager/file_manager, fix gcode_shell_command, kill loop for moonraker restart"
git push origin main
```