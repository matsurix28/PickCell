import collections
import csv
import ctypes
import glob
import os
import re
import threading
from os.path import expanduser

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

import cv2
#import japanize_kivy
import numpy as np
from kivy import platform
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelContent

from src.python.analyze.multi_graph import multi_graph
from src.python.custom_widgets.myboxlayout import MyBoxLayout

currentActivity = None
CLS_Activity = None
CLS_Intent = None
ImagesMedia = None

REQUEST_GALLERY = 1
MediaStore_Images_Media_DATA = '_data'

default_threshold = 60
default_color1 = [[0, 0, 0], [30, 255, 255]]
default_color2 = [[30, 0, 0], [60, 255, 255]]
default_size2d = 5
default_size3d = 1

src_dir = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'src'
    )
)

home_dir = os.path.expanduser('~')

resource_add_path(os.path.join(src_dir, 'fonts'))
LabelBase.register(DEFAULT_FONT, 'Mplus1-Regular.ttf')

class PickcellApp(App):
    leaf_texture = ObjectProperty(None)
    fvfm_texture = ObjectProperty(None)
    res_leaf_texture = ObjectProperty(None)
    res_fvfm_texture = ObjectProperty(None)
    file_name = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_var()
        self.setup_fvfm_thread = threading.Thread(target=self.setup_fvfm)
        self.setup_fvfm_thread.start()

    def set_var(self):
        self.leaf_img = None
        self.fvfm_img = None
        self.leaf_obj = None
        self.fvfm_obj = None
        self.fvfm_list = None
        self.res_leaf_img = None
        self.res_fvfm_img = None
        self.overlay_img = None
        self.res_leaf1_img = None
        self.res_leaf2_img = None
        self.leaf_detect = None
        self.fvfm_detect = None
        self.fvfm = None
        self.align = None
        self.pickcell = None
        self.graph = None
        self.low1 = None
        self.high1 = None
        self.low2 = None
        self.high2 = None
        self.leaf_thr = default_threshold
        self.fvfm_thr = default_threshold
        self.color1 = default_color1
        self.color2 = default_color2
        self.size_2d = default_size2d
        self.size_3d = default_size3d

    def setup_fvfm(self):
        from src.python.analyze.fvfm import Fvfm
        self.fvfm = Fvfm()

    def run_detect(self, path, thr=None):
        if self.leaf_detect is None:
            from src.python.analyze.detect import Detect
            self.leaf_detect = Detect()
        if thr is not None:
            self.leaf_detect.set_param(bin_thr=thr)
        self.leaf_img, self.leaf_obj = self.leaf_detect.extr_leaf(path)

    def run_fvfm(self, path, thr=None):
        if self.fvfm_detect is None:
            from src.python.analyze.detect import Detect
            self.fvfm_detect = Detect()
        if thr is not None:
            self.fvfm_detect.set_param(bin_thr=thr)
        self.fvfm_img, self.fvfm_obj = self.fvfm_detect.extr_leaf(path)
        self.setup_fvfm_thread.join()
        self.fvfm_list = self.fvfm.get(path)

    def run_align(self, args):
        print('analyze')
        if self.align is None:
            print('import align')
            from src.python.analyze.align import Align
            print('import kanryo')
            self.align = Align()
        self.res_leaf_img, self.res_fvfm_img, self.overlay_img = self.align.run(*args)
        
    def extr_color(self, low, high):
        img = self.res_leaf_img
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, low, high)
        extr_img = cv2.bitwise_and(img, img, mask=mask)
        return extr_img
    
    def run_extr_color1(self, low, high):
        self.low1 = low
        self.high1 = high
        self.res_leaf1_img = self.extr_color(low, high)

    def run_extr_color2(self, low, high):
        self.low2 = low
        self.high2 = high
        self.res_leaf2_img = self.extr_color(low, high)

    def run_split_color(self):
        if (self.low1 is not None) and (self.high1 is not None):
            self.res_leaf1_img = self.extr_color(self.low1, self.high1)
        if (self.low2 is not None) and (self.high2 is not None):
            self.res_leaf2_img = self.extr_color(self.low2, self.high2)

    def run_pickcell(self, leaf_img, fvfm_img, fvfm_list):
        if self.pickcell is None:
            from src.python.analyze.pickcell import Pickcell
            self.pickcell = Pickcell()
        if self.graph is None:
            from src.python.analyze.create_graph import Graph
            self.graph = Graph()
        res_px, res_fvfm = self.pickcell.run(leaf_img, fvfm_img, fvfm_list)
        fig_color3d, fig_fvfm3d, fig_scat2d = self.graph.draw(res_px, res_fvfm)
        fig_all = multi_graph(fig_color3d, fig_fvfm3d, fig_scat2d)
        return fig_color3d, fig_fvfm3d, fig_scat2d, fig_all

    def update_marker_size(self, figures, size_2d, size_3d):
        figures[0]['data'][0]['marker']['size'] = size_3d
        figures[1]['data'][0]['marker']['size'] = size_3d
        figures[2]['data'][0]['marker']['size'] = size_2d
        figures[3]['data'][0]['marker']['size'] = size_2d
        figures[3]['data'][1]['marker']['size'] = size_3d
        figures[3]['data'][2]['marker']['size'] = size_3d
        return figures

    def set_marker_size(self, size_2d, size_3d):
        if self.graph is None:
            from src.python.analyze.create_graph import Graph
            self.graph = Graph()
        self.size_2d = size_2d
        self.size_3d = size_3d
        self.graph.set_val(size_2d=size_2d, size_3d=size_3d)

    def set_params(self,
                 leaf_thr, fvfm_thr,
                 is_extr1, is_extr2,
                 color1, color2,
                 size2d, size3d,
                 outdir):
        self.leaf_thr = leaf_thr
        self.fvfm_thr = fvfm_thr
        self.is_extr1 = is_extr1
        self.is_extr2 = is_extr2
        self.color1 = color1
        self.color2 = color2
        self.size_2d = size2d
        self.size_3d = size3d
        self.outdir = outdir

    def run_auto_test(self, name, leaf, fvfm):
        import time
        time.sleep(5)

    def run_auto(self,name, leaf_input, fvfm_input):
        self.clear()
        self.file_name = name
        try:
            self.run_detect(leaf_input, self.leaf_thr)
            self.run_fvfm(fvfm_input, self.fvfm_thr)
            self.run_align([self.leaf_img, self.fvfm_img, self.leaf_obj, self.fvfm_obj])
            if self.is_extr1:
                self.run_extr_color1(self.color1[0], self.color1[1])
            if self.is_extr2:
                self.run_extr_color2(self.color2[0], self.color2[1])
        except Exception as e:
            self.save_imgs(self.outdir)
            raise
        self.save_imgs(self.outdir)
        self.set_marker_size(self.size_2d, self.size_3d)
        fig = self.run_pickcell(self.res_leaf_img, self.res_fvfm_img, self.fvfm_list)
        self.save_figs(self.outdir, 'All_color', fig)
        if self.res_leaf1_img is not None:
            fig1 = self.run_pickcell(self.res_leaf1_img, self.res_fvfm_img, self.fvfm_list)
            self.save_figs(self.outdir, 'Color1', fig1)
        if self.res_leaf2_img is not None:
            fig2 = self.run_pickcell(self.res_leaf2_img, self.res_fvfm_img, self.fvfm_list)
            self.save_figs(self.outdir, 'Color2', fig2)
        print('run auto owari')
        
    def save(self, fig, outdir, name):
        self.save_imgs(outdir)
        self.save_figs(outdir, name, fig)
        
    def save_figs(self, outdir, name, figures):
        def make_res_dir(dir):
            if os.path.exists(dir):
                i = 1
                while True:
                    new_name = '{}_{}'.format(dir, i)
                    if os.path.exists(new_name):
                        i += 1
                    else:
                        os.makedirs(new_name)
                        return new_name
            else:
                os.makedirs(dir)
                return dir
        print('app args', outdir, self.file_name, name)
        res_dir = os.path.join(outdir, self.file_name, name)
        res_dir = make_res_dir(res_dir)
        print('hozon basho', res_dir)
        fig_types = ['color3d', 'fvfm3d', 'scatter2d', 'all']
        for i, fig in enumerate(figures):
            print(f'{res_dir}: {fig_types[i]}')
            fig.write_html(os.path.join(res_dir, fig_types[i] + '.html'))

    def save_imgs(self, outdir):
        os.makedirs(os.path.join(outdir, self.file_name), exist_ok=True)
        if self.res_leaf_img is not None:
            cv2.imwrite(os.path.join(outdir, self.file_name, self.file_name + '_leaf.png'), self.res_leaf_img)
        if self.res_fvfm_img is not None:
            cv2.imwrite(os.path.join(outdir, self.file_name, self.file_name + '_fvfm.png'), self.res_fvfm_img)
        if self.res_leaf1_img is not None:
            cv2.imwrite(os.path.join(outdir, self.file_name, self.file_name + '_color1.png'), self.res_leaf1_img)
        if self.res_leaf2_img is not None:
            cv2.imwrite(os.path.join(outdir, self.file_name, self.file_name + '_color2.png'), self.res_leaf2_img)

    def set_val(self):
        try:
            auto = self.root.children[0].children[0]
        except:
            return
        if isinstance(auto, AutoWidget):
            auto.set_val(self.leaf_thr, self.fvfm_thr, self.color1, self.color2, self.size_2d, self.size_3d)

    def set_leaf_thr(self, thr):
        if self.leaf_detect is None:
            from src.python.analyze.detect import Detect
            self.leaf_detect = Detect()
        self.leaf_thr = thr
        self.leaf_detect.set_param(bin_thr=thr)

    def set_fvfm_thr(self, thr):
        if self.fvfm_detect is None:
            from src.python.analyze.detect import Detect
            self.fvfm_detect = Detect()
        self.fvfm_thr = thr
        self.fvfm_detect.set_param(bin_thr=thr)

    def set_color1(self, hl, sl, vl, hh, sh, vh):
        self.color1 = [[hl, sl, vl], [hh, sh, vh]]

    def set_color2(self, hl, sl, vl, hh, sh, vh):
        self.color2 = [[hl, sl, vl], [hh, sh, vh]]
        
    def clear(self):
        self.file_name = ''
        self.leaf_img = None
        self.fvfm_img = None
        self.leaf_obj = None
        self.fvfm_obj = None
        self.fvfm_list = None
        self.res_leaf_img = None
        self.res_fvfm_img = None
        self.overlay_img = None
        self.res_leaf1_img = None
        self.res_leaf2_img = None

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
            Window.size = (1280, 900)
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
        self.input_path = None
        self.app = App.get_running_app()
        self.d = self.app
        Clock.schedule_once(self.bind_func, 0)

    def bind_func(self, dt):
        self.ids.thresh_slider.bind(value=self.set_thr)

    def set_thr(self, *args):
        self.app.set_leaf_thr(self.ids.thresh_slider.value)

    def run(self):
        if self.input_path is None:
            self.show_error_popup('Select leaf image.')
            return
        name = os.path.splitext(os.path.basename(self.input_path))[0]
        if re.fullmatch('.*-(L|F)$', name):
            name = re.sub('-(L|F)$', '', name)
        self.app.file_name = name
        self.show_progress_popup(self.cancel_process, 'Detect leaf', 'Running...')
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()

    def run_process(self):
        thr = self.ids.thresh_slider.value
        try:
            self.app.run_detect(self.input_path, thr=thr)
            Clock.schedule_once(self.update_texture, 0)
        except (ValueError, TypeError) as e:
            self.err_msg = str(e)
            Clock.schedule_once(self.thread_error, 0)
        self.popup.dismiss()    

    def update_texture(self, dt):
        texture = self.cv2_to_texture(self.app.leaf_img)
        self.app.leaf_texture = texture

    def set_default(self, dt):
        self.ids.thresh_slider.value = default_threshold
        
