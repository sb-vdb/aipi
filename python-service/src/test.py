import lib
import subprocess
import pathlib
import os

if __name__ == '__main__':

    with open("buffer.txt", "w") as f:
        f.write("0")

    with open("prompt.txt", "w") as f:
        f.write("a cat" + "\n" + "cat.png")

    for file in pathlib.Path(".").glob("output/*"):
        os.remove(file)
    # trigger model execution
    subprocess.Popen(["python3", "python-service/src/sd_runner.py"])
    #stderr=open("error.txt", "a"), stdout=open("stdout.txt", "a")

    for message in lib.buffer_generator():
        print(message)
