from cryptography.hazmat.primitives import serialization
from cryptography import x509

def convert_to_pem(certificate: x509.Certificate) -> str:
    """
    Converts an X509 certificate to PEM format.

    :param certificate: An X509 certificate object
    :return: PEM-formatted certificate string
    """
    pem = certificate.public_bytes(serialization.Encoding.PEM)
    return pem.decode('utf-8')

# Example usage
# Assuming you have an X509 certificate object, `cert`
# print(convert_to_pem(cert))