class FvFmWidget(MyBoxLayout):
    def __init__(self, **kwargs):
        super(FvFmWidget, self).__init__(**kwargs)
        self.src_dir = src_dir
        self.default_thresh = default_threshold
        self.f = None
        self.d = None
        self.input_path = None
        self.app = App.get_running_app()
        Clock.schedule_once(self.bind_func, 0)

    def bind_func(self, dt):
        self.ids.thresh_slider.bind(value=self.set_thr)

    def set_thr(self, *args):
        self.app.set_fvfm_thr(self.ids.thresh_slider.value)

    def run(self):
        if self.input_path is None:
            self.show_error_popup('Select Fv/Fm result image.')
            return
        self.show_progress_popup(
            self.cancel_process,
            'Read Fv/Fm value',
            'Running...'
        )
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()

    def run_process(self):
        thr = self.ids.thresh_slider.value
        try:
            self.app.run_fvfm(self.input_path, thr=thr)
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
        self.app = App.get_running_app()

    def run(self):
        leaf_img = self.app.leaf_img
        fvfm_img = self.app.fvfm_img
        leaf_obj = self.app.leaf_obj
        fvfm_obj = self.app.fvfm_obj
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
        self.args = [leaf_img, fvfm_img, leaf_obj, fvfm_obj]
        self.show_progress_popup(self.cancel_process, 'Align two images', 'Running...')
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()
        
    def run_process(self):
        try:
            self.app.run_align(self.args)
            Clock.schedule_once(self.update_texture, 0)
        except Exception as e:
            self.popup.dismiss()
            self.err_msg = str(e)
            Clock.schedule_once(self.thread_error, 0)
        self.popup.dismiss()

    def update_texture(self, dt):
        self.app.res_leaf_texture = self.cv2_to_texture(self.app.res_leaf_img)
        self.res_fvfm_texture = self.cv2_to_texture(self.app.res_fvfm_img)
        self.overlay_texture = self.cv2_to_texture(self.app.overlay_img)

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
        self.app.set_color1(self.h1l, self.s1l, self.v1l, self.h1h, self.s1h, self.v1h)
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
        self.app.set_color2(self.h2l, self.s2l, self.v2l, self.h2h, self.s2h, self.v2h)
        self.update_texture(
            self.h2l, self.h2h,
            self.s2l, self.s2h,
            self.v2l, self.v2h,
            self.ids.range2_img
        )
        
    def update_texture(self, hl, hh, sl, sh, vl,vh, range_img):
        height = int(range_img.height)
        width = int(range_img.width)
        print('spl', height, width)
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
        color1 = self.app.color1
        color2 = self.app.color2
        self.h1l = color1[0][0]
        self.h1h = color1[1][0]
        self.s1l = color1[0][1]
        self.s1h = color1[1][1]
        self.v1l = color1[0][2]
        self.v1h = color1[1][2]
        self.ids.h1_slider.value = (self.h1l, self.h1h)
        self.ids.s1_slider.value = (self.s1l, self.s1h)
        self.ids.v1_slider.value = (self.v1l, self.v1h)
        self.h2l = color2[0][0]
        self.h2h = color2[1][0]
        self.s2l = color2[0][1]
        self.s2h = color2[1][1]
        self.v2l = color2[0][2]
        self.v2h = color2[1][2]
        self.ids.h2_slider.value = (self.h2l, self.h2h)
        self.ids.s2_slider.value = (self.s2l, self.s2h)
        self.ids.v2_slider.value = (self.v2l, self.v2h)

    def resize_widgets(self, dt):
        print('resize split')
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
        if self.app.res_leaf_img is None:
            self.show_error_popup('Run previous steps before color extraction.')
            return
        low = (self.h1l, self.s1l, self.v1l)
        high = (self.h1h, self.s1h, self.v1h)
        self.app.run_extr_color1(low, high)
        texture = self.cv2_to_texture(self.app.res_leaf1_img)
        self.extr1_texture = texture

    def extr_color2(self):
        if self.app.res_leaf_img is None:
            self.show_error_popup('Run previous steps before color extraction.')
            return
        low = (self.h2l, self.s2l, self.v2l)
        high = (self.h2h, self.s2h, self.v2h)
        self.app.run_extr_color2(low, high)
        texture = self.cv2_to_texture(self.app.res_leaf2_img)
        self.extr2_texture = texture

