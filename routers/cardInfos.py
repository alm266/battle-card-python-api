from typing import List
from fastapi import APIRouter, Depends, HTTPException
from tinydb import TinyDB, Query

from ..dependencies import get_token_header

db = TinyDB('db.json')
card_infos_table = db.table('cardInfos')

router = APIRouter(
    prefix="/cardInfos",
    tags=["cardInfos"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_card_infos():
    """
    Gets all the card info objects in the database
    """
    return card_infos_table.all()

@router.get("/{cardInfo_id}")
async def read_cardInfo(cardInfo_id: str):
    """
    Gets a card info object based on its unique id value
    """
    card_info_query = Query()
    card_info = card_infos_table.search(card_info_query.id == cardInfo_id)
    if card_info is None:
        raise HTTPException(status_code=404, detail="cardInfo not found")
    return card_infos_table.get(card_info_query.id == cardInfo_id)

@router.put(
    "/{cardInfo_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_cardInfo(card_info_id: str, name: str, attack: int, number_of_levels: int, codes: List[str]):
    """
    Creates or updates a card info object if an object with that id already exists in
    the database
    """
    card_info_query = Query()
    card_info = {"id": card_info_id, "name": name, "attack": attack, "numberOfLevels": number_of_levels, "codes": codes}
    card_infos_table.upsert(card_info, card_info_query.id == card_info_id)
    return card_info