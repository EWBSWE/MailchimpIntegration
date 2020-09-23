from pprint import pprint
import json
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# Read credentials
cred_data = json.load(open('mailchimp_credentials.json', 'r')) 

try:
    mailchimp = Client()
    mailchimp.set_config(cred_data)

    list_id = "dd02c68798"
    body_params = {
            "members": [{"email_address": "test@ewb-swe.org", "status": "subscribed"}],
            "update_existing": False
            }

    response = mailchimp.lists.batch_list_members(list_id, body_params)
    pprint(response)
except ApiClientError as error:
    print(f"Error: {error.text}")

