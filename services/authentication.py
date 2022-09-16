import requests
import json

from configs import env
from utils import errors


def login(username: str, password: str):
    try:
        env_config = env.get_env()
        base_url = env_config.get('apiBaseUrl')
        auth_token = 'bmdkZy1wYXNzd29yZDpzZWNyZXQ'
        headers = {
            'Authorization': f'Basic {auth_token}',
            'Content-type': 'application/x-www-form-urlencoded'
        }
        data = {'username': username, 'password': password, 'grant_type': 'password'}
        response = requests.post(
            f'{base_url}/auth/oauth/token',
            data=data,
            headers=headers
        )
        response.raise_for_status()

        return response.json()
    except requests.exceptions.HTTPError as http_error:
        error_data = json.loads(http_error.response.text)
        error_status = http_error.response.status_code
        message = errors.get_error_message(error_data, error_status)
        return errors.error_response(message)
    except requests.exceptions.ConnectionError as connection_error:
        return errors.error_response('Error Connecting', connection_error)
    except requests.exceptions.Timeout as timeout_error:
        return errors.error_response('Timeout Error', timeout_error)
    except requests.exceptions.RequestException as request_error:
        return errors.error_response('Request Error', request_error)
    except FileNotFoundError as file_error:
        return errors.error_response(f'File Not Found Error: {file_error.filename}', file_error)
    except RuntimeError:
        return errors.error_response(f'Runtime Error', RuntimeError)
