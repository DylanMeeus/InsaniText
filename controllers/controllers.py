from models import models

class EditorController():
    """ controller for the editor """
    def __init__(self):
        self.editorModel = models.EditorModel()

    def setTextContent(self,textContent):
        self.editorModel.setText(textContent)

    def subscribe(self,object):
        self.editorModel.addObserver(object)

    def getWordCount(self):
        return self.editorModel.wordCount

    def getCharCount(self):
        return self.editorModel.characterCount

    def dumpcharbuffer(self,buffer,buffer_starttime, buffer_endtime):
        self.editorModel.dumpbuffer(buffer,buffer_starttime,buffer_endtime)

    def getCPM(self):
        return self.editorModel.cpm

    def getWPM(self):
        return self.editorModel.wpm

    def setActiveDocument(self,document):
        self.editorModel.setDocument(document)

    def getActiveDocument(self):
        return self.editorModel.activeDocument