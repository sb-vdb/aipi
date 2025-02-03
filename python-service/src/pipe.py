import gc

PIPE = None
PIPE_NAME = None
PIPE_RUNNING = False

def setPipe(pipe, name):
    global PIPE, PIPE_NAME
    PIPE = pipe
    PIPE_NAME = name

def get_or_kill_pipe(name):
    global PIPE, PIPE_NAME
    if PIPE_NAME != name:
        del PIPE
        gc.collect()
        return None
    else:
        return PIPE

def change_status(bl):
    global PIPE_RUNNING
    PIPE_RUNNING = bl

def is_running():
    global PIPE_RUNNING
    return PIPE_RUNNING