import requests
import json

from configs import env
from utils import errors


def upload_file(file_id: str, file_path, access_token: str):
    try:
        env_config = env.get_env()
        base_url = env_config.get('apiBaseUrl')
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        file_content = open(file_path, 'rb')
        files = {'file': file_content}
        response = requests.post(
            f'{base_url}/uno-template/v1/upload/uno-templates/{file_id}/single-file',
            files=files,
            headers=headers
        )
        response.raise_for_status()

        return response.text
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
