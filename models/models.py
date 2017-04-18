import re
from models import editorobservers

class EditorModel(editorobservers.EditorObservable):
    """ class that represents the data/state of the editor """
    def __init__(self):
        super().__init__()
        self.wordCount = 0
        self.textContent = ""
        self.characterCount = 0

    def setText(self,text):
        self.textContent = text
        self.updateState()
        super().notify()

    # When the text changes, we might need to update multiple variables.
    def updateState(self):
        self.wordCount = self.countWords()
        self.characterCount = len(self.textContent)


    def countWords(self):
        words = re.split("[' '|'\\n']",self.textContent)
        # filter out empty blocks that somehow happen
        words = list(filter(lambda k: k != '',words))
        #filter out non-words
        words = list(filter(lambda k : re.search("^[aA-zZ]+.?$",k) != None, words))
        return len(words)

