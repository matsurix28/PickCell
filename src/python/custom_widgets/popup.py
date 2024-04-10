import os

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup


class FileDialogPopup(Popup):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

class FolderDialogPopup(Popup):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)
    
    def is_dir(self, dirname, filename):
        return os.path.isdir(os.path.join(dirname, filename))

class ErrorPopup(Popup):
    title_text = StringProperty('Error')
    message = StringProperty('')

class ProgressPopup(Popup):
    title_text = StringProperty('')
    message = StringProperty('')
    def __init__(self, cancel_func, **kwargs):
        super(ProgressPopup, self).__init__(**kwargs)
        self.cancel = cancel_func
