from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BoundedNumericProperty, OptionProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView


class FvFm(BoxLayout):
    src = OptionProperty('src/img/graphic.png', options=('src/img/graphic.png', 'src/img/icon.png'))
    name = BoundedNumericProperty(0, min=0)

KV_CODE = '''
<FvFm>:
    Image:
        source: root.src
    Label:
        text: root.name
        
RecycleView:
    viewclass: 'FvFm'
    RecycleBoxLayout:
        spacing: 8
        padding: 8
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
        default_size_hint: 1, None
        default_size: 0, 80
'''



class MyRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(RecycleView, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(20)]

class MyApp(App):
    def build(self):
        return Builder.load_string(KV_CODE)

    def on_start(self):
        rv = self.root
        rv.data = (
            {'src': 'src/img/icon.png', 'name': 37} for i in range(20)
        )


MyApp().run()