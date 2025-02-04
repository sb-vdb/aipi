import torch
from diffusers import AutoPipelineForText2Image
import datetime
import asyncio
import gc
from concurrent.futures import ThreadPoolExecutor
import pipe

# Init Model
model_id = "stabilityai/sdxl-turbo"

def init():
    PIPE = pipe.get_or_kill_pipe("sdxlturbo")
    if not PIPE:
        PIPE = AutoPipelineForText2Image.from_pretrained(model_id, torch_dtype=torch.float32)
        pipe.set(PIPE.to("cpu"), "sdxlturbo")
    pipe.change_status(True)


async def run_prompt(prompt, stream):
    init()
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, generate, prompt, stream)

def generate(prompt, stream):
    stream.put("Generating image...\n" + "Running prompt: " + prompt)
    with torch.no_grad():
        image = pipe.PIPE(
            prompt,
            num_inference_steps = stream.get_total_steps(),
            callback_on_step_end = stream.write,
            guidance_scale = 0.0
        ).images[0]
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    image.save("output/" + date + ".png")
    pipe.change_status(False)