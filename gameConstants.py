import pyglet

''' Screen title and size '''

SCREEN_TITLE = "Dominó Monetario"
SCREEN_NUM = 0
SCREENS = pyglet.canvas.Display().get_screens()
SCREEN = SCREENS[SCREEN_NUM]
SCREEN_WIDTH = SCREEN.width
SCREEN_HEIGHT = SCREEN.height

''' Draw text '''
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 20

''' Positioning and object scaling '''
DOMINO_SCALE = 0.12
DOMINO_WIDTH = 2040 * DOMINO_SCALE
DOMINO_HEIGHT = 602 * DOMINO_SCALE

SCREEN_WIDTH_DIV = 20
SCREEN_HEIGHT_DIV = 10

BANK_X = 500
BANK_Y = 500

PLAYER_START_HAND = 13

DOMINOS_VALUES = ["0", "005", "010", "025", "050", "1", "2", "5", "10", "20", "50", "100", "200"]