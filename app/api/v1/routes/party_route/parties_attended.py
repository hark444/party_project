from fastapi import Depends, APIRouter, HTTPException, status
from models import get_db
import logging
from settings.base import env
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api.v1.schema.request.parties_attended import (
    PartiesAttendedRequestSchema,
    PartyAttendedArgs,
)
from app.api.v1.schema.response.parties_attended import (
    PartiesAttendedResponseSchema,
    AllPartiesAttendedResponseSchema,
)
from app.api.v1.schema.response.user import UserResponseSchema
from app.api.v1.routes.auth import get_current_user
from models.parties_attended import PartiesAttended


parties_attended_router = APIRouter(
    prefix="/parties_attended", tags=["parties_attended"]
)
MAX_PARTY_RATING = env.int("MAX_PARTY_RATING")
logger = logging.getLogger("main")


@parties_attended_router.post("", response_model=PartiesAttendedResponseSchema)
async def create_parties_attended(
    party_attended: PartiesAttendedRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    try:
        parties_attended_obj = PartiesAttended(
            party_id=party_attended.party_id,
            user_id=current_user.id,
            rating=party_attended.rating,
            comment=party_attended.comment,
            created_on=party_attended.created_on,
            last_modified_on=party_attended.last_modified_on,
        )

        db.add(parties_attended_obj)
        db.commit()
        db.refresh(parties_attended_obj)

        update_rating_and_approval(
            parties_attended_obj, new_rating=parties_attended_obj.rating
        )
        db.add(parties_attended_obj)
        db.commit()
        db.refresh(parties_attended_obj)

        return parties_attended_obj

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@parties_attended_router.get(
    "/{party_attended_id}", response_model=PartiesAttendedResponseSchema
)
async def get_party(
    party_attended_id: int,
    db: Session = Depends(get_db),
):
    try:
        party_attended_obj = (
            db.query(PartiesAttended).filter_by(id=party_attended_id).first()
        )
        if not party_attended_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Party object for this party id and user id",
            )
        return party_attended_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@parties_attended_router.get("", response_model=AllPartiesAttendedResponseSchema)
async def get_all_parties_attended(
    db: Session = Depends(get_db),
    args: PartyAttendedArgs = Depends(),
    curr_user: UserResponseSchema = Depends(get_current_user),
):
    try:
        result = {}
        query = db.query(PartiesAttended).filter_by(user=curr_user)
        if args.party_id:
            query = query.filter_by(party_id=args.party_id)

        party_attended_obj = query.all()
        result["data"] = party_attended_obj
        result["total"] = query.count()
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@parties_attended_router.put(
    "/{party_attended_id}", response_model=PartiesAttendedResponseSchema
)
async def put_party(
    party_attended_id: int,
    party_attended: PartiesAttendedRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    party_attended_obj = (
        db.query(PartiesAttended)
        .filter_by(id=party_attended_id, user_id=current_user.id)
        .first()
    )
    if not party_attended_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Party object for this party id and user id",
        )

    try:
        # Update party record with new rating and approved
        update_rating_and_approval(
            party_attended_obj,
            party_attended.rating,
            old_rating=party_attended_obj.rating,
        )

        for field, value in party_attended.dict().items():
            setattr(party_attended_obj, field, value)

        db.add(party_attended_obj)
        db.commit()
        db.refresh(party_attended_obj)

        return party_attended_obj

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@parties_attended_router.delete("/{party_attended_id}")
async def delete_party(
    party_attended_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    party_attended_obj = (
        db.query(PartiesAttended)
        .filter_by(id=party_attended_id, user_id=current_user.id)
        .first()
    )
    if not party_attended_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Party object for this party id and user id",
        )
    try:
        db.delete(party_attended_obj)
        db.commit()
        return None

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def update_rating_and_approval(party_attended_obj, new_rating=0, old_rating=0):
    try:
        party = party_attended_obj.party
        total_weight = party.ratings * party.guests_invited
        net_change = old_rating - new_rating
        updated_rating = (total_weight - net_change) / party.guests_invited
        is_approved = updated_rating > (MAX_PARTY_RATING // 2)
        logger.info("Updating party ratings and approval.")
        party_attended_obj.party.ratings = updated_rating
        party_attended_obj.party.approved = is_approved
    except Exception as e:
        logger.exception(f"Unable to update party ratings and approvals because: {e}")
