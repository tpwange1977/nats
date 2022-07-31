import asyncio
from typing import AsyncGenerator, Dict

from fastapi import FastAPI
from nats.aio.client import Client as NATS
from nats.aio.client import Msg
from starlette.requests import Request
from starlette.responses import StreamingResponse

app = FastAPI()
nats = NATS()


async def get_nats() -> NATS:
    global nats

    if not nats.is_connected:
        await nats.connect('localhost:4222')

    return nats


async def subscription_to_generator(nats: NATS, topic: str) -> AsyncGenerator[Msg, Msg]:
    queue: asyncio.Queue[Msg] = asyncio.Queue()

    async def subscription_callback(msg: Msg) -> None:
        await queue.put(msg)
    sid = await nats.subscribe(topic, cb=subscription_callback)

    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=60)
            queue.task_done()
            yield item
        except asyncio.TimeoutError:
            await nats.unsubscribe(sid)
            yield None


async def event_stream(request: Request, user_id: int) -> AsyncGenerator[str, str]:
    messages = subscription_to_generator(await get_nats(), f'user.{user_id}')

    async for msg in messages:
        if msg is None or await request.is_disconnected():
            return
        msg_data = msg.data.decode()
        data_str = f'data: {msg_data}\n\n'
        yield data_str


@app.get('/')
async def root() -> Dict[str, str]:
    return {'message': 'Hello world'}


@app.get('/stream/{user_id}')
async def stream(user_id: int, request: Request) -> StreamingResponse:
    return StreamingResponse(event_stream(request, user_id), media_type='text/event-stream')