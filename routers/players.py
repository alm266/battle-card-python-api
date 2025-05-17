from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/players",
    tags=["players"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_players_db = {
    "andrew": {
        "id": "andrew",
        "email": "andrew@email.com",
        "passwordHash": "abcd"
    },
    "reggie": {
        "id": "reggie",
        "email": "reggie@email.com",
        "passwordHash": "wxyz"
    }
}

@router.get("/")
async def read_players():
    return fake_players_db

@router.get("/{player_id}")
async def read_player(player_id: str):
    if player_id not in fake_players_db:
        raise HTTPException(status_code=404, detail="Player not found")
    return fake_players_db[player_id]

@router.put(
    "/{player_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_player(player_id: str, new_email: str, new_password_hash: str):
    new_player = {"id": player_id, "email": new_email, "passwordHash": new_password_hash}
    fake_players_db[player_id] = new_player
    return new_player