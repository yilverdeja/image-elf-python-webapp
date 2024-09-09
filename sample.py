from PIL import Image, ImageDraw

# color tuples
ELF_GREEN_TUPLE = (102, 255, 102)
WHITE_TUPLE = (255, 255, 255)

# get xy location for the central placement of the text
def get_central_placement_loc(im_draw: ImageDraw, width, height, text, font_size):
    left, top, right, bottom = im_draw.textbbox((0, 0), text, font_size=font_size)
    x = (int(width) / 2) - ((right - left) / 2)
    y = (int(height) / 2) - ((bottom - top) / 2)
    return (x, y)

def main():
    # get image size
    height = input("Input height in pixels: ")
    width = input("Input width in pixels: ")
    
    # create new image with size and color
    im = Image.new(mode="RGB", size=(int(width), int(height)), color=ELF_GREEN_TUPLE)
    
    # create text and calculate font size
    size_text = f"{width} x {height}"
    font_size = min(int(height), int(width)) / 10
    
    # draw text in the center
    im_draw = ImageDraw.Draw(im)
    xy_loc = get_central_placement_loc(im_draw, int(width), int(height), size_text, font_size)
    im_draw.text(xy_loc, size_text, fill=WHITE_TUPLE, font_size=font_size)
    
    # show image
    im.show()

if __name__ == "__main__":
    main()