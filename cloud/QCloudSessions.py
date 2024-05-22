import requests

def new_qcloud_session(Tenant, TenantAdminAPI, ReturnTenants=False):
    """
    Creates a new QCloud session.

    :param Tenant: QCloud tenant
    :param TenantAdminAPI: QCloud tenant admin API key
    :param ReturnTenants: Flag to return tenants along with the session (default: False)
    :return: QCloud session or session and tenants
    """
    TenantAdminHeader = {
        'Authorization': f'Bearer {TenantAdminAPI}'
    }

    API_URI = f'{Tenant}/api/v1/tenants'

    UriBuilder = requests.compat.urlparse(API_URI)
    UriBuilder = UriBuilder._replace(port=443, scheme='https')

    Tenants = requests.get(UriBuilder.geturl(), headers=TenantAdminHeader).json()

    AdminSession = requests.Session()
    AdminSession.headers['authority'] = UriBuilder.hostname

    if ReturnTenants:
        return {'Session': AdminSession, 'Tenants': Tenants}
    else:
        return AdminSession
