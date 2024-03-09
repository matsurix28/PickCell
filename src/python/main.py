import ctypes
import os
import threading
from os.path import expanduser

import numpy as np
from detect import Detect
from kivy import platform
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
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

default_threshold = 60

class FileDialogPopup(Popup):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

class ErrorPopup(Popup):
    title_text = StringProperty('Error')
    message = StringProperty('')

class ProgressPopup(Popup):
    title_text = StringProperty('')
    message = StringProperty('')
    def __init__(self, cancel_func, **kwargs):
        super(ProgressPopup, self).__init__(**kwargs)
        self.cancel = cancel_func

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.src_dir = src_dir
        self.input_path = None

    def input_img(self, file):
        if file != []:
            self.ids.input_img.source = file[0]
            self.input_path = file[0]

    def cv2_to_texture(self, cv2_img):
        texture = Texture.create(size=(cv2_img.shape[1], cv2_img.shape[0]), colorfmt='bgr', bufferfmt='ubyte')
        texture.blit_buffer(cv2_img.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture
    
    def show_progress_popup(self,cancel_func, title, message):
        popup = ProgressPopup(cancel_func, title_text=title, message=message)
        popup.open()
        return popup

    def show_error_popup(self, message, title='Error'):
        popup = ErrorPopup(message=message, title_text=title)
        popup.open()
    
class PickcellApp(App):
    leaf_img = None
    fvfm_img = None
    leaf_texture = ObjectProperty(None)
    fvfm_texture = ObjectProperty(None)
    leaf_obj = None
    fvfm_obj = None
    res_leaf_img = None
    res_fvfm_img = None
    res_leaf_texture = ObjectProperty(None)
    res_fvfm_texture = ObjectProperty(None)
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

class WorkingThread(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        resu = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
        if resu > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), 0)
            

class DetectWidget(MyBoxLayout):
    def __init__(self, **kwargs):
        super(DetectWidget, self).__init__(**kwargs)
        self.src_dir = src_dir
        self.d = None
        self.input_path = None
        Clock.schedule_once(self.set_default, 1.2)
        self.app = App.get_running_app()

    def run(self):
        if self.input_path is None:
            self.show_error_popup('Select leaf image.')
            return
        self.popup = self.show_progress_popup(self.cancel, 'Detect leaf', 'Running...')
        if self.d is None:
            self.d = Detect()
        thr = self.ids.thresh_slider.value
        self.d.set_param(bin_thr=thr)
        self.thread = WorkingThread(target=self.detect)
        self.thread.start()

    def detect(self):
        try:
            output_img, main_obj = self.d.extr_leaf(self.input_path)
            self.app.leaf_img = output_img
            self.app.leaf_obj = main_obj
            Clock.schedule_once(self.update_texture, 0)
        except (ValueError, TypeError) as e:
            #self.show_error_popup(str(e))
            self.err = str(e)
            Clock.schedule_once(self.thread_err, 0)
            print(e)
        self.popup.dismiss()

    def thread_err(self, dt):
        self.show_error_popup(self.err)
        self.err = None

    def set_default(self, dt):
        self.ids.thresh_slider.value = default_threshold
    
    def cancel(self):
        self.thread.raise_exception()

    def update_texture(self, dt):
        texture = self.cv2_to_texture(self.app.leaf_img)
        self.app.leaf_texture = texture
        
class FvFmWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(FvFmWidget, self).__init__(**kwargs)
        self.src_dir = src_dir
        self.f = None
        self.d = None
        self.input_path = None

    def run(self):
        app = App.get_running_app()
        if self.input_path is None:
            self.err_pop('Select Fv/Fm result image.')
            return
        if self.f is None:
            from fvfm import Fvfm
            self.f = Fvfm()
        if self.d is None:
            from detect import Detect
            self.d = Detect()
        thr = self.ids.thresh_slider.value
        self.d.set_param(bin_thr=thr)
        try:
            output_img, main_obj = self.d.extr_leaf(self.input_path)
            out_texture = self.cv2_to_texture(output_img)
            #self.ids.output_img.texture = out_texture
            self.fvfm_list = self.f.get(self.input_path)
            self.show_fvfm_list(self.fvfm_list)
            app.fvfm_texture = out_texture
            app.fvfm_img = output_img
            app.fvfm_obj = main_obj
        except Exception as e:
            self.err_pop(e)

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
        popup.ids.err_msg.text = msg
        popup.open()

    def show_fvfm_list(self, fvfm_list=None):
        for f in fvfm_list:
            color = f[0]
            img = np.full((36,36,3), color, np.uint8)
            texture = self.cv2_to_texture(img)
            self.ids.rv.data.append({
                'texture': texture,
                'text': str(f[1])
            })

class ArrangeWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(ArrangeWidget, self).__init__(**kwargs)
        self.src_dir = src_dir
        self.a = None

    def run(self):
        app = App.get_running_app()
        leaf_img = app.leaf_img
        fvfm_img = app.fvfm_img
        leaf_obj = app.leaf_obj
        fvfm_obj = app.fvfm_obj
        args = [leaf_img, fvfm_img, leaf_obj, fvfm_obj]
        #if None in args:
        #    self.err_pop('There is no input.')
        #    return
        if self.a is None:
            from arrange import Arrange
            self.a = Arrange()
        try:
            arranged_leaf_img, arranged_fvfm_img = self.a.run(*args)
            leaf_texture = self.cv2_to_texture(arranged_leaf_img)
            fvfm_texture = self.cv2_to_texture(arranged_fvfm_img)
            app.res_leaf_texture = leaf_texture
            app.res_fvfm_texture = fvfm_texture
        except:
            pass

    def cv2_to_texture(self, cv2_img):
        texture = Texture.create(size=(cv2_img.shape[1], cv2_img.shape[0]), colorfmt='bgr', bufferfmt='ubyte')
        texture.blit_buffer(cv2_img.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture
    
    def err_pop(self, msg):
        popup = ErrorPopup()
        popup.ids.err_msg.text = msg
        popup.open()

class SplitColorWidget(BoxLayout):
    color1_texture = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(SplitColorWidget, self).__init__(**kwargs)

    def analyze(self):
        pass

class Root(TabbedPanel):
    pass


if __name__ == '__main__':
    PickcellApp().run()