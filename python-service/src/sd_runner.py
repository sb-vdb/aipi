import torch
from diffusers import StableDiffusionPipeline
import os
import lib

# Init Model
model_id = "sd-legacy/stable-diffusion-v1-5"
total_steps = lib.get_total_steps()
PIPE = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
PIPE.to("cpu")

def read_input():
    with open("prompt.txt", "r") as f:
        content = f.read()
    return content.split("\n")

def write_output(pipe, step, timestep, callback_kwargs):
    global total_steps

    # Get Image
    latents = callback_kwargs["latents"]
    image_base64 = lib.image_to_base64(lib.latents_to_rgb(latents[0]))

    with open(f"output/buffer_{step}.txt", "x") as f:
        f.write(f"{image_base64}")
    return callback_kwargs

def run_prompt():
    global total_steps

    prompt, filename = read_input()
    
    with torch.no_grad():
        image = PIPE(
            prompt,
            num_inference_steps=total_steps,
            callback_on_step_end = write_output
        ).images[0]
    

    image.save(filename)

if __name__ == "__main__":
    run_prompt()