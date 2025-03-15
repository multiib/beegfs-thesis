#!/usr/bin/env bash

# --- Configuration ---
sync-all() {
    sync-18-fio
    sync-17-scripts
    sync-18-scripts
}

sync-18-fio() {

    local FIO_PATH="$HOME/thesis/fio/"
    local REMOTE_PATH="benjabor@mpg18:/home/benjabor/fio/"

    # --- Step A: Pull from remote to local ---
    echo "Pulling from $REMOTE_PATH -> $FIO_PATH ..."
    rsync -avz --exclude='.DS_Store' "$REMOTE_PATH/" "$FIO_PATH/" || {
        echo "Pull failed. Aborting entire sync." >&2
        return 1
    }


    echo "Sync complete! (Pulled then pushed to $REMOTE_18)."
}

sync-17-scripts() {

    local SCRIPTS_PATH="$HOME/thesis/scripts/"
    local REMOTE_PATH="benjabor@mpg17:/home/benjabor/scripts/"

    echo "Pushing from $SCRIPTS_PATH -> $REMOTE_PATH ..."
    rsync -avz --exclude='.DS_Store' "$SCRIPTS_PATH/" "$REMOTE_PATH/" || {
        echo "Push failed. Check the logs/errors." >&2
        return 1
    }

    echo "Sync complete! (Pulled then pushed to $REMOTE_17)."
}

sync-18-scripts() {



    local SCRIPTS_PATH="$HOME/thesis/scripts/"
    local REMOTE_PATH="benjabor@mpg18:/home/benjabor/scripts/"

    echo "Pushing from $SCRIPTS_PATH -> $REMOTE_PATH ..."
    rsync -avz --exclude='.DS_Store' "$SCRIPTS_PATH/" "$REMOTE_PATH/" || {
        echo "Push failed. Check the logs/errors." >&2
        return 1
    }

    echo "Sync complete! (Pulled then pushed to $REMOTE_18)."
}


