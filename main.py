from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MainApp(App):
    def build(self):
        return Root()

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        

MainApp().run()
