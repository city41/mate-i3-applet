# MATE I3 Workspace Applet

![screenshot](https://raw.github.com/city41/mate-i3-applet/master/screenshot.png)

This applet shows the current state of i3 workspaces when using i3 as your window manager in MATE.

## Very Alpha!

This thing is currently very raw. Not only that, this project is my first time using GTK, MATE applets *and* Python. So yeah, not really ready for general usage.

## Known Issue

Pretty often when receiving a message from i3, it will throw `UnicodeDecodeError`. Seems it either received an incomplete message from i3, or it's truncating the message somehow.

## Tested On

I am using Ubuntu MATE 16.04 with i3 4.11

