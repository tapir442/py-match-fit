class Model(object):
    def __init__(self):
        self._args = ""
        self.observers = []
        
    def register_observer(self, observer):
        self.observers.append(observer)
        
    def notify(self):
        [observer.update() for observer in self.observers]
        
    @property
    def args(self):
        return self._args
    
    @args.setter
    def args(self, value):
        self._args = value
        self.notify()
    
    
class GUI(object):
    def __init__(self):
        pass
    
    def show(self, data):
        print data
        
        
class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.model.register_observer(self)
        
    def update(self):
        self.view.show(self.model.args)
        
        
model = Model()
gui = GUI()
ctrl = Controller(model, gui)

model.args = "new data"
model.args = "even more new data"
