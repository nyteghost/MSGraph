import msal
import atexit
import os
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('excel_CLIENT_ID')
AUTHORITY = 'https://login.microsoftonline.com/' + TENANT_ID


def getAuth():
    print('getAuth Used')
    SCOPES = [
        'Files.ReadWrite.All',
        'Sites.ReadWrite.All',
        'User.Read'
    ]

    cache = msal.SerializableTokenCache()

    if os.path.exists('excel_token_cache.bin'):
        cache.deserialize(open('excel_token_cache.bin', 'r').read())

    atexit.register(lambda: open('excel_token_cache.bin', 'w').write(cache.serialize()) if cache.has_state_changed else None)

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
    print('obtained a Auth Token')
    return result
