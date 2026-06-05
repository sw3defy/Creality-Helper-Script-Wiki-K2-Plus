#!/bin/sh
# entware.sh - Install Entware on K2 Plus
# Entware is a software repository for embedded systems
# Once installed, you can use 'opkg' to install additional packages
# like mjpg-streamer, git, wget, curl, etc.

SCRIPT_DIR=/mnt/UDISK/helper-script
. "$SCRIPT_DIR/scripts/system.sh"

ENTWARE_DIR=/mnt/UDISK/entware
ENTWARE_INSTALLER=http://bin.entware.net/armv7sf-k3.2/installer/generic.sh

check_entware() {
    [ -f "$ENTWARE_DIR/bin/opkg" ] && return 0
    return 1
}

install_entware() {
    echo ""
    log_info "Installing Entware..."
    echo ""

    if check_entware; then
        log_info "Entware is already installed at $ENTWARE_DIR"
        echo ""
        echo "  1) Reinstall Entware"
        echo "  2) Update Entware packages"
        echo "  0) Cancel"
        echo ""
        printf "  Enter choice: "
        read subchoice
        case "$subchoice" in
            1) : ;;
            2) 
                log_info "Updating Entware packages..."
                $ENTWARE_DIR/bin/opkg update
                $ENTWARE_DIR/bin/opkg upgrade
                log_success "Entware packages updated."
                return 0
                ;;
            *) log_info "Cancelled."; return 0 ;;
        esac
    fi

    # Create entware directory
    mkdir -p "$ENTWARE_DIR"

    # Download and run installer using Python3
    log_info "Downloading Entware installer..."
    python3 << PYEOF
import urllib.request, os, stat
print('Downloading Entware installer...')
urllib.request.urlretrieve(
    '$ENTWARE_INSTALLER',
    '/tmp/entware_install.sh'
)
# Make executable
os.chmod('/tmp/entware_install.sh', stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)
print('Done')
PYEOF

    if [ ! -f /tmp/entware_install.sh ]; then
        log_error "Failed to download Entware installer."
        return 1
    fi

    log_info "Running Entware installer..."
    # The installer needs to know the target directory
    OPENWRT_PREFIX="$ENTWARE_DIR" sh /tmp/entware_install.sh
    rm -f /tmp/entware_install.sh

    if ! check_entware; then
        log_error "Entware installation failed."
        return 1
    fi

    # Add Entware to PATH permanently
    setup_entware_path

    # Update package list
    log_info "Updating Entware package list..."
    $ENTWARE_DIR/bin/opkg update

    mark_installed "entware"
    echo ""
    log_success "Entware installed successfully!"
    echo ""
    log_info "Available commands: opkg install <package>"
    log_info "Useful packages:    mjpg-streamer, git, wget, curl, nano"
    echo ""
    log_info "Example: opkg install mjpg-streamer"
    echo ""
}

setup_entware_path() {
    # Add Entware bin to PATH in profile
    PROFILE=/etc/profile
    if ! grep -q "entware" "$PROFILE" 2>/dev/null; then
        cat >> "$PROFILE" << 'EOF'

# Entware
export PATH=/mnt/UDISK/entware/bin:/mnt/UDISK/entware/sbin:$PATH
export LD_LIBRARY_PATH=/mnt/UDISK/entware/lib:/mnt/UDISK/entware/usr/lib:$LD_LIBRARY_PATH
EOF
        log_success "Added Entware to PATH in /etc/profile"
    fi

    # Export for current session
    export PATH="$ENTWARE_DIR/bin:$ENTWARE_DIR/sbin:$PATH"
    export LD_LIBRARY_PATH="$ENTWARE_DIR/lib:$ENTWARE_DIR/usr/lib:$LD_LIBRARY_PATH"
}

remove_entware() {
    echo ""
    echo "${YELLOW}WARNING: This will remove Entware and all installed packages.${NC}"
    echo "Any packages installed via opkg will stop working."
    echo ""
    printf "Are you sure? [y/N]: "
    read confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        log_info "Cancelled."
        return 0
    fi

    # Remove PATH from profile
    sed -i '/# Entware/,/^$/d' /etc/profile

    # Remove entware directory
    rm -rf "$ENTWARE_DIR"

    mark_removed "entware"
    log_success "Entware removed."
    echo ""
}

case "$1" in
    install) install_entware ;;
    remove)  remove_entware ;;
    *)       echo "Usage: $0 [install|remove]" ;;
esac
