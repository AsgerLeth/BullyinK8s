import asyncio
from aiohttp import web
import os
import socket
import random
import aiohttp
import requests
import json
from kubernetes import client, config
from kubernetes.client.api import core_v1_api
import time

POD_IP = str(os.environ['POD_IP'])
WEB_PORT = int(os.environ['WEB_PORT'])
POD_ID = random.randint(0, 100)
pod_name = socket.gethostname()
with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as f:
    namespace = f.read()
TimeOut = time.time()
LastTime = time.time()

currentCoordinatorID = 0
config.load_incluster_config()
v1 = core_v1_api.CoreV1Api()

async def setup_k8s():
    # If you need to do setup of Kubernetes, i.e. if using Kubernetes Python client
	print("K8S setup completed")


async def run_bully():
    while True:
        print("Running bully algorithm")
        await asyncio.sleep(5) # wait for everything to be up
        
        # Get all pods doing bully
        ip_list = []
        print("Making a DNS lookup to service")
        response = socket.getaddrinfo("bully-service",0,0,0,0)
        print("Get response from DNS")
        for result in response:
            ip_list.append(result[-1][0])
        ip_list = list(set(ip_list))
        
        # Remove own POD ip from the list of pods
        ip_list.remove(POD_IP)
        print("Got %d other pod ip's" % (len(ip_list)))
        
        # Get ID's of other pods by sending a GET request to them
        await asyncio.sleep(2)
        other_pods = dict()
        for pod_ip in ip_list:
            endpoint = '/pod_id'
            url = 'http://' + str(pod_ip) + ':' + str(WEB_PORT) + endpoint
            response = requests.get(url)    
            other_pods[str(pod_ip)] = response.json()
        
        # Other pods in network
        
        
        print("Check if there is a higher ID")
        higher_id = False
        for pod_ip, pod_id in other_pods.items():
            if pod_id > POD_ID:
                higher_id = True
                break
        if higher_id:
             for pod_ip in ip_list:
                if (pod_id > POD_ID):
                    endpoint = '/update_election'
                    url = 'http://' + str(pod_ip) + ':' + str(WEB_PORT) + endpoint
                    response = requests.post(url, json='{"message": "election"}')
        else:
            # Send coordinator to all other pods
            v1.patch_namespaced_pod(pod_name, namespace, {"metadata": {"labels": {"leader": "true"}}})
            for pod_ip in ip_list:
                endpoint = '/update_coordinator'
                url = 'http://' + str(pod_ip) + ':' + str(WEB_PORT) + endpoint
                stringpod = str(POD_ID)
                response = requests.post(url, json='{"message": "coordinator", "ID": stringpod}')

        if v1.read_namespaced_pod(pod_name, namespace).metadata.labels["leader"] == "true":
            print("I am the coordinator")
            for pod_ip in ip_list:
                endpoint = '/leader_alive'
                url = 'http://' + str(pod_ip) + ':' + str(WEB_PORT) + endpoint
                stringpod = str(POD_ID)
                response = requests.post(url, json='{"message": "leaderAlive", "ID": stringpod}')

        elif v1.read_namespaced_pod(pod_name, namespace).metadata.labels["leader"] == "false" and time.time() - LastTime > TimeOut:
            print("Leader is dead")
            timer = time.time()
            okmsg = False
            for pod_ip in ip_list:
                if (pod_id > POD_ID):
                    endpoint = '/update_election'
                    url = 'http://' + str(pod_ip) + ':' + str(WEB_PORT) + endpoint
                    stringpod = str(POD_ID)
                    response = requests.post(url, json='{"message": "election", "ID": stringpod}')
                    if response.json() == "OK":
                        okmsg = True
            if okmsg == False:
                v1.patch_namespaced_pod(pod_name, namespace, {"metadata": {"labels": {"leader": "true"}}})
                for pod_ip in ip_list:
                    endpoint = '/update_coordinator'
                    url = 'http://' + str(pod_ip) + ':' + str(WEB_PORT) + endpoint
                    stringpod = str(POD_ID)
                    response = requests.post(url, json='{"message": "coordinator", "ID": stringpod}')
           
             
                
        
        print("Listing other pods with their IPs:")
        print(other_pods)
        # Sleep a bit, then repeat
        await asyncio.sleep(2)
    
#GET /pod_id
async def pod_id(request):
    return web.json_response(POD_ID)
    
#POST /receive_answer
async def receive_answer(request):
    # Send answer to all other pods
    message = request.json()
    string = json.loads(message)
    if string["message"] == "election":
        print("I am the leader")
    return web.json_response("OK")

#POST /receive_election
async def update_election(request):
    # Send election to all other pods
    
    return web.json_response("OK")

async def leader_alive(request):
    LastTime = time.time()
    return web.json_response("OK")


#POST /receive_coordinator
async def update_coordinator(request):
    # Send coordinator to all other pods
    #message = request.json()
    #print("----------------------------------------------------------",type(request))
    #print("-----------------------------------------------------------",type(message))
    #string = json.loads(message)
    #currentCoordinatorID = string["ID"]
    
    v1.patch_namespaced_pod(pod_name, namespace, {"metadata": {"labels": {"leader": "false"}}})
    return web.json_response("OK")




async def background_tasks(app):
    task = asyncio.create_task(run_bully())
    yield
    task.cancel()
    await task

if __name__ == "__main__":
    app = web.Application()
    app.router.add_get('/pod_id', pod_id)
    app.router.add_post('/receive_answer', receive_answer)
    app.router.add_post('/update_election', update_election)
    app.router.add_post('/update_coordinator', update_coordinator)
    app.router.add_post('/leader_alive', leader_alive)
    app.cleanup_ctx.append(background_tasks)
    web.run_app(app, host='0.0.0.0', port=WEB_PORT)