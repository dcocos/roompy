# Usage:
# motionDetected = Event()
#
# call it with:
# motionDetected()
#
# register with:
# def log_motion_detected():
#     print("Motion! %s" % datetime.now())
# motionDetected += log_motion_detected


class Event:
    def __init__(self):
        self.handlers = set()

    def register(self, handler):
        self.handlers.add(handler)
        return self

    def unregister(self, handler):
        self.handlers.remove(handler)
        return self

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    def get_handler_count(self):
        return len(self.handlers)

    __iadd__ = register
    __isub__ = unregister
    __call__ = fire
    __len__ = get_handler_count
