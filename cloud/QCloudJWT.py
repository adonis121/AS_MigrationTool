import requests
import datetime
import subprocess
import os

def new_qcloud_jwt(Tenant, TenantAdminAPI, Certificate=None, Lifespan=7):
    """
    Creates a new QCloud JWT.

    :param Tenant: Tenant URI
    :param TenantAdminAPI: Tenant admin API
    :param Certificate: X.509 certificate (optional)
    :param Lifespan: Lifespan of the JWT in days (default: 7)
    :return: JWT information
    """
    TenantURI = format_qcloud_tenant_uri(Tenant)

    if Certificate is None:
        ValidTo = datetime.datetime.utcnow() + datetime.timedelta(days=Lifespan)
        SystemDNS = subprocess.check_output(['hostname']).decode().strip()
        Command = ['openssl', 'req', '-x509', '-nodes', '-newkey', 'rsa:2048', '-keyout', 'jwt.key',
                   '-out', 'jwt.crt', '-days', str(Lifespan), '-subj',
                   '/CN=JWT Auth {},L={}'.format(os.environ['USERNAME'], SystemDNS)]
        subprocess.run(Command, check=True)

        Certificate = {
            'Issuer': os.environ['USERNAME'],
            'Thumbprint': subprocess.check_output(['openssl', 'x509', '-in', 'jwt.crt', '-fingerprint', '-noout'])
                            .decode().strip().split('=')[-1].replace(':', '').upper(),
            'PrivateKey': 'jwt.key'
        }

    elif Certificate.get('PrivateKey') is None:
        raise ValueError("Certificate Provided requires Private key")

    TenantSession = new_qcloud_session(Tenant=TenantURI, TenantAdminAPI=TenantAdminAPI, ReturnTenants=True)
    AdminSession = TenantSession['Session']
    tenants = TenantSession['Tenants']
    Pem = convert_to_pem(Certificate)
    CreateJWTAuthPayload = {
        'provider': 'external',
        'description': 'QSaasJWT Created by {} on {}'.format(os.environ['USERNAME'], SystemDNS),
        'interactive': False,
        'protocol': 'jwtAuth',
        'tenantIds': [tenants['data'][0]['id']],
        'options': {
            'issuer': Certificate['Issuer'],
            'staticKeys': [{
                'pem': Pem.replace("\r\n", ""),
                'kid': Certificate['Thumbprint']
            }]
        }
    }

    APIURI = "/v1/identity-providers"
    EJWTIDP = invoke_rest_method("{}api{}".format(TenantURI, APIURI), WebSession=AdminSession)
    if Certificate['Thumbprint'] not in [key['kid'] for key in EJWTIDP['data']['options']['statickeys']]:
        JWTIDP = invoke_rest_method("{}api{}".format(TenantURI, APIURI), Method='POST',
                                    Body=CreateJWTAuthPayload, WebSession=AdminSession)
    else:
        JWTIDP = next((item for item in EJWTIDP['data'] if item['options']['statickeys'][0]['kid'] == Certificate['Thumbprint']), None)

    return {
        'Certificate': Certificate,
        'TenantURI': TenantURI,
        'JWTIDP': JWTIDP,
        'AdminSession': AdminSession
    }

def remove_qcloud_jwt(Tenant, TenantAdminAPI, ID):
    """
    Removes a QCloud JWT.

    :param Tenant: Tenant URI
    :param TenantAdminAPI: Tenant admin API
    :param ID: ID of the JWT to remove
    """
    TenantURI = format_qcloud_tenant_uri(Tenant)
    TenantAdminHeader = {
        'Authorization': 'Bearer {}'.format(TenantAdminAPI)
    }
    APIURI = "/v1/identity-providers"
    identityproviders = invoke_rest_method("{}api{}".format(TenantURI, APIURI), Headers=TenantAdminHeader, Method='GET')
    JWTIDPObj = next((item for item in identityproviders['data'] if item['protocol'] == 'jwtAuth' and item['id'] == ID), None)

    if JWTIDPObj is not None:
        APIURI = "/v1/identity-providers/{}".format(JWTIDPObj['id'])
        invoke_rest_method("{}api{}".format(TenantURI, APIURI), Headers=TenantAdminHeader, Method='DELETE')

def format_qcloud_tenant_uri(Tenant):
    # Assuming FormatQCloudTenantURI is a separate function, you can implement it here
    pass

def convert_to_pem(Certificate):
    # Assuming ConvertToPem is a separate function, you can implement it here
    pass

def new_qcloud_session(Tenant, TenantAdminAPI, ReturnTenants):
    # Assuming New-QCloudSession is a separate function, you can implement it here
    pass

def invoke_rest_method(URL, Method='GET', Body=None, Headers=None, WebSession=None):
    # Assuming Invoke-RestMethod is a separate function, you can implement it here
    pass
