import requests

def get_qcloud_roles(Session=None):
    """
    Retrieves QCloud roles.

    :param Session: Web request session
    :return: Response data
    """
    API_URI = "/v1/roles"

    param_get_qsaas_api_response = {
        'API': API_URI
    }

    if Session is not None:
        param_get_qsaas_api_response['Session'] = Session

    return get_qcloud_api_response(param_get_qsaas_api_response)

def get_qcloud_api_response(params):
    """
    Retrieves QCloud API response.

    :param params: Parameters for API request
    :return: Response data
    """
    if 'Session' in params:
        response = requests.get(params['API'], session=params['Session'])
    else:
        response = requests.get(params['API'])

    return response.json()
