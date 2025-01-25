# Ollama

[Ollama](https://github.com/ollama/ollama) is a platform that acts basically as a language model runtime, model download manager and as web server to send and receive text streams via HTTP web requests. It can run on a Raspberry Pi 5 is perfect to be accessed over the network.

It is managed through command line, but once it runs, its' HTTP endpoint makes it easily integrateable with arbitrary frontends. In your request's body, you simply define the model's name, the prompt as a string, and additional data (like image data for multi modal models) attached as certain text representations (base64 in the case of images) and send it. The server will then spin up the model (download weights first, if necessary) and run your request in it. You may stream every resulting token piece by piece, or wait for the whole request to finish.

This repos also provides two prepared frontends, that deal with all of that.

## Install

According to this [Issue](https://github.com/ollama/ollama/issues/7733), there is a bug in newer versions of Ollama, that prevents you from running multi-modal models with image input efficiently (enough) on a Raspberry Pi.

If you want to use image inputs as well, you have to install a specific version. Version 0.3.9 works fine for all the demos of this repo:
```
curl -fsSL https://ollama.com/install.sh | OLLAMA_VERSION=0.3.9 sh
```

Otherwise, you may just install the newest version:
```
curl -fsSL https://ollama.com/install.sh | sh
```

## Start

Which command to use, to startup the Ollama server depends on whether you controlling the Raspi remotely via SSH:

```
// from SSH connected to the Raspi
ollama serve &; disown

// locally from the Raspi
ollama serve
```



## Usage

### Locally via Ollama CLI

Whether you need to manually start you server as above depends on the system, you are installing Ollama on. Try ``ollama list`` to test.

You can run any model available with a simple Ollama command, either just with a single prompt, or interactively awaiting prompts until you close it:

```
// Single prompt with a single result
ollama run "phi3-mini" "why is the sky blue"
```

```
// Interactive mode 
ollama run "phi3-mini"
```

### With Jupyter Notebooks

Ollama models can be used with the provided Notebooks in this repo. To use the Notebooks, you need to [set up](../frontend/jupyter/README.md) the Jupyter Lab frontend first.

Use this, if you want to explore more than just the varieties of Ollama models or want to stick to common data science workflows.

After that, inside the Notebooks, a simple HTTP Request is sent, using standard Python libraries, and its result is used. Below is an example on how to use Python to communicate with Ollama: 

```
import requests     # standard Python library

data = {
    "model": "llama3.2",
    "prompt": "why is the sky blue?"
}

result = requests.post(url, json=data, stream=stream)
```

The returned element is also a typical response object, as we know it from Python. However, the shape of the returned data depends on whether you are streaming the result or are awaiting the finished result. In the first case, you can simply access the latest response item as a JSON-object, extracting your AI-generated token. If you dont stream, however, it will simply concatenate the token record's JSON-representation into a single String, that can not be automatically converted back to JSON (because of missing commas). Hence, some extra logic is requred to extract the actual tokens, as seen in the `lib.py` file.

### With Web Frontend

This way is supposed to be most streamlined way to just use the models. The web frontend is available wherever the Raspberry Pi is accessible via network. To use it, you have to setup the Web Frontend first.

The web frontend is based on common web technologies (JavaScript) and uses standard libraries to access Ollama, just as Jupyter Notebooks in the shape as shown above.