from enum import Enum
from typing import List
from fastapi import HTTPException
from pydantic import BaseModel
from schemas.Process import ProcessSchema


class Status(Enum):
    ERROR = "error"
    SUCCESS = "success"

class ProcessView(BaseModel):
    status: Status
    message: str
    data: ProcessSchema | List[ProcessSchema] | None


def success(
    data: ProcessSchema | List[ProcessSchema],
    message: str = "The operation was successful."
) -> ProcessView:
    """
    Answer returned by the API when successfully retrieving a process.

    Parameters
    ----------
    data: ProcessSchema | List[ProcessSchema]
        The retrieved process metadata.
    message: str, default="The operation was successful."
        The information message returned by the API.

    Returns
    -------
    ProcessView
        The success process view.
    """
    return ProcessView(
        status=Status.SUCCESS,
        message=message,
        data=data
    )

def error(
    status_code: int = 404,
    message: str = "An error occurred with the API."
) -> None:
    """
    Answer returned by the API when an error occurs while trying to retrieve a process.

    Parameters
    ----------
    status_code: int, default=404
        The API status code returned.
    message: str, default="An error occurred with the API."
        The API error message returned.

    Raises
    ------
    HTTPException
        The API HTTP error returned.
    """
    raise HTTPException(status_code=status_code, detail=message)
