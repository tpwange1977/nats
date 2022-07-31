import asyncio
import nats
from nats.errors import TimeoutError

async def main():
    nc = await nats.connect("127.0.0.1:4222")

    # Create JetStream context.
    js = nc.jetstream()
    # Persist messages on 'foo's subject.
    try:
        await js.add_stream(name="stream1", subjects=["foo"], max_age=0)     #max_age 10 seconds
    
    except nats.js.errors.BadRequestError as msg:
        print(msg)
        await js.delete_stream(name="stream1")
        print("stream removed")
        

    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())