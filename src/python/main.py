import os
from os.path import expanduser

from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooser
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget

src_dir = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../'))
currentActivity = None
CLS_Activity = None
CLS_Intent = None
ImagesMedia = None

REQUEST_GALLERY = 1
MediaStore_Images_Media_DATA = '_data'

class PickcellApp(App):
    def build(self):
        if platform == 'android':
            Window.fullscreen = 'auto'
            Window.bind(on_keyboard=self.key_input)
            from jnius import autoclass, cast

            global currentActivity
            global CLS_Activity
            global CLS_Intent
            global ImagesMedia

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            CLS_Activity = autoclass('android.app.Activity')
            CLS_Intent = autoclass('android.content.Intent')
            ImagesMedia = autoclass('android.provider.MediaStore$Images$Media')

            from android.permissions import Permission, request_permissions
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.MANAGE_DOCUMENTS])
        else:
            Window.size = (1280, 800)
            Builder.load_file(src_dir + '/layouts/pc.kv')
            self.home_dir = expanduser('~')
        return Root()

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            return True
        else:
            return False

class DetectWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(DetectWidget, self).__init__(**kwargs)
        self.src_dir = src_dir
        self.d = None

    def run(self, img_path):
        if self.d is None:
            from detect import Detect
            self.d = Detect()

    def set_default_value(self):
        self.ids.thresh_slider.min

class FvFmWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(FvFmWidget, self).__init__(**kwargs)

class ArrangeWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(ArrangeWidget, self).__init__(**kwargs)

class SplitColorWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(SplitColorWidget, self).__init__(**kwargs)

class Root(BoxLayout):
    pass

if __name__ == '__main__':
    PickcellApp().run()