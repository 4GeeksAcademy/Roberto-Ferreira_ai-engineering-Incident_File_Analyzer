from pydantic import BaseModel, ConfigDict
from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_user
from api.models import Record, RecordNote, RecordStage, RecordStatus, User
from api.services import (
    add_note,
    create_record,
    delete_note,
    delete_record,
    get_record_by_id,
    get_records,
    patch_record_status,
    update_record,
)

router = APIRouter(prefix="/records", tags=["records"])


# ------- Request/Response schemas -------


class RecordCreateBody(BaseModel):
    full_name: str
    email: str
    phone: str
    position: str
    linkedin_url: str | None = None
    cv_url: str | None = None
    status: RecordStatus = RecordStatus.RECEIVED
    stage: RecordStage = RecordStage.PENDING
    experience_years: int = 0


class RecordUpdateBody(BaseModel):
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    position: str | None = None
    linkedin_url: str | None = None
    cv_url: str | None = None
    status: RecordStatus | None = None
    stage: RecordStage | None = None
    experience_years: int | None = None


class RecordPatchStatusBody(BaseModel):
    status: RecordStatus | None = None
    stage: RecordStage | None = None


class AddNoteBody(BaseModel):
    content: str


class RecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    email: str
    phone: str
    position: str
    linkedin_url: str | None
    cv_url: str | None
    status: RecordStatus
    stage: RecordStage
    experience_years: int
    applied_at: str
    updated_at: str
    notes_count: int
    notes: list[RecordNote]


class RecordListResponse(BaseModel):
    data: list[RecordResponse]
    meta: dict[str, int]


class RecordNoteResponse(BaseModel):
    data: list[RecordNote]
    meta: dict[str, int]


def _serialize_record(record: Record) -> RecordResponse:
    return RecordResponse(
        id=record.id,
        full_name=record.full_name,
        email=record.email,
        phone=record.phone,
        position=record.position,
        linkedin_url=record.linkedin_url,
        cv_url=record.cv_url,
        status=record.status,
        stage=record.stage,
        experience_years=record.experience_years,
        applied_at=record.applied_at.isoformat(),
        updated_at=record.updated_at.isoformat(),
        notes_count=record.notes_count,
        notes=record.notes,
    )


# ------- Routes -------


@router.get("", response_model=RecordListResponse)
def list_records(_current_user: User = Depends(get_current_user)) -> RecordListResponse:
    records = get_records()
    return RecordListResponse(
        data=[_serialize_record(r) for r in records],
        meta={"total": len(records)},
    )


@router.get("/{record_id}", response_model=RecordResponse)
def read_record(record_id: str, _current_user: User = Depends(get_current_user)) -> RecordResponse:
    record = get_record_by_id(record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")
    return _serialize_record(record)


@router.post("", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
def create_new_record(payload: RecordCreateBody, _current_user: User = Depends(get_current_user)) -> RecordResponse:
    record = create_record(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        position=payload.position,
        linkedin_url=payload.linkedin_url,
        cv_url=payload.cv_url,
        status=payload.status,
        stage=payload.stage,
        experience_years=payload.experience_years,
    )
    return _serialize_record(record)


@router.put("/{record_id}", response_model=RecordResponse)
def replace_record(record_id: str, payload: RecordUpdateBody, _current_user: User = Depends(get_current_user)) -> RecordResponse:
    record = update_record(
        record_id=record_id,
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        position=payload.position,
        linkedin_url=payload.linkedin_url,
        cv_url=payload.cv_url,
        status=payload.status,
        stage=payload.stage,
        experience_years=payload.experience_years,
    )
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")
    return _serialize_record(record)


@router.patch("/{record_id}", response_model=RecordResponse)
def patch_record(record_id: str, payload: RecordPatchStatusBody, _current_user: User = Depends(get_current_user)) -> RecordResponse:
    record = patch_record_status(record_id=record_id, status=payload.status, stage=payload.stage)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")
    return _serialize_record(record)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_record(record_id: str, _current_user: User = Depends(get_current_user)) -> None:
    if not delete_record(record_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")


@router.get("/{record_id}/notes", response_model=RecordNoteResponse)
def list_notes(record_id: str, _current_user: User = Depends(get_current_user)) -> RecordNoteResponse:
    record = get_record_by_id(record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")
    return RecordNoteResponse(data=record.notes, meta={"total": len(record.notes)})


@router.post("/{record_id}/notes", response_model=RecordNote, status_code=status.HTTP_201_CREATED)
def create_note(record_id: str, payload: AddNoteBody, _current_user: User = Depends(get_current_user)) -> RecordNote:
    record = get_record_by_id(record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")
    return add_note(record_id=record_id, content=payload.content)


@router.delete("/{record_id}/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_note(record_id: str, note_id: str, _current_user: User = Depends(get_current_user)) -> None:
    if not delete_note(record_id=record_id, note_id=note_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")