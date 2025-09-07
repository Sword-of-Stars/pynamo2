import pygame

from .gui_elements import gui, Page, Region
from .misc.debugging_utils import TracePrints

#===== Initilaize GUI =====#
Region.set_gui_builder(gui)
Page("config/page1")
Page("config/page2")
gui.current_page = "main"
gui.init_builder()

pygame.font.init()
