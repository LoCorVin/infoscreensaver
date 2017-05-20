import kivy

import random, os
from kivy.app import App
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.properties import StringProperty


class InfoScreenLayout(BoxLayout):
    pass

class TravelWidget(BoxLayout):
    pass

#class SvgImage(Scatter):
#
#    def __init__(self, filename, **kwargs):
#        super(SvgWidget, self).__init__(**kwargs)
#        with self.canvas:
#            svg = Svg(filename)
#        self.size = svg.width, svg.height

class InfoScreenSaver(App):

    __infoScreenLayout = None

    def __init__(self):
        App.__init__(self)
        self.photos = []
        find_all_photos(self)

    def build(self):
        print("Build")
        #Clock.schedule_interval(self.update_infos, 3)
        self.__infoScreenLayout = InfoScreenLayout()
        self.update_infos()
        return self.__infoScreenLayout


    def add_button(self, box_layout):
        print("Add travel widget")
        box_layout.add_widget(TravelWidget())

    def update_infos(self, whatever = None):
        for i in range(1,6):
            self.__infoScreenLayout.ids.travel_info.add_widget(TravelWidget())

    def add_photos(self, pictures):
        self.photos = pictures

def find_all_photos(app):
    directory="wallpapers"
    indirectory = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".JPG"):
            indirectory.append(directory + "/" + filename)
    app.add_photos(indirectory)
        
if __name__ == '__main__':
    Config.set('graphics', 'fullscreen', '1')
    Config.set('graphics', 'size', '0x0')
    to_start = 2
    while to_start > 0:
        try:
            to_start = to_start -1
            InfoScreenSaver().run()
        except AttributeError as ae:
            print(str(ae) + "\nMay be caused by some initialization error and on the second exection of run works")

