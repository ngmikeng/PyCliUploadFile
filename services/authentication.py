import requests
import json

from utils import errors
from . import base_service


class AuthenticationService(base_service.BaseService):

    def login(self, username: str, password: str):
        try:
            base_url = self.api_url
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
            msg = f'Error Connecting: {str(connection_error.args[0])}'
            return errors.error_response(msg, connection_error)
        except requests.exceptions.Timeout as timeout_error:
            msg = f'Timeout Error: {str(timeout_error.args[0])}'
            return errors.error_response(msg, timeout_error)
        except requests.exceptions.RequestException as request_error:
            msg = f'Request Error: {str(request_error.args[0])}'
            return errors.error_response(msg, request_error)
        except FileNotFoundError as file_error:
            return errors.error_response(f'File Not Found Error: {file_error.filename}', file_error)
        except RuntimeError:
            msg = f'Runtime Error: {str(RuntimeError.args[0])}'
            return errors.error_response(msg, RuntimeError)

