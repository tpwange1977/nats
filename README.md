

# KubeCon 2020 NATS util
https://github.com/nats-io/kubecon2020
https://www.youtube.com/watch?v=3KxjTWcy91o
https://static.sched.com/hosted_files/kccncna20/a4/Nov19_NATS_Streams_And_Services.pdf

# Prometheus NATS exporter
https://github.com/lovoo/nats_exporter


# Other material
https://www.slideshare.net/nats_io/the-zen-of-high-performance-messaging-with-nats-76985268

# Docker Commands
docker run -p 4222:4222 -p 8222:8222 -p 6222:6222 --name nats-server -ti nats:2.8.4-alpine3.15 -js


###### Callback Sample
import asyncio
from posixpath import split
import nats
import time

async def main():
    nc = await nats.connect("127.0.0.1:4222")
    js = nc.jetstream()

    async def cb2(msg):
      print('Received2:', msg.data)

    while True:
        await js.subscribe('foo', 'workers', cb=cb2)
        time.sleep(3)

    await nc.drain()
    await nc.close()    

if __name__ == '__main__':
    asyncio.run(main())

