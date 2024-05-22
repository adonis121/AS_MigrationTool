import requests

def get_qcloud_items(ID=None, collectionId=None, createdByUserId=None, name=None,
                     notCreatedByUserId=None, notOwnerId=None, ownerId=None,
                     query=None, resourceId=None, resourceIds=None,
                     resourceSubType=None, resourceType=None, shared=None,
                     spaceId=None, Filter=None, Type=None, Limit=100,
                     Raw=False, Session=None, All=False):
    """
    Retrieves QCloud items.

    :param ID: Item ID
    :param collectionId: Collection ID
    :param createdByUserId: Created by user ID
    :param name: Item name
    :param notCreatedByUserId: Not created by user ID
    :param notOwnerId: Not owner ID
    :param ownerId: Owner ID
    :param query: Query string
    :param resourceId: Resource ID
    :param resourceIds: Resource IDs
    :param resourceSubType: Resource sub type
    :param resourceType: Resource type
    :param shared: Shared flag
    :param spaceId: Space ID
    :param Filter: Filter string
    :param Type: Type of items
    :param Limit: Limit for results (default: 100)
    :param Raw: Raw response flag (default: False)
    :param Session: Web request session
    :param All: Retrieve all results flag (default: False)
    :return: Response data
    """
    API_URI = "https://localhost/api/v1/items"
    QueryBuilder = {}
    if ID: QueryBuilder['id'] = ID
    if collectionId: QueryBuilder['collectionId'] = collectionId
    if createdByUserId: QueryBuilder['createdByUserId'] = createdByUserId
    if name: QueryBuilder['name'] = name
    if notCreatedByUserId: QueryBuilder['notCreatedByUserId'] = notCreatedByUserId
    if notOwnerId: QueryBuilder['notOwnerId'] = notOwnerId
    if ownerId: QueryBuilder['ownerId'] = ownerId
    if query: QueryBuilder['query'] = query
    if resourceId: QueryBuilder['resourceId'] = resourceId
    if resourceIds: QueryBuilder['resourceIds'] = resourceIds
    if resourceType: QueryBuilder['resourceType'] = resourceType
    if resourceSubType: QueryBuilder['resourceSubType'] = resourceSubType
    if shared: QueryBuilder['shared'] = shared
    if spaceId: QueryBuilder['spaceId'] = spaceId

    params = {'limit': Limit}
    params.update(QueryBuilder)

    if Filter:
        params['filter'] = Filter

    response = invoke_qcloud_api_get(API_URI, params=params, Raw=Raw, Session=Session)

    if All:
        while response['links'].get('next'):
            next_link = response['links']['next']['href']
            response_next = invoke_qcloud_api_get(next_link, Raw=Raw, Session=Session)
            response['data'].extend(response_next['data'])
            response['links'] = response_next['links']

    return response

def invoke_qcloud_api_get(url, params=None, Raw=False, Session=None):
    """
    Invokes QCloud API GET request.

    :param url: URL for the API request
    :param params: Parameters for API request
    :param Raw: Raw response flag (default: False)
    :param Session: Web request session
    :return: Response data
    """
    if Session:
        response = Session.get(url, params=params)
    else:
        response = requests.get(url, params=params)

    return response.json() if not Raw else response.text
