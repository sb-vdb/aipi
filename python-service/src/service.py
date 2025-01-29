from flask import Flask, request, jsonify, Response, stream_with_context
import lib
import subprocess
import os
import pathlib

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')
    filename = data.get('filename')

    if not prompt or not filename:
        return jsonify({"error": "Missing prompt or filename"}), 400
    
    #write prompt to file for the model runner to parse
    with open("prompt.txt", "w") as f:
        f.write(prompt + "\n" + filename)

    if not pathlib.Path("output").exists():
        os.mkdir("output")
    for file in pathlib.Path(".").glob("output/*"):
        os.remove(file)
    if pathlib.Path("stderr.log").exists():
        os.remove("stderr.log")
    if pathlib.Path("stdout.log").exists():
        os.remove("stdout.log")

    # trigger parallel model execution
    subprocess.Popen(["python3", "python-service/src/sd_runner.py"], stderr=open("stderr.log", "w"), stdout=open("stdout.log", "w"))

    # response is a stream of progress messages, polled every second from buffer files
    return Response(stream_with_context(lib.buffer_generator()), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)