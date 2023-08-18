import json
from cryptography.fernet import Fernet

import variables

cipher_suite = Fernet(variables.key)


def encrypt_data(data):
    """
    Encrypts the data according to Fernet symmetric encryption
    :param data: Data that needs to be encrypted.
    :return: Encrypted Data
    """
    # Converting the data into bytecode.
    byte_data = data.encode()
    encrypted_data = cipher_suite.encrypt(byte_data)
    # Convert encrypted bytes back to Hashed Message Authentication Code (HMAC) string.
    return encrypted_data.decode()


def decrypt_data(data):
    """
    Decrypts the data according to Fernet symmetric encryption
    :param data: Encrypted data.
    :return: Decrypted data
    """
    byte_data = data.encode()
    decrypted_data = cipher_suite.decrypt(byte_data)
    return decrypted_data.decode()


def transform_data(data):
    """
    Transform and flatten the data according the database schema.
    :param data: Dictionary formatted data.
    :return: Transformed data
    """
    # Check if the provided data format is string and parse it into JSON format.
    try:
        parsed_data = json.loads(data) if isinstance(data, str) else data
    except json.JSONDecodeError:
        print(f'Error decoding the data. The provided data is not a valid JSON string.')
        return {}
    ip = parsed_data.get('ip', 'DEFAULT_IP')
    device_id = parsed_data.get('device_id', 'DEFAULT_DEVICE_ID')

    masked_ip = encrypt_data(ip)
    masked_device_id = encrypt_data(device_id)

    app_version = 0
    if 'app_version' in parsed_data:
        app_version = int(''.join([i for i in parsed_data.get('app_version') if i.isdigit()]))

    return {
        'user_id': parsed_data['user_id'],
        'device_type': parsed_data.get('device_type', 'DEFAULT_DEVICE_TYPE'),
        'masked_ip': masked_ip,
        'masked_device_id': masked_device_id,
        'locale': parsed_data.get('locale', 'DEFAULT_LOCALE'),
        'app_version': app_version
    }
