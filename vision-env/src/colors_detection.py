from scipy.spatial import KDTree
from webcolors import (
    hex_to_rgb,
)

COLORS = {
    "aqua": ["#00ffff", (0,255,255)],
    "black": ["#000000", (0,0,0)],
    "blue": ["#0000ff", (0,0,255)],
    "fuchsia": ["#ff00ff", (255,0,255)],
    "green": ["#008000", (0,128,0)],
    "gray": ["#808080", (128,128,128)],
    "lime": ["#00ff00", (0,255,0)],
    "olive": ["#808000", (128,128,0)],
    "purple": ["#800080", (128,0,128)],
    "red": ["#ff0000", (255,0,0)],
    "silver": ["#c0c0c0", (192,192,192)],
    "teal": ["#008080", (0,128,128)],
    "white": ["#ffffff", (255,255,255)],
    "yellow": ["#ffff00", (255,255,0)],
    "beige": ["#f5f5dc", (245,245,220)],
    "brown": ["#a52a2a", (165,42,42)],
    "gold": ["#ffd700", (255,215,0)],
    "pink": ["#ffc0cb", (255,192,203)],
    "lavender": ["#e6e6fa", (230,230,250)],
    "turquoise": ["#40e0d0", (64,224,208)],
    "violet": ["#ee82ee", (238,130,238)],
    "orange": ["#ffa500", (255,165,0)],
    "lightblue": ["#add8e6", (173,216,230)]
}

COLORS_HEX = {
    "aqua": "#00ffff",
    "black": "#000000",
    "blue": "#0000ff",
    "fuchsia": "#ff00ff",
    "green": "#008000",
    "gray": "#808080",
    "lime": "#00ff00",
    "olive": "#808000",
    "purple": "#800080",
    "red": "#ff0000",
    "silver": "#c0c0c0",
    "teal": "#008080",
    "white": "#ffffff",
    "yellow": "#ffff00",
    "beige": "#f5f5dc",
    "brown": "#a52a2a",
    "gold": "#ffd700",
    "pink": "#ffc0cb",
    "lavender": "#e6e6fa",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "orange": "#ffa500",
    "lightblue": "#add8e6",
}

def convert_rgb_to_names(rgb_tuple):
    # A dictionary of all the color names and their respective hex in color_db
    color_db = COLORS_HEX
    names = []
    rgb_values = []
    for color_name, color_hex in color_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return str(names[index])
