import requests
import json
import re
import uuid
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


def read_file_bytes(file_path: str) -> bytes:
    with open(file_path, 'rb') as file:
        return file.read()


def Invoke_QCloudAPIPost(API: str, Body: Optional[dict] = None, InFile: Optional[str] = None, Raw: bool = False,
                         Session: Optional[Session] = None, Timeout: int = 86400, SuppressProgress: bool = False):
    """
    Invoke a QCloud API POST request.

    :param API: The API endpoint.
    :param Body: The request body.
    :param InFile: The input file path.
    :param Raw: If True, return the raw response.
    :param Session: The session object containing headers.
    :param Timeout: The request timeout in seconds.
    :param SuppressProgress: If True, suppress progress reporting.
    :return: The response from the API.
    """
    paramInvokeWebRequest = {
        'method': 'POST',
        'headers': {}
    }

    if InFile and Body:
        paramInvokeWebRequest['headers']['Content-Type'] = 'multipart/form-data'
        file_bytes = read_file_bytes(InFile)
        file_enc = file_bytes.decode('ISO-8859-1')
        boundary = str(uuid.uuid4())
        lf = '\r\n'
        databody = json.dumps(Body, separators=(',', ':'))
        body_lines = (
            f"--{boundary}",
            'Content-Disposition: form-data; name="data"',
            '',
            databody,
            f"--{boundary}",
            f'Content-Disposition: form-data; name="file"; filename="{InFile.split("/")[-1]}"',
            'Content-Type: application/x-zip-compressed',
            '',
            file_enc,
            f"--{boundary}--{lf}"
        )
        body = lf.join(body_lines)
        paramInvokeWebRequest['headers']['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        paramInvokeWebRequest['data'] = body
    elif Body:
        paramInvokeWebRequest['data'] = json.dumps(Body)
        paramInvokeWebRequest['headers']['Content-Type'] = 'application/json'
    elif InFile:
        paramInvokeWebRequest['data'] = read_file_bytes(InFile)
        paramInvokeWebRequest['headers']['Content-Type'] = 'application/octet-stream'

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

    if SuppressProgress:
        # Progress suppression equivalent can be implemented here if needed
        pass

    try:
        if Raw:
            response = requests.post(paramInvokeWebRequest['url'], headers=paramInvokeWebRequest['headers'],
                                     data=paramInvokeWebRequest.get('data'), timeout=Timeout)
            return response
        else:
            response = requests.post(paramInvokeWebRequest['url'], headers=paramInvokeWebRequest['headers'],
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
InFile = 'path/to/your/file.zip'
Raw = False
session = Session(headers={'authority': 'your.authority.header.value'})
Timeout = 86400
SuppressProgress = False

script_scope.QSaaSSession = session  # Simulate running Connect-QlikCloud

response = Invoke_QCloudAPIPost(API, Body, InFile, Raw, session, Timeout, SuppressProgress)
print(response)
