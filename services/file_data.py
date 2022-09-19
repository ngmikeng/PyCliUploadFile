import requests
import json

from configs import env
from utils import errors
from . import base_service


class FileDataService(base_service.BaseService):

    def upload_file(self, file_id: str, file_path, access_token: str):
        try:
            base_url = self.api_url
            headers = {
                'Authorization': f'Bearer {access_token}',
            }
            file_content = open(file_path, 'rb')
            files = {'file': file_content}
            response = requests.post(
                f'{base_url}/pjr-template/v1/upload/pjr-templates/{file_id}/single-file',
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

