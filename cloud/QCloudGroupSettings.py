def update_qcloud_group_settings(Session, syncIdpGroups=None, autoCreateGroups=None):
    """
    Updates QCloud group settings.

    :param Session: Web request session
    :param syncIdpGroups: Whether to sync IdP groups
    :param autoCreateGroups: Whether to auto-create groups
    :return: Updated group settings
    """
    API_URI = 'https://your-tenant.region.qlikcloud.com/api/v1/groups/settings'

    current_settings = get_qcloud_group_settings(Session)

    changes = []

    if syncIdpGroups is not None and current_settings.get('syncIdpGroups') != syncIdpGroups:
        changes.append({'op': 'replace', 'path': '/syncIdpGroups', 'value': syncIdpGroups})

    if autoCreateGroups is not None and current_settings.get('autoCreateGroups') != autoCreateGroups:
        changes.append({'op': 'replace', 'path': '/autoCreateGroups', 'value': autoCreateGroups})

    if changes:
        response = requests.patch(API_URI, json=changes, session=Session)
        current_settings = get_qcloud_group_settings(Session)

    return current_settings
