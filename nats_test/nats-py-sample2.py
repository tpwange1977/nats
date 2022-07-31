import asyncio
from posixpath import split
import nats
import time

async def main():
    nc = await nats.connect("127.0.0.1")
    js = nc.jetstream()

    # await js.add_stream(name='hello', subjects=['hello'])
    # await js.publish('hello', b'Hello JS!')

    async def cb1(msg):
      print('Received1:', msg.data)

    async def cb2(msg):
      print('Received2:', msg)

    async def cb3(msg):
      print('Received3:', msg.data)

    # Ephemeral Async Subscribe
    # await js.subscribe('hello', cb=cb)

    # Durable Async Subscribe
    # NOTE: Only one subscription can be bound to a durable name. It also auto acks by default.

    # await js.subscribe('hello', cb=cb, durable='foo')

    # # Durable Sync Subscribe
    # # NOTE: Sync subscribers do not auto ack.
    while True:
        #try:
            # await js.subscribe('hello', cb=cb1, durable='foo')
            # await js.subscribe('hello', durable='bar')
        await js.subscribe('foo', 'workers', cb=cb2)
        time.sleep(3)
        #except:
            #time.sleep(3)
            #print(".", end="")
            #pass

    # # Queue Async Subscribe
    # # NOTE: Here 'workers' becomes deliver_group, durable name and queue name.
    # await js.subscribe('hello', 'workers', cb=cb)

    await js.delete_stream(name="hello")
    print("stream removed")

    await nc.drain()
    await nc.close()    

if __name__ == '__main__':
    asyncio.run(main())
