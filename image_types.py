from abc import ABC, abstractmethod
from PIL import Image, ImageDraw
from io import BytesIO

DEFAULT_BG_COLOR = "#2ae5bc"
DEFAULT_TEXT_COLOR = "#ffffff"

def get_centralized_image_text_location(im_draw: ImageDraw, width: int, height: int, text: str, font_size: int):
    left, top, right, bottom = im_draw.textbbox((0, 0), text, font_size=font_size)
    x = (width / 2) - ((right - left) / 2)
    y = (height / 2) - ((bottom - top) / 2)
    return (x, y)

class ImageType(ABC):
    
    def __init__(self, image_type, image_format):
        self.image_type = image_type
        self.image_format = image_format
    
    def get_config_limits(self):
        return {
            "min_width": 1,
            "max_width": 10000,
            "min_height": 1,
            "max_height": 10000
        }
    
    @abstractmethod
    def calculate_file_size(self, width, height, mode):
        pass
    
    def create(self, mode, width, height, bg_color=DEFAULT_BG_COLOR, draw_text=True, custom_text=None, text_color=DEFAULT_TEXT_COLOR):
        # create new image with size and color
        im = Image.new(mode=mode, size=(width, height), color=bg_color)
        
        if draw_text:
            # create text and calculate font size
            if custom_text != None: image_text = custom_text
            else: image_text = f"{width} x {height}"
            font_size = int(min(width, height) / 10)
            
            # draw text in the center
            if font_size > 0:
                im_draw = ImageDraw.Draw(im)
                xy_loc = get_centralized_image_text_location(im_draw, width, height, image_text, font_size)
                im_draw.text(xy_loc, image_text, fill=text_color, font_size=font_size)
        
        return im
    
    def save_image_as_file(self, im: Image):
        stream = BytesIO()
        im.save(stream, self.image_format)
        stream.seek(0)
        return {
            "path_or_file": stream,
            "mimetype": f'image/{self.image_type}',
            "as_attachment": True,
            "download_name": f'_ImgElf.{self.image_type}'
        }

class PNG(ImageType):
    def __init__(self):
        image_type = "png"
        super().__init__(image_type, image_type.upper())
    
    def get_config_limits(self):
        return {
            "min_width": 1,
            "max_width": 100000,
            "min_height": 1,
            "max_height": 100000
        }

    def calculate_file_size(self, width, height, mode):
        # Approximation for PNG using typical compression efficiency
        bpp = {'1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32}.get(mode, 24)  # Default to 24 bits for RGB
    

class JPEG(ImageType):
    def __init__(self):
        image_type = "jpeg"
        super().__init__(image_type, image_type.upper())
    
    def get_config_limits(self):
        return {
            "min_width": 1,
            "max_width": 65535,
            "min_height": 1,
            "max_height": 65535
        }

    def calculate_file_size(self, width, height, mode):
        # Simplified estimation: JPEG compression can be roughly estimated for typical quality settings
        return int(width * height * len(mode) * 0.15)  # Simplified approach using a constant factor

class GIF(ImageType):
    def __init__(self):
        image_type = "gif"
        super().__init__(image_type, image_type.upper())
    
    def get_config_limits(self):
        return {
            "min_width": 1,
            "max_width": 10000,
            "min_height": 1,
            "max_height": 10000
        }

    def calculate_file_size(self, width, height, mode):
        # GIF uses a palette, so file size depends on the number of colors in the palette
        return width * height * 8  # Assuming 256 colors (8 bits per pixel)

class WebP(ImageType):
    def __init__(self):
        image_type = "webp"
        super().__init__(image_type, image_type.upper())
    
    def get_config_limits(self):
        return {
            "min_width": 1,
            "max_width": 16383,
            "min_height": 1,
            "max_height": 16383
        }

    def calculate_file_size(self, width, height, mode):
        return int(width * height * len(mode) * 0.2)  # WebP is more efficient than JPEG

class TIFF(ImageType):
    
    def __init__(self):
        image_type = "tiff"
        super().__init__(image_type, image_type.upper())
    
    def get_config_limits(self):
        return {
            "min_width": 1,
            "max_width": 30000,  # Commonly used limit for software compatibility
            "min_height": 1,
            "max_height": 30000
        }

    def calculate_file_size(self, width, height, mode):
        return width * height * len(mode)  # TIFF is often uncompressed

class ICO(ImageType):
    def __init__(self):
        image_type = "ico"
        super().__init__(image_type, image_type.upper())
    
    def get_config_limits(self):
        return {
            "min_width": 16,
            "max_width": 256,
            "min_height": 16,
            "max_height": 256
        }

    def calculate_file_size(self, width, height, mode):
        # Simplified estimation for ICO, considering multiple sizes might be stored
        bpp = {'1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32}.get(mode, 32)  # ICOs often include alpha
        return int(width * height * bpp / 8)

class BMP(ImageType):
    def __init__(self):
        image_type = "bmp"
        super().__init__(image_type, image_type.upper())

    def get_config_limits(self):
        # BMP can technically support very large widths, should be adjusted
        return {
            "min_width": 1,
            "max_width": 10000,
            "min_height": 1,
            "max_height": 10000 
        }

    def calculate_file_size(self, width, height, mode):
        # Simplified estimation for BMP, which does not compress pixel data
        bpp = {'1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32}.get(mode, 24)  # Default to 24-bit for RGB
        stride = (width * bpp + 31) // 32 * 4  # Row size must be a multiple of 4 bytes
        return int(height * stride)