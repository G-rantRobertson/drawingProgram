# Imports
import sys
import pygame
import ctypes
import PySimpleGUI as sg
import random

# music
from pygame import mixer

mixer.init()
mixer.music.load("DDLK.mp3.mp3")  # song file must be in folder
mixer.music.set_volume(0.7)
mixer.music.play(loops=-1)
j = 1

# Increase Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Pygame Configuration
pygame.init()
fps = 300
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
global rCheck
rCheck = False
font = pygame.font.SysFont('ComicSans', 15)

# Variables

# Our Buttons will append themselves to this list
objects = []
objectsBottomRow = []

# Initial color
drawColor = [0, 0, 0]

# Initial brush size
brushSize = 30
brushSizeSteps = 3

# Drawing Area Size
canvasSize = [800, 800]


# Button Class
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


# Handler Functions

# Changing the Color
def changeColor(color):
    global rCheck
    rCheck = False
    global drawColor
    drawColor = color
#specific to the rainbow function
def changeColor2(color):
    global drawColor
    drawColor = color

# Changing the Brush Size
def changebrushSize(dir):
    global brushSize
    if dir == 'greater':
        brushSize += brushSizeSteps
    else:
        brushSize -= brushSizeSteps

# Save the surface to the computer
def save():
    global j
    pygame.image.save(canvas, f"canvas{j}.png")
    j += 1
#input custom RGB
def custom():
    layout = [
        [sg.Text('Please enter RGB')],
        [sg.Text('R', size=(15, 1)), sg.InputText()],
        [sg.Text('G', size=(15, 1)), sg.InputText()],
        [sg.Text('B', size=(15, 1)), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('RGB input', layout)
    event, values = window.read()

    # blank spaces
    for i in range(len(values)):
        if values[i] == '':
            values[i] = 0
    dictionary = {}
    for i in range(26):
        dictionary[i] = chr(ord('a') + i)
        dictionary[i + 26] = chr(ord('A') + i)
    special_chars = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    for i in range(len(special_chars)):
        dictionary[i + 52] = special_chars[i]
    # if there is letters in the input
    for i in range(len(values)):
        inp = str(values[i])
        for j in range(len(dictionary)):
            if inp.find(dictionary[j]) != -1:
                values[i] = 0
    # over 255
    for i in range(len(values)):
        if int(values[i]) > 255:
            values[i] = 255
    # less than 0
    for i in range(len(values)):
        if int(values[i]) < 0:
            values[i] = 0
    changeColor([int(values[0]), int(values[1]), int(values[2])])
    window.close()
#rainbow brush
def rainbow():
    global rCheck
    rCheck = True
#clear the canvas to white
def clear():
    canvas.fill((255, 255, 255))

# Button Variables.
buttonWidth = 102.5
buttonHeight = 35

# Buttons and their respective functions.
buttons = [
    ['Black', lambda: changeColor([0, 0, 0])],
    ['White', lambda: changeColor([255, 255, 255])],
    ['Blue', lambda: changeColor([0, 0, 255])],
    ['Green', lambda: changeColor([0, 255, 0])],
    ['Red', lambda: changeColor([225, 0, 0])],
    ['Orange', lambda: changeColor([255, 165, 0])],
    ['Yellow', lambda: changeColor([255, 255, 0])],
    ['Purple', lambda: changeColor([128, 0, 128])],
    ['Pink', lambda: changeColor([255, 192, 203])],
    ['Brown', lambda: changeColor([150, 75, 0])],
    ['Grey', lambda: changeColor([128, 128, 128])],
    ['Brush Larger', lambda: changebrushSize('greater')],
    ['Brush Smaller', lambda: changebrushSize('smaller')],
    ['Custom', lambda: custom()],
    ['Random', lambda: changeColor([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])],
    ['Rainbow', lambda: rainbow()],
    ['Save', save]
]

buttonsBottomRow = [
    ['Clear', lambda: clear()]
    ]

# Making the buttons
for index, buttonName in enumerate(buttons):
    Button(index * (buttonWidth + 10) + 10, 10, buttonWidth,
           buttonHeight, buttonName[0], buttonName[1])

for index, buttonName in enumerate(buttonsBottomRow):
    Button(index * (buttonWidth + 10) + 10, 950, buttonWidth,
           buttonHeight, buttonName[0], buttonName[1])

# Canvas
canvas = pygame.Surface(canvasSize)
canvas.fill((255, 255, 255))

# Game loop.
while True:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    if rCheck:
        rVal = random.randint(0, 255)
        gVal = random.randint(0, 255)
        bVal = random.randint(0, 255)
        changeColor2([rVal, gVal, bVal])

    # Drawing the Buttons
    for object in objects:
        object.process()
    # Draw the Canvas at the center of the screen
    x, y = screen.get_size()
    screen.blit(canvas, [x / 2 - canvasSize[0] / 2, y / 2 - canvasSize[1] / 2])
    # Drawing with the mouse
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        # Calculate Position on the Canvas
        dx = mx - x / 2 + canvasSize[0] / 2
        dy = my - y / 2 + canvasSize[1] / 2
        pygame.draw.circle(
            canvas,
            drawColor,
            [dx, dy],
            brushSize,
        )

    # Reference Dot
    pygame.draw.circle(screen,
                       drawColor,
                       [100, 100],
                       brushSize,
                       )

    pygame.display.flip()
    fpsClock.tick(fps)