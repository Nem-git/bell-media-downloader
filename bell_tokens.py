import json
import logging
from typing import Dict, List
from datetime import datetime, timedelta
import base64
import requests
import tools
import time


# Logger

access_token = None
refresh_token = None
expiry = None
subscriptions = None
scopes = None
packages = None
session = requests.Session()
username = None
password = None
settings_path = "settings.json"


# ===================================================================
#   LOGIN
# ===================================================================


def login(settings_path: str, service_name):

    username, password, wvd_path, custom_string = tools.read_creds_from_file(file_path=settings_path)
    refresh_token = None

    try:
        tokens_info = tools.read_tokens()

        access_token = tokens_info['a_token']
        refresh_token = tokens_info['r_token']
        expiry = time.mktime(datetime.now().timetuple()) + tokens_info['expiry']
    
    except:
        try:
            expiry, access_token, refresh_token = ensure_login(username, password, refresh_token, service_name)
        except:
            expiry = 0
            access_token = ""
            refresh_token = ""

    # ===========================================================
    # Skip if current token is valid
    # ===========================================================

    tools.write_tokens({"a_token": access_token, "r_token": refresh_token, "expiry": expiry})
    headers = {"Authorization": access_token}

    return headers, wvd_path, custom_string
    



def ensure_login(username, password, refresh_token, service_name) -> bool:
    
    # ===========================================================
    # Refresh token if possible
    # ===========================================================
    r = None
    if refresh_token is not None:
        r = refresh_request(refresh_token, service_name)
        if r.status_code != 200:
            r = None



    # ===========================================================
    # Handle refresh + login failure
    # ===========================================================

    if r == None:
        # ===========================================================
        # Do a username/password login if required
        # ===========================================================

        print('Trying username/password login...')
        r = login_request(username, password, service_name)
    
    if r.status_code != 200:
        return
    
    # ===========================================================
    # Parse refresh/login response
    # ===========================================================
    
    resp = r.json()
    access_token = "Bearer " + resp['access_token']
    refresh_token = resp['refresh_token']
    expiry = time.mktime(datetime.now().timetuple()) + resp['expires_in']

    return expiry, access_token, refresh_token


# ===================================================================
#   TOKEN EXPIRY HANDLER
# ===================================================================

def check_expiry(expiry, access_token, refresh_token) -> bool:
    # Check if credentials are provided
    if expiry is None or access_token is None or refresh_token is None:
        return True
    if expiry < time.mktime(datetime.now().timetuple()):
        return True
    return False


# ===================================================================
#   REQUESTS
# ===================================================================


def refresh_request(refresh_token, service_name) -> requests.Response:
    print('Making a refresh request...')
    url = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=refresh_token'
    headers = {
        'accept-encoding': 'gzip',
        'authorization': f'Basic {authorization_name(service_name)}',
        'connection': 'Keep-Alive',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'okhttp/4.9.0'
    }
    data = 'refresh_token={}'.format(refresh_token)
    return session.post(url=url, headers=headers, data=data)



def login_request(username, password, service_name) -> requests.Response:
    print('logging in user username and password...')

    url = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=password'

    headers = {
        'accept-encoding': 'gzip',
        'authorization': f'Basic {authorization_name(service_name)}',
        'connection': 'Keep-Alive',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'okhttp/4.9.0'
    }

    password = password.replace('&', '%26').replace('?', '%3F')
    data = f'password={password}&username={username}'

    return session.post(url=url, headers=headers, data=data)



def authorization_name(service_name) -> str:
    decoded = f"{service_name}-web:default"
    
    encoded = decoded.encode()
    b64 = base64.b64encode(encoded)
    return b64.decode()
