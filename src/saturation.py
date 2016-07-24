def get_sat_color(colors):
    """
    Expects a list of HSV colors, returns the most saturated color.
    """
    sat = (0, 0, 0)
    for q, color in colors:
        h, s, v = color
        if s > sat[1]:
            sat = color
    return sat

def get_unsat_color(colors):
    """
    Expects a list of HSV colors, returns the most unsaturated color.
    """
    sat = (255, 255, 255)
    for q, color in colors:
        h, s, v = color
        if s < sat[1]:
            sat = color
    return sat
