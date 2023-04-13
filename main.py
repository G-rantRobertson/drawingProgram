# Imports
import sys
import pygame
import ctypes
import PySimpleGUI as sg
import random

#music
from pygame import mixer
mixer.init()
mixer.music.load("DDLK.mp3.mp3") #song file must be in folder
mixer.music.set_volume(0.7)
mixer.music.play(loops=-1)

# Increase Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Pygame Configuration
pygame.init()
fps = 300
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

font = pygame.font.SysFont('ComicSans', 15)

# Variables

# Our Buttons will append themselves to this list
objects = []

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
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


# Handler Functions

# Changing the Color
def changeColor(color):
    global drawColor
    drawColor = color

# Changing the Brush Size
def changebrushSize(dir):
    global brushSize
    if dir == 'greater':
        brushSize += brushSizeSteps
    else:
        brushSize -= brushSizeSteps

# Save the surface to the Disk
def save():
    pygame.image.save(canvas, "canvas.png")

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
    #blank spaces
    for i in range(len(values)):
        if len(values[i]) == 0:
            values[1] = 0
    #if there is letters in the input
    for i in range(len(values)):
        for k in range(len(values[i])):
            if values[i][k] == "a" or values[i][k] == "b" or values[i][k] == "c" or values[i][k] == "d" or values[i][k] == "e" or values[i][k] == "f" or values[i][k] == "g" or values[i][k] == "h" or values[i][k] == "i" or values[i][k] == "j" or values[i][k] == "k" or values[i][k] == "l" or values[i][k] == "m" or values[i][k] == "n" or values[i][k] == "o" or values[i][k] == "p" or values[i][k] == "q" or values[i][k] == "r" or values[i][k] == "s" or values[i][k] == "t" or values[i][k] == "u" or values[i][k] == "v" or values[i][k] == "w" or values[i][k] == "x" or values[i][k] == "y" or values[i][k] == "z":
                values[i] = 0
    #over 255
    for i in range(len(values)):
        if int(values[i]) > 255:
            values[i] = 255
    #less than 0
    for i in range(len(values)):
        if int(values[i]) < 0:
            values[i] = 0
    changeColor([int(values[0]), int(values[1]), int(values[2])])
    window.close()


# Button Variables.
buttonWidth = 100
buttonHeight = 35

# Buttons and their respective functions.
buttons = [
    ['Black', lambda: changeColor([0, 0, 0])],
    ['White', lambda: changeColor([255, 255, 255])],
    ['Blue', lambda: changeColor([0, 0, 255])],
    ['Green', lambda: changeColor([0, 255, 0])],
    ['Red', lambda: changeColor([225, 0, 0])],
    ['Orange', lambda: changeColor([255, 165, 0])],
    ['Yellow', lambda: changeColor([255,255,0])],
    ['Purple', lambda: changeColor([128,0,128])],
    ['Pink', lambda: changeColor([255,192,203])],
    ['Brown', lambda: changeColor([150, 75, 0])],
    ['Grey', lambda: changeColor([128, 128, 128])],
    ['Brush Larger', lambda: changebrushSize('greater')],
    ['Brush Smaller', lambda: changebrushSize('smaller')],
    ['Custom', lambda: custom()],
    ['Random', lambda: changeColor([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])],
    ['Save', save],
]

# Making the buttons
for index, buttonName in enumerate(buttons):
    Button(index * (buttonWidth + 10) + 10, 10, buttonWidth,
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

    # Drawing the Buttons
    for object in objects:
        object.process()
    # Draw the Canvas at the center of the screen
    x, y = screen.get_size()
    screen.blit(canvas, [x/2 - canvasSize[0]/2, y/2 - canvasSize[1]/2])
    # Drawing with the mouse
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        # Calculate Position on the Canvas
        dx = mx - x/2 + canvasSize[0]/2
        dy = my - y/2 + canvasSize[1]/2
        pygame.draw.circle(
            canvas,
            drawColor,
            [dx, dy],
            brushSize,
        )
    # Reference Dot
    pygame.draw.circle(        screen,
        drawColor,
        [100, 100],
        brushSize,
    )

    pygame.display.flip()
    fpsClock.tick(fps)