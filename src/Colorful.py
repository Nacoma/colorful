#!/usr/bin/python
from pprint import pprint
from PIL import Image, ImageStat
from subprocess import call
import math
from random import sample
import colorsys
import sys


# should use this, it's a less shitty version of tailing it with my pipe_ function.
# from subprocess import Popen, PIPE
class Colorful:
    def __init__(self, file):
        self.file = file
        self.img = Image.open(self.file)
        self.defaults = [
                #(10, 10, 10),  # Black
                (255, 0, 0),  # Red
                (0, 255, 0),  # Green
                (255, 255, 0),  # Yellow
                (0, 0, 255),  # Blue
                (255, 0, 255),  # Magenta
                (0, 255, 255),  # Cyan
                (64, 64, 64),  # Dark gray
                (228, 0, 0),  # Red
                (0, 228, 0),  # Green
                (228, 228, 0),  # Yellow
                (0, 0, 228),  # Blue
                (228, 0, 228),  # Magenta
                (0, 228, 228),  # Cyan
                (192, 192, 192),  # Light gray
                (255, 255, 255),  # White
        ]
        self.colors = self.get_colors(256)
        self.sats = self.list_to_hsv()
        self.saturation_avg = self.get_index_average(1)
        self.value_avg = self.get_index_average(2)
        self.light_avg = self.get_light_avg()
        self.light = self.is_light()

        print("\r\n")
        print("Colors!")
        print("Image          : %s" % self.file)
        print("Is Light       : %s" % self.light)
        print("Opacity        : %s\r\n" % self.get_opac())
        print("Average Sat.   : %s" % self.saturation_avg)
        print("Average Value  : %s" % self.value_avg)
        print("Average CLight : %s\r\n" % self.light_avg)

    def get_colors(self, num):
        """Get the most used colors in the image"""
        img = self.img
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = img.convert('P', palette=Image.ADAPTIVE, colors=num)
        img = img.convert('RGB')
        colors = sorted(img.getcolors(256), reverse=True)
        self.colors = colors
        return colors

    def list_to_hsv(self):
        """ Convert our color list to HSV """
        return sorted([[x[0], self.rgb_to_hsv(x[1])] for x in self.colors], reverse=True)

    def get_palette(self):
        colors = [x[1] for x in self.colors]
        palette = self.defaults
        scheme = []
        
        scheme.append(self.colors[0][1])

        for color in palette:
            scheme.append(self.closest_match(color, colors))

        scheme[0] = self.tint_shade(scheme[0], 0, 0.2)
        scheme[1] = self.tint_shade(scheme[15], .999, 1)

        if self.light:
            for i in range(2, 15):
                scheme[i] = self.tint_sat(scheme[i], 1 - self.saturation_avg, 1)
                scheme[i] = self.tint_shade(scheme[i], 0, self.light_avg)
        else:
            for i in range(2, 15):
                scheme[i] = self.tint_sat(scheme[i], self.light_avg / 2, 1)
                scheme[i] = self.tint_shade(scheme[i], self.value_avg,  1)

        return [(int(x[0]), int(x[1]), int(x[2])) for x in scheme]

    def closest_match(self, pt, samples):
        current = None
        max_distance = 500
        for i, v in enumerate(samples):
            this_distance = self.euclid_dist(pt, v)
            if this_distance < max_distance:
                current = v
                max_distance = this_distance
        return current

    def tint_shade(self, pt, low, high):
        h, s, v = self.rgb_to_hsv(pt)
        v = max(min(v, high), low)
        return tuple([i * 255. for i in colorsys.hsv_to_rgb(h, s, v)])

    def tint_sat(self, pt, low, high):
        h, s, v = self.rgb_to_hsv(pt)
        s = max(min(s, high), low)
        return tuple([i * 255. for i in colorsys.hsv_to_rgb(h, s, v)])

    def tint_all(self, pt, s_low, s_high, v_low, v_high):
        return self.tint_shade(self.tint_sat(pt, s_low, s_high), v_low, v_high)

    def hsv_to_rgb(self, color):
        h, s, v = color
        return tuple([i * 255. for i in colorsys.hsv_to_rgb(h, s, v)])

    def closest_dist(self, pt, samples):
        cur = self.closest_match(pt, samples)
        if cur is None:
            return 1000
        return self.euclid_dist(samples[cur], pt)

    def euclid_dist(self, a, b):
        """euclidian distance calculation"""
        return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))

    def paper_me_baby(self):
        """Set the image as the wallpaper"""
        call(["feh", "--bg-tile",  self.file])

    def actual_write(self, file, colors):
        with open(file, 'w') as f:
            for color in colors:
                f.write("#%02x%02x%02x" % color)

    def rgb_to_hsv(self, color):
        """ basic, no nonsense conersion to HSV from our RGB tuple. """
        r, g, b = color
        return colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)

    def is_light(self):
        return self.light_avg > .5

    def get_opac(self):
        return .9 + (self.value_avg + self.saturation_avg) / 15

    def get_light_avg(self):
        return self.value_avg * .63 + self.saturation_avg * .37

    def get_index_average(self, index):
        count = 0
        total = 0
        for qty, color in self.colors:
            tmp = self.rgb_to_hsv(color)
            count += qty
            total += qty * (tmp[index])
        return total / count

    def get_bg(self):
        if self.light:
            return self.tint_all(self.colors[0][1], .0, .1,.9,1)
        else:
            return self.tint_all(self.colors[0][1], 0, self.light_avg / 4, 0, self.light_avg / 2)

    def get_max_range(self):
        return [self.colors[64][0]]

    def get_sat_bg(self):
        sat = (0., 0., 0.)
        for qty, color in self.sats:
            h, s, v = color
            if s > sat[1]:
                sat = (h, s, v)
        return self.hsv_to_rgb(sat)

    def get_unsat_bg(self):
        min_h, min_s, min_v = (0, .001, 0)
        sat = (0, 1, 0)
        for qty, color in self.sats:
            h, s, v = color
            if min_s < s and s < sat[1]:
                sat = (h, s, v)
        return self.hsv_to_rgb(sat)
                
        
    def get_fg(self):
        if self.light:
            return self.tint_shade(self.colors[0][1], 0, .3)
        else:
            return self.tint_shade(self.colors[0][1], .8, 1)


    def get_sat_fg(self):
        if self.light:
            return self.tint_all(self.colors[0][1], .2,.5, .7, .9)
        else:
            return self.tint_all(self.colors[0][1], .3, 1, .8, 1)
