class EventEmitter(list):

    def subscribe(self, callback):
        self.append(callback)
        