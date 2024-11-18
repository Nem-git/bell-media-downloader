from datetime import datetime
import base64
import requests
import tools
import time


# Logger

subscriptions = None
scopes = None
packages = None
#session = requests.Session()


# ===================================================================
#   LOGIN
# ===================================================================


def login(settings_path: str, service_name: str):

    username, password, wvd_path, custom_string = tools.read_creds_from_file(file_path=settings_path)
    refresh_token = ""
    access_token = ""
    expiry = 0.0
    try:
        tokens_info = tools.read_tokens(f"{service_name}_tokens")
        if time.mktime(datetime.now().timetuple()) > tokens_info['expiry']:
            refresh_token, access_token, expiry = ensure_login(username, password, refresh_token, service_name)
        else:
            access_token = tokens_info['a_token']
            refresh_token = tokens_info['r_token']
            expiry = tokens_info['expiry']

    except FileNotFoundError:
        refresh_token, access_token, expiry = ensure_login(username, password, refresh_token, service_name)


    # ===========================================================
    # Skip if current token is valid
    # ===========================================================

    headers = {"a_token": access_token, "r_token": refresh_token, "expiry": expiry}
    tools.write_tokens(f"{service_name}_tokens", headers)
    headers = {"Authorization": access_token}

    return headers, wvd_path, custom_string
    



def ensure_login(username, password, refresh_token, service_name) -> None | tuple[str, str, float]:
    
    # ===========================================================
    # Refresh token if possible
    # ===========================================================
    r = None
    if refresh_token != "":
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
    access_token: str = "Bearer " + resp['access_token']
    refresh_token: str = resp['refresh_token']
    expiry: float = time.mktime(datetime.now().timetuple()) + resp['expires_in']

    return refresh_token, access_token, expiry


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
    data = f'refresh_token={refresh_token}'
    return requests.post(url=url, headers=headers, data=data)



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

    return requests.post(url=url, headers=headers, data=data)



def authorization_name(service_name) -> str:
    decoded = f"{service_name}-web:default"
    
    encoded = decoded.encode()
    b64 = base64.b64encode(encoded)
    return b64.decode()
