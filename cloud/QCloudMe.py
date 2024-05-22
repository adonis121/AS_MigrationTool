import requests

def get_qcloud_me(Session=None):
    """
    Retrieves QCloud "me" claims.

    :param Session: Web request session
    :return: Response data
    """
    API_URI = "/v1/claims/me"

    param_get_qsaas_api_response = {
        'API': API_URI
    }

    if Session is not None:
        param_get_qsaas_api_response['Session'] = Session

    return invoke_qcloud_api_get(param_get_qsaas_api_response)

def invoke_qcloud_api_get(params):
    """
    Invokes QCloud API GET request.

    :param params: Parameters for API request
    :return: Response data
    """
    if 'Session' in params:
        response = requests.get(params['API'], session=params['Session'])
    else:
        response = requests.get(params['API'])

    return response.json()
