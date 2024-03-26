import ctypes
import os
import threading
from os.path import expanduser

import cv2
import japanize_kivy
import numpy as np
from analyze.detect import Detect
from analyze.multi_graph import multi_graph
from custom_widgets.myboxlayout import MyBoxLayout
from kivy import platform
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel

currentActivity = None
CLS_Activity = None
CLS_Intent = None
ImagesMedia = None

REQUEST_GALLERY = 1
MediaStore_Images_Media_DATA = '_data'

default_threshold = 60
default_size2d = 5
default_size3d = 1

src_dir = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../'))

class PickcellApp(App):
    file_name = None
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
    res_leaf1_img = None
    res_leaf2_img = None
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
            Window.size = (1280, 850)
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
        self.default_thresh = default_threshold
        self.d = None
        self.input_path = None
        self.app = App.get_running_app()

    def run(self):
        if self.input_path is None:
            self.show_error_popup('Select leaf image.')
            return
        self.app.file_name = os.path.splitext(self.input_path)[0]
        #self.popup = self.show_progress_popup(self.cancel_process, 'Detect leaf', 'Running...')
        self.show_progress_popup(self.cancel_process, 'Detect leaf', 'Running...')
        
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

    def set_default(self, dt):
        self.ids.thresh_slider.value = default_threshold

    def update_texture(self, dt):
        texture = self.cv2_to_texture(self.app.leaf_img)
        self.app.leaf_texture = texture
        
class FvFmWidget(MyBoxLayout):
    def __init__(self, **kwargs):
        super(FvFmWidget, self).__init__(**kwargs)
        self.src_dir = src_dir
        self.default_thresh = default_threshold
        self.f = None
        self.d = None
        self.input_path = None
        self.app = App.get_running_app()
        self.setup_thread = threading.Thread(target=self.setup_analysis)
        self.setup_thread.start()

    def run(self):
        if self.input_path is None:
            self.show_error_popup('Select Fv/Fm result image.')
            return
        #self.popup = self.show_progress_popup(
        self.show_progress_popup(
            self.cancel_process,
            'Read Fv/Fm value',
            'Running...'
        )
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()

    def setup_analysis(self):
        from analyze.detect import Detect
        from analyze.fvfm import Fvfm
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

    def update_texture(self, dt):
        self.app.fvfm_texture = self.cv2_to_texture(self.app.fvfm_img)
        self.show_fvfm_list()

    def show_fvfm_list(self):
        for f in self.app.fvfm_list:
            color = f[0]
            img = np.full((36,36,3), color, np.uint8)
            texture = self.cv2_to_texture(img)
            self.ids.rv.data.append({
                'texture': texture,
                'text': str(f[1])
            })

    def set_default(self, dt):
        self.ids.thresh_slider.value = default_threshold

class AlignWidget(MyBoxLayout):
    res_leaf_texture = ObjectProperty(None)
    res_fvfm_texture = ObjectProperty(None)
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
        #self.popup = self.show_progress_popup(self.cancel_process, 'Align two images', 'Running...')
        self.show_progress_popup(self.cancel_process, 'Align two images', 'Running...')
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()
        
    def run_process(self):
        if self.a is None:
            from analyze.align import Align
            self.a = Align()
        try:
            self.app.res_leaf_img, self.app.res_fvfm_img, self.overlay_img = self.a.run(*self.args)
            Clock.schedule_once(self.update_texture, 0)
        except Exception as e:
            self.err_msg = str(e)
            Clock.schedule_once(self.thread_error, 0)
        self.popup.dismiss()

    def update_texture(self, dt):
        self.app.res_leaf_texture = self.cv2_to_texture(self.app.res_leaf_img)
        self.res_fvfm_texture = self.cv2_to_texture(self.app.res_fvfm_img)
        self.overlay_texture = self.cv2_to_texture(self.overlay_img)

