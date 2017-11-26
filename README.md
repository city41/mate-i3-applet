# MATE i3 Workspace Applet

![screenshot](https://raw.github.com/city41/mate-i3-applet/master/screenshot.png)

This applet shows the current state of i3 workspaces when using i3 as your window manager in MATE.

## Very Alpha!

This thing is currently very raw. Not only that, this project is my first time using GTK, MATE applets *and* Python. So yeah, not really ready for general usage. There are some bugs I am fighting.

## Known Issue

Pretty often when receiving a message from i3, it will throw `UnicodeDecodeError`. Seems it either received an incomplete message from i3, or it's truncating the message somehow.

## Tested On

I am using Ubuntu MATE 16.04 with i3 4.11

## How to Install

No installer yet, for now:

1. edit the org.mate.panel.* files and fix the path to `matei3applet.py`
2. `sudo cp org.mate.panel.applet.I3Applet.server /usr/share/dbus-1/services`
3. `sudo cp org.mate.panel.I3Applet.mate-panel-applet /usr/share/mate-panel/applets`
4. log out and back in
5. On a MATE panel, choose 'Add to Panel...' and add the i3 panel

## How to Work on the applet

Install as above. Then edit the python files and when ready, `killall python3` will cause mate-panel to ask you if you want to reload the applet, say yes. I hardly use anything written in python, so killall does no real harm on my box. Alternatively you can use mate-panel-test-applets` to launch the applet.
