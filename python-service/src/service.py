from flask import Flask, request, jsonify, Response
import lib
from diffusers.utils import logging

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')
    filename = data.get('filename')

    if not prompt or not filename:
        return jsonify({"error": "Missing prompt or filename"}), 400

    return Response(lib.generate_image_with_progress(prompt, filename), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
    logging.disable_progress_bar()