import boto3
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


ERRORS = []

class ThingCrudException(Exception): pass

def thing_exists(c_iot, thing_name):
    logger.info("thing exists: thing_name: {}".format(thing_name))
    try:
        response = c_iot.describe_thing(thingName=thing_name)
        logger.info('response: {}'.format(response))
        return True
    except Exception as e:
        logger.warn('describe thing: {}'.format(e))
        return False


def delete_thing(c_iot, thing_name):
    global ERRORS

    try:
        if not thing_exists(c_iot, thing_name):
            logger.warn("thing does not exist: {}".format(thing_name))
            return

        r_principals = c_iot.list_thing_principals(thingName=thing_name)

        for arn in r_principals['principals']:
            cert_id = arn.split('/')[1]
            logger.info("arn: {} cert_id: {}".format(arn, cert_id))

            r_detach_thing = c_iot.detach_thing_principal(thingName=thing_name,principal=arn)
            logger.info("detach thing: {}".format(r_detach_thing))

            r_upd_cert = c_iot.update_certificate(certificateId=cert_id,newStatus='INACTIVE')
            logger.info("certificate inactivate: {}".format(r_upd_cert))

            r_policies = c_iot.list_principal_policies(principal=arn)
            logger.info("policies: {}".format(r_policies))

            for pol in r_policies['policies']:
                pol_name = pol['policyName']
                logger.info("pol_name: {}".format(pol_name))
                r_detach_pol = c_iot.detach_policy(policyName=pol_name,target=arn)
                logger.info("detach policy: {}".format(r_detach_pol))

            r_del_cert = c_iot.delete_certificate(certificateId=cert_id,forceDelete=True)
            logger.info("delete certificate: {}".format(r_del_cert))

        r_del_thing = c_iot.delete_thing(thingName=thing_name)
        logger.info("delete thing: {}".format(r_del_thing))
    except Exception as e:
        logger.error("delete_thing: {}".format(e))
        ERRORS.append("delete_thing: {}".format(e))

def create_thing(c_iot, thing_name, attrs):
    logger.info("create thing: thing_name: {}".format(thing_name))
    global ERRORS
    try:
        if not thing_exists(c_iot, thing_name):
            response = c_iot.create_thing(
                thingName=thing_name,
                attributePayload=attrs
            )
            logger.info("create_thing: response: {}".format(response))
        else:
            logger.info("thing exists already: {}".format(thing_name))
    except Exception as e:
        logger.error("create_thing: {}".format(e))
        ERRORS.append("create_thing: {}".format(e))


def lambda_handler(event, context):
    global ERRORS
    ERRORS = []
    logger.info(json.dumps(event, indent=4))

    c_iot = boto3.client('iot')

    try:
        if event['NewImage']['operation']['S'] == 'CREATED':
            thing_name = event['NewImage']['thingName']['S']
            logger.info("thing_name: {}".format(thing_name))
            attrs = {"attributes": {}}
            for key in event['NewImage']['attributes']['M']:
                attrs['attributes'][key] = event['NewImage']['attributes']['M'][key]['S']

            if attrs['attributes']:
                attrs['merge'] = False
            logger.info("attrs: {}".format(attrs))
            create_thing(c_iot, thing_name, attrs)

        if event['NewImage']['operation']['S'] == 'DELETED':
            thing_name = event['NewImage']['thingName']['S']
            logger.info("thing_name: {}".format(thing_name))
            delete_thing(c_iot, thing_name)

    except Exception as e:
        logger.error(e)

    if ERRORS:
        raise ThingCrudException("{}".format(ERRORS))

    return {"message": "success"}
