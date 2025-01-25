import time

class ProgressStream:
    def __init__(self):
        self.start_time = time.time()
        self.messages = []
        self.done = False
    
    def parse(self, msg):
        percent, bar, count, t = msg.split(" ")
        if percent == "100%":
            self.done = True
        return percent

    def write(self, msg):
        self.messages.append(msg)

    def flush(self):
        self.messages = []

    def print(self):
        print(f"logged msg: {self.messages}")
    