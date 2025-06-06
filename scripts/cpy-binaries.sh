###############################################################################
#  Copy binaries to the right directories on the specified hosts. Strip 
#  unneeded symbols from the binaries to save space. Skip transferring to the
#  local host if the IP address matches one of the specified hosts.
#
#  Functions:
#    cp-binaries <none>
###############################################################################

# --- Configuration ---
_TARGET_DIR="$HOME/beegfs-thesis/bin/beegfs-bin-ssocks"


# --- Copy binaries to target directory and sync to remote hosts ---
cpy-binaries() {

    mkdir -p "$_TARGET_DIR"

    base_src="$HOME/beegfs-thesis/beegfs-ssocks"
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
        echo "Stripped and copied $rel to $dst"
    done
}