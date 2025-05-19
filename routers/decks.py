from typing import List
from fastapi import APIRouter, Depends, HTTPException
from tinydb import TinyDB, Query

from ..dependencies import get_token_header

db = TinyDB('db.json')
decks_table = db.table('decks')

router = APIRouter(
    prefix="/decks",
    tags=["decks"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_decks():
    """
    Gets all the deck objects in the database
    """
    return decks_table.all()

@router.get("/{deck_id}")
async def read_deck(deck_id: str):
    """
    Gets a deck object based on its unique id value
    """
    deck_query = Query()
    deck = decks_table.search(deck_query.id == deck_id)
    if deck is None:
        raise HTTPException(status_code=404, detail="deck not found")
    return decks_table.get(deck_query.id == deck_id)

@router.put(
    "/{deck_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_deck(deck_id: str, player_id: str, name: str, deck_ids: List[str]):
    """
    Creates or updates a deck object if an object with that id already exists in
    the database
    """
    deck_query = Query()
    deck = {"id": deck_id, "playerId": player_id, "name": name, "deckIds": deck_ids}
    decks_table.upsert(deck, deck_query.id == deck_id)
    return deck