from pathlib import Path
from typing import Union, Type

import bson
from halo import Halo

from controllers.base_controller import BaseController
from models.error import ErrorResponse
from services.file_data import FileDataService


class UploadController(BaseController):
    file_data_service: Type[FileDataService]

    def __init__(self, logger, file_data_service: Type[FileDataService]):
        super().__init__(logger)
        self.file_data_service = file_data_service

    def upload_file(self, access_token: str, api_url: str, file_path: str, well_stage_selected: list) -> Union[str, ErrorResponse]:
        spinner = Halo(text='Loading...', spinner='dots')
        service = self.file_data_service(api_url)
        path_resolved = Path(file_path)
        file_id = bson.ObjectId()
        spinner.start('Uploading...')
        upload_response = service.upload_file(str(file_id), path_resolved, access_token, well_stage_selected)
        if isinstance(upload_response, ErrorResponse):
            msg = upload_response.message
            self.logger.error(msg)
            spinner.fail(msg)
        else:
            spinner.succeed(f'File upload result: {upload_response}')

        return upload_response
