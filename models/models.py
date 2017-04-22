import re
import time
from models import editorobservers


from PyQt5.QtWidgets import * # import for file dialogs


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
        self.activeDocument = None

    def setDocument(self,document):
        """ Set a new document as active document """
        self.activeDocument = document
        self.resetState()

    def setText(self,text):
        self.textContent = text
        self.updateState()
        super().notify()

    def updateState(self):
        # When the text changes, we might need to update multiple variables.
        self.wordCount = self.countWords()
        self.characterCount = len(self.textContent)


    def resetState(self):
        """ Reset the values of this model """
        self.wordCount = 0
        self.textContent = ""
        self.characterCount = 0
        self.wpm = 0
        self.cpm = 0
        self.cpm_buffer = []
        super().notify()

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


    def saveContentToFile(self, saveAs = False):
        if (self.activeDocument is None or self.activeDocument == "") or saveAs == True:
            result = QFileDialog.getSaveFileName()
            if result:
                filename = result[0]
                # todo: allow non-txt extensions
                if(not len(filename.split("."))==2):
                    filename = filename+".txt"
                self.activeDocument = filename


        file = open(self.activeDocument,'w')
        file.write(self.textContent)
        file.close()


    def saveAs(self):
        self.saveContentToFile(True)

