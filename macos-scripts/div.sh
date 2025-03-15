#!/usr/bin/env bash


z17(){
    sshfs \
    -o reconnect,ServerAliveInterval=15,ServerAliveCountMax=3 \
    benjabor@mpg17:/home/benjabor/ \
    /Users/benjaminborge/thesis/z17
    }



z18(){
    sshfs \
  -o reconnect,ServerAliveInterval=15,ServerAliveCountMax=3 \
  benjabor@mpg18:/home/benjabor/ \
  /Users/benjaminborge/thesis/z18
}


#umount

zz17(){
    umount /Users/benjaminborge/thesis/z17
}

zz18(){
    umount /Users/benjaminborge/thesis/z18
}