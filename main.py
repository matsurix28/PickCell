from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from range_slider import RangeSlider


class Root(BoxLayout):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)

class MyApp(App):
    def build(self):
        return Root()

if __name__ == '__main__':
    MyApp().run()