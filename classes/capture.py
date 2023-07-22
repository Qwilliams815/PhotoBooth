import pygame
import pygame.camera
from pygame.locals import *

# Camera object that locates and initiates a local camera device
class Capture:
    def __init__(self, display):
        self.size = (1280, 720)

        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()

        self.snapshot = pygame.surface.Surface(self.size, 0, display)

    # Constantly blits new frame to display
    def get_and_flip(self, display):
        if self.cam.query_image():
            self.snapshot = self.cam.get_image()
            display.blit(self.snapshot, (320, 50))

    # Toggles camera colorspace for easy "filter" effects
    def change_filter(self, button):
        self.cam.stop()
        if button == 1:
            self.cam = pygame.camera.Camera(self.clist[0], self.size, "YUV")
            self.cam.start()
        elif button == 2:
            self.cam = pygame.camera.Camera(self.clist[0], self.size, "HSV")
            self.cam.start()
        elif button == 3:
            self.cam = pygame.camera.Camera(self.clist[0], self.size, "RGB")
            self.cam.start()
