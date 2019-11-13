import boto3
import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info('Loading function, boto3 version: {}'.format(boto3.__version__))

STATEMACHINE_ARN = os.environ['STATEMACHINE_ARN']

c_sfn = boto3.client('stepfunctions')

def lambda_handler(event, context):
    #logger.info("event: {}".format(event))
    logger.info(json.dumps(event, indent=4))

    try:
        logger.info("len: {}".format(len(event['Records'])))
        logger.info("event type: {}".format(event['Records'][0]['dynamodb']['NewImage']['eventType']['S']))
    
        record = event['Records'][0]['dynamodb']
        logger.info("record: {}".format(record))
        logger.info("event type: {}".format(record['NewImage']['eventType']['S']))
    
        logger.info(json.dumps(record, indent=2))
        input = json.dumps(record)
        logger.info(input)
    
        logger.info("STATEMACHINE_ARN: {}".format(STATEMACHINE_ARN))
        response = c_sfn.start_execution(
            stateMachineArn=STATEMACHINE_ARN,
            input=input
        )
    
        logger.info("response: {}".format(response))
    
        return record
    except Exception as e:
        logger.error('{}'.format(e))
        return False
