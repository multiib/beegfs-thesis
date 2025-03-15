#!/bin/bash

cp-binaries() {

# --- Configuration ---
    TARGET_DIR="/home/benjabor/beegfs-ssock-binaries/"
    REMOTE_HOST="172.16.3.117"


    cp /home/benjabor/beegfs-ssock/client_module/build/beegfs.ko $TARGET_DIR/beegfs.ko

    cp /home/benjabor/beegfs-ssock/ctl/build/beegfs-ctl $TARGET_DIR/beegfs-ctl
    strip --strip-unneeded $TARGET_DIR/beegfs-ctl

    cp /home/benjabor/beegfs-ssock/event_listener/build/beegfs-event-listener $TARGET_DIR/beegfs-event-listener
    strip --strip-unneeded $TARGET_DIR/beegfs-event-listener

    cp /home/benjabor/beegfs-ssock/fsck/build/beegfs-fsck $TARGET_DIR/beegfs-fsck
    strip --strip-unneeded $TARGET_DIR/beegfs-fsck

    cp /home/benjabor/beegfs-ssock/helperd/build/beegfs-helperd $TARGET_DIR/beegfs-helperd
    strip --strip-unneeded $TARGET_DIR/beegfs-helperd

    cp /home/benjabor/beegfs-ssock/meta/build/beegfs-meta $TARGET_DIR/beegfs-meta
    strip --strip-unneeded $TARGET_DIR/beegfs-meta

    cp /home/benjabor/beegfs-ssock/mgmtd/build/beegfs-mgmtd $TARGET_DIR/beegfs-mgmtd
    strip --strip-unneeded $TARGET_DIR/beegfs-mgmtd

    cp /home/benjabor/beegfs-ssock/mon/build/beegfs-mon $TARGET_DIR/beegfs-mon
    strip --strip-unneeded $TARGET_DIR/beegfs-mon

    cp /home/benjabor/beegfs-ssock/storage/build/beegfs-storage $TARGET_DIR/beegfs-storage
    strip --strip-unneeded $TARGET_DIR/beegfs-storage

    rsync -avz --progress $TARGET_DIR benjabor@$REMOTE_HOST:$TARGET_DIR

}