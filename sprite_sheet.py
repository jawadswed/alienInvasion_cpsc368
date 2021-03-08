import pygame as pg


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet"""
        try:
            self.sheet = pg.image.load(filename)
        except pg.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)



    # def image_at(self, rectangle):
    #     """Load an image from the sheet x,y, x+offset, y+offset"""
    #     rect = pg.Rect(rectangle)
    #     image = pg.Surface(rect.size).convert()
    #     image.blit(self.sheet, (0, 0), rect)
    #     return image

    def image_at(self, rectangle, colorkey=None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        # image.blit(self.sheet, (0, 0), rect)
        # if colorkey is not None:
        #     if colorkey is -1:
        #         colorkey = image.get_at((0, 0))
        #     image.set_colorkey(colorkey, pg.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """load all images in a sheet return them as a list"""
        return[self.image_at(rect) for rect in rects]

    def makeSpriteList(self, rows, cols, size):
        """Load a sprite sheet with sprites of size x size pixels organized rows, cols into a list"""
        sprite_rects = []
        sprite_size = size
        for row_num in range(rows):
            for col_num in range(cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = col_num * (sprite_size)
                y = row_num * (sprite_size)
                sprite_rect = (x, y, sprite_size, sprite_size)
                sprite_rects.append(sprite_rect)

        return self.images_at(sprite_rects)
