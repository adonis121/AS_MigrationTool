import requests
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


def Invoke_QCloudAPIPatch(API: str, Body: Optional[dict] = None, Raw: bool = False, Session: Optional[Session] = None,
                          Timeout: int = 86400):
    """
    Invoke a QCloud API PATCH request.

    :param API: The API endpoint.
    :param Body: The request body.
    :param Raw: If True, return the raw response.
    :param Session: The session object containing headers.
    :param Timeout: The request timeout in seconds.
    :return: The response from the API.
    """
    paramInvokeWebRequest = {
        'method': 'PATCH',
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    if Body is not None:
        print("Adding Body")  # Write-Verbose equivalent
        paramInvokeWebRequest['json'] = Body

    if Session:
        print("Adding Session as WebSession")  # Write-Verbose equivalent
        paramInvokeWebRequest['headers'].update(Session.headers)
    elif script_scope.QSaaSSession:
        print("Adding QSaaSSession as WebSession")  # Write-Verbose equivalent
        paramInvokeWebRequest['headers'].update(script_scope.QSaaSSession.headers)
    else:
        print("No WebSession information present")  # Write-Verbose equivalent
        raise ValueError("Please run Connect-QlikCloud first or supply a Session")

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

    print(f"{paramInvokeWebRequest['method']}: {paramInvokeWebRequest['url']}")  # Write-Verbose equivalent

    response = requests.patch(paramInvokeWebRequest['url'], headers=paramInvokeWebRequest['headers'],
                              json=paramInvokeWebRequest.get('json'), timeout=Timeout)

    if Raw:
        return response
    else:
        return response.json()


# Example usage
API = 'your/api/endpoint'
Body = {'key': 'value'}
Raw = False
session = Session(headers={'authority': 'your.authority.header.value'})
Timeout = 86400

script_scope.QSaaSSession = session  # Simulate running Connect-QlikCloud

response = Invoke_QCloudAPIPatch(API, Body, Raw, session, Timeout)
print(response)
