from apscheduler.schedulers.blocking import BlockingScheduler
from config import config
import json
import paho.mqtt.publish as mqtt
import random

auth = {
    'username': config['credentials']['apiKey'],
    'password': config['credentials']['authToken']
}
client_id = 'a:{}:{}'.format(config['credentials']['orgId'], config['credentials']['apiKey'])
hostname = config['credentials']['orgId'] + '.messaging.internetofthings.ibmcloud.com'

def generatePayload(props):
    payload = ''
    for propName, propBounds in props.items():
        left, right = propBounds.split(':')
        propValue = random.uniform(float(left), float(right))
        if len(payload):
            payload += ','
        payload += '"{}": {}'.format(propName, propValue)
    return '{' + payload + '}'

def generateMessages():
    messages = []
    for deviceTypeName, deviceType in config['deviceTypes'].items():
        for deviceName in deviceType['devices']:
            topic = 'iot-2/type/{}/id/{}/evt/{}/fmt/json'.format(deviceTypeName, deviceName, deviceType['event'])
            payload = generatePayload(deviceType['properties'])
            messages.append({'topic': topic, 'payload': payload, 'qos': 0, 'retain': False})
    return messages

def oneSimulationRun():
    mqtt.multiple(generateMessages(), hostname=hostname, client_id=client_id, auth=auth)
        
scheduler = BlockingScheduler()
scheduler.add_job(oneSimulationRun, 'interval', seconds=config['parameters']['updateInterval'])
scheduler.start()