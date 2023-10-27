from Classes.Common import *



class CharacterExtractor:
    def __init__(self, font_path, desired_characters, point_size=32, background_color=(255, 255, 255, 0), font_color=(0, 0, 0, 255)):
        self.font_path = font_path
        self.desired_characters = desired_characters
        self.point_size = point_size
        self.background_color = self._convert_color(background_color)
        self.font_color = self._convert_color(font_color)

        self.font = ImageFont.truetype(self.font_path, self.point_size)


    @staticmethod
    def _convert_color(color):
        if isinstance(color, str) and color.startswith("rgba("):
            # Handle rgba string input
            color = color.lstrip("rgba(").rstrip(")")
            components = color.split(",")
            if len(components) == 4:
                return tuple(int(component.strip()) for component in components)
        elif isinstance(color, str) and color.startswith("RGBA("):
            # Handle rgba string input
            color = color.lstrip("RGBA(").rstrip(")")
            components = color.split(",")
            if len(components) == 4:
                return tuple(int(component.strip()) for component in components)
        elif isinstance(color, str) and color.startswith("#"):
            # Handle hex color code
            color = color.lstrip("#")
            if len(color) == 6:
                return tuple(int(color[i:i+2], 16) for i in (0, 2, 4)) + (255,)
            elif len(color) == 8:
                return tuple(int(color[i:i+2], 16) for i in (0, 2, 4, 6))
        elif isinstance(color, tuple) and len(color) == 3:
            # Handle RGB tuple
            return color + (255,)
        elif isinstance(color, tuple) and len(color) == 4:
            # Handle RGBA tuple
            return color
        # Raise an error for invalid color format
        raise ValueError("Invalid color format. Please provide a valid hex color code, RGBA tuple, or rgba string.")


    def extract_characters(self, char):
        # loop through charlist
        image = Image.Image()._new(self.font.getmask(char))
        image_with_background = Image.new("RGBA", image.size, self.background_color)

        # Create an image with font color
        image_with_font_color = Image.new("RGBA", image.size, (0, 0, 0, 0))
        font_color_image = Image.new("RGBA", image.size, self.font_color)
        image_with_font_color.paste(font_color_image, (0, 0), image)

        # Composite the font color image with the background image
        self.final_image = Image.alpha_composite(image_with_background, image_with_font_color)

        return self.final_image