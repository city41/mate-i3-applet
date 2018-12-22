#!/usr/bin/env python3


#* a simple i3 workspace applet for MATE Desktop
#* Copyright (c) 2017 Matt Greer <matt.e.greer@gmail.com>
#* see README for more information


from distutils.core import setup
from distutils.command.install_data import install_data


class InstallData(install_data):
    def run(self):
        install_data.run(self)


setup(
    name="mate-i3-applet",
    version="2.3.0",
    description="MATE i3 Workspace Applet",
    long_description="Applet for MATE Panel showing i3 workspaces and mode.",
    license="BSD",
    url="https://github.com/city41/mate-i3-applet",
    author="Matt Greer",
    author_email="matt.e.greer@gmail.com",

    data_files=[
        ('/usr/lib/mate-i3-applet', [
            'matei3applet.py',
            'log.py',
            'i3conn.py',
            'i3ipc.py',
            'mate_version.py',
        ]),
        ('/usr/share/dbus-1/services', ['matei3applet.service']),
        ('/usr/share/mate-panel/applets', ['matei3applet.mate-panel-applet']),
    ],
    cmdclass={'install_data': InstallData}
)
