from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.deps import get_current_user
from api.models import Profile, ProfileCreate, User
from api.services import get_profile_by_user_id, update_profile

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/me", response_model=Profile)
def read_my_profile(user_id: str | None = Query(None), current_user: User = Depends(get_current_user)) -> Profile:
    target_user_id = user_id or current_user.id
    if target_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this profile.")

    profile = get_profile_by_user_id(target_user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found.")
    return profile


@router.put("/me", response_model=Profile)
def update_my_profile(
    payload: ProfileCreate,
    user_id: str | None = Query(None),
    current_user: User = Depends(get_current_user),
) -> Profile:
    target_user_id = user_id or current_user.id
    if target_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this profile.")

    profile = update_profile(user_id=target_user_id, name=payload.name, phone=payload.phone, address=payload.address)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found.")
    return profile