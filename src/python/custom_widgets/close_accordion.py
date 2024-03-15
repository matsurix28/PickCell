from kivy.logger import Logger
from kivy.uix.accordion import Accordion, AccordionItem


class CloseAccordionItem(AccordionItem):
    def __init__(self, **kwargs):
        super(CloseAccordionItem, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self.disabled:
            return True
        if self.collapse:
            self.collapse = False
            return True
        else:
            if self.container_title.collide_point(*touch.pos):
                self.collapse = True
            else:
                self.collapse = False
            return super(AccordionItem, self).on_touch_down(touch)

class CloseAccordion(Accordion):
    def __init__(self, **kwargs):
        super(CloseAccordion, self).__init__(**kwargs)

    def _do_layout(self, dt):
        children = self.children
        if children:
            all_collapsed = all(x.collapse for x in children)
        else:
            all_collapsed = False

        if all_collapsed:
            children[0].collapse = True

        orientation = self.orientation
        min_space = self.min_space
        min_space_total = len(children) * self.min_space
        w, h = self.size
        x, y = self.pos
        if orientation == 'horizontal':
            display_space = self.width - min_space_total
        else:
            display_space = self.height - min_space_total

        if display_space <= 0:
            Logger.warning('Accordion: not enough space '
                           'for displaying all children')
            Logger.warning('Accordion: need %dpx, got %dpx' % (
                min_space_total, min_space_total + display_space))
            Logger.warning('Accordion: layout aborted.')
            return

        if orientation == 'horizontal':
            children = reversed(children)

        for child in children:
            child_space = min_space
            child_space += display_space * (1 - child.collapse_alpha)
            child._min_space = min_space
            child.x = x
            child.y = y
            child.orientation = self.orientation
            if orientation == 'horizontal':
                child.content_size = display_space, h
                child.width = child_space
                child.height = h
                x += child_space
            else:
                child.content_size = w, display_space
                child.width = w
                child.height = child_space
                y += child_space