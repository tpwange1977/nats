import asyncio
import nats
from nats.errors import TimeoutError
import time

async def main():
    nc = await nats.connect("127.0.0.1:4222")

    # Create JetStream context.
    js = nc.jetstream()

    # Create pull based consumer on 'foo'.
    # psub = await js.pull_subscribe("foo", "psub")     # pull based consumer on 'foo'.

    # Fetch and ack messagess from consumer.
    # for i in range(0, 10):
    # msgs = await psub.fetch(1)      ## 一下 OK 一下有問題，好像要稍等 10秒，才能 fetch 下一個
    # for msg in msgs:
    #     print(msg)

    # # Create single ephemeral push based subscriber.
    # sub = await js.subscribe("foo")
    # msg = await sub.next_msg()
    # await msg.ack()

    # # Create single push based subscriber that is durable across restarts.
    #sub = await js.subscribe("foo", durable="myapp", stream="stream1")


    # pull_subscribe 會自動 timeout!!! 
    sub = await js.pull_subscribe(subject="foo", durable="psub", stream="stream1")
    
    while True:
        try:
            msgs = await sub.fetch(batch=1, timeout=10)
            
        except nats.errors.TimeoutError:
            #time.sleep(10)
            continue
            #break        
        for msg in msgs:
            await msg.ack()
            print(msg.data)
            #main_process.run(params)


    # # Create deliver group that will be have load balanced messages.
    # async def qsub_a(msg):
    #     print("QSUB A:", msg)
    #     await msg.ack()

    # async def qsub_b(msg):
    #     print("QSUB B:", msg)
    #     await msg.ack()
    # await js.subscribe("foo", "workers", cb=qsub_a)
    # await js.subscribe("foo", "workers", cb=qsub_b)

    # for i in range(0, 10):
    #     ack = await js.publish("foo", f"hello world: {i}".encode())
    #     print("\t", ack)

    # # Create ordered consumer with flow control and heartbeats
    # # that auto resumes on failures.
    # osub = await js.subscribe("foo", ordered_consumer=True)
    # data = bytearray()

    # while True:
    #     try:
    #         msg = await osub.next_msg()
    #         #data.extend(msg.data)
    #         print(str(msg.data))
    #     except TimeoutError:
    #         break
    # #print("All data in stream:", data)

    await nc.close()

if __name__ == '__main__':
    # loop = asyncio.get_event_loop() # 建立一個Event loop    
    # loop.run_forever()
    asyncio.run(main())