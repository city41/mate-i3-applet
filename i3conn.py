import i3ipc
import threading
import time

from log import log

class WorkspaceSub(threading.Thread):
    def __init__(self, con, callback, modeCallback):
        self.con = con

        i3callback = lambda _, workspaces: callback(self.con.get_workspaces())
        i3ModeCallback = lambda _, mode: modeCallback(mode)
        self.con.on('workspace', i3callback)
        self.con.on('mode', i3ModeCallback)

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

    def get_bar_config_list(self):
        return self.con.get_bar_config_list()

    def get_bar_config(self, bar_id):
        return self.con.get_bar_config(bar_id)

    # TODO: this is a hack to get workspace switching working.
    # The problem is listening to i3 events needs to be on its own
    # thread because it constantly blocks. So that means sending a command
    # is taking place on the main thread(s), I suspect GTK spins up more than
    # one thread or uses a thread pool. So the gtk thread(s) can't use the same
    # connection, as they will trip over themselves and
    # clobber the socket. The hack is to create a new connection each time, which 
    # opens its own independent socket to i3.
    # 
    # ways to fix this:
    # 1) figure out how to make this a critical section on the gtk thread
    # 2) spin up a third thread who's job is to send commands to i3, use a queue
    # 3) figure out how to use coroutines and ditch threads altogether
    #
    # to anyone reading this, I'm brand new to python, which is why I'm stumbling on this
    #
    def go_to_workspace(self, workspace_name):
        log('go to workspace: ' + workspace_name)
        throwawayCon = i3ipc.Connection()
        throwawayCon.command('workspace ' + workspace_name)
        throwawayCon.close()

    def subscribe(self, callback, modeCallback):
        if not self.con:
            raise "subscribing but there is no connection"
        self.callback = callback
        self.modeCallback = modeCallback
        self.sub = WorkspaceSub(self.con, self.callback, self.modeCallback)

    def close(self):
        log('I3Conn close')
        if self.con:
            self.con.close()
            self.con = None

    def restart(self, data=None):
        log('I3Conn restart')
        self.close()

        self.try_to_connect()

        if self.con and self.callback and self.modeCallback:
            self.subscribe(self.callback, self.modeCallback)

