# beegfs-service.sh
# Source this file to have the beegfs-service function available.
#
# Usage:
#   beegfs-service start all
#   beegfs-service start mgmtd
#   beegfs-service stop client
#   beegfs-service stop all

beegfs-service() {
    # List of all BeeGFS services
    local BEEGFS_SERVICES=( "beegfs-mgmtd" "beegfs-meta" "beegfs-storage" "beegfs-helperd" "beegfs-client" )
    local action="$1"
    local target="$2"
    local svc
    local valid

    # Usage message
    if [[ $# -ne 2 ]]; then
        echo "Usage: beegfs-service {start|stop} {all|service_name}"
        echo "Example: beegfs-service start all"
        echo "         beegfs-service stop client"
        return 1
    fi

    # Validate action parameter
    if [[ "$action" != "start" && "$action" != "stop" ]]; then
        echo "Invalid action: $action"
        echo "Usage: beegfs-service {start|stop} {all|service_name}"
        return 1
    fi

    # Function to perform service action
    perform_action() {
        local svc="$1"
        echo "${action^}ing ${svc} ..."  # Capitalize first letter of action for display
        sudo systemctl "$action" "$svc"
    }

    if [[ "$target" == "all" ]]; then
        # Loop through all defined services
        for svc in "${BEEGFS_SERVICES[@]}"; do
            perform_action "$svc"
        done
    else
        # If target doesn't already start with 'beegfs-', prepend it
        if [[ "$target" != beegfs-* ]]; then
            target="beegfs-$target"
        fi

        # Validate that the target is in our list of services
        valid=0
        for svc in "${BEEGFS_SERVICES[@]}"; do
            if [[ "$svc" == "$target" ]]; then
                valid=1
                break
            fi
        done

        if [[ $valid -ne 1 ]]; then
            echo "Invalid service name: $target"
            echo "Valid services: ${BEEGFS_SERVICES[*]//beegfs-/}"
            return 1
        fi

        perform_action "$target"
    fi
}


