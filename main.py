import kivy

import random, os
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.config import Config


class PhotoScreensaver(App):

    def __init__(self):
        App.__init__(self)
        self.photos = []
        find_all_photos(self)

    def print_it(instance, value):
        print('User clicked on', value)
    widget = Label(text='Hello [ref=world]World[/ref]', markup=True)
    widget.bind(on_ref_press=print_it)

    def build(self):
        keyb = Window.request_keyboard(self.stop, self)
        keyb.bind(on_key_down = self.key_pressed)
        self.image = Image()
        self.change_image()
        Clock.schedule_interval(self.change_image, 10)
        return self.image

    def key_pressed(self, keyboard, keycode, text, modifiers):
        self.stop()

    def change_image(self, whatever = None):
        self.image.source = random.choice(self.photos)

    def add_photos(self, pictures):
        self.photos = pictures

def find_all_photos(app):
    directory="/home/pi/screensaver/wallpapers"
    indirectory = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".JPG"):
            indirectory.append(directory + "/" + filename)
    app.add_photos(indirectory)
        
if __name__ == '__main__':
    Config.read('config.ini')
    Config.set('graphics', 'fullscreen', '1')
    Config.set('graphics', 'size', '0x0')
    to_start = True
    while to_start:
        try:
            to_start = False
            PhotoScreensaver().run()
        except AttributeError as ae:
            print(str(ae) + "\nMay be caused by some initialization error and on the second exection of run works")
            to_start = True

