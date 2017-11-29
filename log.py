import os

SHOULD_LOG = True
have_logged = False

def log(message):
    global SHOULD_LOG

    if SHOULD_LOG:
        global have_logged
        mode = 'w'

        if have_logged:
            mode = 'a'

        have_logged = True

        file = open(os.path.expanduser("~/.matei3applet.log"), mode)
        file.write(message)
        file.write('\n')
        file.close()
