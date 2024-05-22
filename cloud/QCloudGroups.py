import requests

def get_qcloud_groups(ID=None, Filter=None, Limit=100, Raw=False, Session=None, All=False):
    """
    Retrieves QCloud groups.

    :param ID: Group ID (optional)
    :param Filter: Filter string (optional)
    :param Limit: Limit for results (default: 100)
    :param Raw: Raw response flag (default: False)
    :param Session: Web request session (optional)
    :param All: Retrieve all results flag (default: False)
    :return: Response data
    """
    API_URI = 'https://localhost/api/v1/groups'
    if ID is not None:
        API_URI = f'https://localhost/api/v1/groups/{ID}'

    params = {
        '"totalResults"': 'true',  # Enclosing totalResults in double quotes
        'limit': Limit
    }

    if Filter:
        params['filter'] = Filter

    response_data = []

    while True:
        response = requests.get(API_URI, params=params, session=Session)
        response_json = response.json()

        response_data.extend(response_json.get('data', []))

        if not All or 'next' not in response_json.get('links', {}):
            break

        next_link = response_json['links']['next']['href']
        response = requests.get(next_link, session=Session)
        response_json = response.json()

        API_URI = next_link
        params = {}

    return response_data

def remove_qcloud_groups(ID, Session=None):
    """
    Removes QCloud groups.

    :param ID: Group ID
    :param Session: Web request session (optional)
    :return: None
    """
    API_URI = f'https://your-tenant.us.qlikcloud.com/api/v1/groups/{ID}'

    response = requests.delete(API_URI, session=Session)
    return response

# Example usage:
# get_qcloud_groups(ID='example_id', Filter='example_filter', Limit=100, Raw=False, Session=None, All=False)
# remove_qcloud_groups(ID='example_id', Session=None)
