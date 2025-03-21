from __future__ import annotations

from enum import Enum 
from typing import Optional

from fastapi import status
from fastapi.responses import JSONResponse
from shared.base import BaseModel
from structlog.stdlib import BoundLogger


class ResponseMessage(str, Enum):   
    INTERNAL_SERVER_ERROR = 'Server might meet some errors. Please try again later !!!'
    SUCCESS = 'Process successfully !!!'
    NOT_FOUND = 'Resource not found !!!'
    BAD_REQUEST = 'Invalid request !!!'
    UNPROCESSABLE_ENTITY = 'Input is not allowed !!!'

class ExceptionHandler(BaseModel):
    logger: BoundLogger
    service_name: str

    def _create_message(self, e: str) -> str:
        return f'[{self.service_name}] error: {e}'

    def _create_response(
        self,
        message: str,
        data: Optional[dict] = None,
        status_code: int = status.HTTP_200_OK,
    ) -> JSONResponse:
        """Create a response object

        Args:
            message (str): message to be returned
            data (Optional[dict], optional): data to be returned. Defaults to None.
            status_code (int, optional): status code of the response. Defaults to status.HTTP_200_OK.

        Returns:
            Response: response object
        """
        response_data = {'message': message}
        if data:
            response_data.update(data)

        return JSONResponse(content=response_data, status_code=status_code)

    def handle_exception(self, e: str, extra: dict) -> JSONResponse:
        """Handle exception

        Args:
            e (str): exception message
            extra (dict): extra information

        Returns:
            Response: response object
        """
        self.logger.exception(e, extra=extra)
    
    