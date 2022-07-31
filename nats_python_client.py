# from pynats import NATSClient

# with NATSClient() as client:
#     client.publish("foo", payload=b"test-payloadxxxxxxxxxxxxxxxxx3")

import asyncio
import nats
import time
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError

async def main():
    # It is very likely that the demo server will see traffic from clients other than yours.
    # To avoid this, start your own locally and modify the example to use it.
    nc = await nats.connect("nats://127.0.0.1:4222")

    await nc.publish("foo", b'Hello')
    await nc.publish("foo", b'World')
    await nc.publish("foo", b'!!!!!')

    # Terminate connection to NATS.
    await nc.drain()

if __name__ == '__main__':
    asyncio.run(main())
