#!/bin/bash
#
# update-beegfs-if.sh: Update the local BeeGFS connection interfaces file
# with interfaces provided interactively.
#
# Instead of taking arguments, this script prompts you to enter interfaces
# one at a time. It provides auto-completion (using the TAB key) for available
# network interfaces (as found via the ip or ifconfig command). When you are done,
# press Enter twice in a row.
#

# --- Determine available network interfaces ---
if command -v ip &>/dev/null; then
    # Using ip to list interfaces (the output of "ip -o link show" looks like:
    # "1: lo: <LOOPBACK,UP,...>" so we extract the 2nd field)
    available_interfaces=$(ip -o link show | awk -F': ' '{print $2}')
else
    # Fallback to ifconfig (this may include a header line on some systems)
    available_interfaces=$(ifconfig | grep '^[a-zA-Z]' | awk -F: '{print $1}')
fi

echo "Available interfaces:"
for iface in $available_interfaces; do
    echo "  $iface"
done
echo

# --- Define a custom completion function for the interactive prompt ---
_interface_completions() {
    local cur="${READLINE_LINE}"
    local comp=""
    for iface in $available_interfaces; do
        if [[ "$iface" == "$cur"* ]]; then
            comp="$iface"
            break
        fi
    done
    if [ -n "$comp" ]; then
        READLINE_LINE="$comp"
        READLINE_POINT=${#READLINE_LINE}
    fi
}

bind -x '"\t": _interface_completions' 2>/dev/null




# --- Read interfaces interactively ---
echo "Enter network interfaces to use for BeeGFS."
echo "Type one interface per prompt. When finished, press Enter on an empty line twice."
echo

chosen_interfaces=()
prev_blank=false

while true; do
    read -e -p "Interface: " iface
    if [ -z "$iface" ]; then
        break
    fi
    chosen_interfaces+=("$iface")
done


# Check that at least one interface was entered.
if [ ${#chosen_interfaces[@]} -eq 0 ]; then
    echo "No interfaces entered. Exiting."
    exit 1
fi

# --- Build the new interfaces file content ---
conn_content=$(printf "%s\n" "${chosen_interfaces[@]}")

echo
echo "New content for /etc/beegfs/connInterfacesFile:"
echo "----------------------------------------------"
echo "$conn_content"
echo "----------------------------------------------"

echo "Restarting BeeGFS services..."

# --- Update the file locally ---
echo "$conn_content" | sudo tee /etc/beegfs/connInterfacesFile > /dev/null
if [ $? -ne 0 ]; then
    echo "Error: Failed to update /etc/beegfs/connInterfacesFile"
    exit 1
fi

# --- Restart BeeGFS services ---
sudo systemctl restart beegfs-storage.service
echo "Storage service restarted successfully."
sudo systemctl restart beegfs-meta.service
echo "Meta service restarted successfully."
sudo systemctl restart beegfs-client.service
echo "Client service restarted successfully."

echo "BeeGFS interfaces file updated and services restarted successfully."
