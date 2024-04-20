from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import os
from test_src.python.custom_widgets.range_slider import RangeSlider

src_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_src'))

class MyApp(App):
    def build(self):
        Builder.load_file(os.path.join(src_dir, 'layouts', 'my.kv'))
        return Root()

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)

if __name__ == '__main__':
    MyApp().run()
