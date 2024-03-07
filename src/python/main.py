import os
from os.path import expanduser

from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel

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

class FileDialogPopup(Popup):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

class ErrorPopup(Popup):
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
        self.input_path = None

    def run(self):
        if self.input_path is None:
            self.err_pop('Select leaf image.')
            return
        
        if self.d is None:
            from detect import Detect
            self.d = Detect()
        thr = self.ids.thresh_slider.value
        print(thr)
        self.d.set_param(bin_thr=thr)
        try:
            self.output_img, self.main_obj = self.d.extr_leaf(self.input_path)
            out_texture = self.cv2_to_texture(self.output_img)
            self.ids.output_img.texture = out_texture
        except Exception as e:
            self.err_pop(e)
            print(e)

    def input_img(self, file):
        if file != []:
            self.ids.input_img.source = file[0]
            self.input_path = file[0]

    def cv2_to_texture(self, cv2_img):
        texture = Texture.create(size=(cv2_img.shape[1], cv2_img.shape[0]), colorfmt='bgr', bufferfmt='ubyte')
        texture.blit_buffer(cv2_img.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture
    
    def cancel(self):
        pass

    def err_pop(self, msg):
        popup = ErrorPopup()
        popup.ids.err_msg = msg
        popup.open()

class FvFmWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(FvFmWidget, self).__init__(**kwargs)

class ArrangeWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(ArrangeWidget, self).__init__(**kwargs)

class SplitColorWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(SplitColorWidget, self).__init__(**kwargs)

class Root(TabbedPanel):
    pass

if __name__ == '__main__':
    PickcellApp().run()