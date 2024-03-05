from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager

currentActivity = None
CLS_Activity = None
CLS_Intent = None
ImagesMedia = None

REQUEST_GALLERY = 1
MediaStore_Images_Media_DATA = '_data'

class DetectWidget(Screen):
    def move_to_fvfm(self):
        self.manager.current = "fvfm"

class FvFmWidget(Screen):
    def __init__(self, **kwargs):
        super(FvFmWidget, self).__init__(**kwargs)
        self.ids.rv.data = [
            {'text': str(i), 'src': 'src/img/icon.png'} for i in range(20)
        ]


class ArrangeWidget(Screen):
    pass

class AnalysisWidget(Screen):
    pass

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
            Window.size = (1280, 720)
            Builder.load_file('src/layouts/pc.kv')
        self.set_widgets()
        print('build')
        return self.sm
    
    def set_widgets(self):
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(DetectWidget(name='detect'))
        self.sm.add_widget(FvFmWidget(name='fvfm'))
        self.sm.add_widget(ArrangeWidget(name='arrange'))
        self.sm.add_widget(AnalysisWidget(name='analysis'))
        
    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            return True
        else:
            return False

if __name__ == '__main__':
    PickcellApp().run()