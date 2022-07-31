import asyncio
import nats
import time
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError

async def main():
    # It is very likely that the demo server will see traffic from clients other than yours.
    # To avoid this, start your own locally and modify the example to use it.
    
    while 1==1:
        nc = await nats.connect("nats://127.0.0.1:4222")

        # You can also use the following for TLS against the demo server.
        #
        # nc = await nats.connect("tls://demo.nats.io:4443")

        async def message_handler(msg):
            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()
            print("1Received a message on '{subject} {reply}': {data}".format(subject=subject, reply=reply, data=data))

        # Simple publisher and async subscriber via coroutine.
        sub = await nc.subscribe("foo", cb=message_handler)

        # Stop receiving after 2 messages.
        # await sub.unsubscribe(limit=2)
        
        
        #time.sleep(10)
        # await nc.publish("foo", b'Hello')
        # await nc.publish("foo", b'World')
        # await nc.publish("foo", b'!!!!!')

        # try:
        #     async for msg in sub.messages:
        #         print(f"2Received a message on '{msg.subject} {msg.reply}': {msg.data.decode()}")
        #         await sub.unsubscribe()
        # except Exception as e:
        #     pass

        async def help_request(msg):
            print(f"3Received a message on '{msg.subject} {msg.reply}': {msg.data.decode()}")
            await nc.publish(msg.reply, b'I can help')

        # # Use queue named 'workers' for distributing requests
        # # among subscribers.
        sub = await nc.subscribe("help", "workers", help_request)



        # Send a request and expect a single response
        # and trigger timeout if not faster than 500 ms.
        # try:
        #     response = await nc.request("help", b'help me', timeout=0.5)
        #     print("4Received response: {message}".format(
        #         message=response.data.decode()))
        # except TimeoutError:
        #     print("Request timed out")

    # Remove interest in subscription.
    await sub.unsubscribe()

    # Terminate connection to NATS.
    await nc.drain()

if __name__ == '__main__':
    asyncio.run(main())