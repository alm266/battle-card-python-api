from fastapi import APIRouter, Depends, HTTPException
from tinydb import TinyDB, Query

from ..dependencies import get_token_header

db = TinyDB('db.json')
player_cards_table = db.table('cards')

router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_cards():
    """
    Gets all the player card objects in the database
    """
    return player_cards_table.all()

@router.get("/{player_card_id}")
async def read_card(player_card_id: str):
    """
    Gets a card object based on its unique id value
    """
    player_card_query = Query()
    player_card = db.search(player_card_query.id == player_card_id)
    if player_card is None:
        raise HTTPException(status_code=404, detail="Player Card not found")
    return player_cards_table.get(player_card_query.id == player_card_id)

@router.put(
    "/{player_card_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_card(card_id: str, player_id: str, code: str, level: int, xp: int):
    """
    Creates or updates a card object if an object with that id already exists in
    the database
    """
    card_query = Query()
    player_card = {"id": card_id, "playerId": player_id, "code": code, "level": level, "xp": xp}
    player_cards_table.upsert(player_card, card_query.id == card_id)
    return player_card