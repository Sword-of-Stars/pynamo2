import pygame

from PIL import Image
import pygame

class Animation():
    def __init__(self, looping, frames, layer, rect):
        self.level = layer
        self.rect = rect

        self.looping = looping
        self.frames = frames
        self.num_frames = len(frames)
        self.current_frame = 0

        self.FPS = 15

        self.alive = True

    def play(self):
        # plays the animation, advancing igf appropriate
        self.alive = True
        self.current_frame += 1/self.FPS

        if self.current_frame > self.num_frames:
            if self.looping:
                self.current_frame = 0
            else:
                self.stop()

    def stop(self):
        self.current_frame = self.num_frames - 1

    def draw(self, camera, pos, flip=False):
        if self.alive:
            img = self.frames[int(self.current_frame)%self.num_frames]
            img = pygame.transform.flip(img, flip, False)
            camera.display.blit(img, pos)

def extract_spritesheet(filepath, sprite_width, sprite_height, loops, rect, titles=None):
    sprite_sheet = pygame.image.load(filepath).convert_alpha()
    sheet_width, sheet_height = sprite_sheet.get_size()

    cols = sheet_width // sprite_width
    rows = sheet_height // sprite_height

    animations = {}

    for row in range(rows):
        row_frames = []
        for col in range(cols):
            rect = pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height)
            frame = sprite_sheet.subsurface(rect).copy()

            frame = pygame.transform.scale_by(frame, 4).convert_alpha()

            # Check if frame is not completely transparent
            if pygame.surfarray.pixels_alpha(frame).max() > 0:
                row_frames.append(frame)

        if row_frames:
            if titles == None:
                animations[f"anim_row{row}"] = Animation(loops[row], row_frames, 5, rect)
            else:
                animations[f"{titles[row]}"] = Animation(loops[row], row_frames, 5, rect)

    return animations