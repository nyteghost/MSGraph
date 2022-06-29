import requests
import msal
import atexit
import os.path
import json
from requests.structures import CaseInsensitiveDict
from ConnectPyse.service import ticket_notes_api, ticket_note,ticket,tickets_api
from ConnectPyse.schedule import schedule_entries_api,schedule_entry
import os,sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import doorKey as dk
config = dk.tangerine()

### Dictionary class
class my_dictionary(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict()   
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 


# ### Create list of staff members that are being disabled
# list_a=[]
# for i in staffTopsBlock['UserPrincipalName']:
#         list_a.append(i)
# list_a_joined= "\n".join(list_a)


# Variables 
TENANT_ID = config['tenant_id'] 
CLIENT_ID = config['client_id']
cwURL = 'https://api-na.myconnectwise.net/v2021_2/apis/3.0/'
AUTHORITY = 'https://login.microsoftonline.com/' + TENANT_ID
ENDPOINT = 'https://graph.microsoft.com/v1.0'

SCOPES = [
    'Files.ReadWrite.All',
    'Sites.ReadWrite.All',
    'User.Read',
    'User.ReadBasic.All'
]

cache = msal.SerializableTokenCache()

if os.path.exists('token_cache.bin'):
    cache.deserialize(open('token_cache.bin', 'r').read())

atexit.register(lambda: open('token_cache.bin', 'w').write(cache.serialize()) if cache.has_state_changed else None)

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

accounts = app.get_accounts()
result = None
if len(accounts) > 0:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])

if result is None:
    flow = app.initiate_device_flow(scopes=SCOPES)
    if 'user_code' not in flow:
        raise Exception('Failed to create device flow')

    print(flow['message'])

    result = app.acquire_token_by_device_flow(flow)

budata = """{"accountEnabled": 'False'}}"""
buheaders= {'Accept': 'application/json', 'Authorization': 'Bearer '+result['access_token'], 'Content-Type': 'application/json'}

user = "rjacobs@georgiacyber.online"

blockl = requests.patch(f'{ENDPOINT}/users/{user}', headers=buheaders, data=budata)

if blockl.status_code == 404:
    print(user + " not found in portal.")
    print(user + " not found in portal.")
else:
    print(user)
    ubresult = requests.get(f'{ENDPOINT}/users/{user}?$select=accountEnabled', headers={'Authorization': 'Bearer ' + result['access_token']})
    ubresult.raise_for_status()
    print(blockl.text)
    print(ubresult.text)