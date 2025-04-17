pending_command = {'command': None, 'command-URL': None, 'command-expected': None, 'command-expected-URL': None}

def reset_command():
    global pending_command
    pending_command = {
        'command': None,
        'command-URL': None,
        'command-expected': None,
        'command-expected-URL': None
    }