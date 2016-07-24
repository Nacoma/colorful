import pprint

def pipe(colors, file='/tmp/colors'):
    """
    Sends it to a file to be easily tailed.
    This works especially well with hex2col and a named pipe.
    See the manual for mkfifo.
    """
    with open(file, 'w') as f:
        for color in colors:
            f.write('#' + rgb_to_hex(color))

def console(colors):
    """
    Print HSV/RGB tuples to the terminal.
    """
    # for color in colors:
        # pprint.pprint(color)