class SplitColorWidget(MyBoxLayout):
    extr1_texture = ObjectProperty(None)
    extr2_texture = ObjectProperty(None)
    range1_texture = ObjectProperty(None)
    range2_texture = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(SplitColorWidget, self).__init__(**kwargs)
        self.src_dir = src_dir
        self.app = App.get_running_app()
        Clock.schedule_once(self.bind_func, 0)

    def bind_func(self, dt):
        self.ids.h1_slider.bind(
            value1=lambda slider, value: self.set_value1(value, 'h1l'),
            value2=lambda slider, value: self.set_value1(value, 'h1h')
        )
        self.ids.s1_slider.bind(
            value1=lambda slider, value: self.set_value1(value, 's1l'),
            value2=lambda slider, value: self.set_value1(value, 's1h')
        )
        self.ids.v1_slider.bind(
            value1=lambda slider, value: self.set_value1(value, 'v1l'),
            value2=lambda slider, value: self.set_value1(value, 'v1h')
        )
        self.ids.h2_slider.bind(
            value1=lambda slider, value: self.set_value2(value, 'h2l'),
            value2=lambda slider, value: self.set_value2(value, 'h2h')
        )
        self.ids.s2_slider.bind(
            value1=lambda slider, value: self.set_value2(value, 's2l'),
            value2=lambda slider, value: self.set_value2(value, 's2h')
        )
        self.ids.v2_slider.bind(
            value1=lambda slider, value: self.set_value2(value, 'v2l'),
            value2=lambda slider, value: self.set_value2(value, 'v2h')
        )
        Window.bind(
            on_resize=lambda window, size, size2: Clock.schedule_once(self.resize_widgets, 0)
        )

    def set_value1(self, value, val_type):
        if val_type == 'h1l':
            self.h1l = int(value)
        elif val_type == 'h1h':
            self.h1h = int(value)
        elif val_type == 's1l':
            self.s1l = int(value)
        elif val_type == 's1h':
            self.s1h = int(value)
        elif val_type == 'v1l':
            self.v1l = int(value)
        elif val_type == 'v1h':
            self.v1h = int(value)
        self.update_texture(
            self.h1l, self.h1h,
            self.s1l, self.s1h,
            self.v1l, self.v1h,
            self.ids.range1_img
        )
        
    def set_value2(self, value, val_type):
        if val_type == 'h2l':
            self.h2l = int(value)
        elif val_type == 'h2h':
            self.h2h = int(value)
        elif val_type == 's2l':
            self.s2l = int(value)
        elif val_type == 's2h':
            self.s2h = int(value)
        elif val_type == 'v2l':
            self.v2l = int(value)
        elif val_type == 'vh':
            self.v2h = int(value)
        self.update_texture(
            self.h2l, self.h2h,
            self.s2l, self.s2h,
            self.v2l, self.v2h,
            self.ids.range2_img
        )
        
    def update_texture(self, hl, hh, sl, sh, vl,vh, range_img):
        height = int(range_img.height)
        width = int(range_img.width)
        if width == 0:
            width = 1
        hue = np.linspace(hl, hh, width)
        saturation = np.linspace(sl, sh, height)
        value = np.linspace(vl, vh, height)
        img_hsv = np.array([[h,s,v] for (s, v) in zip(saturation, value) for h in hue], np.uint8).reshape(height, width, 3)
        img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        texture = self.cv2_to_texture(img)
        range_img.texture = texture

    def set_default(self, dt):
        self.h1l = 30
        self.h1h = 60
        self.s1l = 0
        self.s1h = 255
        self.v1l = 0
        self.v1h = 255
        self.ids.h1_slider.value = (self.h1l, self.h1h)
        self.ids.s1_slider.value = (self.s1l, self.s1h)
        self.ids.v1_slider.value = (self.v1l, self.v1h)
        self.h2l = 60
        self.h2h = 90
        self.s2l = 0
        self.s2h = 255
        self.v2l = 0
        self.v2h = 255
        self.ids.h2_slider.value = (self.h2l, self.h2h)
        self.ids.s2_slider.value = (self.s2l, self.s2h)
        self.ids.v2_slider.value = (self.v2l, self.v2h)

    def resize_widgets(self, dt):
        self.update_texture(
            self.h1l, self.h1h,
            self.s1l, self.s1h,
            self.v1l, self.v1h,
            self.ids.range1_img
        )
        self.update_texture(
            self.h2l, self.h2h,
            self.s2l, self.s2h,
            self.v2l, self.v2h,
            self.ids.range2_img
        )
        
    def extr_color1(self):
        img = self.app.res_leaf_img
        if img is None:
            self.show_error_popup('Run previous steps before color extraction.')
            return
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        low = (self.h1l, self.s1l, self.v1l)
        high = (self.h1h, self.s1h, self.v1h)
        mask = cv2.inRange(img_hsv, low, high)
        self.app.res_leaf1_img = cv2.bitwise_and(img, img, mask=mask)
        texture = self.cv2_to_texture(self.app.res_leaf1_img)
        self.extr1_texture = texture

    def extr_color2(self):
        img = self.app.res_leaf_img
        if img is None:
            self.show_error_popup('Run previous steps before color extraction.')
            return
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        low = (self.h2l, self.s2l, self.v2l)
        high = (self.h2h, self.s2h, self.v2h)
        mask = cv2.inRange(img_hsv, low, high)
        self.app.res_leaf2_img = cv2.bitwise_and(img, img, mask=mask)
        texture = self.cv2_to_texture(self.app.res_leaf2_img)
        self.extr2_texture = texture

