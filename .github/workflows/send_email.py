""" Module to manage eMail events """

from sys import exit
from argparse import ArgumentParser
from base64 import b64encode
from os.path import basename
from requests import post


rc=0

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--recipients', nargs='+', help="Addresses that will received the email", type=str, required=True)
    parser.add_argument('--subject', help="Subject line", type=str, required=True)
    parser.add_argument('--message', help="Email body", type=str, required=True)
    parser.add_argument('--attachments', nargs='*', default=[], help="Files to attach", type=str )
    parser.add_argument('--auth-token', help="AutoIQ Authentication Token", type=str, required=True)
    parser.add_argument('--warn', help="Don't return a bad return code. Only print problems.", action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    headers = {
        'authorization': f'PAT {args.auth_token}',
        'Content-Type': 'application/json'
    }

    encoded_attachments = []
    if args.attachments:
        for attachment in args.attachments:
            with open(attachment, 'rb') as f:
                encoded_attachments.append({
                    "filename": basename(attachment),
                    # Read file as bytes, encode bytes as base64, then stringify that for JSON to be happy
                    "data": b64encode(f.read()).decode('utf-8')
                })

    request_body = {
        "toAddress": ",".join(args.recipients),
        "subject": args.subject,
        "body": args.message,
        "attachments": encoded_attachments
    }
    print(f'Request Body: {request_body}')

    response = post(url="https://autoiq.extremenetworks.com/email-service/awsmail/postMail", headers=headers, json=request_body)
    # response = post(url="http://localhost:2005/email-service/awsmail/postMail", headers=headers, json=request_body)
    print(f'Response code: {response.status_code} \nResponse Message: {response.json()}')

    exit(rc)

    # Test command options
    # --recipients psadej@extremenetworks.com psadej@extremenetworks.com --subject hi --message test --attachments README.md --auth-token <>
