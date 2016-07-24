import re
from pprint import pprint


class LayoutParser:
    def __init__(self, target, format, image, type):
        self.format = format
        self.target = target
        self.prefix = "%"

        if type:
            self.set_int_map(image.get_palette())
        else:
            self.set_int_map([x[1] for x in image.colors])

        self.set_opac(image)
        self.set_bg(image)
        self.set_fg(image)
        self.set_int_map(image)

    def set_opac(self, image):
        """ Helper to set the opacity string """
        self.set_keys('opacity', image.get_opac())

    def set_bg(self, image):
        """ Helper to set background string """
        self.set_color_keys('background', image.get_bg())
        self.set_color_keys('bg_sat', image.get_sat_bg())
        self.set_color_keys('bg_unsat', image.get_unsat_bg())

    def set_fg(self, image):
        """ Helper to set foreground string """
        self.set_color_keys('foreground', image.get_fg())
        self.set_color_keys('fg_sat', image.get_sat_fg())

    def set_color_keys(self, key, value):
        self.set_keys(key, self.format_color(value))

    def set_keys(self, key, value):
        """ Find/replace all key values """
        self.target = self.target.replace(self.prefix + key, str(value))

    def set_int_map(self, colors):
        needles = re.findall('\%\d+', self.target)
        for occurrence in needles:
            color = self.format_color(colors[int(occurrence[1:])])
            self.target = self.target.replace(occurrence, color, 1)

    def format_color(self, value):
        """ Convert the RGB tuple to a formatted string"""
        """ Currently supports hex and RGB """
        if 'hex' in self.format:
            return '%02x%02x%02x' % value
        if 'rgb' in self.format:
            return ','.join([str(int(x)) for x in value])
