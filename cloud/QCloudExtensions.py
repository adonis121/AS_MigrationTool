import requests
import json


def get_qcloud_extensions(session=None):
    APIURI = "https://your-tenant.us.qlikcloud.com/api/v1/extensions"

    param_get_qsaas_api_response = {
        "API": APIURI
    }

    if session is not None:
        param_get_qsaas_api_response["Session"] = session

    return invoke_qcloud_api_get(**param_get_qsaas_api_response)


def publish_qcloud_extensions(session=None, infile=None, name=None, tags=None):
    APIURI = "https://your-tenant.us.qlikcloud.com/api/v1/extensions"

    param_get_qsaas_api_response = {
        "API": APIURI
    }

    if session is not None:
        param_get_qsaas_api_response["Session"] = session
    if infile is not None:
        param_get_qsaas_api_response["InFile"] = infile

    body = {}
    if name is not None:
        body["name"] = name
    if tags is not None:
        body["tags"] = tags

    param_get_qsaas_api_response["body"] = json.dumps(body)

    return invoke_qcloud_api_post(**param_get_qsaas_api_response)


def invoke_qcloud_api_get(API, Session=None):
    headers = {
        "Content-Type": "application/json",
    }

    if Session:
        response = requests.get(API, headers=headers, cookies=Session.cookies)
    else:
        response = requests.get(API, headers=headers)

    response.raise_for_status()
    return response.json()


def invoke_qcloud_api_post(API, body=None, Session=None):
    headers = {
        "Content-Type": "application/json",
    }

    if Session:
        response = requests.post(API, headers=headers, data=body, cookies=Session.cookies)
    else:
        response = requests.post(API, headers=headers, data=body)

    response.raise_for_status()
    return response.json()

# Example usage:
# session = requests.Session()  # if you need to manage session cookies
# print(get_qcloud_extensions(session=session))
# publish_qcloud_extensions(session=session, infile='path/to/file.zip', name="MyExtension", tags=["tag1", "tag2"])
