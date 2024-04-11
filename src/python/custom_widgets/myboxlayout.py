import os

from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout

from .popup import ErrorPopup, ProgressPopup


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.input_path = None
        self.thread = None
        Clock.schedule_once(self.set_default, 0)

    def input_img(self, file):
        if file != []:
            self.ids.input_img.source = file[0]
            self.input_path = file[0]

    def input_dir_files(self, file):
        if len(file) == 1:
            if os.path.isdir(file[0]):
                self.input_path = file
            elif os.path.isfile(file[0]):
                self.show_error_popup('Please select directory or multiple files.')
        elif len(file) > 1:
            self.input_path = file
                

    def cv2_to_texture(self, cv2_img):
        texture = Texture.create(size=(cv2_img.shape[1], cv2_img.shape[0]), colorfmt='bgr', bufferfmt='ubyte')
        texture.blit_buffer(cv2_img.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
        texture.flip_vertical()
        return texture
    
    def show_progress_popup(self,cancel_func, title, message):
        self.popup = ProgressPopup(cancel_func, title_text=title, message=message)
        self.popup.open()

    def show_error_popup(self, message, title='Error'):
        popup = ErrorPopup(message=message, title_text=title)
        popup.open()

    def cancel_process(self):
        try:
            self.thread.raise_exception()
        except Exception as e:
            print('erorr dayooooo')
            print(self.popup)
            self.popup.dismiss()
            self.show_error_popup(str(e))

    def thread_error(self, dt):
        self.show_error_popup(self.err_msg)
        self.err_msg = None

    def close_popup(self):
        self.popup.dismiss()
    
    def int_input(self, input, target=None):
        if (input.text == '') or (int(input.text) < 0):
            input.text = '0'
        elif int(input.text) > 255:
            input.text = '255'
        if target is not None:
            target = int(input.text)

    def set_default(self, dt):
        pass