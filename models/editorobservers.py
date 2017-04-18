
class EditorObservable():
    def __init__(self):
        self.observers = []

    def addObserver(self,observer):
        self.observers.append(observer)

    def notify(self):
        for observer in self.observers:
            observer.update()

class EditorObserver():
    def update(self):
        pass
