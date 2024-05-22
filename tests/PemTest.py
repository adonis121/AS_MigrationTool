# Generate a private key
openssl genpkey -algorithm RSA -out private_key.pem

# Generate a self-signed certificate in PEM format
openssl req -new -x509 -key private_key.pem -out certificate.pem -days 365 -subj "/CN=Test"

# Convert the PEM certificate to DER format
openssl x509 -outform der -in certificate.pem -out certificate.der


from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_der_x509_certificate, load_pem_x509_certificate
from cryptography import x509

def convert_to_pem(certificate: x509.Certificate) -> str:
    """
    Converts an X509 certificate to PEM format.

    :param certificate: An X509 certificate object
    :return: PEM-formatted certificate string
    """
    pem = certificate.public_bytes(serialization.Encoding.PEM)
    return pem.decode('utf-8')

def test_convert_to_pem():
    # Load certificate from DER
    with open('certificate.der', 'rb') as cert_file:
        cert_bytes = cert_file.read()
        cert_der = load_der_x509_certificate(cert_bytes)
        pem_der = convert_to_pem(cert_der)
        print("PEM from DER:")
        print(pem_der)

    # Load certificate from PEM
    with open('certificate.pem', 'rb') as cert_file:
        cert_bytes = cert_file.read()
        cert_pem = load_pem_x509_certificate(cert_bytes)
        pem_pem = convert_to_pem(cert_pem)
        print("PEM from PEM:")
        print(pem_pem)

    # Verify the outputs are the same
    assert pem_der == pem_pem, "PEM outputs from DER and PEM should match"
    print("Test passed: PEM outputs match.")

# Run the test
test_convert_to_pem()
