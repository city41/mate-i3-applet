#!/usr/bin/env python3
 
import gi
gi.require_version("Gtk", "2.0")
gi.require_version("MatePanelApplet", "4.0")
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import MatePanelApplet

import i3

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
    def on_workspace_button_click(self, event, button):
        i3.command('workspace', button.get_label())

    def destroy(self, event):
        self.close_sub(event)

    def __init__(self, applet):
        log('initting')
        self.applet = applet
        self.init_widgets()

        self.set_initial_label()

        self.open_sub(None)
        self.applet.connect("destroy", self.destroy)

    def init_widgets(self):
        self.workspace_label = Gtk.Label()
        self.workspace_label.set_use_markup(True)
        self.applet.add(self.workspace_label)

    def set_initial_label(self):
        socket = i3.Socket()
        self.set_workspace_label(socket.get('get_workspaces'))
        socket.close()

    def close_sub(self, event):
        log('close_sub')
        if self.subscription:
            self.subscription.close()

    def open_sub(self, event):
        log('open_sub')
        callback = lambda data, workspaces, _: self.on_workspace_event(data, workspaces)
        self.subscription = i3.Subscription(callback, 'workspace')

    def on_workspace_event(self, data, workspaces):
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

