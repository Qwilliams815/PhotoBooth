import pygame

countdown_duration = 5000
loop = 0


# Surface object that creates/updates/and displays a countown before each photo.
class Countdown:
    def __init__(self):
        self.countdown_active = False
        self.countdown_start_time = 0
        self.timer_surface = pygame.Surface((400, 550), pygame.SRCALPHA)
        self.font = pygame.font.Font(None, 900)
        self.loop = 0

    # Calculates frame accurate countdown by using pygame's get_ticks() method
    def start_countdown(self, display):
        self.timer_surface.fill((0, 0, 0, 0))

        # Countdown is calculated by subtracting milliseconds passed since
        # intiation from the initial set countdown duration, and displaying
        # the greater of the 2 values.
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.countdown_start_time
        remaining_time = max(countdown_duration - elapsed_time, 0)
        countdown_text = str(int(remaining_time / 1000) + 1)

        # Render the countdown text
        text_surface = self.font.render(countdown_text, True, (255, 255, 255, 0))

        # Blit the countdown text to the display surface
        self.timer_surface.blit(text_surface, (0, 0))
        display.blit(self.timer_surface, (760, 100))

        # If countdown has finished...
        if elapsed_time >= countdown_duration:
            # We dont have to worry about removing countdown text since
            # the font gets covered by a new frame of the camera feed on
            # each display flip.
            self.countdown_active = False

            pygame.display.flip()
            return "done"
