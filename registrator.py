from config import config
import argparse
import wiotp.sdk.application

if __name__ == "__main__":

    parser = argparse.ArgumentParser('Utility to create and delete devices')
    parser.add_argument('-c', '--create', action='store_const', const=True, help='Create config devices.')
    parser.add_argument('-d', '--delete', action='store_const', const=True, help='Delete config devices.')
    args = parser.parse_args()

    if ((args.create and args.delete) or not (args.create or args.delete)):
        parser.print_usage()
        exit(0)

    options = {
        'identity': {
            'appId': config['credentials']['orgId']
        },
        'auth': {
            'key': config['credentials']['apiKey'],
            'token': config['credentials']['authToken']
        }
    }

    client = wiotp.sdk.application.ApplicationClient(options)

    bulkCreateRequest = []
    for deviceTypeName, deviceType in config['deviceTypes'].items():
        for deviceName in deviceType['devices']:
            bulkCreateRequest.append({'typeId': deviceTypeName, 'deviceId': deviceName})

    if (args.create):
        createResponse = client.registry.devices.create(bulkCreateRequest)
    else:
        createResponse = client.registry.devices.delete(bulkCreateRequest)

    for device in createResponse:
        print('type: {}, name: {}, {}={}'.format(
            device['typeId'], 
            device['deviceId'], 
            'created' if args.create else 'deleted', 
            device['success']))