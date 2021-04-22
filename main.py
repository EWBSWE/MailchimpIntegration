from pprint import pprint
import json
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

from MemberStats import Session
from MemberStats import get_new_members
from datetime import datetime

# Read credentials
mc_cred_data = json.load(open('mailchimp_credentials.json', 'r')) 
ewb_cred_data = json.load(open('member_site_credentials.json','r'))

ewb_session = Session(save_token_to_file=False)
ewb_session.login_with_credentials(json.dumps(ewb_cred_data))
all_members = ewb_session.get_all_members()

# Get the datetime when we last updated Mailchimp
datetime_str = ''
last_update_filename = 'last_update.txt'
with open(last_update_filename, 'r') as last_update_file:
    datetime_str = last_update_file.read().strip()
    print(f'Last update: {datetime_str}')



nbr_new_members, new_members = get_new_members(all_members, 
                                               datetime.fromisoformat(datetime_str), 
                                               extract=True)
print(f'Number new members since {datetime_str}: {nbr_new_members}')

with open(last_update_filename, 'w') as last_update_file:
    current_datetime = datetime.today().isoformat()
    last_update_file.write(current_datetime)
    print(f'This update: {current_datetime}')
    print(f'Updated "{last_update_filename}"')

if len(new_members) < 1:
    print('No new members to update!')
    exit()

# Extract only emails
new_emails = [member['email'] for member in new_members]

# Make the correct body for Mailchimp
member_body = [{"email_address": email, "status": "subscribed"} for email in new_emails]


print('Updating members:')
pprint(new_emails)

try:
    mailchimp = Client()
    mailchimp.set_config(mc_cred_data)

    list_id = "dd02c68798"
    body_params = {
            "members": member_body,
            "update_existing": False
            }

    response = mailchimp.lists.batch_list_members(list_id, body_params)
    pprint(response)
except ApiClientError as error:
    print(f"Error: {error.text}")

