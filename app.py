import os
from flask import Flask, jsonify, redirect, render_template, request, send_file, send_from_directory
import image_types as ImageTypes

# constants
MAX_PIXELS = 50000
ELF_GREEN_COLOR = "#2ae5bc"
WHITE_COLOR = "white"
IMAGE_TYPES = ["png", "jpeg", "webp", "gif", "bmp", "tiff", "ico"]

selected_image_type: ImageTypes.ImageType = ImageTypes.PNG()

# validate form
def validate_form(image_width: str, image_height: str, image_type: str):
    global selected_image_type
    errors = {}
    max_width = max_height = MAX_PIXELS
    
    if image_type.lower() not in IMAGE_TYPES:
        errors['type'] = "Unsupported image type"
    else:
        limits = selected_image_type.get_config_limits()
        max_width = min(MAX_PIXELS, limits["max_width"])
        max_height = min(MAX_PIXELS, limits["max_height"])
    
    print(max_width, max_height)
    
    try:
        width = int(image_width)
        if width <= 0 or width > max_width:
            raise ValueError(f"Width must be a positive integer between 1 and {max_width}")
    except ValueError as e:
        errors['width'] = str(e)
    
    try:
        height = int(image_height)
        if height <= 0 or height > max_height:
            raise ValueError(f"Height must be a positive integer between 1 and {max_height}")
    except ValueError as e:
        errors['height'] = str(e)
    
    return errors

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
        im = selected_image_type.create(mode="RGB", width=image_width, height=image_height)
        
        # save & download image
        file_args = selected_image_type.save_image_as_file(im)
        return send_file(**file_args)
    
    return render_template('index.html')

@app.route('/updateImageType', methods=['POST'])
def update_image_type():
    global selected_image_type  # declare that we're using the global variable
    data = request.get_json()
    image_type = data['imageType'].lower() if data else ""
    if image_type == "png": 
        selected_image_type = ImageTypes.PNG()
    elif image_type == "jpeg": 
        selected_image_type = ImageTypes.JPEG()
    elif image_type == "gif": 
        selected_image_type = ImageTypes.GIF()
    elif image_type == "webp": 
        selected_image_type = ImageTypes.WebP()
    elif image_type == "bmp": 
        selected_image_type = ImageTypes.BMP()
    elif image_type == "tiff": 
        selected_image_type = ImageTypes.TIFF()
    elif image_type == "ico": 
        selected_image_type = ImageTypes.ICO()
    else:
        return jsonify({'error': 'Invalid image type'}), 400

    config_limits = selected_image_type.get_config_limits()
    config_limits["max_width"] = min(MAX_PIXELS, config_limits["max_width"])
    config_limits["max_height"] = min(MAX_PIXELS, config_limits["max_height"])
    return jsonify(config_limits)

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