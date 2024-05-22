import requests
import json


def get_qcloud_glossaries(ID=None, Filter=None, Raw=False, Session=None, All=False):
    APIURI = 'https://localhost/api/v1/glossaries'
    if ID is not None:
        APIURI = f"https://localhost/api/v1/glossaries/{ID}/terms"

    param_get_qsaas_api_response = {
        "API": APIURI
    }

    if Filter is not None:
        join_char = "?" if '?' not in APIURI else "&"
        str_filter = f"filter={format_filter_string(Filter)}"
        param_get_qsaas_api_response["API"] = f"{APIURI}{join_char}{str_filter}"

    if Session is not None:
        param_get_qsaas_api_response["Session"] = Session

    response = invoke_qcloud_api_get(**param_get_qsaas_api_response, Raw=Raw)

    try:
        response_data = response.get('data', [])
        if All:
            while response.get('links', {}).get('next') is not None:
                param_get_qsaas_api_response["API"] = response['links']['next']['href']
                next_response = invoke_qcloud_api_get(**param_get_qsaas_api_response, Raw=Raw)
                response_data.extend(next_response.get('data', []))
                response['links'] = next_response.get('links', {})
    except Exception as e:
        print(f"Error: {e}")

    return response


def format_filter_string(filter_string):
    # Implement this function based on how the filter string needs to be formatted
    return filter_string


def invoke_qcloud_api_get(API, Raw=False, Session=None):
    headers = {
        "Content-Type": "application/json",
    }

    if Session:
        response = requests.get(API, headers=headers, cookies=Session.cookies)
    else:
        response = requests.get(API, headers=headers)

    response.raise_for_status()
    return response.json() if not Raw else response.text

# Example usage:
# session = requests.Session()  # if you need to manage session cookies
# print(get_qcloud_glossaries(ID='some_id', Filter='some_filter', Raw=False, Session=session, All=True))
