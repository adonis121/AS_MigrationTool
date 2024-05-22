import requests

def get_qcloud_users(ID=None, Filter=None, Limit=100, Raw=False, Session=None, All=False, Me=False):
    """
    Retrieves QCloud users.

    :param ID: User ID
    :param Filter: Filter string
    :param Limit: Limit for results (default: 100)
    :param Raw: Raw response flag (default: False)
    :param Session: Web request session
    :param All: Retrieve all results flag (default: False)
    :param Me: Retrieve information about the current user
    :return: Response data
    """
    if Me:
        APIURI = "https://localhost/api/v1/users/me"
    elif ID:
        APIURI = f"https://localhost/api/v1/users/{ID}"
    else:
        APIURI = "https://localhost/api/v1/users"

    Query = {}
    Query['totalResults'] = "true"
    Query['limit'] = Limit

    if Filter:
        APIURI += f"?filter={Filter}"
    if Query:
        APIURI += "&" + "&".join([f'{key}="{value}"' for key, value in Query.items()])

    paramGetQSaaSAPIResponse = {}
    if Session:
        paramGetQSaaSAPIResponse['Session'] = Session

    RawResponse = requests.get(APIURI, headers={}, params={}, session=Session)
    Response = RawResponse.json()

    if Response.get('data'):
        Response['data'] = Response['data'] if isinstance(Response['data'], list) else [Response['data']]
        if All:
            while Response.get('links', {}).get('next'):
                paramGetQSaaSAPIResponse['API'] = Response['links']['next']['href']
                RawNextResponse = requests.get(paramGetQSaaSAPIResponse['API'], headers={}, params={}, session=Session)
                NextResponse = RawNextResponse.json()
                Response['data'].extend(NextResponse['data'] if isinstance(NextResponse['data'], list) else [NextResponse['data']])
                Response['links'] = NextResponse['links']

        return Response

    return Response
