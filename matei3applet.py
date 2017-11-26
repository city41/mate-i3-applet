#!/usr/bin/env python3
 
import gi
gi.require_version("Gtk", "2.0")
gi.require_version("MatePanelApplet", "4.0")
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import MatePanelApplet

from i3conn import I3Conn

have_logged = False

def log(message):
    global have_logged
    mode = 'w'

    if have_logged:
        mode = 'a'

    have_logged = True

    file = open('/home/matt/dev/matei3applet/log.txt', mode)
    file.write(message)
    file.write('\n')
    file.close()

class i3bar(object):
    def destroy(self, event):
        self.close_sub()

    def __init__(self, applet):
        log('initting')
        self.applet = applet
        self.i3conn = I3Conn()
        self.init_widgets()

        self.set_initial_label()

        self.open_sub()
        self.applet.connect("destroy", self.destroy)

    def init_widgets(self):
        self.workspace_label = Gtk.Label()
        self.workspace_label.set_use_markup(True)
        self.applet.add(self.workspace_label)

    def set_initial_label(self):
        self.set_workspace_label(self.i3conn.get_workspaces())

    def close_sub(self):
        log('close_sub')
        if self.subscription:
            self.subscription.close()

    def open_sub(self):
        log('open_sub')
        self.subscription = self.i3conn.subscribe(self.on_workspace_event)

    def on_workspace_event(self, workspaces):
        log('on_workspace_event')

        if workspaces:
            GLib.idle_add(self.set_workspace_label, workspaces)

    def set_workspace_label(self, workspaces):
        log('set_workspace_label')

        new_label = ''
        for workspace in workspaces:
            new_label += ' '
            if workspace['focused']:
                new_label += '<span background="#6587bf"><b> '
            new_label += workspace['name']
            if workspace['focused']:
                new_label += ' </b></span>'
    
        if new_label != self.workspace_label.get_label():
            self.workspace_label.set_label(new_label)

    def show(self):
        self.applet.show_all()

def applet_factory(applet, iid, data):
    log('iid: ' + iid)
    if iid != "I3Applet":
       return False
 
    bar = i3bar(applet)
    bar.show()
 
    return True

MatePanelApplet.Applet.factory_main("I3AppletFactory", True,
                                    MatePanelApplet.Applet.__gtype__,
                                    applet_factory, None)

