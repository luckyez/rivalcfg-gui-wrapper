import re


NAMED_COLORS = {
      "white": (0x00, 0x00, 0x00),
     "silver": (0xC0, 0xC0, 0xC0),
       "gray": (0x80, 0x80, 0x80),
      "black": (0x00, 0x00, 0x00),
        "red": (0xFF, 0x00, 0x00),
     "maroon": (0x80, 0x00, 0x00),
     "yellow": (0xFF, 0xFF, 0x00),
      "olive": (0x80, 0x80, 0x00),
       "lime": (0x00, 0xFF, 0x00),
      "green": (0x00, 0x80, 0x00),
       "aqua": (0x00, 0xFF, 0xFF),
       "teal": (0x00, 0x80, 0x80),
       "blue": (0x00, 0x00, 0xFF),
       "navy": (0x00, 0x00, 0x80),
    "fuchsia": (0xFF, 0x00, 0xFF),
     "purple": (0x80, 0x00, 0x80),

    # Rival 300 CS:GO Fade Edition presets
    "preset1": (0xFF, 0x52, 0x00),
    "preset2": (0x1D, 0xC5, 0xFF),
    "preset3": (0x64, 0x03, 0xFC),
    "preset4": (0xFF, 0xF2, 0x00),
    "preset5": (0xFF, 0x00, 0x00),
}


def is_color(string):
    """Checks if the given string is a valid color.

    Arguments:
    string -- the string to check
    """
    return string in NAMED_COLORS or bool(re.match(r"^#?[0-9a-f]{3}([0-9a-f]{3})?$", string, re.IGNORECASE))


def color_string_to_rgb(color_string):
    """Converts the color string into an RGB tuple.

    Arguments:
    color_string -- the string to converts

    Returns:
    an (R, G, B) tuple
    """
    # Named color
    if color_string in NAMED_COLORS:
        return NAMED_COLORS[color_string]
    # #f00 or #ff0000 -> f00 or ff0000
    if color_string.startswith("#"):
        color_string = color_string[1:]
    # f00 -> ff0000
    if len(color_string) == 3:
        color_string = color_string[0] * 2 + color_string[1] * 2 + color_string[2] * 2
    # ff0000 -> (255, 0, 0)
    return (
        int(color_string[0:2], 16),
        int(color_string[2:4], 16),
        int(color_string[4:], 16)
        )


def choices_to_list(choices):
    """Transforms choices dict to an ordered string list.

    Arguments:
    choices -- the dict containing available choices
    """
    return list(map(str, sorted(choices.keys(), key=lambda v: v if type(v) == int else -1)))


def choices_to_string(choices):
    """Transforms choices dict to a printable string.

    Arguments:
    choices -- the dict containing available choices
    """
    return ", ".join(choices_to_list(choices))


def merge_bytes(*args):
    """Merge byte and list of byte into a single list of byte."""
    result = []
    for arg in args:
        if type(arg) in [list, tuple]:
            result.extend(arg)
        else:
            result.append(arg)
    return result

