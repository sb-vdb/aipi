import torch
import gc
import asyncio
from concurrent.futures import ThreadPoolExecutor
from peft import PeftConfig, PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.manual_seed(42)
# config
BASE_MODEL_NAME = "LSX-UniWue/LLaMmlein_1B"
CHAT_ADAPTER_NAME = "LSX-UniWue/LLaMmlein_1B_chat_all"
DEVICE = "cpu"  # or mps
config = None
model = None
tokenizer = None

def init():
    global config, model, tokenizer
    # load model
    config = PeftConfig.from_pretrained(CHAT_ADAPTER_NAME)
    base_model = model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        torch_dtype=torch.float32,
        device_map=DEVICE,
    )
    base_model.resize_token_embeddings(32064)
    model = PeftModel.from_pretrained(base_model, CHAT_ADAPTER_NAME)
    tokenizer = AutoTokenizer.from_pretrained(CHAT_ADAPTER_NAME)

async def run_prompt(prompt, role, stream):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, generate, prompt, role, stream)

def generate(prompt, role, stream):
    global model, tokenizer
    # encode message in "ChatML" format
    chat = tokenizer.apply_chat_template(
        [{"role":role, "content": prompt}],
        return_tensors="pt",
        add_generation_prompt=True,
    ).to(DEVICE)

    if stream:
        stream.set_tokenizer(tokenizer)

    tokenizer.decode(
        model.generate(
            chat,
            max_new_tokens=300,
            streamer=stream,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )[0],
        skip_special_tokens=False,
    )

def pipe_is_none():
    global model, tokenizer
    return model is None and tokenizer is None

def clear_pipe():
    global model, tokenizer
    del model, tokenizer
    gc.collect()
    model = tokenizer = None