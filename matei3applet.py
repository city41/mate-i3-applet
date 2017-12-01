#!/usr/bin/env python3
 
import gi
gi.require_version("Gtk", "2.0")
gi.require_version("MatePanelApplet", "4.0")
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import MatePanelApplet

from i3conn import I3Conn
from log import log

DEFAULT_COLORS = {
    'background': '#000000', 
    'statusline': '#ffffff',
    'separator': '#666666',

    'binding_mode_border': '#2f343a',
    'binding_mode_bg': '#900000',
    'binding_mode_text': '#ffffff',

    'active_workspace_border': '#333333',
    'active_workspace_bg': '#5f676a',
    'active_workspace_text': '#ffffff',

    'inactive_workspace_border': '#333333',
    'inactive_workspace_bg': '#222222',
    'inactive_workspace_text': '#888888',

    'urgent_workspace_border': '#2f343a',
    'urgent_workspace_bg': '#900000',
    'urgent_workspace_text': '#ffffff',

    'focused_workspace_border': '#4c7899',
    'focused_workspace_bg': '#285577',
    'focused_workspace_text': '#ffffff'
}

class i3bar(object):
    def __init__(self, applet):
        log('initting')
        self.applet = applet
        self.applet.connect("destroy", self.destroy)
        self.i3conn = I3Conn()

        self.colors = self.init_colors()
        log('colors: ' + str(self.colors))

        self.init_widgets()
        self.set_initial_buttons()

        self.open_sub()

    def __del__(self):
        self.destroy(None)

    def destroy(self, event):
        self.close_sub()

    def init_widgets(self):
        self.box = Gtk.HBox()
        self.applet.add(self.box)

    def set_initial_buttons(self):
        self.set_workspace_buttons(self.i3conn.get_workspaces())

    def init_colors(self):
        global DEFAULT_COLORS

        bar_ids = self.i3conn.get_bar_config_list()

        colors = None
        while not colors and bar_ids:
            bar_id = bar_ids.pop()
            bar = self.i3conn.get_bar_config(bar_id)
            colors = bar['colors']

        return colors or DEFAULT_COLORS

    def close_sub(self):
        log('close_sub')
        self.i3conn.close()

    def open_sub(self):
        log('open_sub')
        self.i3conn.subscribe(self.on_workspace_event)

    def on_workspace_event(self, workspaces):
        log('on_workspace_event')

        if workspaces:
            GLib.idle_add(self.set_workspace_buttons, workspaces)

    def go_to_workspace(self, workspace):
        if not workspace['focused']:
            self.i3conn.go_to_workspace(workspace['name'])

    def set_workspace_buttons(self, workspaces):
        log('set_workspace_buttons')

        for child in self.box.get_children():
            self.box.remove(child)

        def get_workspace_bgcolor(workspace):
            if workspace['urgent']:
                return self.colors['urgent_workspace_bg']
            if workspace['focused']:
                return self.colors['focused_workspace_bg']
            return self.colors['active_workspace_bg']

        def get_workspace_fgcolor(workspace):
            if workspace['urgent']:
                return self.colors['urgent_workspace_text']
            if workspace['focused']:
                return self.colors['focused_workspace_text']
            return self.colors['active_workspace_text']

        def workspace_to_label(workspace):
            bgcolor = get_workspace_bgcolor(workspace)
            return '<span background="%s"><b> %s </b></span>' % (bgcolor, workspace['name'])

        def get_button(workspace):
            button = Gtk.EventBox()
            label = Gtk.Label(workspace_to_label(workspace))
            label.set_use_markup(True)
            button.add(label)
            button.connect("button_press_event", lambda w,e:  self.go_to_workspace(workspace))
            return button

        for workspace in workspaces:
            self.box.pack_start(get_button(workspace), False, False, 0)

        self.box.show_all()

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

