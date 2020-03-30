import apscheduler
import paho.mqtt.publish as mqtt
import json
import random

from apscheduler.schedulers.blocking import BlockingScheduler

CONFIG_FILE='./config.json'
global config

try:
    with open(CONFIG_FILE) as f:
        config = json.load(f)
except Exception as e:
    print(e)

hostUrl = config['credentials']['orgId'] + '.messaging.internetofthings.ibmcloud.com'
id = 'a:{}:{}'.format(config['credentials']['orgId'], config['credentials']['apiKey'])
auth = {
    "username": config['credentials']['apiKey'],
    "password": config['credentials']['authToken']
}
updateInterval = config['parameters']['updateInterval']

def generatePayload(props):
    payload = ''
    for propName, propBounds in props.items():
        left, right = propBounds.split('-')
        propValue = random.uniform(int(left), int(right))
        if len(payload):
            payload += ','
        payload += '"{}": {}'.format(propName, propValue)
    return '{' + payload + '}'

def generateMessages():
    messages = []
    for deviceTypeName, deviceType in config['deviceTypes'].items():
        for device in deviceType['devices']:
            topic = 'iot-2/type/{}/id/{}/evt/{}/fmt/json'.format(deviceTypeName, device, deviceType['event'])
            payload = generatePayload(deviceType['properties'])
            message = {"topic": topic, "payload": payload, "qos": 0, "retain": False}
            messages.append(message)
    return messages

def oneSimulationRun():
    mqtt.multiple(generateMessages(), hostname=hostUrl, client_id=id, auth=auth)
        
scheduler = BlockingScheduler()
scheduler.add_job(oneSimulationRun, 'interval', seconds=updateInterval)
scheduler.start()