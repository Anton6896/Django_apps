from django.conf import settings
import hashlib
import re
import json
import requests

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_LIST_ID


def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError('String passed is not a valid email address')
    return


def get_subscriber_hash(member_email):
    """
    This makes a email hash which is required by the Mailchimp API
    """
    check_email(member_email)
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()


class Mailchimp(object):

    def __init__(self):
        super(Mailchimp, self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = f'{self.api_url}/lists/{self.list_id}'

    def get_members_endpoint(self):
        return f'{self.list_endpoint}/members'

    def add_email(self, email):
        check_email(email)
        endpoint = self.get_members_endpoint()
        data = {
            "email_address": email,
            "status": "subscribed"
        }
        r = requests.post(
            endpoint,
            auth=("", MAILCHIMP_API_KEY),
            data=json.dumps(data)
        )

        return r.status_code, r.json()

    def check_valid_status(self, status):
        choices = ['subscribed', 'unsubscribed', 'cleaned', 'pending']
        if status not in choices:
            raise ValueError("Not a valid choice")
        return status

    def change_subscription_status(self, email, status):
        subscriber_hash = get_subscriber_hash(email)
        members_endpoint = self.get_members_endpoint()
        endpoint = f"{members_endpoint}/{subscriber_hash}"
        data = {
            "status": self.check_valid_status(status)
        }
        r = requests.put(endpoint,
                         auth=("", MAILCHIMP_API_KEY),
                         data=json.dumps(data)
                         )

        return r.status_code, r.json()

    def check_subscription_status(self, email):
        subscriber_hash = get_subscriber_hash(email)
        members_endpoint = self.get_members_endpoint()
        endpoint = f"{members_endpoint}/{subscriber_hash}"
        r = requests.get(
            endpoint,
            auth=("", MAILCHIMP_API_KEY)
        )

        return r.status_code, r.json()

    def unsubscribe(self, email):
        return self.change_subscription_status(email, status='unsubscribed')

    def subscribe(self, email):
        return self.change_subscription_status(email, status='subscribed')
