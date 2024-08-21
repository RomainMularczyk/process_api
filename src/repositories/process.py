import logging
from typing import List
from psycopg2.errors import UniqueViolation
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from schemas.Process import ProcessSchema
from models.Process import Process
from views.view_process import error


def add_process(db: Session, data: ProcessSchema) -> ProcessSchema | None:
    """
    Insert a given process in the database.

    Parameters
    ----------
    db: Session
        The database client session.
    data: Dict
        The input process inserted by the user. This piece
        of data is first validated by the process schema.

    Returns
    -------
    ProcessSchema | None
        If created successfully, returns the process metadata. 

    Raises
    ------
    HTTPException
        If the process could not be inserted properly in the database.
    """
    process = Process(
        id=data.id,
        user=data.user,
        cpu=data.cpu,
        memory=data.memory,
        command=data.command,
        time=data.time_interval
    )
    try:
        db.add(process)
        db.commit()
        db.refresh(process)
        logging.info("Data was inserted successfully in the database.")
        return data
    except IntegrityError as integ_error:
        if isinstance(integ_error.orig, UniqueViolation):
            error_message = (
                f"The process inserted with pid {data.id}" 
                " already exists in the database."
            )
            logging.error(error_message)
            error(status_code=422, message=error_message)
        else:
            error_message = f"An integrity error happened : {integ_error}."
            logging.error(error_message)
            error(status_code=422, message=error_message)
    except Exception as e:
        db.rollback()
        logging.error(
            f"An error occurred when inserting data in the database: {e}."
        )
        error()

def add_processes(db: Session, data: List[ProcessSchema]) -> List[ProcessSchema] | None:
    """
    Remove all existing processes and insert a new batch.

    Parameters
    ----------
    db: Session
        The database client session.
    data: Dict
        The input processes inserted by the user. This piece
        of data is first validated by the process schema.

    Returns
    -------
    ProcessSchema | None
        If created successfully, returns the process metadata. 

    Raises
    ------
    HTTPException
        If the processes could not be inserted properly in the database.
    """
    # First, remove all existing data
    try:
        db.query(Process).delete()
        db.commit()
        logging.info("Database was flushed successfully.")
    except Exception as e:
        db.rollback()
        error_message = f"An error as occurred when flushing the database : {e}" 
        logging.error(error_message)
        error(status_code=500, message=error_message)

    processes = [
        process.model_dump() for process in data
    ]
    stmt = insert(Process).values(processes)
    try:
        db.execute(stmt)
        db.commit()
        logging.info("Data was inserted succesfully in the database.")
        return data
    except IntegrityError as integ_error:
        if isinstance(integ_error.orig, UniqueViolation):
            error_message = (
                "Some processes inserted share the same IDs"
                " with existing ones already registered in the database."
            )
            logging.error(error_message)
            error(status_code=422, message=error_message)
        else:
            error_message = f"An integrity error happened : {integ_error}."
            logging.error(error_message)
            error(status_code=422, message=error_message)
    except Exception as e:
        db.rollback()
        error_message = f"An error occurred when trying bulk insert : {e}."
        logging.error(error_message)
        error(status_code=422, message=error_message)

def read_process(db: Session, pid: int) -> ProcessSchema | None:
    """
    Read a process with a given ID in the database.

    Parameters
    ----------
    db: Session
        The database client session.
    id: int
        The process ID (pid).

    Raises
    ------
    HTTPException
        If the process could not be retrieved properly from the database.

    Returns
    -------
    ProcessSchema | None
        If found, returns the matching process.
    """
    try:
        result = db.query(Process).filter(Process.id == pid).first()
        validated_data = ProcessSchema.model_validate(result)
        return validated_data
    except Exception as e:
        logging.error(
            f"An error occurred when retrieving data with id {pid}: {e}."
        )
        error()

def read_processes(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[ProcessSchema] | None:
    """
    Read all processes in the database.

    Parameters
    ----------
    db: Session
        The database client session.
    skip: int, default=0
        The page number.
    limit: int, default=100
        The limit number of processes returned.

    Raises
    ------
    HTTPException
        If the processes could not be retrieved properly from the database.

    Returns
    -------
    List[ProcessSchema] | None
        If any found, returns all the processes in the database.
    """
    try:
        results = db.query(Process).offset(skip).limit(limit).all()
        validated = [ProcessSchema.model_validate(row) for row in results]
        return validated
    except Exception as e:
        logging.error(
            f"An error occured when retrieving processes: {e}."
        )
        error()
