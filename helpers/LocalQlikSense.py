import win32api
import win32con
import win32crypt
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from typing import List

class QSECMConnection:
    def __init__(self, connected: bool, qlik_client: x509.Certificate):
        self.connected = connected
        self.qlik_client = qlik_client

def get_certificates(subject_name: str) -> List[x509.Certificate]:
    certificates = []

    def get_certificates_from_store(store_name, store_location):
        store_flag = {
            "CurrentUser": win32con.CERT_SYSTEM_STORE_CURRENT_USER,
            "LocalMachine": win32con.CERT_SYSTEM_STORE_LOCAL_MACHINE
        }[store_location]

        store = win32crypt.CertOpenStore(
            win32crypt.CERT_STORE_PROV_SYSTEM, 0, None, store_flag, store_name
        )
        if not store:
            raise OSError("Failed to open certificate store")

        context = win32crypt.CertFindCertificateInStore(
            store, win32crypt.X509_ASN_ENCODING, 0, win32crypt.CERT_FIND_SUBJECT_STR, subject_name, None
        )

        while context:
            cert_data = context.pbCertEncoded[:context.cbCertEncoded]
            cert = x509.load_der_x509_certificate(cert_data, default_backend())
            certificates.append(cert)
            context = win32crypt.CertFindCertificateInStore(
                store, win32crypt.X509_ASN_ENCODING, 0, win32crypt.CERT_FIND_SUBJECT_STR, subject_name, context
            )

        win32crypt.CertCloseStore(store, 0)

    get_certificates_from_store("My", "CurrentUser")
    get_certificates_from_store("My", "LocalMachine")

    return certificates

def connect_qlik_sense(certificate: x509.Certificate, username: str, trust_all_certificates: bool) -> bool:
    # Replace this with the actual connection logic to Qlik Sense
    return True

def connect_local_qlik_sense() -> QSECMConnection:
    subject_name = 'CN=QlikClient'
    qlik_client_certificates = get_certificates(subject_name)
    connected = False
    qsecm_connection = QSECMConnection(connected, None)

    for cert in qlik_client_certificates:
        if not connected:
            try:
                success = connect_qlik_sense(cert, 'internal\\sa_api', True)
                if success:
                    connected = True
                    qsecm_connection.connected = connected
                    qsecm_connection.qlik_client = cert
            except Exception as e:
                print(f"Connection failed: {e}")

    return qsecm_connection

# Example usage
if __name__ == "__main__":
    connection = connect_local_qlik_sense()
    if connection.connected:
        print("Connected to Qlik Sense")
    else:
        print("Failed to connect to Qlik Sense")
