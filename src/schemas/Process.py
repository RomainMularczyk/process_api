import re
from datetime import timedelta
from fastapi import HTTPException
from pydantic import BaseModel, field_serializer, field_validator


class ProcessSchema(BaseModel):
    id: int
    user: str
    cpu: float
    memory: float
    command: str
    time: timedelta

    class Config:
        orm_mode = True
        from_attributes = True

    @field_validator("time", mode="before")
    def validate_time(cls, value: str | timedelta) -> timedelta:
        """
        Validate process time inputs provided by the users.

        Parameters
        ----------
        value: str | timedelta
            The input time process metadata.

        Returns
        -------
        timedelta
            The parsed and validated timedelta.

        Raises
        ------
        ValueError
            If the input data could not be parsed properly.
        """
        if type(value) is timedelta:
            return value
        else:
            regex = re.compile(r"^(\d+-)?(\d{1,3}):(\d{2})\.(\d{2})$")
            results = re.search(regex, value)  # type: ignore
            if results:
                if results.group(1):
                    return timedelta(
                        days=int(results.group(1)[:-1]),
                        hours=int(results.group(2)),
                        minutes=int(results.group(3)),
                        seconds=int(results.group(4))
                    )
                else:
                    return timedelta(
                        hours=int(results.group(2)),
                        minutes=int(results.group(3)),
                        seconds=int(results.group(4))
                    )
            else:
                error_message = (
                    "The time metadata could not be parsed properly" 
                    f" for the process with pid: {cls.id}."
                )
                raise HTTPException(status_code=422, detail=error_message)

    @field_serializer("time")
    def serialize_time(self, time: timedelta) -> str:
        return str(time)

    @property
    def time_interval(self) -> str:
        """
        Convert timedelta into INTERVAL Postgres data type.

        Returns
        -------
        str
            A Postgres INTERVAL compatible data type.
        """
        return str(self.time)
