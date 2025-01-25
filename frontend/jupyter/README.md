# JupyterLab IDE

This frontend provides a ready-to-go setup of Demos in prepared notebooks (``.ipynb``).

The frontend is used via the browser and is served via a service process that needs to be run on the Raspberry Pi that also runs the models.

Use this frontend, if you want to develop or explore in more detail, as its' architecture is heavier and more error-prone than the web frontend.

## Install

Since JupyterLab is based on Python, it requires a configured Python environment. For simplicity, all Python stuff is shared via a single maintained environment. So, if you haven't already, see the [Python Dependency](../../python-service/README.md) guide.

## Start

First, navigate to the top-level repo directory.

Then, activate the shared Python environment:
```
source venv/bin/activate
```

To start the server, run the following command:
```
jupyter-lab --ip=0.0.0.0 --no-browser --notebook-dir="demos"
```

`--ip=0.0.0.0` enables the server to be addressed externally

`--no-browser` prevents the server from opening a browser on-device

`--notebook-dir="demos"` sets the folder "demos" as root project folder


## Use

In the terminal you'll be shown URLs that can be used to access the frontend from the browser. If you have started the server via SSH, use the address with your Raspi's device name in it.

