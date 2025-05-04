###############################################################################
#  Copy binaries to the right directories on the specified hosts. Strip 
#  unneeded symbols from the binaries to save space. Skip transferring to the
#  local host if the IP address matches one of the specified hosts.
#
#  Functions:
#    cp-binaries <none>
###############################################################################
set -euo pipefail

# --- Configuration ---
_TARGET_DIR="$HOME/bin/beegfs-bin-ssocks"
_HOSTS=(172.16.3.117 172.16.3.118)

# --- Copy binaries to target directory and sync to remote hosts ---
cp-binaries() {

    mkdir -p "$_TARGET_DIR"

    base_src="$HOME/thesis/beegfs-ssock"
    declare -A bins=(
      [client_module/build/beegfs.ko]=beegfs.ko
      [ctl/build/beegfs-ctl]=beegfs-ctl
      [event_listener/build/beegfs-event-listener]=beegfs-event-listener
      [fsck/build/beegfs-fsck]=beegfs-fsck
      [helperd/build/beegfs-helperd]=beegfs-helperd
      [meta/build/beegfs-meta]=beegfs-meta
      [mgmtd/build/beegfs-mgmtd]=beegfs-mgmtd
      [mon/build/beegfs-mon]=beegfs-mon
      [storage/build/beegfs-storage]=beegfs-storage
    )

    for rel in "${!bins[@]}"; do
        dst="$_TARGET_DIR/${bins[$rel]}"
        cp   "$base_src/$rel" "$dst"
        [[ "$dst" == *.ko ]] || strip --strip-unneeded "$dst"
    done

    # ── Sync to remotes (rsync makes dirs for us) ─────────────────────────────
    read -r -a LOCAL_IPS <<<"$(hostname -I)"
    for host in "${_HOSTS[@]}"; do
        printf '%s\n' "${LOCAL_IPS[@]}" | grep -qx "$host" && {
            echo "Skipping local host $host"
            continue
        }

        echo "Syncing to $host …"
        rsync -az --delete --mkpath "$_TARGET_DIR/" "$USER@$host:$_TARGET_DIR/"
    done
}

cp-binaries()
