import os, re
from PIL import Image, ImageFont



class CharacterExtractor:
    def __init__(self, font_path, output_dir, desired_characters, point_size=32, background_color=(255, 255, 255, 0), font_color=(0, 0, 0, 255)):
        self.font_path = font_path
        self.output_dir = output_dir
        self.desired_characters = desired_characters
        self.point_size = point_size
        self.background_color = self._convert_color(background_color)
        self.font_color = self._convert_color(font_color)

        self.font = ImageFont.truetype(self.font_path, self.point_size)


    @staticmethod
    def _create_dir(path, option):
        # Create a directory if it does not exist
        os.makedirs(path, exist_ok=option)


    @staticmethod
    def _convert_color(color):
        # Convert color to RGBA format
        if isinstance(color, str) and color.startswith("#"):
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
        raise ValueError("Invalid color format. Please provide a valid hex color code or RGBA tuple.")


    @staticmethod
    def _sanitize_filename(filename, path, extension=".png"):
        # Replace invalid characters with "invalid_<num>"
        sanitized_filename = re.sub(r'[\\/:;\*\?"<>|!@#$%^&*()+=,{}`~\'\[\]\r\n\t]', 'invalid_0', filename)

        # Handle filenames starting with periods
        # _1 is just a placeholder, loop will handle value increment
        if sanitized_filename.startswith('.'):
            sanitized_filename = 'invalid_1' + sanitized_filename.strip(".")

        # Append a counter to handle multiple sanitizations
        counter = 1
        original_sanitized_filename = sanitized_filename.replace("0", "")
        while os.path.exists(os.path.join(path, sanitized_filename + extension)):
            sanitized_filename = original_sanitized_filename + str(counter)
            counter += 1

        return sanitized_filename


    def extract_characters(self):
        self._create_dir(self.output_dir, True)

        for char in self.desired_characters:
            image = Image.Image()._new(self.font.getmask(char))
            image_with_background = Image.new("RGBA", image.size, self.background_color)

            # Create an image with font color
            image_with_font_color = Image.new("RGBA", image.size, (0, 0, 0, 0))
            font_color_image = Image.new("RGBA", image.size, self.font_color)
            image_with_font_color.paste(font_color_image, (0, 0), image)

            # Composite the font color image with the background image
            final_image = Image.alpha_composite(image_with_background, image_with_font_color)

            # Sanitize the filename
            sanitized_char = self._sanitize_filename(char, self.output_dir)

            file_path = os.path.join(self.output_dir, sanitized_char + ".png")
            final_image.save(file_path)
            print(f"Saved {char} as: {sanitized_char}.png")



# Usage example
if __name__ == "__main__":
    font_path = "megu.ttf"
    output_dir = "./output/"
    desired_characters = "!@#$%^&*()0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    point_size = 64
    background_color = "#FFFFFF00"  # Hex color code with alpha channel

    extractor = CharacterExtractor(font_path, output_dir, desired_characters, point_size, background_color=background_color)
    extractor.extract_characters()