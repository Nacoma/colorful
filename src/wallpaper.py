def set_bg_tile(image):
    """
    Sets the wallpaper using feh.
    """
    call(["feh", "--bg-tile", image])

def set_bg_scale(image):
    """
    Sets the wallpaper using feh.
    """
    call(["feh", "--bg-scale", image])
