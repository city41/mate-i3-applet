import i3

class WorkspaceSub(object):
    def __init__(self, callback):
        i3callback = lambda data, workspaces, _: callback(workspaces)
        self.subscription = i3.Subscription(i3callback, 'workspace')

    def close(self):
        if self.subscription:
            self.subscription.close()

class I3Conn(object):
    def get_workspaces(self):
        socket = i3.Socket()
        ws = socket.get('get_workspaces')
        socket.close()
        return ws

    def subscribe(self, callback):
        return WorkspaceSub(callback)
        
