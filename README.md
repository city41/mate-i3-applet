# MATE i3 Workspace Applet

![screenshot](https://raw.github.com/city41/mate-i3-applet/master/screenshot.png)

This applet shows the current state of i3 workspaces when using i3 as your window manager in MATE.

## Status

Needs a better install story, but seems pretty stable. I've been using it all day long at work with no issues

## Tested On

Ubuntu MATE 16.04 with i3 4.11

## How to Install

No installer yet, for now:

1. edit the org.mate.panel.* files and fix the path to `matei3applet.py`
2. `sudo cp org.mate.panel.applet.I3Applet.service /usr/share/dbus-1/services`
3. `sudo cp org.mate.panel.I3Applet.mate-panel-applet /usr/share/mate-panel/applets`
4. log out and back in
5. On a MATE panel, choose 'Add to Panel...' and add the i3 panel

## Todo

Check the github issues, tracking all known issues and work there
