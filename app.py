from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import base64
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    data = request.json

    image_data = data['image']
    color = data['color']

    # Decode base64 image
    image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_array = np.array(image)

    # Mask from drawing (white = selected)
    mask = img_array[:, :, 0] > 200  # simple mask logic

    # Convert HEX → RGB
    new_color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))

    result = img_array.copy()
    result[mask] = new_color

    # Convert back to image
    output = Image.fromarray(result)
    buf = io.BytesIO()
    output.save(buf, format="PNG")

    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")

    return jsonify({"image": encoded})


if __name__ == '__main__':
    app.run(debug=True)