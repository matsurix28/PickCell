from kivy.uix.accordion import Accordion, AccordionItem


class CloseAccordionItem(AccordionItem):
    def __init__(self, **kwargs):
        super(CloseAccordionItem, self).__init__(**kwargs)