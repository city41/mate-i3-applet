import i3ipc
import threading

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

        self.close()

    def close(self):
        self.con.event_socket_teardown()

class I3Conn(object):
    def __init__(self):
        self.con = i3ipc.Connection()

    def get_workspaces(self):
        return self.con.get_workspaces()

    def subscribe(self, callback):
        return WorkspaceSub(self.con, callback)
        
