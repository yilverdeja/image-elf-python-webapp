import os
from flask import Flask, jsonify, redirect, render_template, request, send_file, send_from_directory
from PIL import Image, ImageDraw
from io import BytesIO

# constants
ELF_GREEN_TUPLE = (102, 255, 102)
WHITE_TUPLE = (255, 255, 255)
IMAGE_TYPES = ["png", "jpeg"]

# validate form
def validate_form(image_width: str, image_height: str, image_type: str):
    errors = {}
    try:
        width = int(image_width)
        if width <= 0:
            raise ValueError("Width must be a positive integer")
    except ValueError as e:
        errors['width'] = str(e)
    
    try:
        height = int(image_height)
        if height <= 0:
            raise ValueError("Height must be a positive integer")
    except ValueError as e:
        errors['height'] = str(e)
    
    if image_type.lower() not in IMAGE_TYPES:
        errors['type'] = "Unsupported image type"
    
    return errors

# get xy location for the central placement of the text
def get_central_placement_loc(im_draw: ImageDraw, width: int, height: int, text: str, font_size: int):
    left, top, right, bottom = im_draw.textbbox((0, 0), text, font_size=font_size)
    x = (width / 2) - ((right - left) / 2)
    y = (height / 2) - ((bottom - top) / 2)
    return (x, y)

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def create_image():
    if request.method == 'POST':
        image_width = request.form.get("imageWidth", "")
        image_height = request.form.get("imageHeight", "")
        image_type = request.form.get("imageType", "").lower()
        
        errors = validate_form(image_width, image_height, image_type)
        if errors:
            return render_template('index.html', errors=errors, imageWidth=image_width, imageHeight=image_height, imageType=image_type)
        
        # get image size
        image_width = int(image_width)
        image_height = int(image_height)
        image_type = image_type.lower()
        
        # create new image with size and color
        im = Image.new(mode="RGB", size=(image_width, image_height), color=ELF_GREEN_TUPLE)
        
        # create text and calculate font size
        size_text = f"{image_width} x {image_height}"
        font_size = int(min(image_width, image_height) / 10)
        
        # draw text in the center
        if font_size > 0:
            im_draw = ImageDraw.Draw(im)
            xy_loc = get_central_placement_loc(im_draw, image_width, image_height, size_text, font_size)
            im_draw.text(xy_loc, size_text, fill=WHITE_TUPLE, font_size=font_size)
       
        # save image
        stream = BytesIO()
        im.save(stream, image_type.upper())
        stream.seek(0)
        return send_file(stream, mimetype=f'image/{image_type}', as_attachment=True, download_name=f'_imgelf.{image_type}')
    
    return render_template('index.html')

# handle favicon redirect
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

# handle page not found
@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)