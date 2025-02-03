import torch
import gc
import asyncio
from concurrent.futures import ThreadPoolExecutor
from peft import PeftConfig, PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import pipe

torch.manual_seed(42)
# config
BASE_MODEL_NAME = "LSX-UniWue/LLaMmlein_1B"
CHAT_ADAPTER_NAME = "LSX-UniWue/LLaMmlein_1B_chat_all"

def init():
    pipe_obj = pipe.get_or_kill_pipe("llammlein1b")
    if pipe_obj == None:
        pipe_obj = {
            "config": PeftConfig.from_pretrained(CHAT_ADAPTER_NAME),
            "base_model": AutoModelForCausalLM.from_pretrained(
                BASE_MODEL_NAME,
                torch_dtype=torch.float32,
                device_map="cpu",
            )
        }
        pipe_obj["base_model"].resize_token_embeddings(32064)
        pipe_obj["model"] = PeftModel.from_pretrained(pipe_obj["base_model"], CHAT_ADAPTER_NAME)
        pipe_obj["tokenizer"] = AutoTokenizer.from_pretrained(CHAT_ADAPTER_NAME)
        pipe.setPipe(pipe_obj, "llammlein1b")
    pipe.change_status(True)


async def run_prompt(prompt, role, stream):
        init()
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, generate, prompt, role, stream)

def generate(prompt, role, stream):
    # encode message in "ChatML" format
    chat = pipe.PIPE["tokenizer"].apply_chat_template(
        [{"role":role, "content": prompt}],
        return_tensors="pt",
        add_generation_prompt=True,
    ).to("cpu")

    if stream:
        stream.set_tokenizer(pipe.PIPE["tokenizer"])

    pipe.PIPE["tokenizer"].decode(
        pipe.PIPE["model"].generate(
            chat,
            max_new_tokens=300,
            streamer=stream,
            pad_token_id=pipe.PIPE["tokenizer"].pad_token_id,
            eos_token_id=pipe.PIPE["tokenizer"].eos_token_id,
        )[0],
        skip_special_tokens=False,
    )
    pipe.change_status(False)