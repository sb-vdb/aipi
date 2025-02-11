# Install

## Install Python Dependencies

In Python, dependencies must be pre-installed at a location, that can be found by the Python Runtime (sounds logical, but is not trivial). For this, we will use a virtual environment, which is basically a created directory with a Python copy in a specific version and all Python-dependencies (we need) installed next to it. With this, we can retain an isolated environment that is not affected by system-wide uses of Python. At the same time, when activating this environment, our Shell will act like this is the default system Python - hence, allows us to use our specific Python version with the `python3` command, without providing a path to the specific environment's python executable. We will use Python's `venv` module to create such an environment.

```bash
python3 -m venv venv
```

This will create a folder named `venv/`, named after the name of the environment we gave as the last argument. We could use anything we like, actually, but I'll keep it self-describing at this point. Also, that name in a project folder is very unlikely to collide with something else. Next, we will use `pip` to install dependencies into our environment.

But before we install stuff, we have to activate the virtual environment, so python and friends know *where* to install and find stuff:
```bash
source venv/bin/activate
```
You should now see the name of the virtual environment in brackets right in front of your command line prompt.

Now we can install our dependencies. In general, `pip install <dependency-name>` does the job for each dependency. But for a larger number of dependencies, we can also use a file to let `pip` know about what we want to install:
```bash
pip install -r requirements.txt 
```
If everything succeeded up until this point, Jupyter and everything Python is ready to go.


## Install Ollama
According to this [Issue](https://github.com/ollama/ollama/issues/7733), there is a bug in newer versions of Ollama, that prevents you from running multi-modal models with image input efficiently (enough) on a Raspberry Pi.

If you want to use image inputs as well, you have to install a specific version. Version 0.3.9 works fine for all the demos of this repo:
```bash
curl -fsSL https://ollama.com/install.sh | OLLAMA_VERSION=0.3.9 sh
```

Otherwise, you may just install the newest version:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## [Continue](README.md#start-services)