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
                (10, 10, 10),  # Black
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

    def get_colors_hsv(self):
        colors = self.colors
        ncolors = [x[1] for x in colors]
        tcolors = []
        for i, v in enumerate(ncolors):
            r, g, b = v
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if .1 < s < .8:
                tcolors.append([s, (r, g, b)])

        return [x[1] for x in sorted(tcolors, reverse=True)]

    def get_palette(self):
        colors = [x[1] for x in self.colors]
        palette = self.defaults
        scheme = []

        for color in palette:
            scheme.append(self.closest_match(color, colors))

        scheme[0] = self.tint_shade(scheme[0], 0, 0.14)
        scheme[1] = self.tint_shade(scheme[15], .999, 1)
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
        r, g, b = pt
        h, s, v = colorsys.rgb_to_hsv(r / 256., g / 256., b / 256.)
        v = max(min(v, high), low)
        return tuple([i * 256. for i in colorsys.hsv_to_rgb(h, s, v)])

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
        call(["feh", "--bg-scale",  self.file])

    def actual_write(self, file, colors):
        with open(file, 'w') as f:
            for color in colors:
                f.write("#%02x%02x%02x" % color)

    def write_colors(self, colors):
        self.actual_write('/tmp/colors2', self.get_palette())

        colors = [x[1] for x in self.colors if x[0] > 300]
        self.actual_write('/tmp/colors', colors)
