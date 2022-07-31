# python3.5
# ubuntu 16.04

import requests
import time

url = 'https://www.google.com.tw/'

start_time = time.time()

def send_req(url):

    t = time.time()
    delta_request = t-start_time
#    print("Send a req at:",delta_request,"seconds.")

    res = requests.get(url)

    t = time.time()
    delta_response = t-start_time
#    print("Rec. a res at:",delta_response,"seconds.")
    return delta_request, delta_response

count = 100
total_time_request = 0
total_time_response = 0
for i in range(count):
    delta_request, delta_response = send_req(url)
    total_time_request += delta_request
    total_time_response += delta_response


print("Send a req. Avg:",total_time_request/count,"seconds.")
print("Send a res. Avg:",total_time_response/count,"seconds.")
t = time.time()
print("Total Time:", t-start_time,"seconds.")