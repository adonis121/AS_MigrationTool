import requests


def get_qcloud_app(AppID, Session=None):
    APIURI = f"/v1/apps/{AppID}"
    param_get_qsaas_api_response = {
        "API": APIURI
    }
    if Session is not None:
        param_get_qsaas_api_response["Session"] = Session

    return invoke_qcloud_api_get(**param_get_qsaas_api_response)


def copy_qcloud_app(AppID, Session=None):
    APIURI = f"/v1/apps/{AppID}/copy"
    param_get_qsaas_api_response = {
        "API": APIURI
    }
    if Session is not None:
        param_get_qsaas_api_response["Session"] = Session

    return invoke_qcloud_api_post(**param_get_qsaas_api_response)


def invoke_qcloud_api_get(API, Session=None):
    url = f"https://your-qlik-sense-server.com{API}"
    headers = {
        "Content-Type": "application/json",
    }
    if Session:
        response = requests.get(url, headers=headers, cookies=Session.cookies)
    else:
        response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json()


def invoke_qcloud_api_post(API, Session=None):
    url = f"https://your-qlik-sense-server.com{API}"
    headers = {
        "Content-Type": "application/json",
    }
    if Session:
        response = requests.post(url, headers=headers, cookies=Session.cookies)
    else:
        response = requests.post(url, headers=headers)

    response.raise_for_status()
    return response.json()

# Example usage:
# session = requests.Session() # if you need to manage session cookies
# app_id = "your-app-id"
# get_qcloud_app(app_id, session)
# copy_qcloud_app(app_id, session)
