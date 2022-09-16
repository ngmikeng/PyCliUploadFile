import bson
import typer
import logging

from services import authentication, file_data
from pathlib import  Path

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def main(username: str, password: str, file_path: str):
    auth_response: dict = authentication.login(username, password)
    if isinstance(auth_response, dict) and auth_response.get('error'):
        msg = auth_response.get('message')
        logger.error(msg)
        print(msg)
        return
    else:
        print('Log in successfully')
    access_token = auth_response.get('access_token')
    path_resolved = Path(file_path)
    file_id = bson.ObjectId()
    upload_response = file_data.upload_file(file_id, path_resolved, access_token)
    if isinstance(upload_response, dict) and upload_response.get('error'):
        msg = upload_response.get('message')
        logger.error(msg)
        print(msg)
        return
    else:
        print('File Uploaded')
        return


if __name__ == "__main__":
    typer.run(main)
