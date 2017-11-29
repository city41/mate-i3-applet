import i3ipc
import threading
import time

from log import log

class WorkspaceSub(threading.Thread):
    def __init__(self, con, callback):
        self.con = con

        i3callback = lambda _, workspaces: callback(self.con.get_workspaces())
        self.con.on('workspace', i3callback)

        threading.Thread.__init__(self)
        self.start()
        
    def run(self):
        log('run')
        self.con.event_socket_setup()

        while not self.con.event_socket_poll():
            log('loop')

class I3Conn(object):
    def __init__(self):
        self.try_to_connect()

    def try_to_connect(self, tries=5):
        con = None
        while not con and tries > 0:
            try:
                con = self.create_connection()
            except:
                tries -= 1
                time.sleep(0.3)

        if not con:
            raise "Failed to connect to i3, is it running?"
        else:
            self.con = con

    def create_connection(self):
        log('I3Conn create_connection')
        con = i3ipc.Connection()
        con.on('ipc_shutdown', self.restart)
        return con

    def get_workspaces(self):
        return self.con.get_workspaces()

    def subscribe(self, callback):
        if not self.con:
            raise "subscribing but there is no connection"
        self.callback = callback
        self.sub = WorkspaceSub(self.con, self.callback)

    def close(self):
        log('I3Conn close')
        if self.con:
            self.con.close()
            self.con = None

    def restart(self, data=None):
        log('I3Conn restart')
        self.close()

        self.try_to_connect()

        if self.con and self.callback:
            self.subscribe(self.callback)

