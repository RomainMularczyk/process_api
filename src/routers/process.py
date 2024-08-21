from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.config import db_session
from schemas.Process import ProcessSchema
from repositories.process import (
    add_process, add_processes, read_process, read_processes
)
from views.view_process import success, error, ProcessView

router = APIRouter(prefix="/api")

@router.get("/process/{pid}", status_code=status.HTTP_200_OK)
async def get_process(
    pid: int,
    db: Session = Depends(db_session)
) -> ProcessView | None:
    response = read_process(db, pid)
    if response:
        return success(response)
    return error()

@router.get("/processes", status_code=status.HTTP_200_OK)
async def get_processes(db: Session = Depends(db_session)) -> ProcessView | None:
    response = read_processes(db)
    if response:
        return success(response, "The process was retrieved sucessfully.")
    return error()

@router.post("/process", status_code=status.HTTP_201_CREATED)
def create_process(
    data: ProcessSchema,
    db: Session = Depends(db_session)
) -> ProcessView | None:
    response = add_process(db, data)
    if response:
        return success(response, "The process was created successfully.")
    return error()

@router.post("/processes", status_code=status.HTTP_201_CREATED)
async def create_processes(
    data: List[ProcessSchema],
    db: Session = Depends(db_session)
) -> ProcessView | None:
    response = add_processes(db, data)
    if response:
        return success(response, "The processes were created successfully.")
    return error()
