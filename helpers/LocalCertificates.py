import win32crypt
import win32certificate
from ctypes import POINTER, byref
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from win32com.client import Dispatch


def get_certificates(subject_name):
    certificates = []

    def get_certificates_from_store(store_name, store_location):
        store_flag = {
            "CurrentUser": win32crypt.CERT_SYSTEM_STORE_CURRENT_USER,
            "LocalMachine": win32crypt.CERT_SYSTEM_STORE_LOCAL_MACHINE
        }[store_location]

        store = win32crypt.CertOpenStore(win32crypt.CERT_STORE_PROV_SYSTEM, 0, None, store_flag, store_name)
        if not store:
            raise OSError("Failed to open certificate store")

        context = win32crypt.CertFindCertificateInStore(store, win32crypt.X509_ASN_ENCODING, 0,
                                                        win32crypt.CERT_FIND_SUBJECT_STR, subject_name, None)

        while context:
            cert_data = context.pbCertEncoded[:context.cbCertEncoded]
            cert = x509.load_der_x509_certificate(cert_data, default_backend())
            certificates.append(cert)
            context = win32crypt.CertFindCertificateInStore(store, win32crypt.X509_ASN_ENCODING, 0,
                                                            win32crypt.CERT_FIND_SUBJECT_STR, subject_name, context)

        win32crypt.CertCloseStore(store, 0)

    get_certificates_from_store("My", "CurrentUser")
    get_certificates_from_store("My", "LocalMachine")

    return certificates


# Example usage
if __name__ == "__main__":
    subject_name = "Your Subject Name"
    certs = get_certificates(subject_name)
    for cert in certs:
        print(cert.subject)
