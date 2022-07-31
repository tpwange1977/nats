import asyncio
import nats

async def main():
    nc = await nats.connect()
    js = nc.jetstream()

    await js.add_stream(name='hello', subjects=['hello'])
    ack = await js.publish('hello', b'Hello JS!')
    print(f'Ack: stream={ack.stream}, sequence={ack.seq}')
    # Ack: stream=hello, sequence=1
    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())