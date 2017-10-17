from models import models

class EditorController():
    """ controller for the editor """
    def __init__(self):
        self.editorModel = models.EditorModel()

    def set_textcontent(self, textContent):
        self.editorModel.setText(textContent)

    def get_textcontent(self):
        return self.editorModel.textContent

    def get_root(self):
        return self.editorModel.working_dir

    def subscribe(self,object):
        self.editorModel.addObserver(object)

    def get_wordcount(self):
        return self.editorModel.wordCount

    def get_charcount(self):
        return self.editorModel.characterCount

    def dump_charbuffer(self, buffer, buffer_starttime, buffer_endtime):
        self.editorModel.dumpbuffer(buffer, buffer_starttime, buffer_endtime)

    def get_CPM(self):
        return self.editorModel.cpm

    def get_WPM(self):
        return self.editorModel.wpm

    def set_document_by_path(self,path):
        self.editorModel.set_document_by_path(path)

    def set_active_document(self, document):
        self.editorModel.setDocument(document)

    def get_active_document(self):
        return self.editorModel.activeDocument

    def save_active_document(self):
        self.editorModel.saveContentToFile()

    def save_active_document_as(self):
        self.editorModel.saveAs()

    def reset_metrics(self):
        self.editorModel.reset_metrics()

    def set_working_dir(self,dir):
        self.editorModel.set_working_dir(dir)

    def open_file(self):
        self.editorModel.open_file()