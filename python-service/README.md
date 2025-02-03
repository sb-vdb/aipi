# Python Dependencies & HTTP Endpoint

**PyTorch** is a library for Python that runs AI models on your hardware.

**Diffusers**, developed by Hugging Face, is a library to manage and use its' Diffuser models (e.g. used for Image Generation).

The **Transformers** library, is a pendant to ``Diffusers`` but for Transformers (e.g. used for generative Language Models)

**FastAPI** is a lightweight framework, that supersedes `Flask` in this repo, as `FastAPI` is working better with asynchronous streams. Both libraries provide a HTTP endpoint to send data to and receives responses from.

While the dependencies are used by both the Jupyter Lab frontend and the Web frontend, they both use it differently. Jupyter Lab can use Python dependencies natively. But for the web frontend we need to wrap them into something accessible - in our case, an HTTP API.

## Install Dependencies

If you followed the Jupyter-frontend guide, you were already guided here. If you followed these steps, then you do not need to repeat this.

In Python, dependencies must be pre-installed at a location, that can be found by the Python Runtime (sounds logical, but is not trivial). For this, we will use a virtual environment, which is basically a created directory with a Python copy in a specific version and all Python-dependencies (we need) installed next to it. With this, we can retain an isolated environment that is not affected by system-wide uses of Python. At the same time, when activating this environment, our Shell will act like this is the default system Python - hence, allows us to use our specific Python version with the `python3` command, without providing a path to the specific environment's python executable. We will use Python's `venv` module to create such an environment.

In the top-level folder of this repo, run:
```
python3 -m venv venv
```

This will create a folder named `venv/`, named after the name of the environment we gave as the last argument. We could use anything we like, actually, but I'll keep it self-describing at this point. Also, that name in a project folder is very unlikely to collide with something else. Next, we will use `pip` to install dependencies into our environment.

But before we install stuff, we have to activate the virtual environment, so python and friends know *where* to install and find stuff. From your top-level repo folder, run:
```
source venv/bin/activate
```
You should now see the name of the virtual environment in brackets right in front of your command line prompt.

Now we can install our dependencies. In general, `pip install <dependency-name>` does the job for each dependency. But for a larger number of dependencies, we can also use a file to let `pip` know about what we want to install. Navigate to the top-level of this repo, where the `requirements.txt` file resides and run:
```
pip install -r requirements.txt 
```
If everything succeeded up until this point, Jupyter and everything Python is ready to go.

## Start HTTP Endpoint

You can skip this step, if you want to only use the Jupyter frontend, as the Python HTTP endpoint is only needed by the web frontend. 

First, navigate to the top-level folder of the repo and activate your environment, if not already done:
```
source venv/bin/activate
```

To now run the server:
```
python3 python-service/src/service.py

// if started via SSH
python3 python-service/src/service.py &; disown
```
