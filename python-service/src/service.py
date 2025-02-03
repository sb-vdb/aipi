from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import asyncio
import uvicorn
import streams
from runner import stablediffusion, llammlein1b

app = FastAPI()

@app.post("/image")
async def generate_image(request: Request):
    data = await request.json()
    prompt = data.get('prompt')
    total_steps = data.get('total_steps')
    stream = streams.DiffuserStream(total_steps)

    if not prompt:
        raise HTTPException(status_code=400, detail="Missing prompt")
    
    if not llammlein1b.pipe_is_none():
        llammlein1b.clear_pipe()
    
    async def coroutine():
        stablediffusion.init()       
        await stablediffusion.run_prompt(prompt, stream)

    async def stream_response():
        async for message in stream.get_generator():
            yield message
            
    asyncio.create_task(coroutine())
    return StreamingResponse(stream_response(), media_type='application/json')

@app.post("/text")
async def generate_text(request: Request):
    data = await request.json()
    prompt = data.get('prompt')
    role = data.get('role')
    stream = streams.TransformerStream()

    if not prompt:
        raise HTTPException(status_code=400, detail="Missing prompt")
    
    if not stablediffusion.pipe_is_none():
        stablediffusion.clear_pipe()

    async def coroutine():
        llammlein1b.init()
        await llammlein1b.run_prompt(prompt, role, stream)

    async def stream_response():
        async for message in stream.get_generator():
            yield message

    asyncio.create_task(coroutine())
    return StreamingResponse(stream_response(), media_type='application/json')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(uvicorn.run("service:app", host="127.0.0.1", port=8000, reload=True))