from fastapi import Depends, APIRouter, HTTPException, status
from models import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api.v1.schema.request.party import PartyRequestSchema
from app.api.v1.schema.response.party import PartyResponseSchema
from app.api.v1.schema.response.user import UserResponseSchema
from models.party import Party
from app.api.v1.routes.auth import oauth2_scheme
from app.api.v1.routes.auth import get_current_user


party_party_router = APIRouter(prefix="/party", tags=["party"])


@party_party_router.post("/create", response_model=PartyResponseSchema)
async def create_party(
    party: PartyRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    try:
        party_obj = Party(
            user_id=current_user.id,
            reason=party.reason,
            proposed_date=party.proposed_date,
            guests_invited=party.guests_invited,
            party_date=party.party_date,
            party_place=party.party_place,
            ratings=party.ratings,
            approved=party.approved,
            created_on=party.created_on,
            last_modified_on=party.last_modified_on,
        )

        db.add(party_obj)
        db.commit()
        db.refresh(party_obj)
        return party_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@party_party_router.get("/{party_id}", response_model=PartyResponseSchema)
async def get_party(
    party_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    try:
        party_obj = (
            db.query(Party).filter_by(id=party_id, user_id=current_user.id).first()
        )
        if not party_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Party object for this party id and user id",
            )
        return party_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@party_party_router.put("/{party_id}", response_model=PartyResponseSchema)
async def put_party(
    party_id: int,
    party: PartyRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    party_obj = db.query(Party).filter_by(id=party_id, user_id=current_user.id).first()
    if not party_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Party object for this party id and user id",
        )

    try:
        for field, value in party.dict().items():
            setattr(party_obj, field, value)

        db.add(party_obj)
        db.commit()
        db.refresh(party_obj)
        return party_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@party_party_router.delete("/{party_id}")
async def delete_party(
    party_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    party_obj = db.query(Party).filter_by(id=party_id, user_id=current_user.id).first()
    if not party_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Party object for this party id and user id",
        )
    try:
        db.delete(party_obj)
        db.commit()
        return None

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
