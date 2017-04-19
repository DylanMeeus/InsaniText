import re
import time
from models import editorobservers

class EditorModel(editorobservers.EditorObservable):
    """ class that represents the data/state of the editor """
    def __init__(self):
        super().__init__()
        self.wordCount = 0
        self.textContent = ""
        self.characterCount = 0
        self.wpm = 0
        self.cpm = 0
        self.cpm_buffer = []

    def setText(self,text):
        self.textContent = text
        self.updateState()
        super().notify()

    # When the text changes, we might need to update multiple variables.
    def updateState(self):
        self.wordCount = self.countWords()
        self.characterCount = len(self.textContent)


    def dumpbuffer(self,charbuffer,buffer_starttime, buffer_endtime):
        """ analyze a buffer of characters to update the wpm and cpm values """

        # filter for only the actual characters of the alphabet, and allow numbers too.
        charbuffer = list(filter(lambda k : re.match('[aA-zZ|0-9|" "]',k) != None,charbuffer))
        cpb = len(charbuffer)
        buffer_delta = (buffer_endtime - buffer_starttime) / 1000 # time in seconds
        cps = cpb / buffer_delta
        self.cpm_buffer.append(cps*60)
        self.cpm = sum(self.cpm_buffer) // len(self.cpm_buffer)
        self.wpm = self.cpm // 5
        super().notify()

    def countWords(self):
        words = re.split("[' '|'\\n']",self.textContent)
        # filter out empty blocks that somehow happen
        words = list(filter(lambda k: k != '',words))
        #filter out non-words
        words = list(filter(lambda k : re.search("^[aA-zZ]+.?$",k) != None, words))
        return len(words)