class AnalyzeWidget(MyBoxLayout):
    def __init__(self, **kwargs):
        super(AnalyzeWidget, self).__init__(**kwargs)
        self.p = None
        self.g = None
        self.fig = None
        self.fig1 = None
        self.fig2 = None
        self.size_2d = default_size2d
        self.size_3d = default_size3d
        self.input_path = home_dir
        self.app = App.get_running_app()
        Clock.schedule_once(self.bind_func, 0)

    def set_default(self, dt):
        self.ids.size_2d.value = default_size2d
        self.ids.size_3d.value = default_size3d
        return super().set_default(dt)

    def bind_func(self, dt):
        self.ids.size_2d.bind(value=self.set_size)
        self.ids.size_3d.bind(value=self.set_size)
        #self.ids.outdir_label.text = self.input_path
    
    def input_dir(self, file):
        super().input_dir(file)
        self.ids.outdir_label.text = self.input_path

    def set_size(self, *args):
        self.size_2d = self.ids.size_2d.value
        self.size_3d = self.ids.size_3d.value
        self.app.set_marker_size(self.size_2d, self.size_3d)

    def run(self):
        if (self.app.res_leaf_img is None) or (self.app.res_fvfm_img is None):
            self.show_error_popup('There is no input. Do previous steps.')
            return
        self.show_progress_popup(self.cancel_process, 'Running', 'Pick up leaf color and its Fv/Fm value.')
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()
        
    def run_process(self):
        leaf_img = self.app.res_leaf_img
        fvfm_img = self.app.res_fvfm_img
        fvfm_list = self.app.fvfm_list
        leaf1_img = self.app.res_leaf1_img
        leaf2_img = self.app.res_leaf2_img
        try:
            self.fig = self.app.run_pickcell(leaf_img, fvfm_img, fvfm_list)
            self.ids.show_res_btn.disabled = False
            if leaf1_img is not None:
                self.fig1 = self.app.run_pickcell(leaf1_img, fvfm_img, fvfm_list)
                self.ids.show_res1_btn.disabled = False
            if leaf2_img is not None:
                self.fig2 = self.app.run_pickcell(leaf2_img, fvfm_img, fvfm_list)
                self.ids.show_res2_btn.disabled = False
        except Exception as e:
            self.popup.dismiss()
            self.err_msg = str(e)
            Clock.schedule_once(self.thread_error, 0)
        else:
            self.ids.save_btn.disabled = False
        self.popup.dismiss()

    def show_figure(self, fig_type):
        self.show_progress_popup(self.cancel_process, 'Show Figure', 'Drawing...')
        self.thread = WorkingThread(target=self.show_fig_process, args=(fig_type,))
        self.thread.start()

    def show_fig_process(self, group):
        if group == 'all':
            self.fig = self.app.update_marker_size(self.fig, self.size_2d, self.size_3d)
            self.fig[3].show()
            print(self.fig[3])
        elif group == 'color1':
            self.fig1 = self.app.update_marker_size(self.fig1, self.size_2d, self.size_3d)
            self.fig1[3].show()
        elif group == 'color2':
            self.fig2 = self.app.update_marker_size(self.fig2, self.size_2d, self.size_3d)
            self.fig2[3].show()
        self.popup.dismiss()

    def save(self):
        self.show_progress_popup(self.cancel_process, 'Save results', 'Running...')
        self.thread = WorkingThread(target=self.save_process)
        self.thread.start()

    def save_process(self):
        print(self.input_path)
        if self.fig is not None:
            print('All save suruyo')
            self.fig = self.app.update_marker_size(self.fig, self.size_2d, self.size_3d)
            self.app.save(self.fig, self.input_path, 'All_color')
        if self.fig1 is not None:
            print('Color2 save suruyo')
            self.fig1 = self.app.update_marker_size(self.fig1, self.size_2d, self.size_3d)
            self.app.save(self.fig1, self.input_path, 'Color1')
        if self.fig2 is not None:
            print('Color2 save suruyo')
            self.fig2 = self.app.update_marker_size(self.fig2, self.size_2d, self.size_3d)
            self.app.save(self.fig2, self.input_path, 'Color2')
        self.popup.dismiss()
        Clock.schedule_once(lambda x: self.show_error_popup('Finished.', 'Save'))
        

