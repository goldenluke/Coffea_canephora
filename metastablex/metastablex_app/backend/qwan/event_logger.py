import time

class EventLogger:

    def __init__(self, max_events=100):
        self.events = []
        self.max_events = max_events

    def add(self, event):

        event["timestamp"] = time.time()
        self.events.append(event)

        if len(self.events) > self.max_events:
            self.events.pop(0)

    def get(self):
        return self.events
