# aipi

This repository showcases AI model deployments on a Raspberry Pi 5 using Ollama and JupyterLab with PyTorch. Both platforms allow remote interaction with models running on the Raspberry Pi.

To setup the Raspberry Pi, [go here](RASPBERRYPI.md).

## Demos
Aipi uses two ways to serve AI models. One is Ollama, a program that is repository client, model runner and API endpoint, all in one. The other is PyTorch, a Python framework being a defacto standard for AI ecosystems.

Ollama proved to be very convenient to use out of the box and is well-populated with noteworthy models. However, Ollama only serves LMs and the choice is not exhaustive.

### Simple Chat
As we know it from ChatGPT: send a prompt text to it and receive a text back. On top of that, multi-modal models are able to process more than just input text. In our demo, ``Moondream`` may also be used to discuss images.

Ollama models tested:
- Phi3 3.8B
- Llama3.2 3.8B
- Codellama 7B
- Moondream (multi-modal)
- DeepSeek-r1 7B

Ollama models may also be customized and derived into [custom models](ollama/README.md). A common use case is to configure a model (temperature = 0) to only produce predictable outputs.
  
PyTorch models tested:
- LläMmlein 1B (Transformers library)

### Image Generation
Two typical text-to-image pipelines; with SDXL-Turbo demonstrating how some models bigger than the Raspberry Pi 5's RAM can be hacked to run.
512x512px, SDv1.5 runs 30 minutes (50 denoising steps) and the SDXL runs about 2 hours.

PyTorch:
- Stable Diffusion v1.5 (Diffusers library)
- SDXL-Turbo (Diffusers library)

## Setup
See here, on how to [install the dependencies](./INSTALL.md)

## Start Services
If you have setup the services (Ollama and JupyterLab), you still need to run them:

### Start ``Ollama``
Which commands to use, to startup the Ollama server depends on whether you controlling the Raspi remotely via SSH:

```
// from SSH connected to the Raspi
ollama serve & disown

// locally from the Raspi
ollama serve
```

### Start ``JupyterLab``
First, navigate to the top-level repo directory.

Then, activate the shared Python environment:
```
source venv/bin/activate
```

To start the server, run the following command:
```
jupyter-lab --ip=0.0.0.0 --no-browser --notebook-dir="jupyter"

// from SSH connected to the Raspi
jupyter-lab --ip=0.0.0.0 --no-browser --notebook-dir="jupyter" & disown
```

`--ip=0.0.0.0` enables the server to be addressed externally

`--no-browser` prevents the server from opening a browser on-device

`--notebook-dir="frontend/jupyter"` sets the folder "frontend/jupyer" as root project folder in the IDE

After you run one of the startup-commands, you cann see the process' output in the Terminal. Wait until it displays the URLs you can use to access the IDE via the Browser. Take the one with the device name, that you gave during the Raspis setup, inside the URL.

## Alternative ways to interact with Ollama only
Ollama is already well-integrated into common environments. For classic desktops we can use `Chatboxai` for a full-fledged chat experience and in the Terminal we can have a text dialogue via ``Ollama`` itself.

### Use ``Chatboxai``
See website: https://www.chatboxai.app/en
Chatboxai is a local desktop application that supports a range of AI-APIs, most natively the OpenAI API. It also supports the Ollama-API, so you can just pass it your Ollama Service-URL in the App's settings.

### Use CLI
You can run any model available with a simple Ollama command, either just with a single prompt, or interactively awaiting prompts until you close it:

```
// Single prompt with a single result
ollama run "phi3-mini" "why is the sky blue"
```

```
// Interactive mode 
ollama run "phi3-mini"
```

## Background
When we want to use a model, we could:
- use a hosted runtime of a model somewhere in the internet
- or locally spin up the runtime ourselves

If we want to use big models with great performance, we mostly have to use hosted runtimes, as we can not provide the necessary resources on a typical local system (with bigger models taking some dozens of Gigabytes to be loaded at the same time). The size of the model is a hard limitation for a smooth AI experience. To conveniently provide a >100bn parameter model, you would need big GPUs that scale well per user. [Adding neural processing power to the Raspi](https://www.raspberrypi.com/products/ai-kit/) improves execution performance, but does not enhance possibilities.

The other side of the story is, that we have been talking about full-fledged general models. Within more specialized use cases, models that can suffice may be crucially smaller than general models with comparable quality. At the same time, edge devices become more and more performant, with a Raspberry Pi 5 being as swift as a contemporary smartphone. And with 8 GB of RAM, there is already quite a choice of models, that are not just a waste of time.

So, how could we get familiar with these two colliding tides of specialized models becoming more efficient and edge devices becoming more perfomant? We look if it's good for a demo already.

## Architecture

Due to the multitude of frameworks and some models being supported by more than just one framework, I tried to structure everything into more or less loose components, and tie them together through guided use cases. If you find the details not well-structured enough to get behind the workings of this repo, it's probably best to stick to the Demo's docs, as they focus on providing a complete picture (of their limited scope).

While Ollama provides an HTTP endpoint with a single CLI-command, PyTorch needs to be embedded not only into a python environment, but also into an app that serves an HTTP API as well. With two frontends, with different requirements, that creates some sort of dependency matrix:
- a Jupyter Notebook on a local Jupyter Lab server:
  - accessing Ollama via HTTP
  - accessing PyTorch directly in the own environment
- a web frontend application
  - accessing Ollama directly via HTTP
  - accessing PyTorch embedded into a simple web service via HTTP
