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
