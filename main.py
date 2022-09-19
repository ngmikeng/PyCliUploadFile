
import bson
import typer
import logging
from pathlib import Path
from typing import Optional
from halo import Halo

from services import authentication, file_data
from configs import env

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def main(username: str, password: str, file_path: str, api_url: Optional[str] = typer.Argument(None)):
    spinner = Halo(text='Loading...', spinner='dots')
    if api_url is None:
        env_config = env.get_env()
        base_url = env_config.get('apiBaseUrl')
        api_url = base_url
    authentication_service = authentication.AuthenticationService(api_url)
    file_data_service = file_data.FileDataService(api_url)
    spinner.start('Authenticating...')
    auth_response: dict = authentication_service.login(username, password)
    if isinstance(auth_response, dict) and auth_response.get('error'):
        msg = auth_response.get('message')
        logger.error(msg)
        spinner.fail(msg)
        return
    else:
        spinner.succeed('Log in successfully')
    access_token = auth_response.get('access_token')
    path_resolved = Path(file_path)
    file_id = bson.ObjectId()
    spinner.start('Uploading...')
    upload_response = file_data_service.upload_file(file_id, path_resolved, access_token)
    if isinstance(upload_response, dict) and upload_response.get('error'):
        msg = upload_response.get('message')
        logger.error(msg)
        spinner.fail(msg)
        return
    else:
        spinner.succeed('File Uploaded')
        return


if __name__ == "__main__":
    typer.run(main)
