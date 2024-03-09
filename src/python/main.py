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
        self.thread = None

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

    def cancel_process(self):
        self.thread.raise_exception()
    
class PickcellApp(App):
    leaf_img = None
    fvfm_img = None
    leaf_texture = ObjectProperty(None)
    fvfm_texture = ObjectProperty(None)
    leaf_obj = None
    fvfm_obj = None
    fvfm_list = None
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
        Clock.schedule_once(self.set_default, 0)
        self.app = App.get_running_app()

    def run(self):
        if self.input_path is None:
            self.show_error_popup('Select leaf image.')
            return
        self.popup = self.show_progress_popup(self.cancel_process, 'Detect leaf', 'Running...')
        
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()

    def run_process(self):
        if self.d is None:
            self.d = Detect()
        thr = self.ids.thresh_slider.value
        self.d.set_param(bin_thr=thr)
        try:
            self.app.leaf_img, self.app.leaf_obj = self.d.extr_leaf(self.input_path)
            Clock.schedule_once(self.update_texture, 0)
        except (ValueError, TypeError) as e:
            self.err_msg = str(e)
            Clock.schedule_once(self.thread_error, 0)
        self.popup.dismiss()

    def thread_error(self, dt):
        self.show_error_popup(self.err_msg)
        self.err_msg = None

    def set_default(self, dt):
        self.ids.thresh_slider.value = default_threshold

    def update_texture(self, dt):
        texture = self.cv2_to_texture(self.app.leaf_img)
        self.app.leaf_texture = texture
        
class FvFmWidget(MyBoxLayout):
    def __init__(self, **kwargs):
        super(FvFmWidget, self).__init__(**kwargs)
        self.src_dir = src_dir
        self.f = None
        self.d = None
        self.input_path = None
        self.app = App.get_running_app()
        self.setup_thread = threading.Thread(target=self.setup_analysis)
        self.setup_thread.start()
        Clock.schedule_once(self.set_default, 0)

    def run(self):
        if self.input_path is None:
            self.show_error_popup('Select Fv/Fm result image.')
            return
        self.popup = self.show_progress_popup(
            self.cancel_process,
            'Read Fv/Fm value',
            'Running...'
        )
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()

    def setup_analysis(self):
        from detect import Detect
        from fvfm import Fvfm
        self.d = Detect()
        self.f = Fvfm()

    def run_process(self):
        self.setup_thread.join()
        thr = self.ids.thresh_slider.value
        self.d.set_param(bin_thr=thr)
        try:
            self.app.fvfm_img, self.app.fvfm_obj = self.d.extr_leaf(self.input_path)
            self.app.fvfm_list = self.f.get(self.input_path)
            Clock.schedule_once(self.update_texture, 0)
        except Exception as e:
            self.err_msg = str(e)
            Clock.schedule_once(self.thread_error, 0)
        self.popup.dismiss()

    def thread_error(self, dt):
        self.show_error_popup(self.err_msg)
        self.err_msg = None

    def update_texture(self, dt):
        self.app.fvfm_texture = self.cv2_to_texture(self.app.fvfm_img)
        self.show_fvfm_list()

    def set_default(self, dt):
        self.ids.thresh_slider.value = default_threshold

    def show_fvfm_list(self):
        for f in self.app.fvfm_list:
            color = f[0]
            img = np.full((36,36,3), color, np.uint8)
            texture = self.cv2_to_texture(img)
            self.ids.rv.data.append({
                'texture': texture,
                'text': str(f[1])
            })

class AlignWidget(MyBoxLayout):
    overlay_texture = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(AlignWidget, self).__init__(**kwargs)
        self.src_dir = src_dir
        self.a = None
        self.app = App.get_running_app()

    def run(self):
        leaf_img = self.app.leaf_img
        fvfm_img = self.app.fvfm_img
        leaf_obj = self.app.leaf_obj
        fvfm_obj = self.app.fvfm_obj
        self.args = [leaf_img, fvfm_img, leaf_obj, fvfm_obj]
        if (leaf_img is None) or (leaf_obj is None):
            if (fvfm_img is None) or (fvfm_obj is None):
                self.show_error_popup('There is no input.\nPlease run "Detect" and "Fv/Fm" before align.')
                return
            else:
                self.show_error_popup('There is no "Leaf".\nPlease run "Detect" before align.')
                return
        elif (fvfm_img is None) or (fvfm_obj is None):
            self.show_error_popup('There is no "Fv/Fm".\nPlease run "Fv/Fm" before align.')
            return
        self.popup = self.show_progress_popup(self.cancel_process, 'Align two images', 'Running...')
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()
        
    
    def run_process(self):
        if self.a is None:
            from align import Align
            self.a = Align()
        try:
            self.app.res_leaf_img, self.app.res_fvfm_img, self.overlay_img = self.a.run(*self.args)
        except:
            pass

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