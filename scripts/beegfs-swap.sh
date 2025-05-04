###############################################################################
#  BeeGFS swap helpers – services and kernel module must be stopped before
#  running this script
#
#  Functions:
#     beegfs-swap       <client|meta|storage|mgmtd|helperd|all|realall>
#     beegfs-ssock-swap <client|meta|storage|mgmtd|helperd|all|realall>
#
#  “all”      = module + MAIN components
#  “realall”  = module + every component (MAIN + tools)
###############################################################################


# --- Configuration ---
MGMT_NODE="mpg-2014-17"

# --- Paths ---
_BEEGFS_MODULE_DIR="/lib/modules/$(uname -r)/updates/fs/beegfs_autobuild"
_BEEGFS_BIN_DIR="$HOME/beegfs-thesis/bin/beegfs-bin"
_BEEGFS_SSOCK_BIN_DIR="$HOME/beegfs-thesis/bin/beegfs-bin-ssocks"
_BEEGFS_TARGET_DIR="/opt/beegfs/sbin"

# --- Components ---
_MAIN_COMPONENTS=(client meta storage mgmtd helperd)
_ALL_COMPONENTS=("${_MAIN_COMPONENTS[@]}" mon ctl fsck event-listener)

# --- Check if this is the management node ---
_is_mgmt_node() {
    [[ $(hostname -s) == "${MGMT_NODE}" ]] && return 0

    return 1
}

# --- Swap client kernel module ---
_beegfs_swap_module() {
    local src_dir="$1"; shift
    local modprobe_opts=("$@")

    echo "Unloading old BeeGFS kernel module …"
    sudo rmmod beegfs 2>/dev/null || echo "Module not loaded (or already removed)"

    echo "Copying new module from ${src_dir} → ${_BEEGFS_MODULE_DIR} …"
    sudo cp "${src_dir}/beegfs.ko" "${_BEEGFS_MODULE_DIR}/"

    echo "Running depmod …"
    sudo depmod -a

    echo "Loading new module ${modprobe_opts[*]} …"
    sudo modprobe beegfs "${modprobe_opts[@]}"

    echo "Verifying loaded module:"
    modinfo beegfs | grep -E 'filename:|version:'

    echo "BeeGFS kernel module swap completed"
}

# --- Swap user space binary ---
_beegfs_swap_bin() {
    local comp="$1" src_dir="$2"
    local bin="beegfs-${comp}"

    [[ -f "${src_dir}/${bin}" ]] || { echo "✖ ${bin} not found in ${src_dir}"; return 1; }

    echo "Swapping ${bin} …"
    sudo cp "${src_dir}/${bin}" "${_BEEGFS_TARGET_DIR}/${bin}"
    sudo chmod +x "${_BEEGFS_TARGET_DIR}/${bin}"
    echo "Swapped ${bin}"
}

# --- Swap driver function ---
_beegfs_swap_driver() {
    local src_dir="$1"; shift
    local modprobe_opts=("$1"); shift
    local component="$1"

    [[ -n "${component}" ]] || {
        echo "Usage: ${FUNCNAME[2]} {client|meta|storage|mgmtd|helperd|all|realall}"
        return 1
    }

    case "${component}" in
        client)
            _beegfs_swap_module "${src_dir}" "${modprobe_opts[@]}"
            ;;
        meta|storage|helperd)
            _beegfs_swap_bin "${component}" "${src_dir}"
            ;;
        mgmtd)
            if _is_mgmt_node; then
                _beegfs_swap_bin "mgmtd" "${src_dir}"
            else
                echo "Skipping beegfs-mgmtd swap – this is not the management node."
            fi
            ;;
        all)
            echo "Swapping MAIN components: ${_MAIN_COMPONENTS[*]}"
            _beegfs_swap_module "${src_dir}" "${modprobe_opts[@]}"
            for comp in "${_MAIN_COMPONENTS[@]:1}"; do
                _beegfs_swap_bin "${comp}" "${src_dir}"
            done
            ;;
        realall)
            echo "Swapping ALL components: ${_ALL_COMPONENTS[*]}"
            _beegfs_swap_module "${src_dir}" "${modprobe_opts[@]}"
            for comp in "${_ALL_COMPONENTS[@]:1}"; do
                _beegfs_swap_bin "${comp}" "${src_dir}"
            done
            ;;
        *)
            echo "Invalid component: ${component}"
            echo "Valid choices: client meta storage mgmtd helperd all realall"
            return 1
            ;;
    esac
}

# --- Functions to be called from the command line ---
beegfs-swap()       { _beegfs_swap_driver "${_BEEGFS_BIN_DIR}"    ""              "$1"; }
beegfs-ssock-swap() { _beegfs_swap_driver "${_BEEGFS_SSOCK_BIN_DIR}" "sockFamily=ssocks" "$1"; }

###############################################################################
# Examples
#   beegfs-swap client          # swap only the client module
#   beegfs-ssock-swap all       # swap module + main comps for ssock build
#   beegfs-swap realall         # swap absolutely everything
###############################################################################
