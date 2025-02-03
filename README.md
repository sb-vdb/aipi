# aipi

This repository showcases AI model deployments on a Raspberry Pi 5 using Ollama and JupyterLab with PyTorch. Both platforms allow remote interaction with models running on the Raspberry Pi.

To setup the Raspberry Pi, [go here](RASPBERRYPI.md). 

To setup und use the Demos, visit their respective README as linked below (or find them in their folder).

## Demos
Aipi uses two ways to serve AI models. One is Ollama, a program that is repository client, model runner and API endpoint, all in one. The other is PyTorch, a Python framework being a defacto standard for AI ecosystems.

Ollama proved to be very convenient to use out of the box and is well-populated with noteworthy models. However, Ollama only serves LMs and the choice is not exhaustive.

### Simple Chat
As we know it from ChatGPT: send a prompt text to it and receive a text back. On top of that, multi-modal models are able to process more than just input text. In our demo, ``Moondream`` may also be sent a picture and be asked a question about it.

Ollama models tested:
- Phi3-mini 3.8B
- Llama3.2 7B
- Codellama 7B
- Moondream (multi-modal)
- DeepSeek-r1 7B
  
PyTorch:
- LläMmlein 1B (Transformers library)

### Image Generation
Downsides first: 512x512px, hard-to-buy level of detail and about 30 minutes of runtime. But hey, just describe it and it serves it.

PyTorch:
- Stable Diffusion v1.5 (Diffusers library)

### Using the Demos

#### [JupyterLab](frontend/jupyter/README.md)
JupyterLab is web-based IDE that can be served right from the Raspi and accessed from the network. So you can open it on any device with a browser and work locally on the Raspi.
For every demo, there are prepared Notebooks in this repo, so you can just check it out and modify stuff. 

#### Web Frontend
Since JupyterLab uses Python code that does a lot more than what is interesting to setup the Aipi demo, there is also a more streamlined UX via a web frontend, that is aimed to not do more than taking prompts and streaming results.

## Background
When we want to use a model, we could:
- use a hosted runtime of a model somewhere in the internet
- or locally spin up the runtime ourselves

If we want to use big models with great performance, we mostly have to use hosted runtimes, as we can not provide the necessary resources on a typical local system (with bigger models taking some dozens of Gigabytes to be loaded at the same time). The size of the model is a hard limitation for a smooth AI experience. To conveniently provide a >100bn parameter model, you would need a system that drastically scales GPU memory and power per user. [Adding neural processing power to the Raspi](https://www.raspberrypi.com/products/ai-kit/) improves execution performance, but does not enhance possibilities.

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
