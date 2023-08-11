import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()
EMAIL_SUBJECT = os.getenv('EMAIL_SUBJECT', '')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')
TO_EMAILS = os.getenv('TO_EMAILS', '')
CC_EMAILS = os.getenv('CC_EMAILS', '')


def lambda_handler(event, context):

    rds_client = boto3.client('rds')
    response = rds_client.describe_pending_maintenance_actions(
        # ResourceIdentifier='string',
        # Filters=[
        #     {
        #         'Name': 'string',
        #         'Values': [
        #             'string',
        #         ]
        #     },
        # ],
        # Marker='string',
        # MaxRecords=123
    )

    resources = response.get('PendingMaintenanceActions', [])
    if not resources:
        print('No RDS maintainance action found')
        return
    else:
        print(f'RDS maintainance actions: {resources}')

    
    ses_client = boto3.client('ses')
    
    # Check sender_email is verified
    response = ses_client.list_identities()
    if SENDER_EMAIL not in response.get('Identities', []):
        # Send verification email
        response = ses_client.verify_email_address(
            EmailAddress=SENDER_EMAIL
        )
        # Exit from lambda function
        raise Exception(f'Sender {SENDER_EMAIL} not verified. Verification email is sent.')
    
    to_emails = TO_EMAILS.split(';')
    cc_emails = CC_EMAILS.split(';')
    resource_actions = []
    for resource in resources:
        action_details = []
        for detail in resource.get('PendingMaintenanceActionDetails'):
            action_details.append(f"<li>{detail.get('Action')}: {detail.get('Description')}</li>")
        resource_actions.append(f"<li>{resource.get('ResourceIdentifier')} <ul>{''.join(action_details)}</ul></li>")
    msg_html = f"List of pending RDS maintainance:<br><ol>{''.join(resource_actions)}</ol>"

    # Optional
    msg_text = json.dumps(resources)
    reply_to_emails = [SENDER_EMAIL]
    
    print(f'Sending email to {to_emails}')
    response = ses_client.send_email(
        Source=SENDER_EMAIL,
        Destination={
            'ToAddresses': to_emails,
            'CcAddresses': cc_emails
        },
        Message={
            'Subject': {
                'Data': EMAIL_SUBJECT,
            },
            'Body': {
                'Text': {
                    'Data': msg_text,
                },
                'Html': {
                    'Data': msg_html,
                }
            }
        },
        ReplyToAddresses=reply_to_emails
    )
    

lambda_handler(None, None)
