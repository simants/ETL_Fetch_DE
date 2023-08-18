import boto3
from botocore.exceptions import NoCredentialsError


def create_sqs_client():
    """
    Create SQS client
    :return: SQS client object
    """
    # Create session with AWS SQS to retrieve messages.
    session = boto3.Session()
    return session.client('sqs', endpoint_url='http://localhost:4566')


def retrieve_messages(client, sqs_url):
    """
    This function retrieves messages from the SQS client.
    :param client: SQS client object.
    :param sqs_url:URL of the SQS to retrieve messages.
    :return: Dictionary formatted data retrieved from the SQS client or None.
    """
    # This block will ensure that the connection with AWS SQS was successful.
    try:
        messages = client.receive_message(QueueUrl=sqs_url)
        if 'Messages' in messages:
            return messages['Messages'][0]
    except NoCredentialsError:
        print('AWS Credentials not found.')
        return None