class AnalyzeWidget(MyBoxLayout):
    def __init__(self, **kwargs):
        super(AnalyzeWidget, self).__init__(**kwargs)
        self.p = None
        self.g = None
        self.fig_color3d = None
        self.fig_fvfm3d = None
        self.fig_scat2d = None
        self.fig_all = None
        self.fig_color3d_leaf1 = None
        self.fig_fvfm3d_leaf1 = None
        self.fig_scat2d_leaf1 = None
        self.fig_color1 = None
        self.fig_color3d_leaf2 = None
        self.fig_fvfm3d_leaf2 = None
        self.fig_scat2d_leaf2 = None
        self.fig_color2 = None
        self.app = App.get_running_app()

    def set_default(self, dt):
        self.ids.size_2d.value = default_size2d
        self.ids.size_3d.value = default_size3d
        return super().set_default(dt)

    def run(self):
        if (self.app.res_leaf_img is None) or (self.app.res_fvfm_img is None):
            self.show_error_popup('There is no input. Do previous steps.')
            return
        #self.popup = self.show_progress_popup(self.cancel_process, 'Running', 'Pick up leaf color and its Fv/Fm value.')
        self.show_progress_popup(self.cancel_process, 'Running', 'Pick up leaf color and its Fv/Fm value.')
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()
        
    def run_process(self):
        if self.p is None:
            from analyze.pickcell import Pickcell
            self.p = Pickcell()
        if self.g is None:
            from analyze.create_graph import Graph
            self.g = Graph()
        leaf_img = self.app.res_leaf_img
        fvfm_img = self.app.res_fvfm_img
        fvfm_list = self.app.fvfm_list
        leaf1_img = self.app.res_leaf1_img
        leaf2_img = self.app.res_leaf2_img
        try:
            self.res_px, self.res_fvfm = self.p.run(leaf_img, fvfm_img, fvfm_list)
            self.fig_color3d, self.fig_fvfm3d, self.fig_scat2d = self.g.draw(self.res_px, self.res_fvfm)
            self.fig_all = multi_graph(self.fig_color3d, self.fig_fvfm3d, self.fig_scat2d)
            self.ids.show_res_btn.disabled = False
            if leaf1_img is not None:
                self.res_leaf1_px, self.res_leaf1_fvfm = self.p.run(leaf1_img, fvfm_img, fvfm_list)
                self.fig_color3d_leaf1, self.fig_fvfm3d_leaf1, self.fig_scat2d_leaf1 = self.g.draw(self.res_leaf1_px, self.res_leaf1_fvfm)
                self.fig_color1 = multi_graph(self.fig_color3d_leaf1, self.fig_fvfm3d_leaf1, self.fig_scat2d_leaf1)
                self.ids.show_res1_btn.disabled = False
            if leaf2_img is not None:
                self.res_leaf2_px, self.res_leaf2_fvfm = self.p.run(leaf2_img, fvfm_img, fvfm_list)
                self.fig_color3d_leaf2, self.fig_fvfm3d_leaf2, self.fig_scat2d_leaf2 = self.g.draw(self.res_leaf2_px, self.res_leaf2_fvfm)
                self.fig_color2 = multi_graph(self.fig_color3d_leaf2, self.fig_fvfm3d_leaf2, self.fig_scat2d_leaf2)
                self.ids.show_res2_btn.disabled = False
        except (ValueError, TypeError) as e:
            self.err_msg = str(e)
            Clock.schedule_once(self.thread_error, 0)
        else:
            self.ids.save_btn.disabled = False
        self.popup.dismiss()

    def show_fig(self):
        #self.popup = self.show_progress_popup(self.cancel_process, 'Show Figure', 'Drawing...')
        self.show_progress_popup(self.cancel_process, 'Show Figure', 'Drawing...')
        self.thread = WorkingThread(target=self.show_fig_process, args=('all',))
        self.thread.start()

    def show_fig_color1(self):
        #self.popup = self.show_progress_popup(self.cancel_process, 'Show Figure', 'Drawing...')
        self.show_progress_popup(self.cancel_process, 'Show Figure', 'Drawing...')
        self.thread = WorkingThread(target=self.show_fig_process, args=('color1',))
        self.thread.start()

    def show_fig_color2(self):
        #self.popup = self.show_progress_popup(self.cancel_process, 'Show Figure', 'Drawing...')
        self.show_progress_popup(self.cancel_process, 'Show Figure', 'Drawing...')
        self.thread = WorkingThread(target=self.show_fig_process, args=('color2',))
        self.thread.start()

    def show_fig_process(self, group):
        if group == 'all':
            self.fig_all.show()
        elif group == 'color1':
            self.fig_color1.show()
        elif group == 'color2':
            self.fig_color2.show()
        self.popup.dismiss()

    def test(self, id):
        print(type(id))
        print(id.id)

    def set_size(self):
        pass

    def save(self):
        #self.popup = self.show_progress_popup(self.cancel_process, 'Save results', 'Running...')
        self.show_progress_popup(self.cancel_process, 'Save results', 'Running...')
        self.thread = WorkingThread(target=self.save_process)
        self.thread.start()

    def save_process(self):
        name = self.app.file_name
        res_root_dir = name + '_PickCells'
        os.makedirs(res_root_dir, exist_ok=True)
        def make_res_dir(dir_name):
            if os.path.exists(dir_name):
                i = 1
                while True:
                    new_name = '{}_{}'.format(dir_name, i)
                    if os.path.exists(new_name):
                        i += 1
                    else:
                        os.makedirs(new_name)
                        return new_name
            else:
                os.makedirs(dir_name)
                return dir_name
        if (self.fig_color3d is not None) and (self.fig_fvfm3d is not None) and (self.fig_scat2d is not None):
            dir_name = os.path.join(res_root_dir, 'All')
            res_dir = make_res_dir(dir_name)
            self.fig_color3d.write_html(os.path.join(res_dir, 'color3d.html'))
            self.fig_fvfm3d.write_html(os.path.join(res_dir, 'fvfm3d.html'))
            self.fig_scat2d.write_html(os.path.join(res_dir, 'scatter2d.html'))
            self.fig_all.write_html(os.path.join(res_dir, 'all.html'))
        if (self.fig_color3d_leaf1 is not None) and (self.fig_fvfm3d_leaf1 is not None) and (self.fig_scat2d_leaf1 is not None):
            dir_name = os.path.join(res_root_dir, 'Color1')
            res_dir = make_res_dir(dir_name)
            self.fig_color3d_leaf1.write_html(os.path.join(res_dir, 'color1_color3d.html'))
            self.fig_fvfm3d_leaf1.write_html(os.path.join(res_dir, 'color1_fvfm3d.html'))
            self.fig_scat2d_leaf1.write_html(os.path.join(res_dir, 'color1_scatter2d.html'))
            self.fig_color1.write_html(os.path.join(res_dir, 'color1_all.html'))
        if (self.fig_color3d_leaf2 is not None) and (self.fig_fvfm3d_leaf2 is not None) and (self.fig_scat2d_leaf2 is not None):
            dir_name = os.path.join(res_root_dir, 'Color2')
            res_dir = make_res_dir(dir_name)
            self.fig_color3d_leaf2.write_html(os.path.join(res_dir, 'color2_color3d.html'))
            self.fig_fvfm3d_leaf2.write_html(os.path.join(res_dir, 'color2_fvfm3d.html'))
            self.fig_scat2d_leaf2.write_html(os.path.join(res_dir, 'color2_scatter2dd.html'))
            self.fig_color2.write_html(os.path.join(res_dir, 'color2_all.html'))
        self.popup.dismiss()
        Clock.schedule_once(lambda x: self.show_error_popup('Finished.', 'Save'))
                
class Root(TabbedPanel):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        self.density = Window._density

    def switch_to(self, header, do_scroll=False):
        width = Window.width
        height = Window.height
        Window.size = ((width+1)/self.density, height/self.density)
        Window.size = (width/self.density, height/self.density)
        return super().switch_to(header, do_scroll)

if __name__ == '__main__':
    PickcellApp().run()
