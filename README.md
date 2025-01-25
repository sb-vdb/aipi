# aipi

This repository showcases AI model deployments on a Raspberry Pi 5 using Ollama and JupyterLab with PyTorch. Both platforms allow remote interaction with models running on the Raspberry Pi.

To setup the Raspberry Pi, [go here](RASPBERRYPI.md). 

To setup und use the Demos, visit their respective README as linked below (or find them in their folder).

## Demos

### [Simple Chat](demos/chat/README.md)
Provided via Ollama, there is a large range of language models, also with specializations like coding and multi-modal models, able to discuss images (and more) as input, provided along with a prompt. When an Ollama endpoint receives a request, it takes the requested model, sends the prompt through it and streams the result back token by token. Models tested are:
- Phi3-mini 3.8B
- Llama3.2 7B
- Codellama 7B
- Moondream (multi-modal)
- DeepSeek-r1 7B
  
Working with PyTorch / Transformers:
- LläMmlein 1B

### [Image Generation](demos/generate-images/README.md)
Downsides first: 512x512px, hard-to-buy level of detail and about 30 minutes of runtime. But hey, just describe it and it serves it.
Models tested are:
- Stable Diffusion v1.5


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
