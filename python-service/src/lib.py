import base64
import json
from io import BytesIO
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import time
import sys
import helper

# Init Model
model_id = "sd-legacy/stable-diffusion-v1-5"
PIPE = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
PIPE.to("cpu")

def image_to_base64(image: Image) -> str:
    """Convert PIL Image to base64 string."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def generate_image_with_progress(prompt: str, filename: str):
    global PIPE
    start_time = time.time()
    total_steps = 50
    images = []

    for step in range(total_steps):
        # Assuming you are able to capture each denoising step with a method
        with torch.no_grad():
            result = PIPE(prompt, num_inference_steps=step+1)
        
        images.append(result.images[0])
        img_base64 = image_to_base64(images[step])

        # Calculate progress
        elapsed_time = time.time() - start_time
        remaining_time = (elapsed_time / (step + 1)) * (total_steps - step - 1)

        # Create progress info
        progress_info = {
            "step": step + 1,
            "total_steps": total_steps,
            "elapsed_time": elapsed_time,
            "remaining_time": remaining_time,
            "image_base64": img_base64
        }

        # Yield progress and image
        yield json.dumps(progress_info) + "\n"

        if step == total_steps - 1:
            images[-1].save(filename)

def alt_gen(prompt: str, filename: str):
    global PIPE
    start_time = time.time()
    total_steps = 3

    print("chekpoint prior pipe")
    out = sys.stdout
    stream = helper.ProgressStream()
    with torch.no_grad():
        sys.stdout = stream
        result = PIPE(prompt, num_inference_steps=total_steps)
        sys.stdout = out
    print("chekpoint after pipe")
    stream.print()
    image = result.images[0]
    img_base64 = image_to_base64(image)

    # Calculate progress
    #elapsed_time = time.time() - start_time
    #remaining_time = (elapsed_time / (step + 1)) * (total_steps - step - 1)

    # Create progress info
    progress_info = {
        "step": 1,
        "total_steps": total_steps,
        #"elapsed_time": elapsed_time,
        #"remaining_time": remaining_time,
        #"image_base64": img_base64
    }

    image.save(filename)
    # Yield progress and image
    return json.dumps(progress_info) + "\n"