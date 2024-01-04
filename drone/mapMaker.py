#this simply just creates the map. sets up all points and pixels
def pixelToAirsimPoint(x_pixel,y_pixel):
    x_norm = round(x_pixel * (50/190))
    y_norm = round(y_pixel * (50/190))
    return [x_norm,y_norm,-20]


map_dict_pixels = {
    "O":(0,0),
    "HY1":(0,-125),
    "H1":(0,110),
    "H2":(0,225),
    "H3":(0,399),
    "I1":(0,470),
    "H4":(55,470),
    "I4":(285,0),
    "HX6_7":(390,0),
    "I3":(450,0),
    "HX5":(450,108),
    "HX2":(345,470)
}

def getMapDict():
    new_dict = {}
    for key in map_dict_pixels.keys():
        new_dict[key] = pixelToAirsimPoint(map_dict_pixels[key][0],map_dict_pixels[key][1])

    # print(new_dict)
    return new_dict