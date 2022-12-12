import boto3
import boto3
from botocore.config import Config


# create code for creating instance


# creating aws instance
def create_aws_instance(params):
    client = boto3.client(
        's3',
        aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
        aws_secret_access_key='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',
        #aws_session_token=SESSION_TOKEN
    )

    resource = boto3.resource(
        'ec2',
        aws_access_key_id='AKIAQAS2UWXQJQVWZRSC',
        aws_secret_access_key='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',
        region_name = 'us-east-1'
    )

    my_config = Config(
        region_name = 'us-east-1',)

    instances = resource.create_instances(
            ImageId=params['aws_image_id'],
            MinCount=1,
            MaxCount=1,
            InstanceType=params['aws_instance_type'],
            KeyName=params['aws_key_name']
        )


# create openstack instnace
