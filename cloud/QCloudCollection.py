import requests
import json


def get_qcloud_collection(raw=False, session=None):
    APIURI = "/v1/collections"
    param_get_qsaas_api_response = {
        "API": APIURI
    }
    if session is not None:
        param_get_qsaas_api_response["Session"] = session

    return invoke_qcloud_api_get(**param_get_qsaas_api_response, raw=raw)


def new_qcloud_collection(name, description=None, type='private', raw=False, session=None):
    APIURI = "/v1/collections"
    body = {
        "name": name,
        "type": type,
        "description": description
    }
    param_qsaas_api_response = {
        "API": APIURI,
        "Raw": raw,
        "Body": json.dumps(body)
    }
    if session is not None:
        param_qsaas_api_response["Session"] = session

    return invoke_qcloud_api_post(**param_qsaas_api_response)


def invoke_qcloud_api_get(API, raw=False, Session=None):
    url = f"https://your-qlik-sense-server.com{API}"
    headers = {
        "Content-Type": "application/json",
    }
    if Session:
        response = requests.get(url, headers=headers, cookies=Session.cookies)
    else:
        response = requests.get(url, headers=headers)

    response.raise_for_status()
    if raw:
        return response.text
    return response.json()


def invoke_qcloud_api_post(API, Raw=False, Body=None, Session=None):
    url = f"https://your-qlik-sense-server.com{API}"
    headers = {
        "Content-Type": "application/json",
    }
    if Session:
        response = requests.post(url, headers=headers, data=Body, cookies=Session.cookies)
    else:
        response = requests.post(url, headers=headers, data=Body)

    response.raise_for_status()
    if Raw:
        return response.text
    return response.json()

# Example usage:
# session = requests.Session() # if you need to manage session cookies
# get_qcloud_collection(raw=True, session=session)
# new_qcloud_collection(name="My Collection", description="This is a test collection", type="public", raw=True, session=session)
