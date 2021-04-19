import pygame.font

class Button():
    def __init__(self, ai_stts, screen, msg, pos_x, pos_y):
        """Initialize button attributes.
        :param screen: Main window of app
        :type screen: pygame.Surface
        """
        self.screen = screen
        self.screen_rect = screen.get_rect() # type: pygame.Rect

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = ( 255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        #self.rect.center = self.screen_rect.center
        #self.rect.centerx = self.screen_rect.width / 2
        #self.rect.centery += self.screen_rect.height / 4

        # We place the button to the new coords.
        self.move_button_to(pos_x, pos_y)

        # The button message needs to be prepped only once.
        self.prep_msg(msg)  # Pygame works with text by rendering the string you want to display as an image.

    def move_button_to(self, pos_x, pos_y ):
        """We move the button to the new coords, we are using pivot center."""
        self.rect.centerx = pos_x
        self.rect.centery = pos_y
        pass

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        # True antialiasing makes the edges of the text smoother.
        # We dont include a background color (button's), render with transparent background.
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)          # First, we draw the button
        self.screen.blit(self.msg_image, self.msg_image_rect)   # Second, we draw the text over the button