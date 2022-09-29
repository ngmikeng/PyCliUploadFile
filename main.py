import bson
import typer
import logging
from pathlib import Path
from typing import Optional, List
from halo import Halo
from pick import pick

from services import authentication, file_data, well as well_sv
from configs import env

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def login(username: str, password: str, api_url: str):
    spinner = Halo(text='Loading...', spinner='dots')
    authentication_service = authentication.AuthenticationService(api_url)
    spinner.start('Authenticating...')
    auth_response: dict = authentication_service.login(username, password)
    if isinstance(auth_response, dict) and auth_response.get('error'):
        msg = auth_response.get('message')
        logger.error(msg)
        spinner.fail(msg)
        return
    else:
        spinner.succeed('Log in successfully')
        return auth_response


def get_selection(access_token: str, api_url: str):
    spinner = Halo(text='Loading...', spinner='dots')
    well_service = well_sv.WellService(api_url)
    well_response = well_service.get_wells(access_token)
    if isinstance(well_response, dict) and well_response.get('error'):
        msg = well_response.get('message')
        logger.error(msg)
        spinner.fail(msg)
        return
    else:
        # get list well api & name for selecting
        if len(well_response) == 0:
            msg = 'List well is empty'
            logger.error(msg)
            spinner.fail(msg)
            return
        else:
            list_selection = list(map(lambda well: f"{well.get('api')} - {well.get('name')}", well_response))
            return dict(options=list_selection, wells=well_response)


def upload_file(access_token: str, api_url: str, file_path: str, well_id: str, stage: int):
    spinner = Halo(text='Loading...', spinner='dots')
    file_data_service = file_data.FileDataService(api_url)
    path_resolved = Path(file_path)
    file_id = bson.ObjectId()
    spinner.start('Uploading...')
    upload_response = file_data_service.upload_file(file_id, path_resolved, well_id, stage, access_token)
    if isinstance(upload_response, dict) and upload_response.get('error'):
        msg = upload_response.get('message')
        logger.error(msg)
        spinner.fail(msg)
        return
    else:
        spinner.succeed('File Uploaded')
        return upload_response


def main(
        username: str,
        password: str,
        file_path: str,
        api_url: Optional[str] = typer.Option(None, help="Base API path, i.e: \"http://evo.com/api\"")
):
    if api_url is None:
        env_config = env.get_env()
        base_url = env_config.get('apiBaseUrl')
        api_url = base_url
    auth_response: dict = login(username, password, api_url)
    if auth_response and auth_response.get('access_token'):
        access_token = auth_response.get('access_token')
        selection = get_selection(access_token, api_url)
        if selection:
            wells: list = selection.get('wells')
            options: list = selection.get('options')
            selected_well, index = pick(options, 'Please choose a well: ')
            arr_str: list = selected_well.rsplit(' - ')
            well_api = arr_str[0]
            selected_well = list(filter(lambda well: well.get('api') == well_api, wells))
            well_id = selected_well[0].get('id')
            total_stages = selected_well[0].get('totalStages')
            if total_stages is None:
                total_stages = 10
            list_stages = list(range(1, total_stages + 1))
            selected_stage, index = pick(list_stages, 'Please choose a stage: ')
            upload_response = upload_file(access_token, api_url, file_path, well_id, selected_stage)
            return upload_response

    return


if __name__ == "__main__":
    typer.run(main)
