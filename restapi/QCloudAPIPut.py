import requests
import json
import re
from typing import Optional


class ScriptScope:
    def __init__(self):
        self.QSaaSSession = None


script_scope = ScriptScope()


class Session:
    def __init__(self, headers: dict):
        self.headers = headers


def FormatQCloudTenantURI(authority: str) -> str:
    # Implement the equivalent of the FormatQCloudTenantURI function here
    return f"https://{authority}"


def Invoke_QCloudAPIPut(API: str, Body: Optional[dict] = None, Raw: bool = False, Session: Optional[Session] = None,
                        Timeout: int = 86400):
    """
    Invoke a QCloud API PUT request.

    :param API: The API endpoint.
    :param Body: The request body.
    :param Raw: If True, return the raw response.
    :param Session: The session object containing headers.
    :param Timeout: The request timeout in seconds.
    :return: The response from the API.
    """
    paramInvokeWebRequest = {
        'method': 'PUT',
        'headers': {'Content-Type': 'application/json'}
    }

    if Body:
        paramInvokeWebRequest['data'] = json.dumps(Body)

    if Session:
        paramInvokeWebRequest['headers'].update(Session.headers)
    elif script_scope.QSaaSSession:
        paramInvokeWebRequest['headers'].update(script_scope.QSaaSSession.headers)
    else:
        raise ValueError('Please run Connect-QlikCloud first or supply a Session')

    regex_http = re.compile(r'^(http|https)://', re.IGNORECASE)
    API = API.lstrip('/')

    if regex_http.match(API):
        paramInvokeWebRequest['url'] = API
    else:
        authority = paramInvokeWebRequest['headers'].get("authority")
        if not authority:
            raise ValueError("The session must contain an 'authority' header.")
        base_uri = FormatQCloudTenantURI(authority)
        if API.startswith('api'):
            paramInvokeWebRequest['url'] = f"{base_uri}{API}"
        else:
            paramInvokeWebRequest['url'] = f"{base_uri}api/{API}"

    try:
        if Raw:
            response = requests.put(paramInvokeWebRequest['url'], headers=paramInvokeWebRequest['headers'],
                                    data=paramInvokeWebRequest.get('data'), timeout=Timeout)
            return response
        else:
            response = requests.put(paramInvokeWebRequest['url'], headers=paramInvokeWebRequest['headers'],
                                    data=paramInvokeWebRequest.get('data'), timeout=Timeout)
            return response.json()
    except Exception as e:
        print(f"Error Calling {paramInvokeWebRequest['method']}: {paramInvokeWebRequest['url']}")
        if Body:
            print(json.dumps(Body, separators=(',', ':')))
        print(str(e))


# Example usage
API = 'your/api/endpoint'
Body = {'key': 'value'}
Raw = False
session = Session(headers={'authority': 'your.authority.header.value'})
Timeout = 86400

script_scope.QSaaSSession = session  # Simulate running Connect-QlikCloud

response = Invoke_QCloudAPIPut(API, Body, Raw, session, Timeout)
print(response)
