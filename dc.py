import json
import os

import boto3

sf = boto3.client('stepfunctions')
""" :type : pyboto3.stepfunctions """

env_type = os.environ['ENV_TYPE']

region = os.environ['AWS_REGION']


def lambda_handler(event, context):
    print(f'event: {event}')
    state_machine_arn = 'arn:aws:states:' + region + ':' + context.invoked_function_arn.split(':')[
        4] + ':' 'stateMachine:toll-registry-' + env_type
    for record in event['Records']:
        s3 = record['s3']
        s3_object = s3['object']
        sf.start_execution(stateMachineArn=state_machine_arn, input=json.dumps({
            'bucket': s3['bucket']['name'],
            'key': s3_object['key'],
            'version-id': s3_object['versionId'],
            "analysisStrategy": "BIG_BOX"
        }))
