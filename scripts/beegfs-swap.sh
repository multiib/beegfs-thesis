# Source this script: source beegfs-swap.sh

BEENGFS_MODULE_DIR="/lib/modules/$(uname -r)/updates/fs/beegfs_autobuild"
BEENGFS_BINARIES_DIR="/home/benjabor/beegfs-binaries"
BEENGFS_SSOCK_BINARIES_DIR="/home/benjabor/beegfs-ssock-binaries"

BINARY_TARGET_DIR="/opt/beegfs/sbin"

# Define component groups
MAIN_COMPONENTS=("client" "meta" "storage" "mgmtd" "helperd")
ALL_COMPONENTS=("${MAIN_COMPONENTS[@]}" "mon" "ctl" "fsck" "event-listener")

swap_module() {
    local binary_dir="$1"
    local use_ssocks_family="$2"

    echo "Unloading old kernel module..."
    sudo rmmod beegfs 2>/dev/null || echo "Module not loaded or already removed"

    echo "Copying new module from $binary_dir..."
    sudo cp "$binary_dir/beegfs.ko" "$BEENGFS_MODULE_DIR/"

    echo "Running depmod..."
    sudo depmod -a

    echo "Loading new module..."
    if [[ "$use_ssocks_family" == "true" ]]; then
        local family
        family=$(cat /proc/net/af_ssocks/family)
        echo "Using ssocks_family=$family"
        sudo modprobe beegfs ssocks_family="$family"
    else
        echo "Using default family"
        sudo modprobe beegfs
    fi

    echo "Verifying new module version..."
    modinfo beegfs | grep -E "filename|version"

    echo "BeeGFS module swap completed successfully!"
}


swap_binary() {
    local binary="$1"
    local binary_dir="$2"

    if [[ ! -f "$binary_dir/$binary" ]]; then
        echo "Error: Binary $binary not found in $binary_dir"
        return 1
    fi

    echo "Swapping $binary..."
    sudo cp "$binary_dir/$binary" "$BINARY_TARGET_DIR/$binary"
    sudo chmod +x "$BINARY_TARGET_DIR/$binary"

    echo "Swapped $binary successfully!"
}

beegfs-swap() {
    local component="$1"

    case "$component" in
        client)
            swap_module "$BEENGFS_BINARIES_DIR"
            ;;
        meta|storage|mgmtd|helperd)
            swap_binary "beegfs-$component" "$BEENGFS_BINARIES_DIR"
            ;;
        all)
            echo "Swapping main components: ${MAIN_COMPONENTS[*]}"
            swap_module "$BEENGFS_BINARIES_DIR"
            for binary in "${MAIN_COMPONENTS[@]:1}"; do
                swap_binary "beegfs-$binary" "$BEENGFS_BINARIES_DIR"
            done
            ;;
        realall)
            echo "Swapping all components: ${ALL_COMPONENTS[*]}"
            swap_module "$BEENGFS_BINARIES_DIR"
            for binary in "${ALL_COMPONENTS[@]:1}"; do
                swap_binary "beegfs-$binary" "$BEENGFS_BINARIES_DIR"
            done
            ;;
        *)
            echo "Usage: beegfs-swap {client|meta|storage|mgmtd|helperd|all|realall}"
            return 1
            ;;
    esac
}

beegfs-ssock-swap() {
    local component="$1"

    case "$component" in
        client)
            swap_module "$BEENGFS_SSOCK_BINARIES_DIR" true
            ;;
        meta|storage|mgmtd|helperd)
            swap_binary "beegfs-$component" "$BEENGFS_SSOCK_BINARIES_DIR"
            ;;
        all)
            echo "Swapping main components: ${MAIN_COMPONENTS[*]}"
            swap_module "$BEENGFS_SSOCK_BINARIES_DIR" true
            for binary in "${MAIN_COMPONENTS[@]:1}"; do
                swap_binary "beegfs-$binary" "$BEENGFS_SSOCK_BINARIES_DIR"
            done
            ;;
        realall)
            echo "Swapping all components: ${ALL_COMPONENTS[*]}"
            swap_module "$BEENGFS_SSOCK_BINARIES_DIR" true
            for binary in "${ALL_COMPONENTS[@]:1}"; do
                swap_binary "beegfs-$binary" "$BEENGFS_SSOCK_BINARIES_DIR"
            done
            ;;
        *)
            echo "Usage: beegfs-ssock-swap {client|meta|storage|mgmtd|helperd|all|realall}"
            return 1
            ;;
    esac
}

