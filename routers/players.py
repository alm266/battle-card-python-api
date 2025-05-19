from fastapi import APIRouter, Depends, HTTPException
from tinydb import TinyDB, Query

from ..dependencies import get_token_header

db = TinyDB('db.json')
players_table = db.table('players')

router = APIRouter(
    prefix="/players",
    tags=["players"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_players():
    """
    Gets all the player objects in the database
    """
    return players_table.all()

@router.get("/{player_id}")
async def read_player(player_id: str):
    """
    Gets a player object based on its unique id value
    """
    player_query = Query()
    player = players_table.search(player_query.id == player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return players_table.get(player_query.id == player_id)

@router.put(
    "/{player_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_player(player_id: str, new_email: str, new_password_hash: str):
    """
    Creates or updates a player object if an object with that id already exists in
    the database
    """
    player_query = Query()
    player = {"id": player_id, "email": new_email, "passwordHash": new_password_hash}
    players_table.upsert(player, player_query.id == player_id)
    return player