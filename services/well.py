from typing import Union, List

import requests
import json

from models.error import ErrorResponse
from models.well import Well
from utils import errors
from . import base_service


class WellService(base_service.BaseService):

    def get_wells(self, access_token: str) -> Union[List[Well], ErrorResponse]:
        try:
            base_url = self.api_url
            headers = {
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(
                f'{base_url}/well/v1/wells/',
                headers=headers
            )
            response.raise_for_status()
            data: list = response.json()
            result = []
            for each in data:
                well = Well(
                    id=each.get('id'),
                    ts=each.get('ts'),
                    created=each.get('created'),
                    modified=each.get('modified'),
                    name=each.get('name'),
                    api=each.get('api'),
                    organization_id=each.get('organizationId'),
                    total_stages=each.get('totalStages')
                )
                result.append(well)
            return result
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
        except RuntimeError:
            msg = f'Runtime Error: {str(RuntimeError.args[0])}'
            return errors.error_response(msg, RuntimeError)