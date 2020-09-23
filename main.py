from pprint import pprint
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# Read credentials
cred_file = open('credentials.txt','r')
api_key = ''
server = ''
for line in cred_file:
    stripped_line = line.strip()
    if stripped_line[:4] == 'key:':
        api_key = stripped_line[4:].strip()
    elif stripped_line[:7] == 'server:':
        server = stripped_line[7:].strip()

try:
    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key ,
        "server": server
        })

    list_id = "dd02c68798"
    body_params = {
            "members": [{"email_address": "test@ewb-swe.org", "status": "subscribed"}],
            "update_existing": False
            }

    response = mailchimp.lists.batch_list_members(list_id, body_params)
    pprint(response)
except ApiClientError as error:
    print(f"Error: {error.text}")

