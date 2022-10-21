from typing import Union, List, Type

from halo import Halo

from controllers.base_controller import BaseController
from models.error import ErrorResponse
from models.well import Well
from services.well import WellService

OptionsType = List[str]


class WellController(BaseController):
    well_service: Type[WellService]

    def __init__(self, logger, well_service: Type[WellService]):
        super().__init__(logger)
        self.well_service = well_service

    def get_wells(self, access_token: str, api_url: str):
        spinner = Halo(text='Loading...', spinner='dots')
        service = self.well_service(api_url)
        well_response = service.get_wells(access_token)
        if isinstance(well_response, ErrorResponse):
            msg = well_response.message
            self.logger.error(msg)
            spinner.fail(msg)
        else:
            # get list well api & name for selecting
            spinner.succeed('Get wells successfully')
        return well_response

    def get_selection(self, wells: List[Well]):
        if len(wells) == 0:
            msg = 'List well is empty'
            self.logger.error(msg)
            return
        else:
            list_selection = list(map(lambda well: f"{well.api} - {well.name}", wells))
            return list_selection
