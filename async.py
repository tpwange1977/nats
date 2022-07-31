# 當程式接收到網路來的response到繼續發送下一個request，中間所需要的時間就只是讓CPU去執行下一個python指令，
# 但是發送request之後，到接收到response中間是需要等待網路另一端的server去回傳response，所需時間當然要長多了。
# 而這段等待sever回傳response的過程，就是io調度的過程，但這過程若要讓CPU掛在一旁等待，實在是太浪費時間了，
# 所以才會引入異步執行的programing方式，讓io調度的過程中，程式不會掛在一旁等待，而是繼續執行下一條指令。
# 現在我們用asyncio模組以異步的方式重複上一段程式所做的事，程式的細節先不要理他，用執行結果來看有沒有為程式的速度帶來提升：

import requests
import time
import asyncio

url = 'https://www.google.com.tw/'
loop = asyncio.get_event_loop()

start_time = time.time()

async def send_req(url):
    t = time.time()
    delta_request = t-start_time
    print("Send a request at",delta_request,"seconds.")

    res = await loop.run_in_executor(None,requests.get,url)

    t = time.time()
    delta_response = t-start_time
    print("Receive a response at",delta_response,"seconds.")
    
    return delta_request#, delta_response

tasks = []
tasks_result = []
count = 10000

for i in range(count):
    task = loop.create_task(send_req(url))
    tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))

delta_response = time.time()-start_time
print("Send a response sum:", delta_response,"seconds.")
