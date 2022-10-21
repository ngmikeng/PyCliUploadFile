from typing import Union, Type

from halo import Halo

from controllers.base_controller import BaseController
from models.auth import AuthResponse
from models.error import ErrorResponse
from services.authentication import AuthenticationService


class AuthenticationController(BaseController):
    authentication_service: Type[AuthenticationService]

    def __init__(self, logger, authentication_service: Type[AuthenticationService]):
        super().__init__(logger)
        self.authentication_service = authentication_service

    def login(self, username: str, password: str, api_url: str) -> Union[AuthResponse, ErrorResponse]:
        spinner = Halo(text='Loading...', spinner='dots')
        service = self.authentication_service(api_url)
        spinner.start('Authenticating...')
        auth_response = service.login(username, password)
        if isinstance(auth_response, ErrorResponse):
            msg = auth_response.message
            self.logger.error(msg)
            spinner.fail(msg)
        else:
            spinner.succeed('Log in successfully')
        return auth_response
