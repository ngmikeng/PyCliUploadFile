import typer
import logging
from typing import Optional
from pick import pick

from controllers.authentication import AuthenticationController
from controllers.upload import UploadController
from controllers.well import WellController
from models.auth import AuthResponse
from models.error import ErrorResponse
from services import authentication, file_data, well as well_sv
from configs import env

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def main(
        username: str,
        password: str,
        file_path: str,
        api_url: Optional[str] = typer.Option(None, help="Base API path, i.e: \"http://evo.com/api\""),
        # well: List[str] = typer.Option(..., help="A Well Id"),
        # stage: List[str] = typer.Option(..., help="A Stage Number relevant to a Well Id"),
):
    # print('well', well)
    # print('stage', stage)
    if api_url is None:
        env_config = env.get_env()
        base_url = env_config.get('apiBaseUrl')
        api_url = base_url
    auth_controller = AuthenticationController(
        logger=logger,
        authentication_service=authentication.AuthenticationService
    )
    well_controller = WellController(logger=logger, well_service=well_sv.WellService)
    upload_controller = UploadController(logger=logger, file_data_service=file_data.FileDataService)

    auth_response = auth_controller.login(username, password, api_url)
    if isinstance(auth_response, AuthResponse):
        access_token = auth_response.access_token
        well_response = well_controller.get_wells(access_token, api_url)
        if not isinstance(well_response, ErrorResponse):
            wells = well_response
            options = well_controller.get_selection(well_response)
            if options:
                well_stage_selected = []
                for side_index in [1, 2]:
                    selected_well, index = pick(options, f'Please choose well {side_index}: ')
                    arr_str: list = selected_well.rsplit(' - ')
                    well_api = arr_str[0]
                    selected_well = list(filter(lambda well: well.api == well_api, wells))
                    well_id = selected_well[0].id
                    total_stages = selected_well[0].totalStages
                    if total_stages is None:
                        total_stages = 10
                    list_stages = list(range(1, total_stages + 1))
                    selected_stage, index = pick(list_stages, f'Please choose a stage for well {side_index}: ')
                    well_stage_selected.append(dict(wellId=well_id, stage=selected_stage))
                print('Selected Wells & Stages: ', well_stage_selected)
                upload_response = upload_controller.upload_file(access_token, api_url, file_path, well_stage_selected)
                return upload_response

    return


if __name__ == "__main__":
    typer.run(main)
