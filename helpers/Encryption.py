import base64
import win32crypt

def protect_with_machine_key(input_string):
    # Convert the input string to bytes
    byte_data = input_string.encode('utf-8')

    # Encrypt the data using the Windows Data Protection API
    encrypted_data = win32crypt.CryptProtectData(byte_data, None, None, None, None, 0)

    # Convert the encrypted data to a base64 encoded string
    return base64.b64encode(encrypted_data[1]).decode('utf-8')


def unprotect_with_machine_key(input_string):
    # Decode the base64 encoded string to bytes
    encrypted_data = base64.b64decode(input_string.encode('utf-8'))

    # Decrypt the data using the Windows Data Protection API
    decrypted_data = win32crypt.CryptUnprotectData(encrypted_data, None, None, None, 0)

    # Convert the decrypted data to a string
    return decrypted_data[1].decode('utf-8')


# Example usage:
if __name__ == "__main__":
    original_string = "This is a secret message."
    print(f"Original String: {original_string}")

    protected_string = protect_with_machine_key(original_string)
    print(f"Protected String: {protected_string}")

    unprotected_string = unprotect_with_machine_key(protected_string)
    print(f"Unprotected String: {unprotected_string}")
