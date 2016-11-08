class EventEmitter(list):

    def subscribe(self, callback):
        self.append(callback)
        
    def emit(self, source, *args, **kwargs):
        for sub in self:
            sub(source, *args, **kwargs)
        