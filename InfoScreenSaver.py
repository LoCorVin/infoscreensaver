import kivy
import random, os, time
from kivy.app import App
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color
from transportMucAPI.query_trips import get_trips, shorten_trips, extend_style, enhance_times, format_output, get_dt, distance, short_distance
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics.svg import Svg
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatter import Scatter
from colour import Color
from kivy.clock import Clock
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.properties import StringProperty, ListProperty
from pprint import pprint

class Separator(Label):
    pass

class InfoScreenLayout(BoxLayout):
    pass

class TravelWidget(BoxLayout):
    pass

class LineLabel(Label):
    pass

class TransImage(Image):
    pass


class TransportMean(BoxLayout):
    colour_property = ListProperty([0, 1, 0, 1])
    def __init__(self, **kwargs):
        self.colour_property = [0, 1, 0, 1]
        super(TransportMean, self).__init__(**kwargs)



class InfoScreenSaver(App):

    __here = ""

    __travel_w_count = 8

    __destinations = ["", ""]

    __infoScreenLayout = None
    __triparray = []
    __colorarray = []
    __colored_index = 0

    def __init__(self):
        App.__init__(self)
        self.photos = []
        find_all_photos(self)

    def build(self):
        print("Build")
        Clock.schedule_interval(self.update_infos, 10)
        Clock.schedule_interval(self.load_trips, 60)
        self.__infoScreenLayout = InfoScreenLayout()
        self.load_trips()
        self.update_infos()
        return self.__infoScreenLayout


    def add_button(self, box_layout):
        print("Add travel widget")
        box_layout.add_widget(TravelWidget())

    def load_trips(self, whatever=None):
        unsorted_trips = []
        for destiantion in self.__destinations:
            trips = get_trips(self.__here, destiantion)
            selected_trip_info = shorten_trips(trips)
            style_ext_trips = extend_style(selected_trip_info)
            time_enhanced_tf = enhance_times(style_ext_trips)
            unsorted_trips += time_enhanced_tf
        self.__triparray = sorted(unsorted_trips, key=lambda trip: trip['predictedDeparture'] if 'predictedDeparture' in trip else trip['departure'])[:self.__travel_w_count]
        self.update_infos()

    def update_infos(self, whatever = None):
        self.__colorarray = []
        self.__colored_index = 0
        self.load_colors(self.__triparray)
        now = now_ms()
        self.__infoScreenLayout.ids.clock.text = get_dt(now_ms())['time']
        self.__infoScreenLayout.ids.here.text = self.__here
        self.__infoScreenLayout.ids.travel_info.clear_widgets()
        for trip in self.__triparray:
            travel_widget = TravelWidget()
            travel_widget.ids.destination.text = trip['trip_parts'][-1]['to']
            in_string = distance(trip['departure'] - now)
            travel_widget.ids.in_time.text = in_string
            travel_widget.ids.duration.text = short_distance(trip['duration'])
            travel_widget.ids.departure.text = get_dt(trip['departure'])['time']
            travel_widget.ids.arrival.text = get_dt(trip['arrival'])['time']
            parts = get_short_transport(trip)
            for part in parts:
                travel_widget.ids.travel_images.add_widget(part)
            self.__infoScreenLayout.ids.travel_info.add_widget(travel_widget)


    def get_label_color(self, label):
        self.__colored_index = self.__colored_index +1
        return self.__colorarray[self.__colored_index -1]


    def load_colors(self, trips):
        for trip in trips:
            for parts in trip['trip_parts']:
                if 'background' in parts['style']:
                    c = Color(parts['style']['background'])
                    self.__colorarray.append([c.red, c.green, c.blue, 0.75])



    def add_photos(self, pictures):
        self.photos = pictures

def scale_f_height(max_height, height):
    return max_height/height


def get_short_transport(trip):
    widgets = []
    for trip_part in trip['trip_parts']:
        #transport = TransportMean()
        trans_image = TransImage()
        trans_image.source = "transportMucAPI/" + trip_part['style']['icon']
        # transport.ids.transport_icon.source = "transportMucAPI/" + trip_part['style']['icon']
        widgets.append(trans_image)
        if 'line' in trip_part and len(trip_part['line']) > 0:
            ll = LineLabel()
            #transport.add_widget(ll)
            if "transportation" in trip_part and 'BOB' in trip_part['transportation']:
                ll.text = 'BOB'
            else:
                ll.text = trip_part['line']
            widgets.append(ll)
        #widgets.append(Separator())
        #widgets.append(transport)
        #svg.scale = scale_f_height(40, svg.height)
        #svg.center = Window.center

    return widgets

def now_ms():
    return int(round(time.time() * 1000))

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

