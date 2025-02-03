import torch
from diffusers import StableDiffusionPipeline
import datetime
import asyncio
import gc
from concurrent.futures import ThreadPoolExecutor

# Init Model
model_id = "sd-legacy/stable-diffusion-v1-5"
PIPE = None

def init():
    global PIPE
    PIPE = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
    PIPE.to("cpu")

async def run_prompt(prompt, stream):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, generate, prompt, stream)

def generate(prompt, stream):
    stream.put("Generating image...\n" + "Running prompt: " + prompt)
    with torch.no_grad():
        image = PIPE(
            prompt,
            num_inference_steps = stream.get_total_steps(),
            callback_on_step_end = stream.write
        ).images[0]
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    image.save("output/" + date + ".png")

def pipe_is_none():
    return PIPE is None

def clear_pipe():
    global PIPE
    del PIPE
    gc.collect()
    PIPE = None