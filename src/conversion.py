def hsv_to_rgb(color):
    """ Convert a single color from HSV to RGB """
    h, s, v = color
    return tuple([
        i * 255.
        for i in
        colorsys.hsv_to_rgb(h, s, v)
    ])

def rgb_to_hsv(color):
    """ Convert a single color from RGB to HSV """
    r, g, b = color
    return tuple([
        i / 255.
        for i in
        colorsys.rgb_to_hsv(r, g, b)
    ])

def l_hsv_to_rgb(colors):
    """
    Converts a list of the count,color from HSV to RBG
    """
    return sorted([[x[0], hsv_to_rgb(x[1])] for x in colors], reverse=True)

def l_rgb_to_hsv(colors):
    """
    Converts a list of the count,color from RGB to HSV
    """
    return sorted([x[0], rgb_to_hsv(x[1])] for x in colors], reverse=True)

def rgb_to_hex_str(color):
    """ Get an RGB value as hex (FFFFFF) """
    return "%02x%02x%02x" % color

def rgb_to_str(color):
    """ Get an rgb value as a string (255, 255, 255) """
    return ",".join(color)
