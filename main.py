import pygame
import pygame.camera
from pygame.locals import *

from classes.button import Button
from classes.capture import Capture
from classes.countdown import Countdown


pygame.init()
pygame.camera.init()
clock = pygame.time.Clock()


pygame.display.set_caption("SOS PhotoBooth")
display_width, display_height = 1920, 1080
display = pygame.display.set_mode((display_width, display_height), 0, pygame.SRCALPHA)

# Create color gradient background for display
gradient_start_color = (27, 27, 27)  # RGB value for #1B1B1B
gradient_end_color = (58, 58, 58)  # RGB value for #3A3A3A

# Create the main window with alpha channel support
display = pygame.display.set_mode((display_width, display_height), pygame.SRCALPHA)

# Calculate the number of steps for the gradient
gradient_steps = display_height
display.fill(gradient_start_color)
# Calculate the incremental change for each RGB component
r_step = (gradient_end_color[0] - gradient_start_color[0]) / gradient_steps
g_step = (gradient_end_color[1] - gradient_start_color[1]) / gradient_steps
b_step = (gradient_end_color[2] - gradient_start_color[2]) / gradient_steps
# Draw the gradient on the display
for step in range(gradient_steps):
    color = (
        int(gradient_start_color[0] + r_step * step),
        int(gradient_start_color[1] + g_step * step),
        int(gradient_start_color[2] + b_step * step),
        255,  # Set alpha value to 255 (fully opaque)
    )
    pygame.draw.rect(
        display,
        color,
        (
            0,
            step * (display_height // gradient_steps),
            display_width,
            display_height // gradient_steps,
        ),
    )


new_capture = Capture(display)
new_countdown = Countdown()

# Populate display with buttons and graphics
fxButton1 = Button(1650, 50, pygame.image.load("buttons/FX_1.png").convert_alpha(), 1)
fxButton2 = Button(1650, 325, pygame.image.load("buttons/FX_2.png").convert_alpha(), 1)
fxButton3 = Button(1650, 600, pygame.image.load("buttons/FX_3.png").convert_alpha(), 1)
shutterButton = Button(
    847, 800, pygame.image.load("buttons/shutter.png").convert_alpha(), 1
)
display.blit(pygame.image.load("buttons/blank_photostrip.png"), (30, 50))
display.blit(pygame.image.load("buttons/sos_banner.png"), (20, 800))


# Blits current new_capture frame to photo strip
def snapPhoto(photoID):
    image = new_capture.cam.get_image()
    scaled_image = pygame.transform.scale(image, (355, 200))
    if photoID == 0:
        display.blit(scaled_image, (10, 50), (27, 0, 300, 200))
    elif photoID == 1:
        display.blit(scaled_image, (10, 330), (27, 0, 300, 200))
    elif photoID == 2:
        display.blit(scaled_image, (10, 610), (27, 0, 300, 200))


# Game Loop
loop = 0
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    # Constantly update display with live camera feed
    new_capture.get_and_flip(display)

    # Initiates countdown
    if shutterButton.clicked_on(display):
        new_countdown.countdown_active = True
        new_countdown.countdown_start_time = pygame.time.get_ticks()

    # Starts countdown and takes photo on loop until 3 photos have been blited to display
    if new_countdown.countdown_active:
        if new_countdown.start_countdown(display) == "done":
            new_capture.snapshot.fill((255, 255, 255))
            display.blit(new_capture.snapshot, (320, 50))
            pygame.display.flip()
            snapPhoto(loop)
            pygame.time.wait(2000)
            if loop < 2:
                new_countdown.countdown_active = True
                new_countdown.countdown_start_time = pygame.time.get_ticks()

                loop += 1
            else:
                loop = 0

    # FX button handlers
    if fxButton1.clicked_on(display):
        new_capture.change_filter(1)

    elif fxButton2.clicked_on(display):
        new_capture.change_filter(2)

    elif fxButton3.clicked_on(display):
        new_capture.change_filter(3)
    pygame.display.flip()


# Stop the camera and quit Pygame
new_capture.cam.stop()
pygame.quit()
