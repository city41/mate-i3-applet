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
        self.create_connection()

    def create_connection(self):
        log('I3Conn create_connection')
        self.con = i3ipc.Connection()
        self.con.on('ipc_shutdown', self.restart)

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

        tries = 5
        while not self.con and tries > 0:
            try:
                self.create_connection()
            except:
                tries -= 1
                time.sleep(0.3)

        log('after create_connection')

        if self.con and self.callback:
            self.subscribe(self.callback)
        else:
            raise "Failed to restart, is i3 still running?"

        
