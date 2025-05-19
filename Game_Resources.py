from pygame import image

#DEFINE IMPORTANT GLOBALLY ACCESSIBLE GAME ATTRIBUTES
RUNNING = False
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

CANVAS_WIDTH = 282
CANVAS_HEIGHT = (CANVAS_WIDTH/4)*3

CANVAStoDISPLAY_width_ratio = CANVAS_WIDTH/DISPLAY_WIDTH
CANVAStoDISPLAY_height_ratio = CANVAS_HEIGHT/DISPLAY_HEIGHT

mouse_pos = (0,0)
mouse_button_down = False
mouse_button_helddown = False
mouse_button_up = False

game_objects = []

#SPRITE ASSETS
Textures = dict()

def get_texture(name: str):
    if name in Textures.keys():
        return Textures[name]
    else:
        return load_texture(name)

def load_texture(name: str):
    pathstr = f"sprites/{name}.png"
    texture = image.load(pathstr)
    Textures[name] = texture
    return texture