class AutoWidget(MyBoxLayout):
    range1_texture = ObjectProperty(None)
    range2_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AutoWidget, self).__init__(**kwargs)
        self.input_path = None
        self.output_path = '.'
        self.img_list = []
        self.tetstext = 'aaa'
        self.app = App.get_running_app()
        exts = ['jpg', 'jpeg', 'png', 'tiff', 'bmp']
        self.exts = sum([[ext.lower(), ext.upper()] for ext in exts], [])
        Clock.schedule_once(self.bind_func, 0)

    def input_dir_files(self, path):
        print('input path: ', path)
        super().input_dir_files(path)

    def click(self):
        self.app.click()
        '''
        try:
            self.create_img_list()
        except ValueError as e:
            self.show_error_popup(str(e))
        '''

    def input_dir(self, file):
        super().input_dir(file)
        self.indir = self.input_path
        self.ids.input_path.text = self.input_path

    def output_dir(self, file):
        super().input_dir(file)
        self.outdir = self.input_path
        self.ids.outdir.text = self.input_path

    def set_val(self, leaf_thr, fvfm_thr, color1, color2, size2d, size3d):
        self.ids.leaf_thr_slider.value = leaf_thr
        self.ids.fvfm_thr_slider.value = fvfm_thr
        self.ids.h1_slider.value1 = color1[0][0]
        self.ids.s1_slider.value1 = color1[0][1]
        self.ids.v1_slider.value1 = color1[0][2]
        self.ids.h1_slider.value2 = color1[1][0]
        self.ids.s1_slider.value2 = color1[1][1]
        self.ids.v1_slider.value2 = color1[1][2]
        self.ids.h2_slider.value1 = color2[0][0]
        self.ids.s2_slider.value1 = color2[0][1]
        self.ids.v2_slider.value1 = color2[0][2]
        self.ids.h2_slider.value2 = color2[1][0]
        self.ids.s2_slider.value2 = color2[1][1]
        self.ids.v2_slider.value2 = color2[1][2]
        self.ids.size2d.value = size2d
        self.ids.size3d.value = size3d
        Clock.schedule_once(self.resize_widgets_auto, 0)
        #self.resize_widgets_auto(0)

    def create_img_list(self):
        if self.input_dir is None:
            raise ValueError('There is no input. Please select directory.')
        files = []
        self.img_list = []
        if os.path.isfile(self.indir):
            raise ValueError(f'{self.indir} is file. Please select directory.')
        elif os.path.isdir(self.indir):
            for ext in self.exts:
                files += glob.glob(self.indir + '/*.' + ext)
        print('files: ', files)
        img_names = [re.sub('-(L|F)$', '', os.path.splitext(os.path.basename(f))[0]) for f in files]
        img_name_list = [k for k, v in collections.Counter(img_names).items() if v > 1]
        print('img name list', img_name_list)
        for name in img_name_list:
            l = glob.glob(self.indir + '/' + name + '-L.*')
            print(l)
            f = glob.glob(self.indir + '/' + name + '-F.*')
            print(f)
            if (len(l) == 0) or (len(f) == 0):
                break
            if len(l) > 1:
                l = self.biggest_img(l)
            if len(f) > 1:
                f = self.biggest_img(f)
            self.img_list.append([name, l[0], f[0]])
        if len(self.img_list) == 0:
            raise ValueError('There is no pair images.')
        print('img list', self.img_list)
        '''
        output = self.outdir + '/images_list.csv'
        header = ['Name', 'Leaf image file', 'FvFm image file']
        with open(output, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(self.img_list)
        return
        '''

    def biggest_img(self, img_list):
        max_size = 0
        biggest = None
        for image in img_list:
            img = cv2.imread(image)
            size = img.size
            if size > max_size:
                max_size = size
                biggest = image
        return [biggest]

    def run(self):
        self.show_progress_popup(self.cancel_process, 'Auto Pickcell', 'Running...')
        self.thread = WorkingThread(target=self.run_process)
        self.thread.start()

    def run_process(self):
        try:
            self.create_img_list()
        except Exception as e:
            self.popup.dismiss()
            self.err_msg = str(e)
            Clock.schedule_once(self.thread_error, 0)
            return
        leaf_thr = self.ids.leaf_thr_slider.value
        fvfm_thr = self.ids.fvfm_thr_slider.value
        color1 = [(self.h1l, self.s1l, self.v1l), (self.h1h, self.s1h, self.v1h)]
        color2 = [(self.h2l, self.s2l, self.v2l), (self.h2h, self.s2h, self.v2h)]
        size2d = self.ids.size2d.value
        size3d = self.ids.size3d.value
        outdir = self.ids.outdir.text
        is_extr1 = self.ids.is_extr1.active
        is_extr2 = self.ids.is_extr2.active
        print('extr1', is_extr1)
        print('extr2', is_extr2)
        self.app.set_params(leaf_thr, fvfm_thr, is_extr1, is_extr2, color1, color2, size2d, size3d, outdir)
        num_proc = len(self.img_list)
        count = 1
        report_file = outdir + '/report.csv'
        f = open(report_file, 'w', newline='')
        writer = csv.writer(f)
        header = ['Name', 'Leaf_image', 'FvFm_image', 'Result']
        writer.writerow(header)
        for file in self.img_list:
            print(f'{count}/{num_proc}')
            self.popup.dismiss()
            Clock.schedule_once(lambda x: self.show_progress_popup(self.cancel_process, 'Auto Pickcell', f'Running... {count}/{num_proc}'), 0)
            name = file[0]
            leaf_img = file[1]
            fvfm_img = file[2]
            print(name, leaf_img, fvfm_img)
            try:
                self.app.run_auto(name, leaf_img, fvfm_img)
            except Exception as e:
                res = [name, leaf_img, fvfm_img, str(e)]
                writer.writerow(res)
                print(e)
                print('break suruyo')
                self.popup.dismiss()
                count += 1
                continue
            print('owari')
            res = [name, leaf_img, fvfm_img, 'OK']
            writer.writerow(res)
            self.popup.dismiss()
            count += 1
        f.close()
        self.popup.dismiss()

    def active_extr1(self, state):
        if state == 'down':
            self.ids.h1_slider.disabled = False
            self.ids.s1_slider.disabled = False
            self.ids.v1_slider.disabled = False
        elif state == 'normal':
            self.ids.h1_slider.disabled = True
            self.ids.s1_slider.disabled = True
            self.ids.v1_slider.disabled = True

    def active_extr2(self, state):
        if state == 'down':
            self.ids.h2_slider.disabled = False
            self.ids.s2_slider.disabled = False
            self.ids.v2_slider.disabled = False
        elif state == 'normal':
            self.ids.h2_slider.disabled = True
            self.ids.s2_slider.disabled = True
            self.ids.v2_slider.disabled = True

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
        self.app.set_color1(self.h1l, self.s1l, self.v1l, self.h1h, self.s1h, self.v1h)
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
        self.app.set_color2(self.h2l, self.s2l, self.v2l, self.h2h, self.s2h, self.v2h)
        self.update_texture(
            self.h2l, self.h2h,
            self.s2l, self.s2h,
            self.v2l, self.v2h,
            self.ids.range2_img
        )
        
    def update_texture(self, hl, hh, sl, sh, vl,vh, range_img):
        height = int(range_img.height)
        width = int(range_img.width)
        print(height, width)
        if width == 0:
            width = 1
        hue = np.linspace(hl, hh, width)
        saturation = np.linspace(sl, sh, height)
        value = np.linspace(vl, vh, height)
        img_hsv = np.array([[h,s,v] for (s, v) in zip(saturation, value) for h in hue], np.uint8).reshape(height, width, 3)
        img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        texture = self.cv2_to_texture(img)
        range_img.texture = texture

    def resize_widgets_auto(self, dt):
        print('resize')
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
    
    def set_default(self, dt):
        self.outdir = home_dir
        self.ids.outdir.text = self.outdir
        self.leaf_thr = self.app.leaf_thr
        self.fvfm_thr = self.app.fvfm_thr
        color1 = self.app.color1
        color2 = self.app.color2
        self.size_2d = self.app.size_2d
        self.size_3d = self.app.size_3d
        self.h1l = color1[0][0]
        self.h1h = color1[1][0]
        self.s1l = color1[0][1]
        self.s1h = color1[1][1]
        self.v1l = color1[0][2]
        self.v1h = color1[1][2]
        self.ids.leaf_thr_slider.value = self.leaf_thr
        self.ids.fvfm_thr_slider.value = self.fvfm_thr
        self.ids.h1_slider.value = (self.h1l, self.h1h)
        self.ids.s1_slider.value = (self.s1l, self.s1h)
        self.ids.v1_slider.value = (self.v1l, self.v1h)
        self.h2l = color2[0][0]
        self.h2h = color2[1][0]
        self.s2l = color2[0][1]
        self.s2h = color2[1][1]
        self.v2l = color2[0][2]
        self.v2h = color2[1][2]
        self.ids.h2_slider.value = (self.h2l, self.h2h)
        self.ids.s2_slider.value = (self.s2l, self.s2h)
        self.ids.v2_slider.value = (self.v2l, self.v2h)
        self.ids.size2d.value = self.size_2d
        self.ids.size3d.value = self.size_3d
        
class Root(TabbedPanel):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        self.density = Window._density
        self.app = App.get_running_app()

    def switch_to(self, header, do_scroll=False):
        super().switch_to(header, do_scroll)
        if header == self.ids.auto:
            self.app.set_val()
        width = Window.width
        height = Window.height
        Window.size = ((width+1)/self.density, height/self.density)
        Window.size = (width/self.density, height/self.density)

if __name__ == '__main__':
    PickcellApp().run()
