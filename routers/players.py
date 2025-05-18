from fastapi import APIRouter, Depends, HTTPException
from tinydb import TinyDB, Query

from ..dependencies import get_token_header

db = TinyDB('db.json')
db.table('players')

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
    return db.all()

@router.get("/{player_id}")
async def read_player(player_id: str):
    """
    Gets a player object based on its unique id value
    """
    player_query = Query()
    player = db.search(player_query.id == player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db.get(player_query.id == player_id)

@router.put(
    "/{player_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_player(player_id: str, new_email: str, new_password_hash: str):
    """
    Creates or updates a player object if an object with that id already exists in
    the database
    """
    player_query = Query()
    player = {"id": player_id, "email": new_email, "passwordHash": new_password_hash}
    db.upsert(player, player_query.id == player_id)
    return player