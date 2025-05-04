###############################################################################
#  BeeGFS service helpers – start/stop individual or all services
#
#  Functions:
#     beegfs-start   <all|service_name>
#     beegfs-stop    <all|service_name>
#     beegfs-restart <all|service_name>
#     beegfs-reload  <all|service_name>
#     beegfs-status  <all|service_name>
#     beegfs-enable  <all|service_name>
#     beegfs-disable <all|service_name>
###############################################################################

# --- Service names ---
_BEEGFS_UNITS=(beegfs-mgmtd beegfs-meta beegfs-storage beegfs-helperd beegfs-client)

# --- Service control function ---
_beegfs_ctl() {
    local action="$1" target="$2" svc valid=0

    if [[ -z "$target" ]]; then
        echo "Usage: beegfs-${action} {all|service_name}"
        return 1
    fi

    if [[ "$target" == "all" ]]; then
        for svc in "${_BEEGFS_UNITS[@]}"; do
            _beegfs_do "$action" "$svc"
        done
        return
    fi

    [[ "$target" != beegfs-* ]] && target="beegfs-${target}"

    for svc in "${_BEEGFS_UNITS[@]}"; do
        [[ "$svc" == "$target" ]] && { valid=1; break; }
    done
    if (( ! valid )); then
        echo "Invalid service name: $target"
        echo "Valid services: ${_BEEGFS_UNITS[*]//beegfs-/}"
        return 1
    fi

    _beegfs_do "$action" "$target"
}

# --- Helper function for systemctl ---
_beegfs_do() {
    local action="$1" unit="$2"
    local verb
    case "$action" in
        start)   verb="Starting" ;;
        stop)    verb="Stopping" ;;
        restart) verb="Restarting" ;;
        reload)  verb="Reloading" ;;
        status)  verb="Checking" ;;
        enable)  verb="Enabling" ;;
        disable) verb="Disabling" ;;
        *)       echo "Invalid action: $action" ; return 1 ;;
    esac
    echo "${verb} ${unit} …"
    sudo systemctl "$action" "$unit"
}

# --- Functions to be called from the command line ---
beegfs-start()   { _beegfs_ctl start   "$1"; }
beegfs-stop()    { _beegfs_ctl stop    "$1"; }
beegfs-restart() { _beegfs_ctl restart "$1"; }
beegfs-reload()  { _beegfs_ctl reload  "$1"; }
beegfs-status()  { _beegfs_ctl status  "$1"; }
beegfs-enable()  { _beegfs_ctl enable  "$1"; }
beegfs-disable() { _beegfs_ctl disable "$1"; }

###############################################################################
# Examples
#   beegfs-start all
#   beegfs-restart client
###############################################################################
