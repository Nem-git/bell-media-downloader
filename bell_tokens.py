import json
import logging
from typing import Dict, List
from datetime import datetime, timedelta
import base64
import requests

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

def ensure_login() -> bool:
    global expiry, access_token, refresh_token

    # ===========================================================
    # Skip if current token is valid
    # ===========================================================

    if not check_expiry(expiry, access_token, refresh_token):
        return expiry, access_token, refresh_token
    
    # ===========================================================
    # Refresh token if possible
    # ===========================================================
    r = None
    if refresh_token is not None:
        r = _make_refresh_request()
        if r.status_code != 200:
            r = None

    # ===========================================================
    # Do a username/password login if required
    # ===========================================================

    if r is None:
        #logger.debug('Trying username/password login...')
        r = login_request()

    # ===========================================================
    # Handle refresh + login failure
    # ===========================================================

    if r.status_code != 200:
        return
    
    # ===========================================================
    # Parse refresh/login response
    # ===========================================================
    
    resp = r.json()
    access_token = "Bearer " + resp['access_token']
    refresh_token = resp['refresh_token']
    expiry = datetime.now() + timedelta(0, resp['expires_in'])
    return expiry, access_token, refresh_token





def login_request():
    print('logging in user username and password...')

    url = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=password'

    decoded = f"crave-web:default"
    encoded = decoded.encode()
    b64 = base64.b64encode(encoded)

    headers = {
        'accept-encoding': 'gzip',
        'authorization': f'Basic {b64.decode()}',
        'connection': 'Keep-Alive',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'okhttp/4.9.0'
    }

    global password, username
    password = password.replace('&', '%26').replace('?', '%3F')
    data = f'password={password}&username={username}'

    return session.post(url=url, headers=headers, data=data)



# ===================================================================
#   TOKEN EXPIRY HANDLER
# ===================================================================

def check_expiry(expiry, access_token, refresh_token) -> bool:
    # Check if credentials are provided
    if expiry is None or access_token is None or refresh_token is None:
        return True
    if expiry < datetime.now() - timedelta(0, 3600):
        return True
    return False


# ===================================================================
#   REQUESTS
# ===================================================================

def _make_refresh_request():
    #logger.debug('Making a refresh request...')
    url = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=refresh_token'
    headers = {
        'accept-encoding': 'gzip',
        'authorization': 'Basic {}'.format(_get_authorization()),
        'connection': 'Keep-Alive',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'okhttp/4.9.0'
    }
    data = 'refresh_token={}'.format(refresh_token)
    return session.post(url=url, headers=headers, data=data)

def _make_login_request():
    print('logging in user username and password...')
    url = 'https://account.bellmedia.ca/api/login/v2.1?grant_type=password'
    headers = {
        'accept-encoding': 'gzip',
        'authorization': 'Basic {}'.format(_get_authorization()),
        'connection': 'Keep-Alive',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'okhttp/4.9.0'
    }
    global password, username
    password = password.replace('&', '%26').replace('?', '%3F')
    data = 'password={}&username={}'.format(password, username)
    return session.post(url=url, headers=headers, data=data)

def _get_authorization() -> str:
    decoded = '{}:{}'.format("crave-web", "default")
    encoded = decoded.encode()
    b64 = base64.b64encode(encoded)
    return b64.decode()

# ===================================================================
#   TOKEN EXPIRY HANDLER
# ===================================================================

def _check_expiry() -> bool:
    # Check if credentials are provided
    if expiry is None or access_token is None or refresh_token is None:
        return True
    if expiry < datetime.now() - timedelta(0, 3600):
        return True
    return False

# ===================================================================
#   OVERLOADS
# ===================================================================

def _process_cache_obj(cache_obj) -> bool:
    if cache_obj is not None:
        try:
            username = cache_obj['username']
            password = cache_obj['password']
            access_token = cache_obj['access_token']
            refresh_token = cache_obj['refresh_token']
            subscriptions = cache_obj['subscriptions']
            scopes = cache_obj['scopes']
            packages = cache_obj['packages']
            try:
                expiry = datetime.strptime(
                    cache_obj['expiry'], '%Y/%m/%d %H:%M:%S')
            except:
                expiry = None
            return True
        except:
            pass
        username = None
        password = None
        access_token = None
        refresh_token = None
        expiry = None
        subscriptions = None
        scopes = None
        packages = None
        return False

def _create_cache_obj() -> Dict[str, str]:
    try:
        expiry = expiry.strftime("%Y/%m/%d %H:%M:%S")
    except:
        expiry = None
    return {
        'username': username,
        'password': password,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expiry': expiry,
        'subscriptions': subscriptions,
        'scopes': scopes,
        'packages': packages
    }

expiry, access_token, refresh_token = ensure_login(expiry, access_token, refresh_token)